# azrael - Jason Tung and <<<NAME>>>
# SoftDev1 pd8
# P00 -- <<<FILL THIS OUT>>>
# <<YEAR-MON-DAY>>
import sqlite3

from flask import Flask, redirect, url_for, render_template

DB_FILE = "dog.db"

db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
c = db.cursor()  # facilitate db ops

app = Flask(__name__)

acct_stack = {}

@app.route('/')
def hello_world():
    return render_template("loginregister.html")

@app.route('/login')
def login_world():
    return render_template("login.html")

@app.route('/register')
def register_world():
    return render_template("register.html")

@app.route('/home')
def register_world():
    #something about getting cookies from register or login
    return render_template("home.html", usr= acct_stack[0])


if __name__ == "__main__":
    app.debug = True
    app.run()


db.commit()  # save changes
db.close()  # close database