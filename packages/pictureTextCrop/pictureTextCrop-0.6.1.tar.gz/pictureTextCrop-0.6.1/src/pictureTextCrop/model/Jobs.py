#   Project:        PictureTextCrop
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           model.Jobs.py
#   Date Started:   December 28, 2023
#   Language:       Python 3.6+
#   Copyright:      Copyright 2022, 2023 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#   Purpose:        Text extraction and cropping job definitions.
#   Development:
#       2023-12-29 (Goals):
#           Job Definition Dialog:
#               Text Line:  User's name for Job
#               Enum:       Job type, enumerated by the user, just a label for now
#               List:       Enhanced selection list with ordered list of file and folder paths, wide and scrollable
#                               since these can be long.
#               Buttons:
#                   For Whole List:     Add File, Add Folder, (TOP)
#                   For Selected:       Delete, Move Up, Move Down, (RIGHT)
#                   Sorting?
#               Popup Menu:
#                   View (file or folder contents tree),
#                   View Meta Data including mime type,
#                   Folder Stats,
#                   ...
#               File Navigator Dialog needs enhanced selection mode, i.e. any combination of files and folders
#                   in the current folder tree view.
#
from collections import OrderedDict
from copy import deepcopy
from functools import partial
from os import environ
from os.path import isfile, isdir
from sys import argv

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QMainWindow

from model.Configuration import ScanType

MODULE_NAME     = "Jobs"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONSOLE_LOGGING = False


class ImageFolder:

    def __init__(self, pathName: str, scanType: ScanType, fileSequence: tuple=None):
        if not isinstance(pathName, str) or not isdir(pathName):
            raise Exception("ImageFolder constructor - Invalid pathName argument:  " + str(pathName))
        if not isinstance(scanType, ScanType):
            raise Exception("ImageFolder constructor - Invalid scanType argument:  " + str(scanType))
        if fileSequence is None:
            self.fileSequence = ()
        else:
            if not isinstance(fileSequence, tuple):
                raise Exception("ImageFolder constructor - Invalid fileSequence argument:  " + str(fileSequence))
            self.fileSequence = fileSequence
        self.pathName = pathName
        self.scanType = scanType

    def getPathName(self):
        return self.pathName

    def getScanType(self):
        return self.scanType

    def getFileSequence(self):
        return self.fileSequence

    def setScanType(self, scanType: ScanType):
        if not isinstance(scanType, ScanType):
            return
        self.scanType = scanType

    def setFileSequence(self, fileSequence: tuple):
        if not isinstance(fileSequence, tuple):
            return
        self.fileSequence = fileSequence

    def addFileToSequence(self, filePath: str):
        if not isinstance(filePath, str) or not isfile(filePath):
            return
        fileSequence = list(self.fileSequence)
        fileSequence.append(filePath)
        self.fileSequence = tuple(fileSequence)

    def removeFileFromSequence(self, filePath, str):
        if not isinstance(filePath, str) or not isfile(filePath):
            return
        if not filePath in self.fileSequence:
            return False
        fileSequence = list(self.fileSequence)
        fileSequence.remove(filePath)
        self.fileSequence = tuple(fileSequence)
        return True


