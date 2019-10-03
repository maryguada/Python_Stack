from flask import Flask, render_template, redirect, request, session, flash

from mysqlconnection import connectToMySQL   # import the function that will return an instance of a connection
app = Flask(__name__)
app.secret_key = "keep it secret"
@app.route("/")
def index():
    # call the function, passing in the name of our db
    mysql = connectToMySQL('first_flask')	 

    # call the query_db function, pass in the query as a string       
    friends = mysql.query_db('SELECT * FROM friends;')  
    print(friends)
    return render_template("index.html", all_friends = friends)


@app.route('/create_friend', methods =["POST"])
def add_friend_to_db():
    is_valid = True		# assume True

    if len(request.form['fname']) < 1:
        is_valid = False
        # display validation error using flash
        flash("Please enter first name")


    if len(request.form['lname']) < 1:
        is_valid = False
        # display validation error using flash
        flash("Please enter last name")


    if len(request.form['occ']) < 2:
        is_valid = False
        # display validation error
        flash("Please enter valid occupation name")
        
    if is_valid:                

        # if there are errors:
            # figure out a way to show the user what went wrong
        # else if there are no errors:
            # code from above to actually insert user into the database

        query = "INSERT INTO users (first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(oc)s, NOW(), NOW()); "
        data = {
            'fn': request.form['fname'],
            'ln': request.form['lname'], 
            'oc': request.form['occ']
        }

        db = connectToMySQL("first_flask")
        db.query_db (query, data)
        flash("Successfully added!")
    return redirect ("/")


if __name__ == "__main__":
    app.run(debug=True)

