from flask import Flask, render_template, request, redirect 
app = Flask (__name__)

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/result', methods = ['POST'])
def getinfo(): 
    print("Got Post Info")

    name_form = request.form['name']
    dojo_form = request.form['location']
    language_form = request.form['language']
    comment_form = request.form['comment'] 

    return render_template("show.html", name_template=name_form, dojo_template=dojo_form, language_template = language_form, comment_template = comment_form )



if __name__=="__main__":
    app.run(debug =True)





