from flask import Flask, render_template, redirect, request, flash, session 
from myconnection import connectToMySQL
from flask_bcrypt import Bcrypt 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')  #add this email Regex 

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "keep it secret"

###############  ROOT   ################
#########################################
@app.route("/")
def main(): 
   return render_template("index.html")


############  CREATE USER   ###########
#########################################
@app.route('/createUser', methods=['POST'])
def create():
    
    mysql = connectToMySQL("got_db")

    if not EMAIL_REGEX.match(request.form['email']):
        flash ("Invalid email address")

    is_valid = True	 # assume True

######## FIRST NAME VALIDATION   ##########
############################################
    if len(request.form['first_name']) < 3:
        is_valid = False
        # display validation error using flash
        flash("First Name must have 3 or more characters", "fchar_error")
        
        #check if first name contains a number 
    def num_there(s): 
        return any(i.isdigit() for i in s) 
    if num_there(request.form['first_name']) == True: 
        flash ("First name cannot contain any numbers", "fnum_error")
        is_valid = False 

######### LAST NAME VALIDATION #############
############################################
    if len(request.form['last_name']) < 1:
        is_valid = False
        # display validation error using flash
        flash("Invalid last name.")
    def numberPresent(s): 
        return any(i.isdigit() for i in s) 
    if numberPresent(request.form['last_name']) == True: 
        flash ("Last name cannot contain any numbers", "fnum_error")
        is_valid = False 

############ EMAIL VALIDATION ############
##########################################
    # if len(request.form['email']) <1: 
    #     flash("Email cannot be left blank.")
    #     return redirect('/')

    if not EMAIL_REGEX.match(request.form['email']):
        flash ("Invalid email address. Please have email in proper email format.")
        return redirect('/')
    
######### Password Validation ###########
##########################################
    if len(request.form['password']) < 8:
        is_valid = False
        # display validation error using flash
        flash("Password needs to be 8 or more characters")

    if request.form['password'] != request.form['confirm']:
        is_valid = False
        flash("Passwords don't match")
    
    if not is_valid: 
        return redirect("/")

    mysql=connectToMySQL("got_db")
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
        mysql = connectToMySQL("got_db")
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

        flash("You've been successfully added, you may now log in.")

        # never render on a post, always redirect!
        return redirect("/")

###################  LOG IN VALIDATE   ##########################
#################################################################
@app.route('/login_validate', methods=["POST"])
def login_validate():
    mysql = connectToMySQL('got_db')
    query = "SELECT * FROM users WHERE email = %(email)s"
    data = {
        "email": request.form ['email_login']        
        }

    loggedin = mysql.query_db(query,data)
    # check = mysql.query_db(query,data)
    # if len(check)>0: #if the len of check is greater than 0: then it exist in db
    if loggedin:
        if bcrypt.check_password_hash(loggedin[0]['password'], request.form['log_in_pw']):
            print("bcrypt matched!")
            session['id'] = loggedin[0]['id']
            return redirect('/success')
        else:
            flash ('Invalid Credentials: Login denied!')
            return redirect('/')
    else:
        flash ("Log In Failed. Log in Error.")
        return redirect('/')


############ SUCCESS LOGIN / HOME  ###################
######################################################
@app.route ('/success')
def success(): 
    if 'id' not in session: 
        flash ('You are not logged in!', 'hacker_error')
        return redirect('/')

    mysql = connectToMySQL('got_db')
    id = session['id']
    query = "SELECT * FROM users WHERE id =" +str(id)
    user = mysql.query_db(query)

    #Additionally we will also need to query for all our characters! 
    #Connect to db once again.
    mysql= connectToMySQL('got_db')

    #This data is coming from your other table called characters.
    characterQuery = "SELECT * FROM characters"
    characters = mysql.query_db(characterQuery)

    return render_template('/results.html', user=user[0], characters = characters)


######## Show Create Landing Page ######## 
#######################################
@app.route('/show-create')
def showCreate(): 
    return render_template('create.html')


####### PROCESS OF CREATING THE CHARACTER #######
#this is the other route that handles the form submission POST route! 
@app.route('/process', methods=['POST'])
def process(): 
    print(request.form['name'])
    print(request.form['house'])
    print(request.form['sigil'])

    create_is_valid = True 

    #need to validate
    if len(request.form['name']) < 3: 
        flash ("Name must be 3 or more characters!", 'gotName')
        create_is_valid = False 

    if len(request.form['house']) < 3: 
        flash ("House must be 3 or more characters!", 'gotHouse')
        create_is_valid = False 

    if len(request.form['sigil']) < 3: 
        flash ("Name must be 3 or more characters!", 'gotSigil')
        create_is_valid = False 

    if not create_is_valid: 
        return redirect('/show-create')

    mysql = connectToMySQL('got_db')
    query = "INSERT INTO characters (name, house, sigil, create_at, updated_at, user_id) VALUES (%(name)s, %(house)s,%(sigil)s, NOW(), NOW(),%(userid)s);"
    
    data = {
        'name': request.form['name'],
        'house': request.form['house'], 
        'sigil' : request.form['sigil'],
        'userid': session['userid'] #when we need the logged in users id we get it in using session!
    }

    mysql.query_db(query,data)

        
    return redirect('/success')

######### SHOW the edit page with ID #############
@app.route('/show/<id>')
def showCharcter(id): 
    mysql = connectToMySQL("got_db")
    query = "SELECT * FROM character WHERE id="+id

    character = mysql.query_db(query)

    #need to show data!! do this on the html page. access using "values!"
    return render_template('edit.html', character = character[0])

######### EDIT PROCESS #####
@app.route('/editProcess', methods=["POST"])
def editProcess(): 
    
    print(request.form['name'])
    print(request.form['house'])
    print(request.form['sigil'])

    ## WE NEED TO VALIDATE THE EDITS! 
    edit_valid = True 

    if len(request.form['name']) <3: 
        flash ("Name must be 3 or more characters!")
        edit_valid= False
    if not edit_valid:
        return redirect('/show/'+request.form['id'])

    mysql = connectToMySQL("got_db")
    query = "UPDATE characters set name = %(name)s, house=%(house)s, sigil=%(sigil)s, updated_at=NOW() WHERE id =%(id)s"
    data = {
    'name': request.form['name'],
    'house': request.form['house'], 
    'sigil' : request.form['sigil'],
    'id': request.form['id'] #when we need the logged in users id we get it in using session!
    }

    mysql.query_db(query, data)
   
    return render_template('show.html')

#################### LOG OUT ######################
###################################################
@app.route('/logout')
def logout():

    session.clear()
    # return redirect('/')
    return render_template('logout.html')



if __name__ == "__main__":
    app.run(debug=True)





