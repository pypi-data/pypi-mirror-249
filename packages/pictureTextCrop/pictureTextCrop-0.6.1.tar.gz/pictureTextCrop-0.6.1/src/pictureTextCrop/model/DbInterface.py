#   Project:        PictureTextCrop
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           model.DbInterface.py
#   Language:       Python 3.6+
#   Copyright:      Copyright 2022 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#
import hashlib
from os.path import isdir
from pickle import loads as convertFromBinary
from pickle import dumps as convertToBytes
from sqlite3 import connect, Binary
from collections import OrderedDict

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMessageBox

from model.Configuration import AppConfig
from model.Installation import TEXT_EXTRACTION_DB_FILE, INSTALLATION_FOLDER
from model.Jobs import Job

MODULE_NAME    = "Database Interface"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONSOLE_LOGGING = True


class AppDatabase:

    DB_FILE   = None

    @staticmethod
    def initializeDatabase(dbFileFolder: str=None):
        if dbFileFolder is not None:
            if not isinstance(dbFileFolder, str) or not isdir(dbFileFolder):
                return
        if dbFileFolder is not None:
            AppDatabase.DB_FILE = dbFileFolder + '/' + TEXT_EXTRACTION_DB_FILE
        else:
            AppDatabase.DB_FILE = TEXT_EXTRACTION_DB_FILE
        pictureTextDB = connect(AppDatabase.DB_FILE)

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "BatchMaster" (
                            "rowId"	INTEGER NOT NULL UNIQUE,
                            "TimeStamp"	TEXT NOT NULL,
                            "FolderPath"	TEXT NOT NULL,
                            "FileName"	TEXT NOT NULL,
                            "Text"	TEXT NOT NULL,
                            "Info"	BLOB NOT NULL,
                            "Exif"	BLOB NOT NULL,
                            "MIME_info"	BLOB,
                            PRIMARY KEY("rowId" AUTOINCREMENT))""")
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "CropLog" (
                            "rowId"	INTEGER NOT NULL UNIQUE,
                            "timeStamp"	TEXT NOT NULL,
                            "filePath"	TEXT NOT NULL,
                            "coordinates"	BLOB NOT NULL,
                            "text"	TEXT NOT NULL,
                            PRIMARY KEY("rowId" AUTOINCREMENT))""")
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "Configuration" (
                            "timeStamp"	TEXT NOT NULL UNIQUE,
                            "info"	BLOB NOT NULL UNIQUE,
                            PRIMARY KEY("timeStamp"))""")
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "Users" (
                            "UserName"	TEXT NOT NULL UNIQUE,
                            "info"	BLOB NOT NULL UNIQUE,
                            PRIMARY KEY("userName"))""")
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "Tasks" (
                                "TaskName"	TEXT NOT NULL UNIQUE,
                                "FileSet"	BLOB NOT NULL,
                                "TimeDefined"	TEXT NOT NULL,
                                "TimeAssigned"	TEXT,
                                "AssignedUser"	BLOB,
                                "TimeStarted"	TEXT,
                                "TimeCompleted"	INTEGER,
                                PRIMARY KEY("TaskName"))""")
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "DB_Mappings" (
                                "rowID"	INTEGER NOT NULL UNIQUE,
                                "TaskName"	TEXT NOT NULL,
                                "FieldName"	INTEGER NOT NULL,
                                PRIMARY KEY("rowID" AUTOINCREMENT))""")
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "TaskLog" (
                                "UserName"	TEXT NOT NULL,
                                "TaskName"	TEXT NOT NULL,
                                "FilePath"	TEXT NOT NULL,
                                "FieldName"	TEXT NOT NULL,
                                "Text"	TEXT NOT NULL,
                                "info"	BLOB,
                                PRIMARY KEY("UserName","TaskName"))""")
        pictureTextDB.commit()

        #   Write initial configuration to the Configuration table with timeStamp="CURRENT"
        info = convertToBytes(AppConfig.getCurrent())
        pictureTextDB.execute("""INSERT OR IGNORE INTO Configuration (timeStamp, info) values(?, ?)""",
                                    ("CURRENT", Binary(info)))
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "Jobs" (
                                    "JobName"	TEXT NOT NULL UNIQUE,
                                    "FileSequence"	BLOB NOT NULL,
                                    "Config"	BLOB NOT NULL,
                                    "Attributes"	BLOB,
                                    PRIMARY KEY("JobName"))""")
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "JobHistory" (
                                    "rowId"	INTEGER NOT NULL UNIQUE,
                                    "JobName"	TEXT NOT NULL,
                                    "Action"	TEXT NOT NULL,
                                    "TimeStamp"	TEXT NOT NULL,
                                    "Info"	BLOB,
                                    FOREIGN KEY("JobName") REFERENCES "Jobs"("JobName"),
                                    PRIMARY KEY("rowId" AUTOINCREMENT))""")
        pictureTextDB.commit()

        pictureTextDB.execute("""CREATE TABLE IF NOT EXISTS "JobRunLog" (
                                    "rowId"	INTEGER NOT NULL UNIQUE,
                                    "JobName"	TEXT NOT NULL,
                                    "TimeStamp"	TEXT NOT NULL,
                                    "Errors"	BLOB,
                                    "Info"	BLOB,
                                    PRIMARY KEY("rowId" AUTOINCREMENT))""")
        pictureTextDB.commit()

        pictureTextDB.close()

        AppDatabase.initTestUserSet()

    @staticmethod
    def initTestUserSet():
        """CREATE TABLE IF NOT EXISTS "Users" (
            "UserName"	TEXT NOT NULL UNIQUE,
            "info"	BLOB NOT NULL UNIQUE,
            PRIMARY KEY("userName"))"""
        pictureTextDB = connect(AppDatabase.DB_FILE)

        digest = hashlib.sha256(convertToBytes('1')).hexdigest()
        pictureTextDB.execute("""INSERT OR IGNORE INTO Users (UserName, info) VALUES (?, ?)""",
                              ("UserOne", Binary(convertToBytes({'userName': digest}))))
        digest = hashlib.sha256(convertToBytes('2')).hexdigest()
        pictureTextDB.execute("""INSERT OR IGNORE INTO Users (UserName, info) VALUES (?, ?)""",
                              ("UserTwo", Binary(convertToBytes({'userName': digest}))))
        digest = hashlib.sha256(convertToBytes('3')).hexdigest()
        pictureTextDB.execute("""INSERT OR IGNORE INTO Users (UserName, info) VALUES (?, ?)""",
                              ("UserThree", Binary(convertToBytes({'userName': digest}))))
        digest = hashlib.sha256(convertToBytes('4')).hexdigest()
        pictureTextDB.execute("""INSERT OR IGNORE INTO Users (UserName, info) VALUES (?, ?)""",
                              ("UserFour", Binary(convertToBytes({'userName': digest}))))
        digest = hashlib.sha256(convertToBytes('5')).hexdigest()
        pictureTextDB.execute("""INSERT OR IGNORE INTO Users (UserName, info) VALUES (?, ?)""",
                              ("UserFive", Binary(convertToBytes({'userName': digest}))))
        pictureTextDB.commit()
        pictureTextDB.close()

    @staticmethod
    def loadUsers():
        pictureTextDB = connect(AppDatabase.DB_FILE)
        userRecords     = pictureTextDB.execute("""SELECT * FROM USERS""").fetchall()
        userMap = OrderedDict()
        for user in userRecords:
            userMap[user[0]] = convertFromBinary(user[1])
        pictureTextDB.close()
        return userMap

    @staticmethod
    def loadConfig():
        pictureTextDB = connect(AppDatabase.DB_FILE)
        configRecord = pictureTextDB.execute("""SELECT * FROM Configuration WHERE timeStamp="CURRENT" """).fetchone()
        pictureTextDB.close()
        configSettings = convertFromBinary(configRecord[1])
        AppConfig.setConfig(configSettings)
        return convertFromBinary(configRecord[1])

    @staticmethod
    def updateConfig(config: dict):
        pictureTextDB = connect(AppDatabase.DB_FILE)
        pictureTextDB.execute("""UPDATE Configuration SET info=? WHERE timeStamp = ?""",
                              (Binary(convertToBytes(config)), "CURRENT"))
        pictureTextDB.commit()
        pictureTextDB.close()

    @staticmethod
    def saveJobDefinition(job: Job):
        #   Only overwrite existing record with same job name after warning user and getting permission
        pictureTextDB = connect(AppDatabase.DB_FILE)
        jobName = job.getIdentifier()
        matchingRecords = pictureTextDB.execute("""SELECT * FROM Jobs WHERE JobName="{jobName}" """.
                                                format(jobName=jobName)).fetchall()
        proceed = None
        if len(matchingRecords) > 0:
            messageDialog = QMessageBox(text="A Job record with the same name exists in the database:\n\t" +
                                             job.getIdentifier() + "\n\n" 
                                            "Do you want to replace it?\n")
            messageDialog.setWindowTitle("Job Name Exists")
            messageDialog.setGeometry(QRect(450, 200, 500, 150))
            messageDialog.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            response = messageDialog.exec()
            proceed = response == QMessageBox.Yes
        else:
            proceed = True
        if proceed:
            fileSequence = convertToBytes(job.getFileCollection())
            config = convertToBytes(job.getConfig())
            attributes = convertToBytes({})
            pictureTextDB.execute("""INSERT OR REPLACE INTO Jobs (JobName, FileSequence, Config, Attributes) 
                                    VALUES(?, ?, ?, ?)""",
                                  (job.getIdentifier(), Binary(fileSequence), Binary(config), Binary(attributes)))
            '''
            textExtractionDB.execute("""INSERT OR REPLACE INTO FileCache
                                        (filePath, timeStamp, text, metaData, mimeInfo) VALUES(?, ?, ?, ?, ?)""",
                                     (filePath, timeStamp, self.textViewer.getContent(),
                                      Binary(metaData), Binary(mimeInfo)))
            '''
            pictureTextDB.commit()
            messageDialog = QMessageBox(text="Job saved to database:\t" + job.getIdentifier())
            messageDialog.setWindowTitle("Job Saved")
            messageDialog.setGeometry(QRect(450, 200, 500, 150))
            messageDialog.setStandardButtons(QMessageBox.Ok)
            messageDialog.exec()

        pictureTextDB.close()

    @staticmethod
    def getJobTable():
        pictureTextDB = connect(AppDatabase.DB_FILE)
        matchingRecords = pictureTextDB.execute("""SELECT * FROM Jobs""").fetchall()
        jobMap = OrderedDict()
        for record in matchingRecords:
            jobMap[record[0]] = {
                'JobName': record[0],
                'FileSequence': convertFromBinary(record[1]),
                'Config': convertFromBinary(record[2]),
                'Attributes': convertFromBinary(record[3])
            }
        return jobMap


class ImageTextDB:

    @staticmethod
    def addRecords(records: list, dbFileFolder: str=None):
        if dbFileFolder is not None:
            if not isinstance(dbFileFolder, str) or not isdir(dbFileFolder):
                return
        if dbFileFolder is not None:
            AppDatabase.initializeDatabase(dbFileFolder)
            connection = connect(dbFileFolder + '/' + TEXT_EXTRACTION_DB_FILE)
        else:
            connection = connect(TEXT_EXTRACTION_DB_FILE)
        for record in records:
            connection.execute("""INSERT OR IGNORE INTO BatchMaster 
                                    (TimeStamp, FolderPath, FileName, Text, Info, Exif) 
                                    VALUES(?, ?, ?, ?, ?, ?)""",
                                    (record['TimeStamp'], record['FolderPath'], record['FileName'],
                                     record['Text'], Binary(record['Info']), Binary(record['Exif'])))
        connection.commit()
        connection.close()

    @staticmethod
    def appendCrop(timeStamp: str, filePath: str, coordinates: dict, text: str):
        if DEBUG:
            print("ImageTextDB.appendCrop:\t" + text)
        coordinates = convertToBytes(coordinates)
        connection = connect(TEXT_EXTRACTION_DB_FILE)
        connection.cursor().execute("""INSERT INTO CropLog (timeStamp, filePath, coordinates, text)
                                        values(?, ?, ?, ?)""",
                                    (timeStamp, filePath, Binary(coordinates), text))
        connection.commit()
        connection.close()

    @staticmethod
    def dumpContent():
        connection = connect(TEXT_EXTRACTION_DB_FILE)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM CropLog""")
        records = cursor.fetchall()
        for record in records:
            print('\n\ttimeStamp:\t' + record[0])
            print("\tfilePath:\t" + record[1])
            print("\tFileName:\t" + record[2])
            print("\tText:\t" + record[3].replace('\n', '\t\t'))
            print("\tInfo:\t" + str(convertFromBinary(record[4])))
            print("\tExif:\t" + str(convertFromBinary(record[5])))
        connection.close()


if __name__ == "__main__":
    print("Running:\t" + MODULE_NAME)

    AppDatabase.initializeDatabase(INSTALLATION_FOLDER)
    userMap = AppDatabase.loadUsers()
    for name, value in userMap.items():
        print("\t" + name + ":\t" + str(value))

