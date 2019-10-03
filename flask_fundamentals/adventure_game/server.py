from flask import Flask, render_template, request, redirect
app = Flask(__name__)   

@app.route('/')
def inder(): 
    return render_template('page1.html') 

@app.route('/choiceA')
def choiceA():
    return render_template('page2.html')

@app.route('/choiceB')
def choiceB():
    return render_template('page3.html')

@app.route('/choiceC')
def choiceC():
    return render_template('page4.html')

@app.route('/choiceD')
def choiceD():
    return render_template('page5.html')

@app.route('/choiceE')
def choiceE():
    return render_template('page6.html')

@app.route('/choiceF')
def choiceF():
    return render_template('page7.html')

@app.route('/choiceG')
def choiceG():
    return render_template('page8theEnd.html')

@app.route('/choiceH')
def choiceH():
    return render_template('page8theEnd.html')

@app.route('/choiceI')
def choiceI():
    return render_template('page8theEnd.html')

@app.route('/choiceJ')
def choiceJ():
    return render_template('page8theEnd.html')

@app.route('/choiceK')
def choiceK():
    return render_template('page8theEnd.html') 

@app.route('/choiceL')
def choiceL():
    return render_template('page8theEnd.html')

@app.route('/choiceM')
def choiceM():
    return render_template('page8theEnd.html')

@app.route('/choiceN')
def choiceN():
    return render_template('page8theEnd.html')



if __name__=="__main__":  # Ensure this file is being run directly and not from a different module 
    app.run(debug=True)    # Run the app in debug mode.
