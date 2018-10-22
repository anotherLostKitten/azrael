# azrael - Sarar Aseer, Jason Tung, Johnny Wong and Zane Wang
# SoftDev1 pd8
# P00 -- Da Art of Storytellin'

import os
import sqlite3

from flask import Flask, redirect, url_for, render_template, request, flash, get_flashed_messages
import utils.db as dog

DB_FILE = "data/azrael_stories.db"

x = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
c = x.cursor()  # facilitate db ops

app = Flask(__name__)

app.secret_key = os.urandom(32)

accts = {}

def reloadAccts():
    test = c.execute("SELECT * FROM users;")

    accts = {}

    for x in test:
        accts[str(x[0])] = {"pass": str(x[1]), "user": int(x[2])}

    print (accts)

reloadAccts()

who  = {}

dog.insertRow('users', ('j', 0, 't'))

@app.route('/')
def hello_world():
    return render_template("root.html")

@app.route('/login')
def login_world():
    return render_template("login.html")

@app.route('/register')
def register_world():
    return render_template("register.html")

@app.route('/auth', methods=['POST'])
def auth():
    #LOGGING IN MEN
    if request.form["submit"] == "login":
        if request.form["username"] in accts:
            if str(request.form['password']) == accts[request.form["username"]]["pass"]:
                who["username"] = request.form["username"]
                return "u r men"
            print(str(request.form['password']), accts[request.form["username"]])
            flash('bad! not ur password bro')
        else:
            flash('bad! username not here!')
        #print("hello", get_flashed_messages())
        return(render_template("login.html"))
    #REGISTERING MEN
    else:
        if len(request.form["username"]) > 0 and request.form["username"] not in accts:
            if len(request.form['password']) > 0:
                #add acct
                return "u r men"
            flash('bad! pass too short')
        else:
            flash('bad! username taken or maybe it\'s too short!')
        # print("hello", get_flashed_messages())
        return (render_template("register.html"))

    # if request.form['username'] in acc:
    #     if request.form['password'] == 'Tung':
    #         session['Ahmed'] = 'Tung'
    #         flash('Success! Logged in as Ahmed', 'success')
    #         return render_template('yes.html',usr = 'Ahmed')
    #     else:
    #         flash('Incorrect Password!', 'error')
    #         return render_template('login.html')
    # flash('Incorrect Username!', 'error')
    # return render_template('login.html')

@app.route('/home')
def homer():
    #something about getting cookies from register or login
    return render_template("root.html")


app.debug = True
app.run()


db.commit()  # save changes
db.close()  # close database
