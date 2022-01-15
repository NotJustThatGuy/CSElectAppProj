import mysql.connector

class Database:
    def __init__(self, dbUsername, dbPassword, dbHostname, dbDatabase):
        self.dbUsername = dbUsername
        self.dbPassword = dbPassword
        self.dbHostname = dbHostname
        self.dbDatabase = dbDatabase
        self.dbConn = self.load()
        self.dbCursor = self.dbConn.cursor()
        self.currentUser = ""

    def load(self):
        return mysql.connector.connect(
            host=self.dbHostname,
            user=self.dbUsername,
            password=self.dbPassword,
            database=self.dbDatabase,
            buffered=True
        )

    def open(self):
        self.dbConn = self.load()
        self.dbCursor = self.dbConn.cursor()

    def close(self):
        self.dbConn.close()

    def isUserPass(self, username, password):
        sql = "SELECT username, password from Users WHERE username = '{}'".format(username)
        self.dbCursor.execute(sql)
        dbResult = self.dbCursor.fetchone()
        if password == dbResult[1]:
            return True
        else:
            return False

    def createAcc(self, username, password):
        sql = "INSERT INTO Users (Username, Password) VALUES ('{}', '{}')".format(username, password)
        self.dbCursor.execute(sql)
        self.dbConn.commit()

    def isExisting(self, username):
        sql = "SELECT username from Users WHERE username = '{}'".format(username)
        self.dbCursor.execute(sql)
        dbResult = self.dbCursor.fetchone()
        if dbResult is None:
            return False
        else:
            return True

    def setStatus(self, status):
        sql = "UPDATE Users set Status = '{}' WHERE Username = '{}'".format(status, self.currentUser)
        self.dbCursor.execute(sql)
        self.dbConn.commit()

