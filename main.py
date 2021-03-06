# azrael - Sarar Aseer, Jason Tung, Johnny Wong and Zane Wang
# SoftDev1 pd8
# P00 -- Da Art of Storytellin'

import os

from flask import Flask, redirect, url_for, render_template, session, request, flash, get_flashed_messages
from utils import db as azrael

DB_FILE = "data/azrael_stories.db"
app = Flask(__name__)
user = None
currStory = None
app.secret_key = os.urandom(32)

def setUser(userName):
    global user
    user = userName
def setStory(storyTitle):
    global currStory
    currStory = storyTitle

@app.route('/')
def home():
    if user in session:
        data = azrael.DB_Manager(DB_FILE)
        userStories = sorted(data.getStoriesContributedTo(user))
        contribute = len(userStories) > 0
        return render_template('user.html', user_name = user, good = True, stories = userStories, contributed = contribute)
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
        if len(username.strip()) != 0 and not data.findUser(username):
            if len(password.strip()) != 0:
                # add the account to DB
                data.registerUser(username, password)
                data.save()
                return redirect(url_for('home'))
            else:
                flash('Password needs to have stuff in it')
        elif len(username) == 0:
            flash("Username needs to have stuff in it")
        else:
            flash("Username already taken!")
        # TRY TO REGISTER AGAIN
        return render_template("register.html", errors = True)

@app.route('/logout')
def logout():
    session.pop(user, None)
    setUser(None)
    return redirect(url_for('home'))

@app.route('/creator')
def storyCreator():
    return render_template('create.html')

@app.route('/create', methods=['POST'])
def create():
    data = azrael.DB_Manager(DB_FILE)
    allStories = data.getStories()
    story, line = request.form['title'], request.form['line']
    if story in allStories:
        flash('Story title taken!')
        return render_template('create.html', errors = True)
    if (len(story.strip()) == 0 or len(line.strip())==0):
        flash("Please don't contribute blank spaces!")
        return render_template('create.html', errors = True)
    id = data.getID_fromUser(user)
    data.createStory(story)
    data.addToStory(story, line, id)
    data.save()
    return render_template('story.html', storyTitle = story, content = line)

@app.route('/viewothers')
def viewothers():
    data = azrael.DB_Manager(DB_FILE)
    allStories = data.getStories()
    userStories = data.getStoriesContributedTo(user)
    notUserStories = filter(lambda x: x not in userStories, allStories)
    return render_template("view.html",stories = notUserStories)


@app.route('/viewstory', methods=['POST'])
def viewstory():
    data = azrael.DB_Manager(DB_FILE)
    storyTitle = request.form['submit']
    content = data.getStoryText(storyTitle)
    data.save()
    return render_template('story.html', storyTitle = storyTitle, content = content)


@app.route('/viewotherstory', methods=["POST"])
def addForm():
    data = azrael.DB_Manager(DB_FILE)
    storyTitle = request.form['submit']
    setStory(storyTitle)
    mostRecent = data.findMostRecentUpdate(storyTitle)
    data.save()
    return render_template('otherstory.html', storyTitle = storyTitle, content = mostRecent)

@app.route('/addauth', methods=["POST"])
def addauth():
    data = azrael.DB_Manager(DB_FILE)
    user_id = data.getID_fromUser(user)
    appendContent = request.form["text"]
    if (len(appendContent.strip()) == 0):
        flash("Please don't contribute blank spaces!")
        return render_template('otherstory.html', storyTitle=currStory, content=data.findMostRecentUpdate(currStory), errors = True)
    data.addToStory(currStory, appendContent, user_id)
    data.save()
    flash('Contributed to {0}'.format(currStory))
    setStory(None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.debug = True
    app.run()
