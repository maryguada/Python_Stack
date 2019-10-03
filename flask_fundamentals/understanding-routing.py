# Import Flask to allow us to create our app
from flask import Flask  
# Create a new instance of the Flask class called "app"
app = Flask(__name__)   
# The "@" decorator associates this route with the function immediately following
@app.route('/')     
def hello_world():
    return 'Hello World!'  # Return the string 'Hello World!' as a response

@app.route('/<name>')
def hello_dojo(name): 
    print(name)
    return f"Hello {name}!" 


@app.route('/say/<info>')
def say_function(info):
    print(info)
    return f"Hello {info}!"

@app.route('/repeat/<int:number>/<string>')
def repeat(string,number):  
    rep = (string * number)  
    return rep 
  
    
if __name__=="__main__":  # Ensure this file is being run directly and not from a different module 
    app.run(debug=True)    # Run the app in debug mode.

