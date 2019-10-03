from flask import Flask, render_template, redirect, request 
app = Flask(__name__)  

# #play should render three blue boxes. Use template to do this.
@app.route('/play')
def index():
    return render_template("playground.html",times=3)

# 7 BOXES
@app.route('/play/<times>')
def index_play_x(times):
    return render_template('playground.html', times=int(times))


@app.route('/play/<times>/<color>') 
def index_play_color(times, color):
    return render_template('playground.html', times=int(times), color=color)


if __name__=="__main__":  # Ensure this file is being run directly and not from a different module 
    app.run(debug=True)    # Run the app in debug mode.



