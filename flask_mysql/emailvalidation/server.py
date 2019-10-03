from flask import Flask, render_template, redirect, request, flash, session
import re 
from myconnection import connectToMySQL

#add this email Regex 
emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')  


app = Flask(__name__)
app.secret_key = 'Secret Key' 
mysql = connectToMySQL('email_validation')	  

############## INDEX ##############
@app.route('/')
def index():
    return render_template('index.html')


############# CREATE ######## 
@app.route('/create', methods=["POST"])
def create():
    is_valid = True
    
    #if email is left blank 
    if request.form['email'] == " ": 
        flash("Email cannot be left blank")
        is_valid = False 
        
    elif not emailRegex.match(request.form['email']): 
        flash("Invalid email address")

    else: 
        email = request.form['email']
        session['email'] = email
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(session['email'])
        print(query)
        
        mysql = connectToMySQL('email_validation')
        mysql.query_db(query)

    return redirect('results')


######### Results ##########
@app.route('/results')
def show(): 
    query = "SELECT * FROM emails"
    users = mysql.query_db('SELECT * FROM emails;')
    
    return render_template('results.html', email = session['email'], list=users)


######## Delete ###########
@app.route('/delete', methods=['POST'])
def delete():
    id = int(request.form['hidden'])
    query = "DELETE FROM emails WHERE idemails = '{}'".format(id)
    print (query)
    mysql.query_db(query)
    return redirect('/results')

if __name__ == "__main__": 
    app.run(debug=True)