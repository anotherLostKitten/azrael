# azrael - Sarar Aseer, Jason Tung, Johnny Wong and Zane Wang
# SoftDev1 pd8
# P00 -- Da Art of Storytellin'

import os

from flask import Flask, redirect, url_for, render_template, session, request, flash, get_flashed_messages
from utils import db as azrael

DB_FILE = "data/azrael_stories.db"
app = Flask(__name__)
user = None
app.secret_key = os.urandom(32)

def setUser(userName):
    global user
    user = userName

@app.route('/')
def home():
    if user in session:
        data = azrael.DB_Manager(DB_FILE)
        userStories = sorted(data.getStoriesContributedTo(user))
        print(userStories)
        return render_template('user.html', user_name = user, errors = False, stories = userStories)
    return render_template("home.html", errors = False)

@app.route('/login')
def login():
    return render_template("login.html", errors = True)

@app.route('/register')
def register():
    return render_template("register.html", errors = True)

@app.route('/auth', methods=['POST'])
def auth():
    # instantiates DB_Manager with path to DB_FILE
    data = azrael.DB_Manager(DB_FILE)
    username, password = request.form["username"], request.form['password']
    # LOGGING IN
    if request.form["submit"] == "Login":
        print(username, password)
        if username != "" and password != "" and data.verifyUser(username, password ) :
            session[username] = password
            setUser(username)
            data.save()
            return redirect(url_for('home'))
        # user was found in DB but password did not match
        elif data.findUser(username):
            flash('Incorrect password!')
        # user not found in DB at all
        else:
            flash('Incorrect username!')
        data.save()
        return render_template("login.html", errors = True)
    # REGISTERING
    else:
        if len(username) > 0 and not data.findUser(username):
            if len(password) > 0:
                # add the account to DB
                data.registerUser(username, password)
                data.save()
                return redirect(url_for('home'))
            else:
                flash('Bad password!')
        else:
            flash("Username already taken!")
        # TRY TO REGISTER AGAIN
        data.save()
        return render_template("register.html", errors = True)

@app.route('/logout')
def logout():
    session.pop(user, None)
    setUser(None)
    return redirect(url_for('home'))

@app.route('/viewstory')
def viewstory():
    data = azrael.DB_Manager(DB_FILE)
    storyTitle = request.args['submit']
    content = data.getStoryText(storyTitle)
    data.save()
    return render_template('story.html', storyTitle = storyTitle, content = content)

@app.route('/viewothers')
def viewothers():
    data = azrael.DB_Manager(DB_FILE)
    pass

@app.route('/appendToStory')
def appendToStory():
    data = azrael.DB_Manager(DB_FILE)
    pass

@app.route('/creator')
def storyCreator():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def create():
    data = azrael.DB_Manager(DB_FILE)
    story, line = request.form['title'], request.form['line']
    id = data.getID_fromUser(user)
    data.createStory(story)
    data.addToStory(story, line, id)
    data.save()
    return render_template('story.html', storyTitle = story, content = line)




if __name__ == '__main__':
    app.debug = True
    app.run()
