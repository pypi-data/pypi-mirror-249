#   Project:        PictureTextCrop
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           model.Folders.py
#   Language:       Python 3.6+
#   Copyright:      Copyright 2022, 2023 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#   Purpose:        File and folder operations.
#   Development:
#
from os import listdir, walk
from os.path import islink, isfile
from sys import stderr

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImageReader, QPixmap
from PyQt5.QtWidgets import QMessageBox

from model.Installation import IMAGE_PIXMAP_EXTS
#   Switching to QT5_IMAGE_FORMATS
from model.Installation import QT5_IMAGE_FILE_EXTS


MODULE_NAME     = "Folders"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONSOLE_LOGGING = False


class Scan:

    @staticmethod
    def listFolder(imageFolder: str, pixMapImages: dict):
        fileList = listdir(imageFolder)
        fileCount = 0
        for fileName in fileList:
            nameParts = fileName.split('.')
            if nameParts[-1].lower() in IMAGE_PIXMAP_EXTS:
                #   self.loadImage(self.imageFolder + '/' + fileName)
                pixMapImages[imageFolder + '/' + fileName] = None
                fileCount += 1
        return fileCount

    @staticmethod
    def walkFolder(imageFolder: str, pixMapImages: dict):
        fileCount = 0
        for dirName, subdirList, fileList in walk(imageFolder):
            if islink(dirName):
                continue
            for fileName in fileList:
                filePath = dirName + '/' + fileName
                if islink(filePath):
                    continue
                if not isfile(filePath):
                    continue
                nameParts = fileName.split('.')
                #   if nameParts[-1].lower() in IMAGE_PIXMAP_EXTS:      2023-12-23
                if nameParts[-1].lower() in QT5_IMAGE_FILE_EXTS:
                    #   self.loadImage(dirName + '/' + fileName)
                    pixMapImages[filePath] = None
                    fileCount += 1
        return fileCount

    @staticmethod
    def readImage(filePath: str):
        imageRef = None
        exception = None
        try:
            imageReader = QImageReader(filePath)
            imageReader.setAutoDetectImageFormat(True)
            imageRef = imageReader.read()

        #   These do not appear to be happening at least with a text file as a test:
        except QImageReader.FileNotFoundError:
            exception = "FileNotFoundError"
        except QImageReader.DeviceError:
            exception = "DeviceError"
        except QImageReader.UnsupportedFormatError:
            exception = "UnsupportedFormatError"
        except QImageReader.InvalidDataError:
            exception = "InvalidDataError"
        except QImageReader.UnknownError:
            exception = "UnknownError"

        if exception:
            messageDialog = QMessageBox(text="Exception on attempt to load file:\n\t" + filePath)
            messageDialog.setWindowTitle(exception)
            messageDialog.setGeometry(QRect(450, 200, 500, 150))
            messageDialog.setStandardButtons(QMessageBox.Ok)
            messageDialog.exec()


        if DEBUG:
            print("Type of image object returned by read():\t" + str(type(imageRef)))
        #   pixImage = imageRef.toPixelFormat(QImage)

        return QPixmap(imageRef)


