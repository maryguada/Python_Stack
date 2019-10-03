from flask import Flask, render_template, redirect, request, session, flash

# import the function that will return an instance of a connection
from myconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "secret key"

###################  MAIN INDEX   #######################
#########################################################
@app.route('/')
def index():
    return render_template('index.html') 

#######################  ADD  ##########################
@app.route('/results', methods=['POST'])
def process():
    is_valid = True 
    if len(request.form['full_name']) < 3:
        is_valid = False 
        flash("Name cannot be empty. Please enter name.")

    if len(request.form['location']) < 3:
        is_valid = False
        flash ("Location is not valid")

    if len(request.form['language']) <3: 
        is_valid = False
        flash ("Favorite language is not valid")

    if not is_valid:
        return redirect('/')
             
    if is_valid: 
        mysql = connectToMySQL("survey")

        query = "INSERT INTO users (name, location, fave_language, comments, created_at, updated_at) VALUES( %(name)s, %(location)s, %(language)s, %(comments)s, NOW(), NOW());" 

        data = {
            "name": request.form['full_name'],
            "location": request.form['location'],
            "language": request.form['language'],
            "comments": request.form['comments']
        }

        id=mysql.query_db(query,data)
        print(data)
        flash("survey succesfully added!")
        return redirect('/show/'+str(id))


###################### SHOW #########################
#####################################################
@app.route('/results/<id>')
def show(id): 
    mysql = connectToMySQL('survey')
    query = "SELECT * FROM users WHERE id="+id 
    users = mysql.query_db(query)
    return render_template('results.html', users=users)

if __name__=="__main__":
    app.run(debug=True)




