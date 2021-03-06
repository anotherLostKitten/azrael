#azrael -- Sarar Aseer, Jason Tung, Johnny Wong and Zane Wang
#SoftDev1 pd8
#P00 -- Da Art of Storytellin'

import sqlite3   # enable control of an sqlite database

class DB_Manager:
    '''
    HOW TO USE:
    Every method openDB by connecting to the inputted path of
    a database file. After performing all operations on the
    database, the instance of the DB_Manager must save using
    the save method.
    The operations/methods can be found below. DB_Manager
    has been custom fitted to work with
    P00 -- Da Art of Storytellin'
    '''
    def __init__(self, dbfile):
        '''
        SET UP TO READ/WRITE TO DB FILES
        '''
        self.DB_FILE = dbfile
        self.db = None
    #========================HELPER FXNS=======================
    def openDB(self):
        '''
        OPENS DB_FILE AND RETURNS A CURSOR FOR IT
        '''
        self.db = sqlite3.connect(self.DB_FILE) # open if file exists, otherwise create
        return self.db.cursor()

    def tableCreator(self, tableName, col0, col1, col2):
        '''
        CREATES A 3 COLUMN TABLE IF tableName NOT TAKEN
        ALL PARAMS ARE STRINGS
        '''
        c = self.openDB()
        if not self.isInDB(tableName):
            command = "CREATE TABLE '{0}'({1}, {2}, {3});".format(tableName, col0, col1, col2)
            c.execute(command)


    def insertRow(self, tableName, data):
       '''
         APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
         @tableName is the name the table being written to
         @data is a tuple containing data to be entered
       '''
       c = self.openDB()
       command = "INSERT INTO '{0}' VALUES(?, ?, ?)"
       c.execute(command.format(tableName), data)


    def isInDB(self, tableName):
        '''
        RETURNS True IF THE tableName IS IN THE DATABASE
        RETURNS False OTHERWISE
        '''
        c = self.openDB()
        command = "SELECT * FROM sqlite_master WHERE type = 'table'"
        c.execute(command)
        selectedVal = c.fetchall()
        # list comprehensions -- fetch all tableNames and store in a set
        tableNames = set([x[1] for x in selectedVal])

        return tableName in tableNames

    def table(self, tableName):
        '''
        PRINTS OUT ALL ROWS OF INPUT tableName
        '''
        c = self.openDB()
        command = "SELECT * FROM '{0}'".format(tableName)
        c.execute(command)
        print(c.fetchall())


    def save(self):
        '''
        COMMITS CHANGES TO DATABASE AND CLOSES THE FILE
        '''
        self.db.commit()
        self.db.close()
    #========================HELPER FXNS=======================

    #======================== DB FXNS =========================

    def createStory(self, storyTitle):
        '''
        CREATES TABLE OF storyTitle IF storyTitle IS UNIQUE(NOT FOUND IN DATABASE)
        '''
        if not self.findStory(storyTitle):
            self.tableCreator(storyTitle, 'story_id integer', 'story_line text', 'user_id integer')
            return True
        return False

    def addToStory(self, storyTitle, text, user_id):
        '''
        ADD text TO storyTitle's TABLE TO DATABASE
        IF USER CONTRIBUTED TO storyTitle ALREADY, DON'T ADD TO STORY
        '''
        c = self.openDB()
        if user_id in self.get_user_ids(storyTitle):
            return False
        # otherwise add text to story
        command = "SELECT story_id FROM '{0}' WHERE story_id == (SELECT max(story_id) FROM '{0}')".format(storyTitle)
        c.execute(command)
        selectedVal = c.fetchone()
        # max_id represents the id of the most recent story_line in storyTitle table
        max_id = 0
        if selectedVal == None:
            max_id = 0
        else:
            max_id = selectedVal[0]
        row = (max_id + 1, text, user_id)
        self.insertRow(storyTitle, row)
        return True

    def findMostRecentUpdate(self, storyTitle):
        '''
        RETURNS TEXT OF MOST RECENT UPDATE TO storyTitle
        '''
        c = self.openDB()
        command = "SELECT story_line FROM '{0}' WHERE story_id == (SELECT max(story_id) FROM '{0}')".format(storyTitle)
        c.execute(command)
        selectedVal = c.fetchone()[0]
        return selectedVal

    def getStoryText(self, storyTitle):
        '''
        RETURNS ALL TEXT OF storyTitle
        '''
        c = self.openDB()
        command = "SELECT story_line FROM '{0}'".format(storyTitle)
        c.execute(command)
        selectedVal = c.fetchall()
        textList = [x[0] for x in selectedVal]
        return '\n'.join(textList)

    def findStory(self, storyTitle):
        '''
        Checks if storyTitle is unique
        '''
        storyNames = self.getStories()
        return storyTitle in storyNames

    def getStories(self):
        '''
        RETURNS A SET CONTAINING ALL CURRENT storyTitles
        '''
        c = self.openDB()
        command = "SELECT * FROM sqlite_master WHERE type = 'table'"
        c.execute(command)
        selectedVal = c.fetchall()
        # list comprehensions -- fetch all storyTitles and store in a set
        storyNames = set([x[1] for x in selectedVal if x[3] > 2])
        return storyNames

    def getStoriesContributedTo(self, userName):
        '''
        RETURNS A SET CONTAINING ALL CURRENT storyTitles userName contributed to
        '''
        c = self.openDB()
        contributions = set()
        for story in self.getStories():
            id = str(self.getID_fromUser(userName))
            command = "SELECT user_id FROM '{0}' WHERE user_id = '{1}';".format(story, id)
            c.execute(command)
            selectedVal = c.fetchone()
            if selectedVal != None:
                contributions.add(story)
        #print(contributions)
        return contributions

    def getUsers(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND CORRESPONDING PASSWORDS
        '''
        c = self.openDB()
        command = "SELECT user_name, passwords FROM users"
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def get_user_ids(self, storyTitle):
        '''
        RETURNS SET OF user_ids CONTRIBUTED TO storyTitle
        '''
        c = self.openDB()
        command = "SELECT user_id FROM '{0}'".format(storyTitle)
        c.execute(command)
        ids = set(x[0] for x in c.fetchall())
        return ids

    def registerUser(self, userName, password):
        '''
        ADDS user TO DATABASE
        '''
        c = self.openDB()
        command = "SELECT user_id FROM users WHERE user_id = (SELECT max(user_id) FROM users)"
        c.execute(command)
        selectedVal = c.fetchone()
        max_id = 0
        if selectedVal != None:
            max_id = selectedVal[0]
        else:
            max_id = 0
            # userName is already in database -- do not continue to add
        if self.findUser(userName):
            return False
        # userName not in database -- continue to add
        else:
            row = (userName, password, max_id + 1)
            self.insertRow('users', row)
            return True

    def findUser(self, userName):
        '''
        CHECKS IF userName IS UNIQUE
        '''
        return userName in self.getUsers()

    def verifyUser(self, userName, password):
        '''
        CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
        '''
        c = self.openDB()
        command = "SELECT user_name, passwords FROM users WHERE user_name = {0}".format("'" + userName + "'")
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal == None:
            return False
        if userName == selectedVal[0] and password == selectedVal[1]:
            return True
        return False

    def getID_fromUser(self, userName):
        '''
        RETURNS user_id OF userName
        '''
        c = self.openDB()
        command = "SELECT user_id FROM users WHERE user_name == '{0}'".format(userName)
        c.execute(command)
        id = c.fetchone()[0]
        return id
    #======================== DB FXNS =========================
#======================== END OF CLASS DB_Manager =========================

# TESTS
#x = DB_Manager("../data/azrael.db")
#x.tableCreator('users', 'user_name text', 'passwords text', 'user_id integer')
#x.addToStory('abc', 'snitcher13123', 5)
#print(x.getStoryText('abc'))
#x.registerUser('men', '123')
#x.addToStory('abc', 'lmaoxD', x.getID_fromUser('men'))
#x.registerUser('women', '456')
#x.registerUser('admin', 'admin')
#print(x.get_user_ids('users'))
#print(x.getID_fromUser('jwt'))
#x.addToStory('abc', 'jwtWasHere', 4)
#print(x.getStoryText('abc'))
#print(x.getID_fromUser('jwt'))

#x.table('users')

#x.createStory('cake')
#x.addToStory('cake', 'yummy', 4)
#print(x.getStoriesContributedTo('jwt'))
#x.save()
