from flask import Flask, render_template, request, redirect 
app = Flask(__name__)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/checkout', methods =["POST"])
def checkout():

    return render_template('checkout.html')