class FileCollectionOrdered:

    DEFAULT_ID  = 'FileSequence'

    def __init__(self, identifier: str=None, filePathMap: OrderedDict=None):
        if not isinstance(identifier, str):
            self.identifier = FileCollectionOrdered.DEFAULT_ID
        else:
            self.identifier = identifier
        if filePathMap is not None:
            if not isinstance(filePathMap, OrderedDict):
                raise Exception("FileCollectionOrdered constructor - Invalid filePathMap argument:  " + str(filePathMap))
            for pathName in filePathMap:
                if not isfile(pathName) and not isdir(pathName):
                    raise Exception("FileCollectionOrdered constructor - Invalid pathName in filePathMap argument:  " +
                                    str(pathName))
                if not isinstance(filePathMap[pathName], ImageFolder) and not isfile(filePathMap[pathName]):
                    raise Exception("FileCollectionOrdered constructor - Invalid value in filePathMap argument:  " +
                                    str(filePathMap[pathName]))
            self.filePathMap = deepcopy(filePathMap)
        else:
            self.filePathMap = OrderedDict()

    def getIdentifier(self):
        return self.identifier

    def getFilePathMap(self):
        return self.filePathMap

    def isPathMapped(self, pathName: str):
        return pathName in self.filePathMap

    def isFileListed(self, filePath: str):
        if filePath in self.filePathMap:
            return True
        for pathName in self.filePathMap:
            if isdir(pathName):
                #   is filePath in a folder / pathName's QImageReader() filtered list?
                if filePath in self.filePathMap[pathName].getFileCollection():
                    return True
        return False

    def getFolderContents(self, pathName: str):
        if pathName in self.filePathMap:
            if isinstance(self.filePathMap[pathName], ImageFolder):
                return self.filePathMap[pathName].getFileCollection()
        return None

    def getFileSequence(self):
        sequence = []
        for pathName in self.filePathMap:
            if isinstance(self.filePathMap[pathName], ImageFolder):
                #   for filePath in self.filePathMap[pathName].getFileCollection():
                for filePath in self.filePathMap[pathName].getFileSequence():
                    sequence.append(filePath)
            else:
                sequence.append(pathName)
        return tuple(sequence)

    def addFile(self, filePath: str):
        if isinstance(filePath, str) and isfile(filePath):
            self.filePathMap[filePath] = None
            return True
        return False

    def addFolder(self, folderPath: str, fileSequence: tuple, scanType: ScanType, force: bool=False):
        if not isinstance(folderPath, str) or not isdir(folderPath):
            raise Exception("FileCollectionOrdered.addFolder - Invalid folderPath argument:  " + str(folderPath))
        if not isinstance(fileSequence, tuple):
            raise Exception("FileCollectionOrdered.addFolder - Invalid fileSequence argument:  " + str(fileSequence))
        if not isinstance(scanType, ScanType):
            raise Exception("FileCollectionOrdered.addFolder - Invalid scanType argument:  " + str(scanType))
        if folderPath in self.filePathMap:
            if force:
                self.filePathMap[folderPath] = ImageFolder(folderPath, scanType, fileSequence)
        else:
            self.filePathMap[folderPath] = ImageFolder(folderPath, scanType, fileSequence)

    def removeFolder(self, folderPath: str):
        if isinstance(folderPath, str) and folderPath in self.filePathMap and \
                isinstance(self.filePathMap[folderPath], ImageFolder):
            imageFolder = self.filePathMap[folderPath]
            del self.filePathMap[folderPath]
            return imageFolder
        return None

    def removeFile(self, filePath: str):
        if isinstance(filePath, str) and filePath in self.filePathMap and \
                not isinstance(self.filePathMap[filePath], ImageFolder):
            del self.filePathMap[filePath]
            return True
        return False

    def getFileListingKeyPath(self, filePath: str):
        """
        Find and return a file's folder path if he file is anywhere in the map.
        Only returns first instance found.
        :param filePath: The full path of the file.
        :return: The folder path where the file was located.
        """
        pass

    def append(self, pathName: str, scanType: ScanType=None, fileSequence: tuple=None):
        if isinstance(pathName, str):
            if  isfile(pathName):
                self.filePathMap[pathName] = None
                return True
            elif isdir(pathName):
                if isinstance(fileSequence, tuple):
                    for filePath in fileSequence:
                        if not (isinstance(filePath, str) and isfile(filePath)):
                            return False
                    self.filePathMap[pathName] = ImageFolder(pathName, scanType, fileSequence)
                    return True
        return False

    def removePathName(self, pathName: str):
        if isinstance(pathName, str) and pathName in self.filePathMap:
            valueAtName = self.filePathMap[pathName]
            del self.filePathMap[pathName]
            return valueAtName
        return None

    def moveEntry(self, pathName: str, newLocation: int):
        if newLocation < len(self.filePathMap) and newLocation >= 0:
            index = list(self.filePathMap.keys())
            currentLoc = index.index(pathName)
            if newLocation != currentLoc:
                index.remove(pathName)
                index.insert(newLocation, pathName)
                newMap = OrderedDict()
                for pathName in index:
                    newMap[pathName] = self.filePathMap[pathName]
                self.filePathMap = newMap
                return True
        return False


    def clear(self):
        self.filePathMap = OrderedDict()

    def copy(self, identifier: str=None):
        return FileCollectionOrdered(identifier=identifier, filePathMap=self.filePathMap)


class Job:

    DEFAULT_CONFIG  = {}
    DEFAULT_ID  = ''

    def __init__(self, fileCollection: FileCollectionOrdered=None, identifier: str=None, config: dict=None):
        if fileCollection is None:
            self.fileCollection = FileCollectionOrdered()
        else:
            if not isinstance(fileCollection, FileCollectionOrdered):
                raise Exception("Job constructor - Invalid fileSequence argument:  " + str(fileCollection))
            self.fileCollection = fileCollection
        if identifier is None:
            self.identifier = Job.DEFAULT_ID
        elif isinstance(identifier, str):
            self.identifier = identifier
        else:
            raise Exception("Job constructor - Invalid identifier argument:  " + str(identifier))
        if config is None:
            self.config = Job.DEFAULT_CONFIG
        elif isinstance(config, dict):
            self.config = config
        else:
            raise Exception("Job constructor - Invalid config argument:  " + str(config))

    def getIdentifier(self):
        return self.identifier

    def setIdentifier(self, identifier: str):
        if not isinstance(identifier, str):
            return False
        self.identifier = identifier
        return True

    def getFileCollection(self):
        return self.fileCollection

    def getConfig(self):
        return self.config

    def getJobType(self):
        if 'jobType' in self.config:
            return self.config['jobType']

    def setJobType(self, jobType: str):
        if not isinstance(jobType, str):
            return False
        self.config['jobType'] = jobType
        return False


if __name__ == "__main__":
    print("Running:\t" + MODULE_NAME)
    app = QApplication(argv)

    testFileSequence = FileCollectionOrdered(identifier='testFileSequence',
                                             initialSequence=(environ['HOME'],
                                                     '/home/keithcollins/ACTIVITIES/Employment Search/Indeed/Resume/2023-12-28/George-Keith-Watson.pdf'))
    testJob = Job(testFileSequence, identifier='testJob')


    mainWindow = QMainWindow()
    mainWindow.setGeometry(QRect(200, 100, 700, 400))
    mainWindow.setWindowTitle(MODULE_NAME)
    mainWindow.show()
    app.exec()

