# Import Flask to allow us to create our app
from flask import Flask, render_template, request 
# Create a new instance of the Flask class called "app"

app = Flask(__name__)   
# The "@" decorator associates this route with the function immediately following

@app.route('/')     
def index(): 
    return render_template("index-html.html", phrase="hello", times =5)


@app.route('/lists')
def render_lists():
    student_info= [
        {'name' : 'Michael', 'age' : 35},
        {'name' : 'John', 'age': 30}, 
        {'name' : 'Mark', 'age': 25}, 
        {'name' : 'KB', 'age': 27}, 
    ]
    return render_template("lists-html.html", random_numbers = [3,1,5], students = student_info)

# @app.route('/<name>')
# def hello_person(name): 
#     print("in hello_person function")
#     print(name)
#     return render_template(index.html) 

if __name__=="__main__":  # Ensure this file is being run directly and not from a different module 
    app.run(debug=True)    # Run the app in debug mode.
