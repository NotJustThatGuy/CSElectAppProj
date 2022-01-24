import mysql.connector
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


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
        if dbResult is None:
            return False
        else:
            return check_encrypted(password, dbResult[1])

    def createAcc(self, username, password):
        hashPassword = encrypt(password)
        sql = "INSERT INTO Users (Username, Password) VALUES ('{}', '{}')".format(username, hashPassword)
        self.dbCursor.execute(sql)
        self.dbConn.commit()
        sql = "INSERT INTO UserInfo VALUES ('{}', '{}', '{}', '{}', '{}')".format(username, "Undefined", "Undefined", "Undefined", "Undefined")
        self.dbCursor.execute(sql)
        self.dbConn.commit()

    def getUserInfo(self, username=None):
        if username is None:
            username = self.currentUser
        sql = "SELECT * from UserInfo WHERE username = '{}'".format(username)
        self.dbCursor.execute(sql)
        dbResult = self.dbCursor.fetchone()
        return dbResult

    def setUserInfo(self, fname, mname, lname, bio):
        sql = "UPDATE UserInfo set FName = '{}', MName = '{}', LName = '{}', Bio = '{}' WHERE Username = '{}'".format(fname, mname, lname, bio,
                                                                                                                      self.currentUser)
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

    def getUsersBasic(self):
        sql = "SELECT Users.username as Username, UserInfo.fname as FName, UserInfo.mname as MName, UserInfo.lname as LName FROM `Users` " \
              "INNER JOIN UserInfo ON Users.Username = UserInfo.Username WHERE Users.Username != '{}'".format(self.currentUser)
        self.dbCursor.execute(sql)
        dbResult = self.dbCursor.fetchall()
        return dbResult


def encrypt(text):
    return pwd_context.hash(text)


def check_encrypted(text, hashed):
    return pwd_context.verify(text, hashed)
