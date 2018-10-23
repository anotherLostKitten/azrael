#azrael -- Sarar Aseer, Jason Tung, Johnny Wong and Zane Wang
#SoftDev1 pd8
#P00 -- Da Art of Storytellin'

import sqlite3   # enable control of an sqlite database

# set up to read/write to db files


class db(dbfile):
    self.DB_FILE = dbfile
    self.db = sqlite3.connect(dbfile) # open if file exists, otherwise create
    self.c = self.db.cursor()

    
    
    #========================HELPER FXNS=======================
    def tableCreator(self, tableName, col0, col1, col2):
        '''
        CREATES A 3 COLUMN TABLE
        ALL PARAMS ARE STRINGS
        '''
        command = "CREATE TABLE {0}({1}, {2}, {3});".format(tableName, col0, col1, col2)
        c.execute(command)

    def insertRow(self, tableName, data):
       '''
         APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
         @tableName is the name the table being written to
         @data is a tuple containing data to be entered
       '''
         command = "INSERT INTO {0} VALUES(?, ?, ?)"
         c.execute(command.format(tableName), data)
         db.commit()  # save changes
         db.close()  # close database


    #========================HELPER FXNS=======================

    #======================== DB FXNS =========================

    def createStory(self, storyTitle):
        if self.findStory(storyTitle):
            tableCreator(storyTitle, 'story_id integer', 'story_line text', 'user_id integer')
            return True
        return False

    def addToStory(self, storyTitle, text, user_id):
        '''
        ADD text TO storyTitle's TABLE TO DATABASE
        IF USER CONTRIBUTED TO storyTitle ALREADY, DON'T ADD TO STORY
        '''
        if user_id in self.get_user_ids(storyTitle):
            return False
        # otherwise add text to story
        command = "SELECT story_id FROM {0} WHERE story_id == (SELECT max(story_id) FROM {0})".format(storyTitle)
        self.c.execute(command)
        selectedVal = self.c.fetchone()
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
    RETURNS TEXT OF MOST UPDATE TO storyTitle
    '''
    command = "SELECT story_line FROM {0} WHERE story_id == (SELECT max(story_id) FROM {0})".format("'" + storyTitle + "'")
    self.c.execute(command)
    selectedVal = self.c.fetchone()[0]
    return selectedVal

    def findStory(storyTitle):
    '''
    Checks if storyTitle is unique
    '''
                    storyNames = getStories()
                    if storyTitle in storyNames:
                        return False
                    return True

                def getStories():
                    # Returns a set containing all current storyTitles
                    command = "SELECT * FROM sqlite_master WHERE type = 'table'"
                    c.execute(command)
                    selectedVal = c.fetchall()
                    # list comprehensions -- fetch all storyTitles and store in a set
                    storyNames = set([x[1] for x in selectedVal if x[3] > 2])
                    return storyNames

                def get_user_ids(storyTitle):
                    # Returns set of user_ids contributed to storyTitle
                    command = "SELECT user_id FROM {0}".format("'" + storyTitle + "'")
                    c.execute(command)
                    ids = set(x[0] for x in c.fetchall())
                    return ids

                def registerUser(userName, password):
                    # Adds user to database
                    command = "SELECT user_id FROM users WHERE user_id == (SELECT max(user_id) FROM users)"
                    c.execute(command)
                    selectedVal = c.fetchone()
                    max_id = 0
                    if selectedVal != None:
                        max_id = selectedVal[0]
                    else:
                        max_id = 0
                        # userName is already in database -- do not continue to add
                        if findUser(userName):
                            return False
                        # userName not in database -- continue to add
                        else:
                            row = (userName, password, max_id + 1)
                            insertRow('users', row)
                            return True

                        def findUser(userName):
                            # Checks if userName is unique
                            command = "SELECT user_name FROM users WHERE user_name == {0}".format("'" + userName + "'")
                            c.execute(command)
                            selectedVal = c.fetchone()
                            if selectedVal == None:
                                return False
                            return True

                        def verifyUser(userName, password):
                            # Checks if userName and password match those found in database
                            command = "SELECT user_name, passwords FROM users WHERE user_name == {0}".format("'" + userName + "'")
                            c.execute(command)
                            selectedVal = c.fetchone()
                            if userName == selectedVal[0] and password == selectedVal[1]:
                                return True
                            return False

                        def getID_fromUser(userName):
                            # Returns user_id of userName
                            command = "SELECT user_id FROM users WHERE user_name == {0}".format("'" + userName + "'")
                            c.execute(command)
                            id = c.fetchone()[0]
                            return id
                        #======================== DB FXNS =========================


#========================  TESTS  =========================

# CREATE USERS TABLE
# tableCreator('users', 'user_name text', 'passwords text', 'user_id integer')
#
#
# createStory("story")

#registerUser("p", "p")
#addToStory("story", "yaymebetter!!!!", 1323234)
#print(verifyUser("p", "p"))
#print(findUser("p"))
#findStory("story")
#print(getID_fromUser('p'))

#======================== SAVE CHANGES =========================
#db.commit() #save changes
#db.close()  #close database
