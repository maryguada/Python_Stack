from flask import Flask, render_template, redirect, request, session, flash 
from myconnection import connectToMySQL
import re 
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')  #add this email Regex 

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "keep it secret"


################### MAIN ###############################
########################################################
@app.route("/")
def main(): 

   return render_template("index.html")


############ CREATE / REGISTER USER  ###################
########################################################
@app.route('/createUser', methods=['POST'])
def createUser():
    # include some logic to validate user input before adding them to the database!
    # create the hash
    mysql = connectToMySQL("handy_helper")

    if not EMAIL_REGEX.match(request.form['email']):
        flash ("Invalid email address", "reg_error")

    is_valid = True		# assume True

    if len(request.form['first_name']) < 2:
        is_valid = False
        # display validation error using flash
        flash("Please enter first name","reg_error" )

    if len(request.form['last_name']) < 1:
        is_valid = False
        # display validation error using flash
        flash("Please enter last name.", "reg_error")

    if not EMAIL_REGEX.match(request.form['email']):
        flash ("Invalid email address. Please have email in proper email format.")
        return redirect('/')

    if len(request.form['password']) < 8:
        is_valid = False
        # display validation error using flash
        flash("Password needs to be 8 or more characters", "reg_error")

    if request.form['password'] != request.form['confirm']:
        is_valid = False
        flash("Passwords don't match", "reg_error")
    
    if not is_valid: 
        return redirect("/")

    mysql=connectToMySQL("handy_helper")
    query = "SELECT * FROM users WHERE email =%(email)s"
    data = {
        "email": request.form['email']
    }

    result = mysql.query_db(query, data)
    if len(result)>0: 
        is_valid = False 
        flash('username already exist')
        return redirect("/")

    else: 
        pw_hash = bcrypt.generate_password_hash(request.form['password'])  

        print(pw_hash)  
        # prints something like b'$2b$12$sqjyok5RQccl9S6eFLhEPuaRaJCcH3Esl2RWLm/cimMIEnhnLb7iC'
        # be sure you set up your database so it can store password hashes this long (60 characters)
        mysql = connectToMySQL("handy_helper")
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
        flash("You've been successfully added, you may now log in", "success")
        # never render on a post route, always redirect!
        return redirect("/")

###############  LOG IN VALIDATE   #################
####################################################
@app.route('/login_validate', methods=["POST"])
def login_validate():

    mysql = connectToMySQL("handy_helper")
    query = "SELECT * FROM users WHERE email = %(email)s"
    data = {
        "email": request.form ['email_login']        
        }

    logged_in = mysql.query_db(query,data)

    if logged_in:

        if bcrypt.check_password_hash(logged_in[0]['password'], request.form['log_in_pw']):
            print('BCRYPT MATCHED!')
            session['userid'] = logged_in[0]['id']
            return redirect('/dashboard')

        else:
            flash ("Invalid Credentials. Login denied", "login_error")
            return redirect('')

    else: 
        flash("Log In Failed. Log In Error", "login_error")
        return redirect('/')

            
################## DASHBOARD ###################
################################################
@app.route ('/dashboard')
def show(): 
    #we have to see if user is in session! 
    if 'userid' not in session: 
        flash('You are not logged in, please log in!')
        return redirect ('/')

    mysql = connectToMySQL("handy_helper")
    id = session['userid']

    #user query 
    user_query = "SELECT * FROM users WHERE id =" + str(id)
    user = mysql.query_db(user_query)


    #job query 
    mysql = connectToMySQL("handy_helper")
    book_query =""" SELECT * from jobs
        LEFT JOIN userjobs 
        ON job_posted_id = jobs.id"""

    jobs = mysql.query_db(book_query)

    #print is to check your terminal
    # print(jobs, " *************THIS IS JOBS***************** ")

    return render_template('dashboard.html', user = user, jobs = jobs)



############### ADD A JOB #################
###########################################
@app.route('/add_job')
def addjob():

    return render_template("add_job.html")


### ADD JOB CREATE PROCESS POST ROUTE #####
###########################################
@app.route('/create_process', methods =['POST'])
def create_process(): 
    is_valid=True 

    if len(request.form['job']) < 3: 
        is_valid = False 
        flash("Job must be at least 3 characters long", "job_error")

    if len(request.form['location']) < 3: 
        is_valid = False 
        flash ("Job must be at least 3 characters long", "loc_error")
    
    if is_valid == False: 
        return redirect("/add_job")

    #create a new book!

    else: 

        mysql = connectToMySQL('handy_helper') # connect to db
        query = "INSERT INTO jobs (job, location, user_id, created_at, updated_at) VALUES (%(job)s, %(location)s, %(id)s, NOW(), NOW());"
        data = {
            "job": request.form ['job'],
            "location": request.form ['location'],
            "id": session ['userid']
        }
        
        new_job_id = mysql.query_db(query, data)
        return redirect('/dashboard')


########### SHOW ONE JOB  #############
########################################
@app.route('/show/<job_id>')
def ShowOneJob(job_id): 
    mysql = connectToMySQL('handy_helper')
    query = "SELECT * FROM jobs WHERE id=" +job_id
    job = mysql.query_db(query)
    return render_template("show.html", job = job)


######## ADD TO JOB TO MY LIST  #########
#########################################
@app.route('/add/<job_id>')
def addJobtoList(job_id): 
    mysql = connectToMySQL('handy_helper')
    query = "INSERT into userjobs (user_posted_id, job_posted_id) VALUES (%(uid)s, %(jid)s)"
    data = {
        'uid': session['userid'],
        'jid': job_id
    }

    mysql.query_db(query, data)
    return redirect('/dashboard')


######### REMOVE FROM MY LIST ###############
#############################################
@app.route('/remove/<job_id>')
def remove(job_id): 
    mysql= connectToMySQL('handy_helper')
    query = "DELETE FROM userjobs WHERE job_posted_id ="+job_id
    mysql.query_db(query)
    return redirect('/dashboard')


########### EDIT A JOB ################
#######################################
@app.route('/edit/<job_id>')
def edit(job_id): 
     
    mysql = connectToMySQL('handy_helper') #connect to db 
    query = "SELECT * FROM jobs where id="+job_id #make your query 
    job = mysql.query_db(query)

    return render_template( "edit.html",  job = job)


###### EDIT PROCESS POST ROUTE #########
########################################
@app.route('/edit_process', methods=['POST'])
def edit_process():

    is_valid = True
    if len(request.form['job']) < 3: 
        is_valid = False 
        flash("Title must be at least 3 or more characters long", "job_error")

    if len(request.form['location']) < 3: 
        is_valid = False 
        flash ("Author must be at least 3 or more characters long", "loc_error")

    if is_valid == False: 
        return redirect('/edit/'+ request.form['jobID'])

    else: 
        mysql = connectToMySQL('handy_helper') 
        query = "UPDATE jobs SET job=%(job)s,location=%(location)s,updated_at=NOW() WHERE id=%(id)s"
        data = {
            'job' : request.form['job'],
            'location' : request.form['location'],
            'id' : request.form['jobID']
        }
        mysql.query_db(query, data)
        return redirect("/dashboard")

############# DELETE ##################
########################################
@app.route('/delete/<job_id>')

def delete(job_id): 
    print(job_id)

    mysql = connectToMySQL('handy_helper') #connect to mysql 
    query = "Delete from jobs where id="+job_id
    mysql.query_db(query)
    return redirect("/dashboard")


################  LOG OUT ######################
#################################################
@app.route('/logout')
def logout():

    session.clear()
    # return redirect('/')
    return render_template('logout.html')


if __name__ == "__main__":
    app.run(debug=True)