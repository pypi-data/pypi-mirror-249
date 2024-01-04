#   Project:        PictureTextCrop
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           service.Extraction.py
#   Date Started:   December 31, 2023
#                   Moved from view.Components.py
#   Language:       Python 3.6+
#   Copyright:      Copyright 2022, 2023 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#   Development:
#
from collections import OrderedDict
from datetime import datetime
from os import stat
from os.path import isdir
from pickle import dumps as convertToBytes

from PIL import Image
import pytesseract

from model.DbInterface import ImageTextDB
from model.Jobs import FileCollectionOrdered

MODULE_NAME     = "Text Extraction"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONSOLE_LOGGING = True


class Extractor:

    @staticmethod
    def batchProcessAll(imageFolder: str, pixMapImages: dict, dbFileFolder: str=None):
        if not isinstance(imageFolder, str) or not isdir(imageFolder):
            raise Exception("Extractor.batchProcessAll - Invalid imageFolder argument:  " + str(imageFolder))
        if not isinstance(pixMapImages, dict):
            raise Exception("Extractor.batchProcessAll - Invalid pixMapImages argument:  " + str(pixMapImages))
        if dbFileFolder is not None and (not isinstance(dbFileFolder, str) or not isdir(dbFileFolder)):
            raise Exception("Extractor.batchProcessAll - Invalid dbFileFolder argument:  " + str(dbFileFolder))
        if DEBUG:
            print("ImageManager.batchProcessAll")
        if DEBUG:
            ImageTextDB.dumpContent()

        records = []
        if CONSOLE_LOGGING:
            print("Count of files to process:\t" + str(len(pixMapImages)))
        fileCount = 0
        timeStart = datetime.now()
        for filePath in pixMapImages:
            fileCount += 1
            if CONSOLE_LOGGING:
                print("Getting text from:\t" + str(fileCount) + ':\t' + filePath)
            newRecord = Extractor.makeTextExtractionRecord(filePath)
            records.append(newRecord)
        timeEnd = datetime.now()
        elapsedTime = timeEnd - timeStart
        ImageTextDB.addRecords(records, dbFileFolder)
        if CONSOLE_LOGGING:
            print("Batch text extraction done in :\t" + str(elapsedTime))

    @staticmethod
    def batchProcessJob(flatFileSequence: tuple, consoleOutputConfig: dict):
        if not isinstance(flatFileSequence, FileCollectionOrdered):
            raise Exception("Extractor.batchProcessJob - Invalid flatFileSequence argument:  " + str(flatFileSequence))
        if not isinstance(consoleOutputConfig, dict):
            raise Exception("Extractor.batchProcessJob - Invalid consoleOutputConfig argument:  " + str(consoleOutputConfig))

        records = []
        fileCount = 0
        textSizeMap = OrderedDict()
        timeStart = datetime.now()
        for filePath in flatFileSequence.getFileSequence():
            fileCount += 1
            if 'filePath' in consoleOutputConfig and consoleOutputConfig['filePath']:
                print(str(fileCount) + ":\t" + filePath)
            timeStartFile = datetime.now()
            if 'times' in consoleOutputConfig and consoleOutputConfig['times']:
                print("\tExtraction started:\t" + timeStartFile.ctime())
            newRecord = Extractor.makeTextExtractionRecord(filePath)
            timeEndFile     = datetime.now()
            elapsedTimeFile = timeEndFile - timeStartFile
            if 'times' in consoleOutputConfig and consoleOutputConfig['times']:
                print("\tExtraction ended:\t" + timeEndFile.ctime())
                print("\tElapsed time:\t" + str(elapsedTimeFile))
            records.append(newRecord)
            if 'stats' in consoleOutputConfig and consoleOutputConfig['stats']:
                textSizeMap[filePath] = len(newRecord['Text'])
                print("\tText Byte Count:\t" + str(textSizeMap[filePath]))
            if 'textExtracted' in consoleOutputConfig and consoleOutputConfig['textExtracted']:
                print("\tText Extracted:\n" + newRecord['Text'])
        timeEnd = datetime.now()
        elapsedTime = timeEnd - timeStart
        if 'times' in consoleOutputConfig and consoleOutputConfig['times']:
            print("\nExtraction Job ended:\t" + timeEnd.ctime())
            print("Job elapsed time:\t" + str(elapsedTime))

        ImageTextDB.addRecords(records)

    @staticmethod
    def makeTextExtractionRecord(filePath: str):
        pathParts = filePath.split('/')
        imageFolder = '/'.join(pathParts[:len(pathParts)-1])
        newRecord = {}
        newRecord['TimeStamp'] = datetime.now()
        newRecord['FolderPath'] = imageFolder
        newRecord['FileName'] = filePath
        (mode, inode, dev, nlink, uid, gid, size, atime, mtime, ctime) = stat(filePath)
        newRecord['Info'] = convertToBytes({
            'mode': mode, 'inode': inode, 'dev': dev,
            'nlink': nlink, 'uid': uid, 'gid': gid,
            'size': size,
            'atime': datetime.fromtimestamp(atime).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'mtime': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'ctime': datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S.%f')
        })
        newRecord['Text'] = pytesseract.image_to_string(Image.open(filePath))
        #   exif = PhotoFolder.getExif(filePath)
        #   newRecord['Exif'] = convertToBytes(exif)
        newRecord['Exif'] = convertToBytes({})
        return newRecord
