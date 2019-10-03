from flask import Flask, render_template, request, redirect 

#import function to connect to db
from mydb import connectToMySQL
app = Flask(__name__)

########## INDEX ##########
@app.route('/')
def root():
    # after creating db, we want to display this information to the client 
    # first connect to db
    mysql = connectToMySQL('crpets')
    query = "SELECT * FROM pets"
    pets = mysql.query_db(query)

    return render_template('index.html', pets = pets)


####### Creating a Pet #### Post Method! 
@app.route('/createPet', methods=["POST"])
def create(): 
    #print insert query. this will print in your terminal!! 
    print(request.form['name'])
    print(request.form['type'])
    
    #connect to db! 
    mysql = connectToMySQL('crpets')

    #now to call on the insert query 
    #insert into ___TABLE NAME____
    query = "INSERT into pets (name, type, created_at, updated_at) VALUES (%(name)s, %(type)s, NOW(), NOW())"
    #do the data object table 
    data = {
        'name': request.form['name'], 
        'type': request.form['type']
    }
    mysql.query_db(query, data)
    return redirect('/')

####### Delete ###### 
@app.route('/delete/<id>')
def delete(id): 
    print(id)
    # connect to db! 
    mysql = connectToMySQL('crpets')
    # insert your delete query! add id at the end to tell MySQL which one to delete
    query = "DELETE FROM pets WHERE id="+id
    mysql.query_db(query)
    return redirect('/')

####### Edit ########
@app.route('/edit/<id>')
#pass the id in the function! this is SHOW EDIT PAGE ROUTE 
def showEdit(id): 
    #we need to show the information to the client first 
    #connect to DB! 
    # mysql = connectToMySQL('crpets')
    # # make query
    # query  = "SELECT * FROM pets WHERE id="+id
    # #step two: connect to db
    # pet = mysql.connectToMySQL('crpets')
    # return render_template("edit.html", pet=pet)
    mysql = connectToMySQL("crpets")

    query = "SELECT * FROM pets where id ="+id
    pet = mysql.query_db(query)
    return render_template("edit.html", pet = pet)

###### This is the POST Edit ROUTE 
###### Remeber to pass in the id as a hidden input on your html template!!
###### Hidden input is a way for us to pass our id from our client to the server
###### so server knows which one to edit out and so that id is a part of our post body!
@app.route('/editPet', methods=['POST'])
def edit(): 
    print(request.form['name'])
    print(request.form['type'])
    print(request.form['id'])
    #update table , set name = value. no need for created at but need ID!
    query = "UPDATE pets name=%(name)s, type=%(type)s, updated_at=NOW() WHERE id =%(id)s"

    data ={

        'name': request.form['name'], 
        'type': request.form['type'],
        'id': request.form['id']      
    }
    #connect to database!! 
    mysql = connectToMySQL('crPets')
    mysql.query_db(query, data)

    return redirect('/')


if __name__ =="__main__": 
    app.run(debug=True)
