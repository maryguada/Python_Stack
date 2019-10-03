from flask import Flask, render_template, redirect, request, session, flash 
from myconnection import connectToMySQL
import re 
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')  #add this email Regex 

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "keep it secret"

###################  MAIN ###############################
#########################################################
@app.route("/")
def main(): 
   return render_template("index .html")


############ CREATE/ REGISTER USER  ###################
########################################################
@app.route('/createUser', methods=['POST'])
def createUser():
    # include some logic to validate user input before adding them to the database!
    # create the hash
    mysql = connectToMySQL("fave_books")

    if not EMAIL_REGEX.match(request.form['email']):
        flash ("Invalid email address", "reg_error")

    is_valid = True		# assume True

    if len(request.form['first_name']) < 3:
        is_valid = False
        # display validation error using flash
        flash("Please enter first name", )

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

    mysql=connectToMySQL("fave_books")
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
        mysql = connectToMySQL("fave_books")
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s);"
        # put the pw_hash in our data dictionary, NOT the password the user provided
        data = { 

            "first_name" : request.form['first_name'],
            "last_name": request.form['last_name'], 
            "email" : request.form['email'],
            "password_hash" : pw_hash, 
            }

        id=mysql.query_db(query, data)
        session['userid'] = id 
        flash("You've been successfully added, you may now log in")
        # never render on a post route, always redirect!
        return redirect("/")

########################  LOG IN VALIDATE   ##########################
######################################################################
@app.route('/login_validate', methods=["POST"])
def login_validate():
    mysql = connectToMySQL('fave_books')
    query = "SELECT * FROM users WHERE email = %(email)s"
    data = {
        "email": request.form ['email_login']        
        }

    logged_in = mysql.query_db(query,data)

    # check = mysql.query_db(query,data)
    # if len(check)>0: #if the len of check is greater than 0: then it exist in db

    if logged_in:

        if bcrypt.check_password_hash(logged_in[0]['password'], request.form['log_in_pw']):
            print('bcrypt matched!')
            session['userid'] = logged_in[0]['id']
            return redirect('/show')

        else:
            flash ("Invalid Credentials: Login denied", "login_error")
            return redirect('/')
            

################ SUCCESS/ SHOW ###################
###################################################
@app.route ('/show')
def show(): 
    #we have to see if user is in session! 
    if 'userid' not in session: 
        flash('You are not logged in, please log in!')
        return redirect ('/')
    mysql = connectToMySQL("fave_books")
    id = session['userid']

    #user query 
    user_query = "SELECT * FROM users WHERE id =" + str(id)
    user = mysql.query_db(user_query)


    #another book query 
    mysql = connectToMySQL('fave_books')
    book_query = "SELECT * FROM books"
    books = mysql.query_db(book_query)

    #print is to check your terminal
    print(books, "THIS IS BOOKS")

    
    return render_template('results.html', user = user, books = books)

############### NEW BOOK ##################
###########################################
@app.route('/new_book')
def create():

    return render_template("addbook .html")

### NEW BOOK CREATE PROCESS POST ROUTE ###
###########################################
@app.route('/create_process', methods =['POST'])
def create_process(): 
    is_valid=True 

    if len(request.form['title']) < 3: 
        is_valid = False 
        flash("Title must be at least 3 characters long", "title_error")

    if len(request.form['author']) < 3: 
        is_valid = False 
        flash ("Author must be at least 3 characters long", "author_error")
    
    if is_valid == False: 
        return redirect("addbook.html")

    #create a new book!

    else: 
        mysql = connectToMySQL('fave_books') # connect to db
        query = "INSERT INTO books (title, author, user_id, created_at, updated_at) VALUES (%(title)s, %(author)s, %(id)s, NOW(), NOW());"
        data = {
            "title": request.form ['title'],
            "author": request.form ['author'],
            "id": session ['userid']
        }
        
        new_book_id = mysql.query_db(query, data)
        return redirect('/show')


########### SHOW ONE BOOK  #############
########################################

@app.route('/show/<book_id>')
def showOneBook(book_id): 
    mysql = connectToMySQL('fave_books')
    query = "SELECT * FROM books WHERE id=" +book_id
    book = mysql.query_db(query)
    return render_template("show.html", book = book)

############ DELETE ###############
########################################
@app.route('/delete/<book_id>')

def delete(book_id): 
    print(book_id)
    mysql = connectToMySQL('fave_books') #connect to mysql 
    query = "Delete from books where id="+ book_id
    mysql.query_db(query)
    return redirect("/show")


############### EDIT ##################
#######################################
@app.route('/edit/<book_id>')
def edit(book_id): 
     
    mysql = connectToMySQL('fave_books') #connect to db 
    query = "SELECT * FROM books where id="+book_id  #make your query 
    book = mysql.query_db(query)

    return render_template("edit.html", book = book)


###### EDIT PROCESS POST ROUTE ######
@app.route('/edit_process', methods=['POST'])
def edit_process():
    is_valid = True
    if len(request.form['title']) < 3: 
        is_valid = False 
        flash("Title must be at least 3 or more characters long")
    if len(request.form['author']) < 3: 
        is_valid = False 
        flash ("Author must be at least 3 or more characters long")

    if is_valid == False: 
        return redirect('/edit/'+ request.form['bookID'])

    else: 
        mysql = connectToMySQL('fave_books') 
        query = "UPDATE books SET title=%(title)s,author=%(author)s,updated_at=NOW() WHERE id ="+request.form['bookID']
        data = {
            'title' : request.form['title'],
            'author' : request.form['author']
        }

        mysql.query_db(query, data)
        return redirect('/show')

########### FAVORITES #########
@app.route('/favorite/<book_id>')
def favorite(book_id): 
    mysql = connectToMySQL('fave_books')
    query = "INSERT into favorites (users_liked_id, book_liked_id) VALUES (%(uid)s, %(bid)s)"
    data = {
        'uid': session['user_id'],
        'bid': book_id
    }

    mysql.query_db(query, data)
    return redirect('/show')




################ LOG OUT ######################
#################################################
@app.route('/logout')
def logout():

    session.clear()
    # return redirect('/')
    return render_template('logout.html')



if __name__ == "__main__":
    app.run(debug=True)


