from flask import Flask, render_template 

app = Flask(__name__)

@app.route('/')
def index():
    print("Display checkerboard")
    return render_template('checkerboardindex.html')
    

@app.route('/4')
def index1(): 
    return render_template('checkerboard.html')

if __name__=="__main__":
    app.run(debug = True)


