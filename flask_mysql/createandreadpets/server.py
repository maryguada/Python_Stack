from flask import Flask, render_template, redirect, request 

# import the function that will return an instance of a connection
# "myconnection" is the name of my file! 
from myconnection import connectToMySQL  

app = Flask(__name__)

########### INDEX #############
###############################
@app.route("/")
def root(): 
    #display information to client:
    #step one: connect to db 
    mysql = connectToMySQL("crpets")

    #step two: make query 
    query = "SELECT * FROM pets"
    
    #this query will return us a list of dictionaries 
    # the variable "pets" will hold  a list of dictionaries that we 
    # can loop through to display all of our data 
    pets = mysql.query_db(query)

    # now we can pass pets to the front end to display to user 
    # pets in blue is referenced in our HTML!
    # pets in white comes from our server! 
    return render_template("index.html", pets=pets)


######### CREATE A PET ############
###################################
@app.route('/createPet', methods=["POST"])
def create(): 
    #this will print in the terminal since its a post request
    print (request.form['name']) 
    print (request.form['type'])
    #when inserting/ adding into data base follow these steps:
    mysql = connectToMySQL("crpets") # connect to your db first!
    query = "INSERT INTO pets (name, type, created_at, updated_at) VALUES(%(name)s, %(type)s, NOW(), NOW())"
    data = { 
        'name': request.form['name'],
        'type': request.form['type']
    }
    #call on query_db
    mysql.query_db(query, data)

    return redirect("/")

####### DELETE ########## GET ROUTE. using an <a> tag to send a request to our server along with out id. 
#########################
@app.route("/delete/<petid>")
def delete(petid): 

    print (petid) #access the id of the pet we want to delete 
    # connect to db!
    mysql = connectToMySQL("crpets")
    #make a delete query!!
    query = "DELETE from pets where id="+petid

    mysql.query_db(query)
    return redirect('/')

######## EDIT #####################
###################################
@app.route("/edit/<id>") # This is a get route
def showEdit(id): 
    #get info from db to display to user. 
    mysql = connectToMySQL("crpets")

    query = "SELECT * FROM pets where id ="+id
    pet = mysql.query_db(query)
    return render_template("edit.html", pet = pet)


@app.route('/editProcess', methods=['POST'])
def edit():
    #first thing we want to do when first route
    # lets print the date to make sure we are getting the correct data 

    print(request.form['name'])
    print(request.form['type'])
    print(request.form['id'])
#update the table name then column and then value 
    query = "UPDATE pets SET name=%(name)s, type=%(type)s, updated_at=NOW() WHERE id =%(id)s"
    data = {
        'name': request.form['name'],
        'type': request.form['type'],
        'id': request.form['id']
    }
    mysql = connectToMySQL('crpets')
    mysql.query_db(query,data)

    return redirect('/')
    
    
if __name__ =="__main__":
    app.run(debug=True)