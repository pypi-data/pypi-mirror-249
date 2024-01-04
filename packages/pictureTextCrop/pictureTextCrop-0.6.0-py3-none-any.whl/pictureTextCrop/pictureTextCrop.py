#   Project:        PictureTextCrop
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           pictureTextCrop.py
#   Language:       Python 3.6+
#   Copyright:      Copyright 2022, 2023 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#   Development:
#
from collections import OrderedDict
from os import environ
from os.path import isdir
from sys import argv

from PyQt5.QtCore import QCoreApplication, Qt, QRect
from PyQt5.QtWidgets import QApplication

from model.Configuration import AppConfig, ScanType
from model.DbInterface import AppDatabase
from view.Components import ImageManager, FileDialog, Scan, Extractor

PROGRAM_NAME    = "PictureTextCrop"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONSOLE_LOGGING = False


class PictureTextCrop:

    def __init__(self):
        self.folderSelectionDialog  = None
        self.imageManager = None
        self.currentImageFolder  = environ['HOME']
        self.app = None

    def launchApplication(self, config: dict=None):
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("PictureTextCrop constructor - Invalid config argument:  " + str(config))
            self.config = config
        else:
            self.config = {}
        AppConfig.setConfig(self.config)

        self.app = QApplication(argv)
        compatibility = 'QImageReader'

        if DEBUG:
            print("Starting PictureTextCrop.py to process images compatible with:\t" + compatibility)

        #   To make the tool load only files in the folder you select without traversing all folders under it,
        #   set AppConfig._folderScanType to ScanType.LIST rather than ScanType.WALK.
        #   ScanType.WALK will cause the folder scan to include all subfolders recursively.

        self.currentImageFolder = AppConfig._defaultImageFolder
        self.folderSelectedOnStart = False
        if self.config['openWithFolderSelection']:
            config = {'selectable': True,
                      'title': "Select Folder to Scan for Image Files",
                      'foldersOnly': True,
                      'showCurrentPath': True,
                      'selectionMode': 'extended'}
            self.folderSelectionDialog = FileDialog(identifier='folderSelectionDialog',
                                                    initialFolder=self.currentImageFolder, config=config,
                                                    listener=self._messageReceiver, parent=None)
            self.folderSelectionDialog.setGeometry(QRect(300, 200, 550, 450))
            self.folderSelectionDialog.exec()

        self.imageManager = ImageManager(config={'imageFileFolder': self.currentImageFolder,
                                                    'scanType': self.config['folderScanType'],
                                                    'extSet': compatibility,
                                                    'folderSelectedOnStart': self.folderSelectedOnStart},
                                         displayDimensions = {'width': self.app.primaryScreen().size().width(),
                                                              'height': self.app.primaryScreen().size().height()},
                                         listener=self._messageReceiver)
        self.imageManager.setGeometry(QRect(100, 50, 1200, 500))
        self.imageManager.setWindowTitle(PROGRAM_NAME)
        self.imageManager.show()
        self.app.exec()

    def _messageReceiver(self, message):
        if DEBUG:
            print("FileDialog.messageReceiver:\t" + str(message))
        if not isinstance(message, dict):
            return
        if 'source' in message:
            #   {'source': 'FileViewFrame.closeFrame'}
            if message['source'] == 'FileViewFrame.closeFrame':
                self.folderSelectionDialog.close()
                self.folderSelectionDialog = None
            #   {'source': 'FileViewFrame.setSelection', 'selected': self.currentSelections}
            elif message['source'] == 'FileViewFrame.setSelection':
                if 'identifier' in message and message['identifier'] == 'folderSelectionDialog':
                    if 'selected' in message and isinstance(message['selected'], tuple) and isdir(message['selected'][0]):
                        self.currentImageFolder     = message['selected'][0]
                        self.folderSelectedOnStart = True
                        self.folderSelectionDialog.close()
                        self.folderSelectionDialog = None
            #   {'source': 'ImageManager.toolBarAction', 'actionId': actionId}
            elif message['source'] == 'ImageManager.toolBarAction':
                if 'actionId' in message and isinstance(message['actionId'], str):
                    if message['actionId'] == 'Exit':
                        self.app.exit(0)

    def batchExtract(self, folderPath: str, scanType: str='walk', dbFileFolder: str=None,
                     mimeTypes: tuple=None, fileExts: tuple=None):
        #   Use class Scan from model.Folder to list or walk the folderPath for image files
        #   Configuration should have option of using either file extension or the MIME type for
        #       identification of image files
        #   Possibly have option of selecting particular file extensions or MIME types to scan for.
        pixMapImages = OrderedDict()
        if scanType == 'walk':
            Scan.walkFolder(folderPath, pixMapImages)
        elif scanType == 'list':
            Scan.listFolder(folderPath, pixMapImages)
        Extractor.batchProcessAll(folderPath, pixMapImages, dbFileFolder)

    def sequenceExtract(self, folderPath, scanType: str='walk', regExpr: str=None, dbFIleFolder: str=None,
                        mimeTypes: tuple=None, fileExts: tuple=None):
        """
        This will load the files from the particular folder according to the scanType, filtered using optional
        mimeTypes or fileExts, then extract the text of each, and then search in the text using the specified
        regular expression.
        Enhancements in future versions will include fuzzy matching via tokenization, type derivation with range
        and set matching, e.g. dates and other numerical types, NLP phrase similarity matching,

        :param folderPath:
        :param scanType:
        :param regExpr:
        :param dbFIleFolder:
        :param mimeTypes:
        :param fileExts:
        :return:
        """
        pass


if __name__ == '__main__':
    AppDatabase.initializeDatabase()

    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

    PictureTextCrop().launchApplication(config=AppDatabase.loadConfig())

