from flask import Flask, render_template, redirect, request 
app = Flask(__name__)  

@app.route('/lists')
def lst(): 

    user_names = [
        {'first_name' : 'Michael', 'last_name' : 'Choi'},
        {'first_name' : 'John', 'last_name' : 'Supsupin'},
        {'first_name' : 'Mark', 'last_name' : 'Guillen'},
        {'first_name' : 'KB', 'last_name' : 'Tonel'}
        ]

    return render_template('index.html', user = user_names)


if __name__=="__main__":  # Ensure this file is being run directly and not from a different module 
    app.run(debug=True)    # Run the app in debug mode.