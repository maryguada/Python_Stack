#step 1: Import Flask! 
from flask import Flask, request, redirect, render_template, flash, session

# step2: Connect to MySQL server 
for myconnection import MySQLConnector 

# step 3: import Bycrypt to crypt passwords generated 
import re 
from flask_bcrypt import Bcrypt

#step 4: import email regex 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')  #add this email Regex 

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "keep it secret"

################ MAIN / ROOT PAGE ########################
#########################################################
@app.route("/")
def main(): 
   return render_template("index.html")

################# CREATE USER ##########################
########################################################
@app.route('/createUser', methods=['POST'])
def create():
    # include some logic to validate user input before adding them to the database!
    # create the hash

    if not EMAIL_REGEX.match(request.form['email']):
        flash ("Invalid email address")

    is_valid = True		# assume True

    if len(request.form['first_name']) < 3:
        is_valid = False
        # display validation error using flash
        flash("Please enter first name.")

    if len(request.form['last_name']) < 1:
        is_valid = False
        # display validation error using flash
        flash("Please enter last name.")

    if len(request.form['password']) < 8:
        is_valid = False
        # display validation error using flash
        flash("Password needs to be 8 or more characters")

    if request.form['password'] != request.form['confirm']:
        is_valid = False
        flash("Passwords don't match")
    
    if not is_valid: 
        return redirect("/")

    mysql=connectToMySQL("login_reg")
    query = "SELECT * FROM users WHERE email =%(email)s"
    data = {
        "email": request.form['email']
    }

    result = mysql.query_db(query, data)
    if len(result)>0: 
        is_valid = False 
        flash('username already exist')
        return redirect('/')

    else: 
        pw_hash = bcrypt.generate_password_hash(request.form['password'])  
        print(pw_hash) 
         
        # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'
        # be sure you set up your database so it can store password hashes this long (60 characters)
        mysql = connectToMySQL("login_reg")
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s);"
        # put the pw_hash in our data dictionary, NOT the password the user provided
        data = { 

            "first_name" : request.form['first_name'],
            "last_name": request.form['last_name'], 
            "email" : request.form['email'],
            "password_hash" : pw_hash, 
            }
        id=mysql.query_db(query, data)
        session['id'] = id 
        flash("You've been successfully added, you may now log in")
        # never render on a post, always redirect!
        return redirect("/")

########################  LOG IN VALIDATE   ##########################
######################################################################
@app.route('/login_validate', methods=["POST"])
def login_validate():
    mysql = connectToMySQL('login_reg')
    query = "SELECT * FROM users WHERE email = %(email)s"
    data = {
        "email": request.form ['email_login']        
        }

    check = mysql.query_db(query,data)

    if len(check)>0: #if the len of 'check' is greater than 0: then it exist in db.

        # if check[0]['email'] == request.form['email_login']

        if bcrypt.check_password_hash(check[0]['password'], request.form['log_in_pw']):
            session['id'] = check[0]['id']

            return redirect('/success')
        else:
            flash ('Invalid Credentials: Login denied')
            return redirect('/')
    else:
        flash ('Invalid Credentials. Login denied')
        return redirect('/')

################### SUCCESS/ HOME  ###################
######################################################
@app.route ('/success')
def success(): 
    # if session['id'] == True : 

    return render_template('/home.html')


#     # mysql=connectToMySQL("login_reg")
#     # query ="SELECT * FROM users WHERE id=%(id)s"

#################### LOG OUT ######################
###################################################
@app.route('/logout')
def logout():

    session.clear()
    # return redirect('/')
    return render_template('logout.html')



if __name__ == "__main__":
    app.run(debug=True)












