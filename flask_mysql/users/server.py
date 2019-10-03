from flask import Flask, render_template, redirect, request
import re 

from myconnection import connectToMySQL
app = Flask(__name__)

@app.route("/")
def main(): 
   return render_template("index.html")


############################   MAIN    ######################################
#############################################################################
@app.route("/users/new")
def index():
    # call the function, passing in the name of our db
    mysql = connectToMySQL('users_assignment')	  
    # call the query_db function, pass in the query as a string
    users = mysql.query_db('SELECT * FROM users;')      
    print(users)
    return render_template("index.html", all_users = users)

#############################  CREATE  ######################################
#############################################################################
@app.route("/users/create", methods = ["POST"])
def create_user(): 

    query = "INSERT INTO users (full_name, email, created_at, updated_at) VALUES ( %(fname)s, %(email)s, NOW(),  NOW());"
    data = { 
        'fname': request.form["full_name"],
        'email': request.form["email"]
    }
    db = connectToMySQL("users_assignment")
    new_user_id = db.query_db (query, data)
    return redirect("/users/"+str(new_user_id))

#########################  SHOW INDIVIDUAL INFO  ##########################
###########################################################################
@app.route("/users/<id>") 
def show_user(id): 
    mysql = connectToMySQL('users_assignment')
    users = mysql.query_db("SELECT * FROM users WHERE ID="+id)
    print(users)
    return render_template("show.html", one_us = users) 


########################### SHOW ALL USERS ##############################
#########################################################################
@app.route("/users")
def show_all(): 
    mysql = connectToMySQL('users_assignment')
    users = mysql.query_db('SELECT * FROM users;')
    print(users)
    return render_template('showall.html', all_users = users)

############################# DELETE ###################################
########################################################################
@app.route("/delete/<id>")
def deleter(id): 
    print(id)
    mysql = connectToMySQL("users_assignment")
    query = "DELETE FROM users WHERE id="+id 
    mysql.query_db(query)
    return redirect('/users')

############################  EDIT    ##################################
########################################################################

#add proper resourceful coding aka 'users/edit/<id>'
@app.route('/edit/<id>')  # this is a GET route 
def showEdit(id):
    query = "SELECT * FROM  users WHERE id="+id
    mysql = connectToMySQL('users_assignment')
    
    users = mysql.query_db(query)
    return render_template("edit.html", users = users[0])


@app.route("/edit/Process", methods=['POST'])
def edit(): 
    print (request.form ['full_name'])
    print (request.form ['email'])

    query = "UPDATE users SET full_name = %(name)s, email=%(email)s, updated_at=NOW() WHERE id=%(id)s"

    data = {

        'name': request.form['full_name'],
        'email': request.form['email'],
        'id': request.form['id']
    
    }

    mysql = connectToMySQL('users_assignment')
    mysql.query_db(query, data)

    return redirect('/users/'+data['id'])


if __name__ == "__main__":
    app.run(debug=True)


   













