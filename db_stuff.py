#azrael -- Sarar Aseer, Jason Tung, Johnny Wong and Zane Wang
#SoftDev1 pd8
#P00 -- Da Art of Storytellin'

import sqlite3   # enable control of an sqlite database

# set up to read/write to db files

DB_FILE='azrael_stories.db'
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

#========================HELPER FXNS=======================
def tableCreator(tableName, col0, col1, col2):
    '''
    CREATES A 3 COLUMN TABLE
    ALL PARAMS ARE STRINGS
    '''
    command = "CREATE TABLE {0}({1}, {2}, {3});".format(tableName, col0, col1, col2)
    c.execute(command)

def insertRow(tableName, data):
    '''
    @tableName is the name the table being written to
    @data is a tuple containing data to be entered
    '''
    command = "INSERT INTO {0} VALUES(?, ?, ?)"
    c.execute(command.format(tableName), info)

def createStory(storyTitle):
    tableCreator(storyTitle, 'story_id integer', 'story_line text', 'user_id integer')

def addToStory(storyTitle, text, user_id):
    command = "SELECT id FROM {0} WHERE id == (SELECT max(id) FROM {0})".format(storyTitle)
    c.execute(command)
    max_id = int(c.fetchall())
    addCommand = "INSERT INTO {0} VALUES (?, ?, ?)".format(storyTitle)
    row = (max_id + 1, text, user_id)
    c.execute(addCommand, row)




#===========================================================


#============================MAIN===========================

# CREATE USERS TABLE
tableCreator('users text', 'user_name text', 'passwords text', 'user_id integer')





db.commit() #save changes
db.close()  #close database
