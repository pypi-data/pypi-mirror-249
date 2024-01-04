#   Project:        PictureTextCrop
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           view.Components.py
#   Date Started:   November 12, 2023
#   Language:       Python 3.6+
#   Copyright:      Copyright 2022 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#   Development:    Copied needed GUI components from VolumeIndexerQt project.
#       Future:
#           Files -> View Folder Text:
#               Extract the text of all files in a folder and view in a tabbed pane with search features.
#               This can be applied to any file sequence, in particular those designed by the user in the Jobs manager.
#           Files -> Export:
#               Export selected extraction results to a CSV or JSON format file.
#           Admin -> Users:
#               Set admin password on first access and require for user definitions and some otner confituration
#                   options.
#               Define users and user access privileges (views) and specify whether a password is required.
#                   User's will set password, if required, on their first access to their view of the application.
#


import hashlib
from collections import OrderedDict
from copy import deepcopy
from datetime import datetime
from enum import Enum
from functools import partial
from os import environ, listdir, walk, stat
from os.path import isdir, islink, isfile
from sys import argv
from pickle import dumps as convertToBytes
from math import floor

from PIL import Image
#   from PIL import ImageQt
#   Error:  Cannot mix incompatible Qt library (6.3.2) with this library (6.3.1)
import pytesseract

from PyQt5.QtCore import QRect, QEvent, Qt, QPoint, QItemSelection, QSize, QItemSelectionModel
from PyQt5.QtGui import QCloseEvent, QStandardItemModel, QStandardItem, QMouseEvent, QIcon, QPainter, QPen, QEnterEvent, \
    QContextMenuEvent, QPixmap, QImageReader, QResizeEvent
from PyQt5.QtWidgets import QErrorMessage, QApplication, QDialog, QGridLayout, QLabel, QPushButton, QMenu, QAction, \
    QTextEdit, QFrame, QHBoxLayout, QStatusBar, QMainWindow, QToolBar, QScrollArea, QListView, QMenuBar, QVBoxLayout, \
    QLineEdit, QWidget, QMessageBox, QTreeView, QAbstractItemView, QFileSystemModel, QTabWidget, QCheckBox

from model.DbInterface import ImageTextDB, AppDatabase
from model.Folders import Scan
from model.Installation import TOOLBAR_ICON_FOLDER, IMAGE_PIXMAP_EXTS, HELP_FOLDER_HORIZONTAL_ICON, HELP_FOLDER_ICON, \
    HELP_DOCS_FOLDER, HELP_ABOUT_FILE, HELP_QUICK_START_FILE, FILE_SYSTEM_TECH, QT5_IMAGE_FILE_EXTS, \
    HELP_FILES_MENU_FILE, HELP_RUN_MENU_FILE, HELP_VIEW_MENU_FILE, HELP_ADMIN_MENU_FILE, TEXT_EXTRACTION_DB_FILE

from model.Configuration import ScanType, AppConfig, TimeStampFormat, CropMode, RunMode
from model.Jobs import Job, FileCollectionOrdered
from service.Extraction import Extractor
from view.Help import HelpDialog
from view.QtAppComponents import AppButton, FieldLabel, KeyListView, EditorLine

MODULE_NAME     = "GUI Components"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONSOLE_LOGGING = True

"""
IMAGE_PIXMAP_EXTS = ('bmp', 'gif', 'jpeg', 'jpg', 'pbm', 'pgm', 'png', 'ppm', 'xbm', 'xpm')
PillowFileExtensions = ('ALL', 'apng', 'blp', 'blp1', 'blp2', 'bmp', 'dds', 'dib', 'dxt1', 'dxt3', 'dxt5', 'eps',
                        'gif', 'icns', 'ico', 'im', 'jfif', 'jpeg', 'jpg', 'msp', 'pbm', 'pcx', 'pgm', 'png',
                        'pnm', 'ppm', 'sgi', 'spi', 'tga', 'tiff', 'webp', 'xbm')
"""

class PageType(Enum):
    WEB_PAGE        = "Web Page"
    WEB_XML         = "Web XML Document"
    WEB_XML_GZ      = "Web XML Document - GZIP"
    WEB_MATHML      = "Web MathML Document"

    PYSIDE_LAYOUT   = "PySide Layout"
    PYSIDE_WIDGET   = "PySide Widget"
    PYSIDE_SVG      = "Scalable Vector Graphics"
    WEB_PDF         = "Web PDF Document"

    def __str__(self):
        return self.value


def showNotImplementedMessage(message: str, parent=None):
    messageDialog = QErrorMessage(parent=parent)
    messageDialog.setWindowTitle(" Not Implemented Yet ")
    messageDialog.setGeometry(QRect(250, 100, 400, 150))
    messageDialog.showMessage(message)


def showFoldersNotSelectedNotice(parent=None):
    messageDialog = QErrorMessage(parent=parent)
    messageDialog.setWindowTitle(" No Folders or Files Selected ")
    messageDialog.setGeometry(QRect(250, 100, 400, 150))
    messageDialog.showMessage("Please select one or more folders or files to include in the study.")


class TabbedView(QTabWidget):

    DEFAULT_ID      = 'TabbedView'
    DEFAULT_CONFIG  = {}

    def __init__(self, identifier: str=None, config: dict=None, listener=None, parent=None):
        if identifier is not None:
            if not isinstance(identifier, str):
                raise Exception("TabbedView constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        else:
            self.identifier = TabbedView.DEFAULT_ID
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("TabbedView constructor - Invalid config argument:  " + str(config))
            self.config = config
        else:
            self.config = TabbedView.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        super(TabbedView, self).__init__(parent)

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        pass

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pass


class GeneralConfigView(QFrame):

    DEFAULT_CONFIG  = {}

    def __init__(self, config: dict=None, listener=None, parent=None):
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("GeneralConfigView constructor - Invalid config argument:  " + str(config))
            self.config = config
        else:
            self.config = GeneralConfigView.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        super(GeneralConfigView, self).__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(3)
        self.setLayout(QVBoxLayout())

        self.currentConfig  = AppConfig.getCurrent()
        self.startingConfig = deepcopy(self.currentConfig)

        contentView = QFrame()
        contentView.setFrameStyle(QFrame.Panel | QFrame.Raised)
        contentView.setLineWidth(2)
        self.gridLayout = QGridLayout()
        contentView.setLayout(self.gridLayout)

        self.scroller = QScrollArea(parent=self)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)
        #   self.scroller.setLayout(QVBoxLayout())
        self.scroller.setWidget(contentView)
        self.layout().addWidget(self.scroller)

        self.checkBoxOpenWithFolderSelection    = QCheckBox("Open App With Folder Selection", parent=contentView)
        self.checkBoxOpenWithFolderSelection.setChecked(self.currentConfig['openWithFolderSelection'])
        self.checkBoxOpenWithFolderSelection.clicked.connect(partial(self.handleCheck, 'Open App With Folder Selection'))

        labelFolderScanType     = QLabel("Folder Scan Type:", parent=contentView)
        self.menuButtonFolderScanType    = QPushButton(str(self.currentConfig['folderScanType']), parent=contentView)
        self.menuButtonFolderScanType.setMaximumWidth(150)
        menuFolderScanType  = QMenu("Folder Scan Type", parent=self.menuButtonFolderScanType)
        self.menuButtonFolderScanType.setMenu(menuFolderScanType)
        menuFolderScanType.addAction(QAction(text='Walk', parent=menuFolderScanType,
                                             triggered=partial(self.setFolderScanType, ScanType.WALK)))
        menuFolderScanType.addAction(QAction(text='List', parent=menuFolderScanType,
                                             triggered=partial(self.setFolderScanType, ScanType.LIST)))

        #   _defaultImageFolder
        imageFolderFrame = QFrame(parent=contentView)
        imageFolderFrame.setLayout(QGridLayout())
        imageFolderFrame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        imageFolderFrame.setLineWidth(1)

        labelDefaultImageFolder     = QLabel("Default Image Folder", parent=imageFolderFrame)
        buttonDefaultImageFolder    = QPushButton('Select', parent=imageFolderFrame)
        buttonDefaultImageFolder.setMaximumWidth(100)
        buttonDefaultImageFolder.clicked.connect(partial(self.selectImageFolder,
                                                         self.currentConfig['defaultImageFolder'],
                                                         self.currentConfig['folderScanType']))
        self.textLineDefaultImageFolder  = QLineEdit(parent=imageFolderFrame)
        self.textLineDefaultImageFolder.setText(self.currentConfig['defaultImageFolder'])
        self.textLineDefaultImageFolder.setReadOnly(True)

        imageFolderFrame.layout().addWidget(labelDefaultImageFolder, 0, 0, 1, 1)
        imageFolderFrame.layout().addWidget(buttonDefaultImageFolder, 0, 1, 1, 1)
        imageFolderFrame.layout().addWidget(self.textLineDefaultImageFolder, 1, 0, 1, 2)

        """ Planned for a future release:

        labelTimeStampFormat = QLabel("Time Stamp Format")
        self.menuButtonTimeStampFormat   = QPushButton(str(self.currentConfig['timeStampFormat']), parent=contentView)
        menuTimeStampFormat     = QMenu("Time Stamp Format", parent=self.menuButtonTimeStampFormat)
        self.menuButtonTimeStampFormat.setMenu(menuTimeStampFormat)
        for element in TimeStampFormat:
            newAction = QAction(text=str(element), parent=menuTimeStampFormat,
                                                 triggered=partial(self.setTimeStampFormat, element))
            menuTimeStampFormat.addAction(newAction)
        """

        self.gridLayout.addWidget(self.checkBoxOpenWithFolderSelection, 0, 0, 1, 2)
        self.gridLayout.addWidget(labelFolderScanType, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.menuButtonFolderScanType, 1, 1, 1, 1)
        self.gridLayout.addWidget(imageFolderFrame, 2, 0, 2, 2)
        #   self.gridLayout.addWidget(labelTimeStampFormat, 4, 0, 1, 1)
        #   self.gridLayout.addWidget(self.menuButtonTimeStampFormat, 4, 1, 1, 1)

    def messageReceiver(self, message: dict):
        if not isinstance(message, dict):
            return
        if 'source' in message:

            #   {'source': 'FileViewFrame.setSelection', 'selected': self.currentSelections}
            if message['source'] == 'FileViewFrame.setSelection':
                if 'selected' in message and isinstance(message['selected'], tuple):
                    self.currentConfig['defaultImageFolder'] = message['selected'][0]
                    AppConfig.setDefaultImageFolder(self.currentConfig['defaultImageFolder'])
                    self.textLineDefaultImageFolder.setText(self.currentConfig['defaultImageFolder'])
                    self.imageFolderSelector.close()
                    self.imageFolderSelector = None

            #   {'source': "FolderViewTree.selectionChanged", "newSelections": tuple(self.selectedItems)}
            elif message['source'] == "FolderViewTree.selectionChanged":
                if 'newSelections' in message and isinstance(message['newSelections'], tuple):
                    pass

            #   {'source': "FileViewFrame.closeFrame"}
            elif message['source'] == "FileViewFrame.closeFrame":
                self.imageFolderSelector.close()
                self.imageFolderSelector = None

    def handleCheck(self, configId: str):
        if not isinstance(configId, str):
            return
        if configId == 'Open App With Folder Selection':
            AppConfig.setOpenWithFolderSelection(self.checkBoxOpenWithFolderSelection.isChecked())

    def setFolderScanType(self, scanType: ScanType):
        if not isinstance(scanType, ScanType):
            return
        self.currentConfig["folderScanType"] = scanType
        self.menuButtonFolderScanType.setText(str(scanType))
        AppConfig.setFolderScanType(scanType)

    def setTimeStampFormat(self, timeStampFormat: TimeStampFormat):
        if not isinstance(timeStampFormat, TimeStampFormat):
            return
        self.currentConfig["timeStampFormat"] = timeStampFormat
        self.menuButtonTimeStampFormat.setText(str(timeStampFormat))


    def selectImageFolder(self, initialFolder: str, scanType: ScanType):
        if initialFolder is not None and (not isinstance(initialFolder, str) or not isdir(initialFolder)):
            raise Exception("ImageManager.selectImageFolder - Invalid initialFolder argument:  " + str(initialFolder))
        if scanType is not None and not isinstance(scanType, ScanType):
            raise Exception("ImageManager.selectImageFolder - Invalid scanType argument:  " + str(scanType))

        config = {'selectable': True,
                  'title': "Select Default Folder to Scan for Image Files",
                  'foldersOnly': True,
                  'showCurrentPath': True,
                  'selectionMode': 'single'}
        self.imageFolderSelector = FileDialog(identifier='imageFolderSelector',
                                              initialFolder=initialFolder, config=config,
                                              listener=self.messageReceiver, parent=None)
        self.imageFolderSelector.setGeometry(QRect(300, 200, 550, 450))
        self.imageFolderSelector.exec()


    def getSettings(self):
        return {
            'openWithFolderSelection': self.checkBoxOpenWithFolderSelection.isChecked(),
            'folderScanType': ScanType.valueToConst(self.menuButtonFolderScanType.text()),
            'autoCacheTextExtraction': AppConfig._autoCacheTextExtraction,
            'autoIndexTextExtraction': AppConfig._autoIndexTextExtraction,
            'defaultImageFolder': self.textLineDefaultImageFolder.text(),
            'cropMode': AppConfig._cropMode,
            'timeStampFormat': TimeStampFormat.valueToConst(self.menuButtonTimeStampFormat.text())
        }

    def getStartingSettings(self):
        return self.startingConfig

    def setContent(self, config: dict):
        if not isinstance(config, dict):
            return
        if 'openWithFolderSelection' in config and isinstance(config['openWithFolderSelection'], bool):
            self.checkBoxOpenWithFolderSelection.setChecked(config['openWithFolderSelection'])
            self.currentConfig['openWithFolderSelection'] = config['openWithFolderSelection']
        if 'folderScanType' in config and isinstance(config['folderScanType'], ScanType):
            self.menuButtonFolderScanType.setText(str(config['folderScanType']))
        if 'autoCacheTextExtraction' in config and isinstance(config['autoCacheTextExtraction'], bool):
            pass
            self.currentConfig['autoCacheTextExtraction'] = config['autoCacheTextExtraction']
        if 'autoIndexTextExtraction' in config and isinstance(config['autoIndexTextExtraction'], bool):
            pass
            self.currentConfig['autoIndexTextExtraction'] = config['autoIndexTextExtraction']
        if 'defaultImageFolder' in config and isinstance(config['defaultImageFolder'], str):
            self.textLineDefaultImageFolder.setText(config['defaultImageFolder'])
            self.currentConfig['defaultImageFolder'] = config['defaultImageFolder']
        if 'cropMode' in config and isinstance(config['cropMode'], CropMode):
            pass
            self.currentConfig['cropMode'] = config['cropMode']
        if 'timeStampFormat' in config and isinstance(config['timeStampFormat'], TimeStampFormat):
            self.menuButtonTimeStampFormat.setText(str(config['timeStampFormat']))
            self.currentConfig['timeStampFormat'] = config['timeStampFormat']
        self.currentConfig = deepcopy(config)


class ConfigurationDialog(QDialog):

    DEFAULT_CONFIG  = {}

    def __init__(self, config: dict, listener=None, parent=None):
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("ConfigurationDialog constructor - Invalid config argument:  " + str(config))
            self.config = config
        else:
            self.config = ConfigurationDialog.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(ConfigurationDialog, self).__init__(parent)

        self.setLayout(QVBoxLayout())

        self.configPageNotebook = TabbedView(listener=self.messageReceiver, parent=self)
        self.pageFrames = OrderedDict()
        self.tabTitleToIndex = OrderedDict()
        self.tabIndexToTitle = OrderedDict()

        self.pageFrames["General"] = GeneralConfigView(config={}, listener=self.messageReceiver)
        tabId   = self.configPageNotebook.addTab(self.pageFrames["General"], "General")
        self.tabTitleToIndex["General"] = tabId
        self.tabIndexToTitle[tabId] = "General"

        self.pageFrames["Jobs"] = JobsConfigView(config={}, listener=self.messageReceiver)
        tabId   = self.configPageNotebook.addTab(self.pageFrames["Jobs"], "Jobs")
        self.tabTitleToIndex["Jobs"] = tabId
        self.tabIndexToTitle[tabId] = "Jobs"

        self.pageFrames["DB Mapping"] = DbMappingView(config={}, listener=self.messageReceiver)
        tabId   = self.configPageNotebook.addTab(self.pageFrames["DB Mapping"], "DB Mapping")
        self.tabTitleToIndex["DB Mapping"] = tabId
        self.tabIndexToTitle[tabId] = "DB Mapping"

        buttonBar = QFrame(parent=self)
        buttonBar.setFrameStyle(QFrame.Panel | QFrame.Raised)
        buttonBar.setLineWidth(2)
        buttonBar.setLayout(QHBoxLayout())

        """ Possibly needed in the future:
        
        buttonCommit    = QPushButton('Commit', parent=buttonBar)
        buttonCommit.setToolTip('Commit application configuration changes to the database')
        buttonCommit.setMaximumWidth(100)
        buttonCommit.clicked.connect(partial(self.handleButtonClick, 'Commit'))

        buttonReset     = QPushButton('Reset', parent=buttonBar)
        buttonReset.setToolTip('Reset the configuration to its state when this configuration dialog was started')
        buttonReset.setMaximumWidth(100)
        buttonReset.clicked.connect(partial(self.handleButtonClick, 'Reset'))

        buttonCancel    = QPushButton('Cancel', parent=buttonBar)
        buttonCancel.setToolTip('Cancel any changes committed, restoring starting configuration')
        buttonCancel.setMaximumWidth(100)
        buttonCancel.clicked.connect(partial(self.handleButtonClick, 'Cancel'))
        """

        buttonExit      = QPushButton('Exit', parent=buttonBar)
        buttonExit.setToolTip('Exit keeping any configuration changes committed')
        buttonExit.setMaximumWidth(100)
        buttonExit.clicked.connect(partial(self.handleButtonClick, 'Exit'))

        """ Possibly needed in the future:
        buttonBar.layout().addWidget(buttonCommit)
        buttonBar.layout().addWidget(buttonReset)
        buttonBar.layout().addWidget(buttonCancel)
        """
        buttonBar.layout().addWidget(buttonExit)

        self.layout().addWidget(self.configPageNotebook)
        self.layout().addWidget(buttonBar)

    def handleButtonClick(self, buttonId: str):
        if buttonId == 'Commit':
            #   Collect GUI component entries into current configuration.
            #   Save current configuration to AppConfig.
            #   Save current configuration to database.
            tabId = self.configPageNotebook.currentIndex()
            settings = self.pageFrames[self.tabIndexToTitle[tabId]].getSettings()
            AppConfig.setConfig(settings)
            AppDatabase.updateConfig(settings)
            pass
        elif buttonId == 'Reset':
            tabId = self.configPageNotebook.currentIndex()
            settings = self.pageFrames[self.tabIndexToTitle[tabId]].getStartingSettings()
            self.pageFrames[self.tabIndexToTitle[tabId]].setContent(settings)
            pass
        elif buttonId == 'Exit':
            if self.listener is not None:
                self.listener({'source': 'ConfigurationDialog.handleButtonClick', 'buttonId': buttonId})
        elif buttonId == 'Cancel':
            #   Commit could have already happened.
            #   Save starting configuration to AppConfig.
            #   Save starting configuration to database.
            tabId = self.configPageNotebook.currentIndex()
            settings = self.pageFrames[self.tabIndexToTitle[tabId]].getStartingSettings()
            AppConfig.setConfig(settings)
            AppDatabase.updateConfig(settings)
            if self.listener is not None:
                self.listener({'source': 'ConfigurationDialog.handleButtonClick', 'buttonId': buttonId})

    def messageReceiver(self, message: dict):
        if not isinstance(message, dict):
            return
        if 'source' in message:
            pass


class ConfigView(QFrame):

    DEFAULT_CONFIG  = {}

    def __init__(self, config: dict=None, listener=None, parent=None):
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("DbMappingConfigView constructor - Invalid config argument:  " + str(config))
            self.config = config
        else:
            self.config = ConfigView.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listner = None
        super(ConfigView, self).__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(3)
        self.setLayout(QVBoxLayout())

        self.contentView = QFrame()
        self.contentView.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.contentView.setLineWidth(2)
        self.gridLayout = QGridLayout()
        self.contentView.setLayout(self.gridLayout)

        self.scroller = QScrollArea(parent=self)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.contentView)
        self.layout().addWidget(self.scroller)

    def getSettings(self):
        return {}


class JobsConfigView(ConfigView):
    """
    Configuration fields in job definition process and in running defined jobs.
    """
    DEFAULT_ID      = 'JobsConfigView'

    def __init__(self, identifier: str=None, config: dict=None, listener=None, parent=None):
        if identifier is None:
            self.identifier = JobsConfigView.DEFAULT_ID
        else:
            if not isinstance(identifier, str):
                raise Exception("JobsConfigView constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        super(JobsConfigView, self).__init__(config=config, listener=listener, parent=parent)
        self.currentConfig = AppConfig.getCurrent()

        labelDefaultFolderScanMode  = QLabel('Default Folder Scan Mode:')
        labelDefaultFolderScanMode.setAlignment(Qt.AlignRight)

        self.menuButtonDefaultFolderScanMode = QPushButton('List')
        menuDefaultFolderScanMode = QMenu(parent=self.menuButtonDefaultFolderScanMode)
        self.menuButtonDefaultFolderScanMode.setMenu(menuDefaultFolderScanMode)
        self.actionSetScanModeList = QAction(text="List", triggered=partial(self.setScanMode, ScanType.LIST))
        menuDefaultFolderScanMode.addAction(self.actionSetScanModeList)
        self.actionSetScanModeWalk = QAction(text="Walk", triggered=partial(self.setScanMode, ScanType.WALK))
        menuDefaultFolderScanMode.addAction(self.actionSetScanModeWalk)

        if 'jobDefaultFolderScanMode' in self.currentConfig:
            if self.currentConfig['jobDefaultFolderScanMode'] == ScanType.WALK:
                self.menuButtonDefaultFolderScanMode.setText('Walk')
            elif self.currentConfig['jobDefaultFolderScanMode'] == ScanType.LIST:
                self.menuButtonDefaultFolderScanMode.setText('List')

        labelDefaultRunMode     = QLabel("Default Run Mode:")
        labelDefaultRunMode.setAlignment(Qt.AlignRight)

        self.menuButtonDefaultRunMode = QPushButton('Sequence')
        menuDefaultRunMode = QMenu(parent=self.menuButtonDefaultRunMode)
        self.menuButtonDefaultRunMode.setMenu(menuDefaultRunMode)
        self.actionSetRunModeSequence = QAction(text="Sequence", triggered=partial(self.setRunMode, RunMode.SEQUENCE))
        menuDefaultRunMode.addAction(self.actionSetRunModeSequence)
        self.actionSetRunModeBatch = QAction(text="Batch", triggered=partial(self.setRunMode, RunMode.BATCH))
        menuDefaultRunMode.addAction(self.actionSetRunModeBatch)

        if 'jobDefaultRunMode' in self.currentConfig:
            if self.currentConfig['jobDefaultRunMode'] == RunMode.SEQUENCE:
                self.menuButtonDefaultRunMode.setText('Sequence')
            elif self.currentConfig['jobDefaultRunMode'] == RunMode.BATCH:
                self.menuButtonDefaultRunMode.setText('Batch')

        self.gridLayout.addWidget(labelDefaultFolderScanMode, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.menuButtonDefaultFolderScanMode, 0, 1, 1, 1)
        self.gridLayout.addWidget(labelDefaultRunMode, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.menuButtonDefaultRunMode, 1, 1, 1, 1)

    def setScanMode(self, scanModeId: ScanType):
        if not isinstance(scanModeId, ScanType):
            return
        if scanModeId == ScanType.LIST:
            self.menuButtonDefaultFolderScanMode.setText('List')
        elif scanModeId == ScanType.WALK:
            self.menuButtonDefaultFolderScanMode.setText('Walk')
        AppConfig.setJobsDefaultFolderScanMode(scanModeId)

    def setRunMode(self, runModeId: RunMode):
        if not isinstance(runModeId, RunMode):
            return
        if runModeId == RunMode.SEQUENCE:
            self.menuButtonDefaultRunMode.setText('Sequence')
        elif runModeId == RunMode.BATCH:
            self.menuButtonDefaultRunMode.setText('Batch')
        AppConfig.setJobsDefaultRunMode(runModeId)


class DbMappingView(ConfigView):

    """
    Planning for future release:

    Default field mappings.
    Each mapping will have a name which the user will select for each sequential job they process.
    """
    DEFAULT_ID  = 'DbMappingView'

    def __init__(self, identifier: str=None, config: dict=None, listener=None, parent=None):
        if identifier is None:
            self.identifier = DbMappingView.DEFAULT_ID
        else:
            if not isinstance(identifier, str):
                raise Exception("DbMappingView constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        super(DbMappingView, self).__init__(config=config, listener=listener, parent=parent)

        textFutureReleasePlan   = "Planned for future release:\n\n" \
                                  "During text extraction, it is desirable to be able to extract any number\n" \
                                  "of slices of text and to be able to place them into particular named fields\n" \
                                  "in the database table that collects and stores the extracted text.\n\n" \
                                  "For instance, when working with screen-shots of emails, you might want separate\n " \
                                  "fields for the sender email address, the recipient email address, the subject,\n " \
                                  "etc.  This configuration feature will allow you to define such fields and they\n " \
                                  "will then be available in the text cropping dialog for use when a particular slice\n " \
                                  "of text is extracted." \

        labelFutureReleasePlan  = QLabel(textFutureReleasePlan)
        self.gridLayout.addWidget(labelFutureReleasePlan, 0, 0, 1, 1)


class UserConfigView(ConfigView):
    """
    Planned for future release:

    List of user names on the left with a vertical button bar on its right.
    Buttons:    Details, Add, Edit Delete
    The Details and Edit frames should occupy the entire frame so that developers can add their own details
        to the user's information and access privileges.
    """
    DEFAULT_ID  = 'UserConfigView'

    def __init__(self, identifier: str=None, config: dict=None, listener=None, parent=None):
        if identifier is None:
            self.identifier = DbMappingView.DEFAULT_ID
        else:
            if not isinstance(identifier, str):
                raise Exception("UserConfigView constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        super(UserConfigView, self).__init__(config=config, listener=listener, parent=parent)
        self.userMap = AppDatabase.loadUsers()


class SelectedTextDialog(QDialog):

    DEFAULT_ID  = 'SelectedTextDialog'
    DEFAULT_CONFIG  = {}
    DEFAULT_DESTINATIONS    = ('Default', 'Generic Table', 'Custom Table')
    DEFAULT_TITLE   = 'Selected Text'
    DEFAULT_GEOM    = QRect(600, 100, 300, 250)

    SET_SIZE    = None

    def __init__(self, identifier: str, text: str, config: dict, listener=None, parent=None):
        if identifier is not None:
            if not isinstance(identifier, str):
                raise Exception("")
            self.identifier = identifier
        else:
            self.identifier = SelectedTextDialog.DEFAULT_ID
        if text is None or not isinstance(text, str):
            raise Exception("")
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("")
            self.config = config
        else:
            self.config = SelectedTextDialog.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(SelectedTextDialog, self).__init__(parent)
        self.text = text

        if 'title' in self.config and isinstance(self.config['title'], str):
            self.setWindowTitle(self.config['title'])
        else:
            self.setWindowTitle(SelectedTextDialog.DEFAULT_TITLE)
        if 'geometry' in self.config and isinstance(self.config['geometry'], QRect):
            self.setGeometry(self.config['geometry'])
        else:
            self.setGeometry(SelectedTextDialog.DEFAULT_GEOM)
        if SelectedTextDialog.SET_SIZE is not None:
            self.resize(SelectedTextDialog.SET_SIZE)

        gridLayout = QGridLayout()
        self.setLayout(gridLayout)

        labelDestination    = QLabel('Save to')
        labelDestination.setMaximumWidth(100)


        if 'destinations' in self.config:
            self.destinationList = self.config['destinations']
        else:
            self.destinationList = SelectedTextDialog.DEFAULT_DESTINATIONS
        self.menuButtonDestination  = QPushButton(parent=self)
        if len(self.destinationList) > 0:
            self.menuButtonDestination.setText(self.destinationList[0])
        menuDestination = QMenu(parent=self.menuButtonDestination)
        self.destActionMap = OrderedDict()
        for destination in self.destinationList:
            self.destActionMap[destination] = QAction(destination)
            self.destActionMap[destination].triggered.connect(partial(self.storeToDestination, destination))
            self.destActionMap[destination].setStatusTip("")
            menuDestination.addAction(self.destActionMap[destination])
        self.menuButtonDestination.setMenu(menuDestination)

        textWindow = QTextEdit(parent=self)
        textWindow.setText(self.text)
        textWindow.setReadOnly(True)
        textWindow.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        textWindow.setLineWidth(2)

        buttonBar   = QFrame(parent=self)
        buttonBar.setLayout(QHBoxLayout())
        buttonBar.setFrameStyle(QFrame.Panel | QFrame.Raised)
        buttonBar.setLineWidth(2)

        buttonNext  = QPushButton(text='Next', parent=buttonBar)
        buttonNext.setMaximumWidth(100)
        buttonNext.setToolTip("Save and procede to next")
        buttonNext.clicked.connect(self.nextClicked)
        buttonBar.layout().addWidget(buttonNext)

        buttonCancel    = QPushButton(text='Cancel', parent=buttonBar)
        buttonCancel.setMaximumWidth(100)
        buttonCancel.setToolTip("Cancel save action and exit")
        buttonCancel.clicked.connect(self.cancelClicked)
        buttonBar.layout().addWidget(buttonCancel)

        gridLayout.addWidget(labelDestination, 0, 0, 1, 1)
        gridLayout.addWidget(self.menuButtonDestination, 0, 1, 1, 1)
        gridLayout.addWidget(textWindow, 1, 0, 3, 2)
        gridLayout.addWidget(buttonBar, 4, 0, 1, 2)

    def storeToDestination(self, destinationId: str):
        self.menuButtonDestination.setText(destinationId)

    def nextClicked(self):
        if self.listener is not None:
            self.listener({'source': 'SelectedTextDialog.nextClicked'})

    def cancelClicked(self):
        if self.listener is not None:
            self.listener({'source': 'SelectedTextDialog.cancelClicked'})

    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        if self.listener is not None:
            self.listener({'source': 'SelectedTextDialog.closeEvent'})

    def changeEvent(self, event: QEvent) -> None:
        #   If the window is resized by the user store the new size in the class for use on next showing.
        #   This may require an instance registry keyed on identifier if multiple extracted text windows are
        #       needed for different purposes.
        SelectedTextDialog.SET_SIZE = self.size()


#   Alternative:    class TextSelector(QMainWindow):
#       For toolbars, main menu and standard Window controls
class TextSelector(QDialog):

    DEFAULT_CONFIG  = {}

    def __init__(self, identifier, pixMapImage, imagePath,  config: dict=None, listener=None, parent=None):
        self.listener = None
        if not isinstance(identifier, str):
            raise Exception("TextSelector constructor - Invalid identifier argument:  " + str(identifier))
        if listener is not None and callable(listener):
            self.listener = listener
        if isinstance(config, dict):
            self.config = config
        else:
            self.config = TextSelector.DEFAULT_CONFIG
        super(TextSelector, self).__init__(parent)
        self.identifier = identifier
        self.setWindowTitle("Image Text Selector")

        self.pixMapImage = pixMapImage
        self.imageFilePath = imagePath

        self.scroller = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)

        pathParts = self.imageFilePath.split('/')
        self.imageFileName = pathParts[-1]
        self.setWindowTitle(self.imageFileName)
        self.label = PixMapLabel(self.pixMapImage, self.imageFilePath, listener=self.messageReceiver, parent=self)

        #   self.label.setPixmap(self.imageMap[self.imageFilePath])
        self.scroller.setWidget(self.label)

        #   self.setCentralWidget(self.scroller)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scroller)

        #   self.resize(pixmap.width(), pixmap.height())
        pixMapProps = self.label.getScaledPixMapProps()
        #   self.setGeometry(QRect(QPoint(200, 100), QPoint(200+pixMapProps['width'], 100+pixMapProps['height'])))
        if 'topLeft' in self.config:
            self.topLeft = self.config['topLeft']
        else:
            self.topLeft = QPoint(200, 100)
        if 'size' in self.config:
            self.size = self.config['size']
        else:
            self.size = (700, 500)
        self.setGeometry(QRect(self.topLeft, QPoint(self.topLeft.x() + self.size[0], self.topLeft.y() + self.size[1])))

    def getImageFileName(self):
        return self.imageFileName

    def messageReceiver(self, message: dict):
        if DEBUG:
            print("TextSelector.messageReceiver:\t" + str(message))
        if not isinstance(message, dict):
            return
        if 'source' in message:
            #    {'source': "PixMapLabel.mouseReleaseEvent", 'selectedText': text, 'filePath': filePath}
            if message['source'] == "PixMapLabel.mouseReleaseEvent":
                if self.listener is not None:
                    message['identifier'] = self.identifier
                    self.listener(message)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.listener is not None:
            self.listener({'source': "TextSelector.closeEvent", 'action': 'close requested', 'fileName': self.imageFilePath })


class PixMapLabel(QLabel):

    def __init__(self, pixMapImage, imageFilePath, listener=None, parent=None):
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(PixMapLabel, self).__init__(parent=parent)
        self.pixmap = pixMapImage
        self.imageFilePath = imageFilePath

        self.startPos = self.endPos = None
        self.pixMapProps = {
            'size':     self.pixmap.size(),
            'width':    self.pixmap.width(),
            'height':   self.pixmap.height(),
            'rect':     self.pixmap.rect(),
            'hasAlpha': self.pixmap.hasAlphaChannel(),
            'depth':    self.pixmap.depth(),
            'hash':     self.pixmap.cacheKey()
        }
        if DEBUG:
            print("pixMapProps:\t" + str(self.pixMapProps))

        #   Should have option to turn off scaling
        #   self.scaledPixmap = self.pixmap.scaledToWidth(500)
        self.scaledPixmap = self.pixmap

        self.scaledPixmapProps = {
            'size':     self.scaledPixmap.size(),
            'width':    self.scaledPixmap.width(),
            'height':   self.scaledPixmap.height(),
            'rect':     self.scaledPixmap.rect(),
            'hasAlpha': self.scaledPixmap.hasAlphaChannel(),
            'depth':    self.scaledPixmap.depth(),
            'hash':     self.scaledPixmap.cacheKey()
        }
        if DEBUG:
            print("scaledPixMapProps:\t" + str(self.scaledPixmapProps))
        self.startingDraw = False
        self.endingDraw = False
        self.painter = None
        self.setPixmap(self.scaledPixmap)

    def getPixMapProps(self):
        return self.pixMapProps

    def getScaledPixMapProps(self):
        return self.scaledPixmapProps

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.startPos is not None and self.endPos is not None:
            self.painter = QPainter(self)
            if self.startingDraw:
                #   self.painter.save()
                self.startingDraw = False
            pen = QPen(Qt.blue)
            pen.setWidth(5)
            self.painter.setPen(pen)

            #   painter.setFont(QFont("Arial", 30))
            #   painter.drawText(rect(), Qt.AlignCenter, "Qt")
            if self.endPos.x() > self.startPos.x():
                startX = self.startPos.x()
                endX = self.endPos.x()
            else:
                startX = self.endPos.x()
                endX = self.startPos.x()
            if self.endPos.y() > self.startPos.y():
                startY = self.startPos.y()
                endY = self.endPos.y()
            else:
                startY = self.endPos.y()
                endY = self.startPos.y()
            self.painter.drawRect(startX, startY, endX-startX, endY-startY)
            #   painter.restore()
            self.painter.end()
        elif self.endingDraw:
            self.endingDraw = False

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        pass

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if DEBUG:
            print("PixMapLabel.mouseMoveEvent:\t" + str(event.pos()))
        self.endPos = event.pos()
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if DEBUG:
            print("mousePressEvent")
            print("\tpos:\t" + str(event.pos()))
        self.startPos = event.pos()
        self.startingDraw = True

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.endPos is None or self.startPos is None:
            return
        if self.endPos.x() > self.startPos.x():
            startX = self.startPos.x()
            endX = self.endPos.x()
        else:
            startX = self.endPos.x()
            endX = self.startPos.x()
        if self.endPos.y() > self.startPos.y():
            startY = self.startPos.y()
            endY = self.endPos.y()
        else:
            startY = self.endPos.y()
            endY = self.startPos.y()
        clippedPixMap = self.scaledPixmap.copy(QRect(startX, startY, endX-startX, endY-startY))
        #   QPixmap().toImage()
        image   = clippedPixMap.toImage()
        #   This next line crashed the program when run inside PyCharm's debugger.
        PilImage = Image.fromqimage(image)
        #   PilImage.show(title="Cropped Image")
        text = pytesseract.image_to_string(PilImage)
        if CONSOLE_LOGGING:
            print("\nExtracted Text:\t" + text)

        #   Log to DB:
        timeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        filePath = self.imageFilePath
        coordinates = { "startX": startX,
                        "endX": endX,
                        'startY': startY,
                        'endY': endY,
                        'pixMapProps': self.pixMapProps,
                        'scaledPixmapProps': self.scaledPixmapProps }
        ImageTextDB.appendCrop(timeStamp, filePath, coordinates, text)
        self.startPos = None
        self.endPos = None
        self.endingDraw = True
        self.update()
        if self.listener is not None:
            self.listener({'source': "PixMapLabel.mouseReleaseEvent", 'selectedText': text, 'filePath': filePath})


#   Alternative:    class TextSelector(QMainWindow):
#   If tne menu bar, tool bars, or standard window controls are needed.
class TextSelector(QDialog):

    DEFAULT_CONFIG  = {}

    def __init__(self, identifier, pixMapImage, imagePath,  config: dict=None, listener=None, parent=None):
        self.listener = None
        if not isinstance(identifier, str):
            raise Exception("TextSelector constructor - Invalid identifier argument:  " + str(identifier))
        if listener is not None and callable(listener):
            self.listener = listener
        if isinstance(config, dict):
            self.config = config
        else:
            self.config = TextSelector.DEFAULT_CONFIG
        super(TextSelector, self).__init__(parent)
        self.identifier = identifier
        self.setWindowTitle("Image Text Selector")

        self.pixMapImage = pixMapImage
        self.imageFilePath = imagePath

        self.scroller = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroller.setWidgetResizable(True)

        pathParts = self.imageFilePath.split('/')
        self.imageFileName = pathParts[-1]
        self.setWindowTitle(self.imageFileName)
        self.label = PixMapLabel(self.pixMapImage, self.imageFilePath, listener=self.messageReceiver, parent=self)

        self.scroller.setWidget(self.label)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scroller)
        pixMapProps = self.label.getScaledPixMapProps()
        if 'topLeft' in self.config:
            self.topLeft = self.config['topLeft']
        else:
            self.topLeft = QPoint(200, 100)
        if 'size' in self.config:
            self.size = self.config['size']
        else:
            self.size = (700, 500)
        self.setGeometry(QRect(self.topLeft, QPoint(self.topLeft.x() + self.size[0], self.topLeft.y() + self.size[1])))

    def getImageFileName(self):
        return self.imageFileName

    def messageReceiver(self, message: dict):
        if DEBUG:
            print("TextSelector.messageReceiver:\t" + str(message))
        if not isinstance(message, dict):
            return
        if 'source' in message:
            #    {'source': "PixMapLabel.mouseReleaseEvent", 'selectedText': text, 'filePath': filePath}
            if message['source'] == "PixMapLabel.mouseReleaseEvent":
                if self.listener is not None:
                    message['identifier'] = self.identifier
                    self.listener(message)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.listener is not None:
            self.listener({'source': "TextSelector.closeEvent", 'action': 'close requested', 'fileName': self.imageFilePath })


class FileListView(QListView):
    """
    This needs to display a scaled image or thumbnail on the right when an image is made the current one.
    It should also have the option of displaying a thumbnail as an icon for each list item.
    """
    DEFAULT_ID = 'FileListView'

    def __init__(self, identifier: str=None, imageMap=None, config: dict=None, listener=None, parent=None):
        if identifier is None:
            self.identifier = FileListView.DEFAULT_ID
        else:
            if not isinstance(identifier, str):
                raise Exception("FileListView constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(FileListView, self).__init__(parent)
        self.imageMap = imageMap
        self.config = config
        self.currSelectionIdx = None
        self.selectionList = []

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(FileListView, self).mousePressEvent(event)
        if DEBUG:
            print("FileListView.mousePressEvent:\t" + str(event))
        #   Popup menu if right click
        selectionIdx = self.indexAt(event.pos())
        if selectionIdx is not None:
            selectedItem = self.model().item(selectionIdx.row(), selectionIdx.column())
            if selectedItem is not None:
                #   This is not valid until the GUI event loop finishes:
                #       checked  = selectedItem.checkState() == Qt.CheckState.Checked
                self.currSelectionIdx = selectionIdx
                self.currentImageFilePath = selectedItem.text()
                if self.listener is not None:
                    self.listener({'source': 'FileListView.mousePressEvent',
                                   'selectionText': self.currentImageFilePath})

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super(FileListView, self).mouseReleaseEvent(event)
        if DEBUG:
            print("FileListView.mouseReleaseEvent:\t" + str(event))
        #   Popup menu if right click

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super(FileListView, self).mouseDoubleClickEvent(event)
        if DEBUG:
            print("FileListView.mouseDoubleClickEvent:\t" + str(event))

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        super(FileListView, self).selectionChanged(selected, deselected)
        if self.listener is not None:
            if len(selected.indexes()) > 0:
                selection = self.model().itemData(selected.indexes()[0])[0]
                for item in selected.indexes():
                    self.selectionList.append(self.model().itemData(item)[0])
                for item in deselected.indexes():
                    self.selectionList.remove(self.model().itemData(item)[0])
            else:
                selection = None
            self.listener({'source': 'FileListView.selectionChanged', 'identifier': self.identifier,
                           'selection': selection, 'selectionList': tuple(self.selectionList)})



class FolderViewTree(QTreeView):

    DEFAULT_CONFIG  = {}

    class PopupItem(Enum):
        META    = ("Meta", "View the meta-data of the current selection", None)
        VIEW    = ("View", "View the content of the file", None)
        MOVE    = ("Move", "Move the file / folder to a different location", None)
        COPY    = ("Copy", "Copy the file / folder to a different location", None)

    def __init__(self, initialFolder: str=None,  config: dict=None, dispatcher=None, listener=None, parent=None):
        if not isinstance(initialFolder, str) or not isdir(initialFolder):
            raise Exception("FolderViewTree constructor - Invalid initialFolder argument:  " + str(initialFolder))
        if config is None:
            self.config = FolderViewTree.DEFAULT_CONFIG
        elif not isinstance(config, dict):
            raise Exception("FolderViewTree constructor - Invalid config argument:  " + str(config))
        else:
            self.config = config
        if dispatcher is not None and callable(dispatcher):
            self.dispatcher = dispatcher
        else:
            self.dispatcher = None
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(FolderViewTree, self).__init__(parent)
        self.directoryModel = QFileSystemModel()
        if initialFolder is not None:
            self.rootFolder = initialFolder
        else:
            self.rootFolder = environ['HOME']
        self.selectedItems     = []
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showPopupMenu)

        self.setSelectionMode(QTreeView.SingleSelection)
        if 'selectionMode' in self.config:
            if self.config['selectionMode'] == "extended":
                self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.popupMenu = QMenu(self)
        if 'popupMenu' in self.config:
            for item in self.config['popupMenu']:
                menuAction = self.popupMenu.addAction(item[0], item[2])
                menuAction.setStatusTip(item[1])
        else:
            for item in FolderViewTree.PopupItem:
                menuAction = self.popupMenu.addAction(item.value[0], partial(self.popupMenuAction, item) )
                menuAction.setStatusTip(item.value[1])

        self.directoryModel.setRootPath(self.rootFolder)

        self.setModel(self.directoryModel)
        self.setColumnWidth(0, 250)
        #   Size is not needed for folder selection, but could be computed if necessary
        self.setColumnHidden(1, True)
        #   self.setColumnHidden(3, True)

        self.setRootIndex(self.directoryModel.index(self.rootFolder))
        self.expand(self.rootIndex())
        self.setExpanded(self.rootIndex(), True)

        self.setToolTip("Double click to expand or collapse a folder.\nRight click a file for menu of options.")

        self.foldersVisited = []
        self.foldersVisited.append(self.rootFolder)
        self.folderVisitIdx = self.currentFolderIdx = 0

    def __setattr__(self, key, value):
        if key == 'listener':
            if 'listener' not in self.__dict__:
                self.__dict__[key] = value
            return
        if key == 'dispatcher':
            if 'dispatcher' not in self.__dict__:
                self.__dict__[key] = value
            return
        self.__dict__[key] = value

    def setFolder(self, folderPath):
        if isinstance(folderPath, str) and isdir(folderPath):
            self.rootFolder = folderPath
            self.directoryModel.setRootPath(self.rootFolder)
            self.setRootIndex(self.directoryModel.index(self.rootFolder))
            if folderPath not in self.foldersVisited:
                self.foldersVisited.append(folderPath)
                self.folderVisitIdx += 1
                self.currentFolderIdx = self.folderVisitIdx
            else:
                self.currentFolderIdx = self.foldersVisited.index(folderPath)
            self.setStatusTip(folderPath)

    def navigateTo(self, folderPath):
        if isinstance(folderPath, str) and isdir(folderPath):
            self.rootFolder = folderPath
            self.directoryModel.setRootPath(self.rootFolder)
            self.setRootIndex(self.directoryModel.index(self.rootFolder))
            self.currentFolderIdx = self.foldersVisited.index(self.rootFolder)
            self.setStatusTip(folderPath)

    def getFoldersVisited(self):
        return self.foldersVisited

    def handleNextRequest(self):
        if self.currentFolderIdx < len(self.foldersVisited) - 1:
            self.currentFolderIdx += 1
            self.rootFolder = self.foldersVisited[self.currentFolderIdx]
            self.directoryModel.setRootPath(self.rootFolder)
            self.setRootIndex(self.directoryModel.index(self.rootFolder))
            self.setStatusTip(self.rootFolder)
            return self.rootFolder
        return None

    def handlePrevRequest(self):
        if self.currentFolderIdx > 0:
            self.currentFolderIdx -= 1
            self.rootFolder = self.foldersVisited[self.currentFolderIdx]
            self.directoryModel.setRootPath(self.rootFolder)
            self.setRootIndex(self.directoryModel.index(self.rootFolder))
            self.setStatusTip(self.rootFolder)
            return self.rootFolder
        return None

    def getRootFolder(self):
        return self.rootFolder

    def handlePopupMenuAction(self, popupItem):
        if DEBUG:
            print("FolderViewTree.handlePopupMenuAction:\t" + str(popupItem))

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        super(FolderViewTree, self).selectionChanged(selected, deselected)
        if DEBUG:
            print("FolderViewTree.selectionChanged - selected:\t" + str(selected))
            print("\tselected.indexes():\t" + str(selected.indexes()))

        prevIndex = None
        for index in selected.indexes():
            if prevIndex is None or index.row() != prevIndex.row():
                selectionText = str(self.directoryModel.filePath(index))
                if selectionText not in self.selectedItems:
                    self.selectedItems.append(selectionText)
            prevIndex = index

        prevIndex = None
        for index in deselected.indexes():
            if prevIndex is None or index.row() != prevIndex.row():
                selectionText = str(self.directoryModel.filePath(index))
                if selectionText in self.selectedItems:
                    self.selectedItems.remove(selectionText)
            prevIndex = index

            #   if filePath not in self.foldersVisited:
            #       self.foldersVisited.append(self.rootFolder)
            #       self.folderVisitIdx = self.currentFolderIdx = 0

        if self.listener is not None:
            self.listener({'source': "FolderViewTree.selectionChanged", "newSelections": tuple(self.selectedItems)})


    def getSelectedItems(self):
        return tuple(self.selectedItems)

    def showPopupMenu(self, point):
        self.popupMenu.exec(self.mapToGlobal(point))

    def popupMenuAction(self, actionId: PopupItem):
        showNotImplementedMessage("Popup menu actions for this component are not implemented yet", self)


    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(FolderViewTree, self).mousePressEvent(event)
        if DEBUG:
            print("FolderViewTree.mousePressEvent")
            print("\trootDirectory:\t" + str(self.directoryModel.rootDirectory()))
            print("\trootPath:\t" + str(self.directoryModel.rootPath()))
            #   self.directoryModel.setRootPath()
            #   self.directoryModel.setNameFilters()
            #   QAbstractItemModel()
            print("\tself.pos():\t" + str(self.pos()))
            selectionIndex = self.indexAt(event.pos())
            selectedPath = self.directoryModel.filePath(selectionIndex)

            """
            print("\tfilePath:\t" + str(self.directoryModel.filePath(selectionIndex)))
            print("\tfileName:\t" + str(self.directoryModel.fileName(selectionIndex)))
            print("\tindex:\t" + str(self.directoryModel.index(selectedPath)))
            fileInfo = self.directoryModel.fileInfo(selectionIndex)
            metaData = fileInfo.stat()      #   Returns None for folder or file
            print("\tfileInfo:\t" + str(self.directoryModel.fileInfo(selectionIndex)))
            print("\tmetaData:\t" + str(metaData))

            print("\tflags.__dict__:\t" + str(self.directoryModel.flags(selectionIndex)))
            print("\titemData:\t" + str(self.directoryModel.itemData(selectionIndex)))
            """

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super(FolderViewTree, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super(FolderViewTree, self).mouseDoubleClickEvent(event)
        selectionIndex = self.indexAt(event.pos())
        selectedPath = self.directoryModel.filePath(selectionIndex)
        if DEBUG:
            print("FolderViewTree.mouseDoubleClickEvent on:\t" + selectedPath)
        self.setFolder(selectedPath)
        if self.listener is not None:
            self.listener({'source': 'FolderViewTree.mouseDoubleClickEvent', 'selectedPath': selectedPath})

    def enterEvent(self, event: QEnterEvent) -> None:
        super(FolderViewTree, self).enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        super(FolderViewTree, self).leaveEvent(event)


class FileViewFrame(QFrame):

    def __init__(self, initialPaths: tuple = None, config: dict = None, includeButtonBox=True,
                 doubleView: bool=False, dispatcher=None, listener=None, parent=None):
        if initialPaths is not None:
            if not isinstance(initialPaths, tuple):
                raise Exception("FileViewFrame constructor - Invalid initialPaths argument:  " + str(initialPaths))
            for folderPath in initialPaths:
                if not isdir(folderPath):
                    raise Exception("FileViewFrame constructor - Invalid folderPath in initialPaths argument:  "
                                     + str(folderPath))
            self.initialPaths = initialPaths
        else:
            self.initialPaths = (environ['HOME'], )
        if doubleView and len(self.initialPaths) != 2:
            raise Exception("FileViewFrame constructor - "
                            "Invalid length of initialPaths argument (should be 2 for doubleView):  "
                            + str(initialPaths))

        if isinstance(config, dict):
            self.config = config
        else:
            self.config = None
        if dispatcher is not None and callable(dispatcher):
            self.dispatcher = dispatcher
        else:
            self.dispatcher = None
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(FileViewFrame, self).__init__(parent)
        self.initializing = True
        self.currentSelections = None
        self.pageType = PageType.PYSIDE_LAYOUT
        #   self.setMinimumSize(500, 500)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.currentFolder = self.initialPaths[0]
        if 'showCurrentPath' in self.config and isinstance(self.config['showCurrentPath'], bool):
            self.showCurrentPath = self.config['showCurrentPath']
            self.lineCurrentPath = QLineEdit(self.currentFolder)
            self.lineCurrentPath.setReadOnly(True)
        else:
            self.showCurrentPath = False

        if 'foldersOnly' in self.config and isinstance(self.config['foldersOnly'], bool):
            self.foldersOnly = self.config['foldersOnly']
        else:
            self.foldersOnly = False

        self.toolBar = QFrame(parent=self)
        self.toolBar.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.toolBar.setLineWidth(2)
        self.toolBar.setLayout(QHBoxLayout())

        self.labelSpacer = QLabel("", parent=self.toolBar)
        self.labelSpacer.setMinimumWidth(100)

        self.buttonUp = QPushButton("Up", parent=self.toolBar)
        self.buttonUp.setToolTip("Go to next folder up in the folder tree")
        self.buttonUp.clicked.connect(self.moveUpOneLevel)
        self.buttonUp.setMaximumWidth(50)

        if self.config is not None and 'selectable' in self.config and self.config['selectable']:
            self.buttoncommit = QPushButton("Select", parent=self.toolBar)
            self.buttoncommit.clicked.connect(self.setSelection)
            self.buttoncommit.setToolTip("Select the currently highlighted folder or file")
            self.buttoncommit.setMaximumWidth(100)
        else:
            self.buttoncommit = QPushButton("Build Study", parent=self.toolBar)
            self.buttoncommit.clicked.connect(self.buildStudy)
            self.buttoncommit.setToolTip("Build a Study using this file source")
            self.buttoncommit.setMaximumWidth(100)

        self.buttonCancel = QPushButton("Cancel", parent=self.toolBar)
        self.buttonCancel.clicked.connect(self.closeFrame)
        self.buttonCancel.setToolTip("Close this dialog")
        self.buttonCancel.setMaximumWidth(100)

        self.toolBar.layout().addWidget(self.labelSpacer)
        self.toolBar.layout().addWidget(self.buttonUp)
        self.toolBar.layout().addWidget(self.buttoncommit)
        self.toolBar.layout().addWidget(self.buttonCancel)

        if doubleView:
            self.treeViews = (FolderViewTree(initialFolder=initialPaths[0], config=self.config,
                                             listener=self.messageReceiver, parent=self),
                              FolderViewTree(initialFolder=initialPaths[1], config=self.config,
                                             listener=self.messageReceiver, parent=self))
            self.treeViews.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.treeViews.setLineWidth(2)
            self.layout.addWidget(self.treeViews[0], 0, 0, 1, 1)
            self.layout.addWidget(self.treeViews[1], 0, 1, 1, 1)

            if self.showCurrentPath:
                self.layout.addWidget(self.lineCurrentPath, 1, 0, 1, 2)

            if includeButtonBox == True:
                self.layout.addWidget(self.toolBar, 2, 0, 1, 2)
            elif isinstance(includeButtonBox, QWidget):
                self.layout.addWidget(includeButtonBox, 2, 0, 1, 2)
        else:
            self.treeView = \
                FolderViewTree(initialPaths[0], config=self.config, listener=self.messageReceiver, parent=self)
            self.treeView.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            self.treeView.setLineWidth(2)

            self.layout.addWidget(self.treeView, 0, 0, 1, 1)

            if self.showCurrentPath:
                self.layout.addWidget(self.lineCurrentPath, 1, 0, 1, 1)

            if includeButtonBox == True:
                self.layout.addWidget(self.toolBar, 2, 0, 1, 1)
            elif isinstance(includeButtonBox, QWidget):
                self.layout.addWidget(includeButtonBox, 2, 0, 1, 1)
        self.initializing = False

    def __setattr__(self, key, value):
        if key == 'listener':
            if 'listener' not in self.__dict__:
                self.__dict__[key] = value
            return
        if key == 'dispatcher':
            if 'dispatcher' not in self.__dict__:
                self.__dict__[key] = value
            return
        self.__dict__[key] = value

    def moveUpOneLevel(self):
        currentFolder = self.getCurrentFolder()
        #   pathParts = path.split(currentFolder)
        pathParts = currentFolder.split('/')[1:]
        pathLen = len(pathParts)
        if pathLen > 0:
            newPath = '/' + '/'.join(pathParts[:pathLen-1])
            self.setFolder(newPath)

    def getTreeView(self):
        return self.treeView

    def setFolder(self, folderPath):
        if isinstance(folderPath, str) and isdir(folderPath):
            if not isinstance(self.treeView, tuple):
                self.treeView.setFolder(folderPath)
                self.currentFolder = folderPath

    def getCurrentFolder(self):
        if not isinstance(self.treeView, tuple):
            return self.currentFolder

    def handleNextRequest(self):
        if not isinstance(self.treeView, tuple):
            #   self.currentFolder needs to be set if the request works:
            folderChange = self.treeView.handleNextRequest()
            if folderChange is not None:
                self.currentFolder = folderChange
                return folderChange
            return self.currentFolder

    def handlePrevRequest(self):
        if not isinstance(self.treeView, tuple):
            #   self.currentFolder needs to be set if the request works:
            folderChange = self.treeView.handlePrevRequest()
            if folderChange is not None:
                self.currentFolder = folderChange
                return folderChange
            return self.currentFolder

    def messageReceiver(self, message: dict):
        if self.initializing:
            return
        if not isinstance(message, dict):
            return
        if 'source' in message:
            #   {'source': "FolderViewTree.selectionChanged", "newSelections": tuple(self.selectedItems)}
            if message['source'] == "FolderViewTree.selectionChanged":
                if 'newSelections' in message and isinstance(message['newSelections'], tuple):
                    self.currentSelections = message['newSelections']
                    #   The first element of the tuple might not be a folder, so self.currentFolder might be misnamed.
                    self.currentFolder = self.currentSelections[0]
                    if self.showCurrentPath:
                        self.lineCurrentPath.setText(self.currentFolder)
                    if self.listener is not None:
                        self.listener(message)
            #   {'source': 'FolderViewTree.mouseDoubleClickEvent', 'selectedPath': selectedPath}
            elif message['source'] == "FolderViewTree.mouseDoubleClickEvent":
                if 'selectedPath' in message and isinstance(message['selectedPath'], str) and \
                        isdir(message['selectedPath']):
                    self.currentFolder = message['selectedPath']
                    if self.listener is not None:
                        self.listener(message)


    def getLayout(self):
        return self.layout

    def setSelection(self):
        if self.currentSelections is None:
            messageDialog = QMessageBox(text="You must first select a folder from the file system navigator.\n")
            messageDialog.setWindowTitle("No Selection Made")
            messageDialog.setGeometry(QRect(450, 200, 500, 150))
            messageDialog.setStandardButtons(QMessageBox.Ok)
            messageDialog.exec()
            return

        if self.listener is not None:
            selectionOk = True
            fileSelection = None
            if self.foldersOnly:
                fileSelected = False
                for selection in self.currentSelections:
                    if isfile(selection):
                        fileSelected = True
                        selectionOk = False
                        fileSelection = selection
                        break
                if fileSelected:
                    messageDialog = QMessageBox(text='Your selection includes a file:\n\n'
                                                     + fileSelection + '\n', parent=None)
                    messageDialog.setWindowTitle("Only Folders Allowed")
                    messageDialog.setGeometry(QRect(250, 100, 600, 250))
                    messageDialog.setStandardButtons(QMessageBox.Ok)
                    response = messageDialog.exec()
            if selectionOk:
                self.listener({'source': 'FileViewFrame.setSelection', 'selected': self.currentSelections})

    def buildStudy(self):
        if DEBUG:
            print("FileViewFrame.buildStudy")
        #   Check to see if any folders are selected:
        if self.currentSelections is None or len(self.currentSelections) == 0:
            showFoldersNotSelectedNotice(self)
        else:
            if self.listener is not None:
                self.listener({'source': "FileViewFrame.buildStudy", "selections": self.currentSelections})

    def closeFrame(self):
        if DEBUG:
            print("FileViewFrame.closeFrame")
        if self.listener is not None:
            self.listener({'source': "FileViewFrame.closeFrame"})

    def getPaths(self):
        if DEBUG:
            print("FileViewFrame.getPaths")
        showNotImplementedMessage(
            "This feature, collect the displayed path tree into an index, is not implemented yet.",
            parent=self)

    def buttonClicked(self, *args):
        if DEBUG:
            print("FileViewFrame.buttonClicked:\t" + str(args))
        """
        if buttonId == QDialogButtonBox.Close:
            self.close()
            if self.listener is not None:
                self.listener({'source': "FileViewFrame.closeDialog"})
        """

    def getType(self):
        return self.pageType

    def getUrl(self):
        return None

    def getTitle(self):
        return None


class FileDialog(QDialog):

    DEFAULT_CONFIG  = {}
    DEFAULT_ID      = 'FileDialog'

    def __init__(self, identifier: str=None, initialFolder: str=None, config: dict=None, listener=None, parent=None):
        if identifier is not None:
            if not isinstance(identifier, str):
                raise Exception("FileDialog constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        else:
            self.identifier = FileDialog.DEFAULT_ID
        if initialFolder is not None:
            if not isinstance(initialFolder, str) or not isdir(initialFolder):
                raise Exception("FileDialog constructor - Invalid initialFolder argument:  " + str(initialFolder))
            self.currentFolder = initialFolder
        else:
            self.currentFolder = environ['HOME']
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("FileDialog constructor - Invalid config argument:  " + str(config))
            else:
                self.config = config
        else:
            self.config = FileDialog.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(FileDialog, self).__init__(parent)

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        if 'title' in config and isinstance(config['title'], str):
            self.setWindowTitle(config['title'])

        self.config['selectable'] = True
        self.fileViewFrame = FileViewFrame((self.currentFolder,), config=self.config,
                                           listener=self.messageReceiver, parent=self)

        self.gridLayout.addWidget(self.fileViewFrame, 0, 0, 5, 5)

    def changeEvent(self, event: QEvent) -> None:
        super(FileDialog, self).changeEvent(event)
        #   if self.listener is not None:
        #       self.listener({'source': 'FileDialog.changeEvent', 'newSelection': None})

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(FileDialog, self).mousePressEvent(event)

    def messageReceiver(self, message: dict):
        if DEBUG:
            print("FileDialog.messageReceiver:\t" + str(message))
        if not isinstance(message, dict):
            return
        if 'source' in message:
            #   {'source': 'FileViewFrame.setSelection', 'selected': self.currentSelections}
            if message['source'] == 'FileViewFrame.setSelection':
                if self.listener is not None:
                    message['identifier'] = self.identifier
                    self.listener(message)
            #   {'source': "FolderViewTree.selectionChanged", "newSelections": tuple(self.selectedItems)}
            elif message['source'] == "FolderViewTree.selectionChanged":
                if 'newSelections' in message and isinstance(message['newSelections'], tuple):
                    self.currentSelections = message['newSelections']
                    if self.listener is not None:
                        self.listener(message)

            #   {'source': "FileViewFrame.closeFrame", 'identifier': self.identifier}
            elif message['source'] == "FileViewFrame.closeFrame":
                if self.listener is not None:
                    message['identifier'] = self.identifier
                    self.listener(message)

    def closeEvent(self, event: QCloseEvent) -> None:
        super(FileDialog, self).closeEvent(event)
        self.exit()

    def exit(self):
        if self.listener is not None:
            self.listener({'source': "FileViewFrame.closeFrame", 'identifier': self.identifier})


class ImageManager(QMainWindow):

    DEFAULT_CONFIG = {'imageFileFolder': environ['HOME'], 'scanType': 'walk', 'extSet': 'PixMap'}

    def __init__(self, config: dict, displayDimensions: dict, listener=None, parent=None):
        if config is None:
            self.config = ImageManager.DEFAULT_CONFIG
        else:
            if not isinstance(config, dict):
                raise Exception("ImageManager constructor - Invalid config argument:  " + str(config))
            self.config = config
        if not isinstance(displayDimensions, dict):
            raise Exception("ImageManager constructor - Invalid displayDimensions argument:  " + str(displayDimensions))
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        self.extSet = 'PixMap'
        super(ImageManager, self).__init__(parent)
        #   self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.displayDimensions = displayDimensions

        self.contentFrame = QFrame(parent=self)
        self.contentGridLayout = QGridLayout()
        self.contentFrame.setLayout(self.contentGridLayout)

        self.pixMapImages = OrderedDict()
        self.textSelectorMap = OrderedDict()
        self.imageFolder = None
        self.selectedImgFilePath = None
        self.selectedPixMap = None
        self.viewPixMap = None
        self.imageFolderSelector = None
        self.scanTypeOverride = None
        self.textSelector   = None
        self.configurationDialog = None
        self.helpDialog = None
        self.jobDefinitionView = None
        self.jobSelectionDialog = None
        self.configurationDialog = None

        self.toolBarIcon = self.buildToolBar()
        self.addToolBar(self.toolBarIcon)
        self.initMenuBar()

        statusBar = QStatusBar()
        self.setStatusBar(statusBar)


        #   Alternative for start-up folder selection scan:
        if 'folderSelectedOnStart' in self.config and self.config['folderSelectedOnStart']:
            if 'scanType' in self.config:
                #   Scan the selected folder according to self.config
                if self.config['scanType'] == ScanType.WALK:
                    pass
                elif self.config['scanType'] == ScanType.LIST:
                    pass

        if 'imageFileFolder' in self.config and isdir(self.config['imageFileFolder']):
            self.imageFolder = self.config['imageFileFolder']
            self.scanType = ScanType.LIST
            if 'scanType' in self.config:
                self.scanType   = self.config['scanType']
            if self.scanType == ScanType.LIST:
                Scan.listFolder(self.imageFolder, self.pixMapImages)
            elif self.scanType == ScanType.WALK:
                Scan.walkFolder(self.imageFolder, self.pixMapImages)

        self.setStatusBar(QStatusBar())

        self.toolBarMain = QToolBar()
        self.addToolBar(self.toolBarMain)

        self.buttonSelectFolder = QPushButton(" Select Folder ", self)
        selectFolderHelpText    = "Select a new folder"
        self.buttonSelectFolder.setToolTip(selectFolderHelpText)
        self.buttonSelectFolder.setStatusTip(selectFolderHelpText)
        self.buttonSelectFolder.clicked.connect(lambda: self.selectImageFolder(initialFolder=None))
        self.toolBarMain.addWidget(self.buttonSelectFolder)

        #   Menu button for view mode: large or small, could also include a slider for size setting.
        self.buttonImageSize = QPushButton(" Image Size ", self)
        imageSizeHelpText   ='Resize the image content of the selected file or launch full size view in popup dialog'
        self.buttonImageSize.setToolTip(imageSizeHelpText)
        self.buttonImageSize.setStatusTip(imageSizeHelpText)
        self.imageSizeMenu = QMenu(self.buttonImageSize)
        self.imageSizeMenu.addAction("Fit Frame", lambda:  self.setImageSize("Fit Frame"))
        self.imageSizeMenu.addAction("Original", lambda:  self.setImageSize("Original"))
        self.imageSizeMenu.addAction("Larger", lambda: self.setImageSize("Larger"))
        self.imageSizeMenu.addAction("Smaller", lambda: self.setImageSize("Smaller"))
        self.imageSizeMenu.addAction("to Dialog", lambda: self.setImageSize("to Dialog"))
        self.buttonImageSize.setMenu(self.imageSizeMenu)
        self.toolBarMain.addWidget(self.buttonImageSize)

        self.buttonImageText = QPushButton(" Select Image Text ", self)
        self.buttonImageText.clicked.connect(self.launchTextSelector)
        imageTextExtractHelp = "Display the selected image in the text selection dialog to extract text you select"
        self.buttonImageText.setToolTip(imageTextExtractHelp)
        self.buttonImageText.setStatusTip(imageTextExtractHelp)
        self.toolBarMain.addWidget(self.buttonImageText)

        self.buttonBatchProcess = QPushButton(" Batch Process ", self)
        batchProcessHelpText    = 'Extract all text from each image in the list below and record their text content and meta-data in the database'
        self.buttonBatchProcess.setToolTip(batchProcessHelpText)
        self.buttonBatchProcess.setStatusTip(batchProcessHelpText)
        self.buttonBatchProcess.clicked.connect(lambda: self.batchProcessAll(repeat=True))
        self.toolBarMain.addWidget(self.buttonBatchProcess)

        self.buttonBatchProcess = QPushButton(" Run Job ", self)
        runJobHelpText  = 'Select and run a job you defined using the Job Manager'
        self.buttonBatchProcess.setToolTip(runJobHelpText)
        self.buttonBatchProcess.setStatusTip(runJobHelpText)
        self.buttonBatchProcess.clicked.connect(lambda: self.toolBarAction('Run Job'))
        self.toolBarMain.addWidget(self.buttonBatchProcess)


        self.spacerLabel = FieldLabel(identifier="spacerLabel", text="", listener=self.messageReceiver)
        self.spacerLabel.setFixedWidth(100)
        self.spacerLabel.setFixedHeight(35)
        self.toolBarMain.addWidget(self.spacerLabel)

        self.buttonHelp = AppButton(text='Help', identifier="Help", listener=self.messageReceiver, parent=self.toolBarMain)
        self.buttonHelp.setCheckable(True)
        helpButtonHelpText = "Toggle the multi-tabbed help window"
        self.buttonHelp.setToolTip(helpButtonHelpText)
        self.buttonHelp.setStatusTip(helpButtonHelpText)
        self.buttonHelp.clicked.connect(self.toggleHelp)
        self.buttonHelp.setIcon(QIcon(TOOLBAR_ICON_FOLDER + '/' + HELP_FOLDER_ICON))
        self.buttonHelp.setIconSize(QSize(30, 30))
        self.buttonHelp.setMaximumWidth(75)
        self.toolBarMain.addWidget(self.buttonHelp)

        #   Help button alternative:
        """
        self.buttonHelpToggle = QPushButton(" Help ", self)
        self.buttonHelpToggle.setCheckable(True)
        self.buttonHelpToggle.setToolTip("Toggle the multi-tabbed help window")
        self.buttonSelectFolder.clicked.connect(self.toggleHelp)
        self.mainToolBar.addWidget(self.buttonHelpToggle)
        """

        self.fileCheckedList  = OrderedDict()
        self.fileSelectionList = OrderedDict()
        self.listViewFiles = FileListView(identifier='listViewFiles', imageMap=self.pixMapImages,
                                          config={'listType': self.config['scanType']},
                                          listener=self.messageReceiver, parent=self.contentFrame)
        self.listViewFiles.setWindowTitle("Image File List")
        self.listViewFiles.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.fileListModel = QStandardItemModel()
        self.listItemMap = OrderedDict()
        for filePath in self.pixMapImages:
            self.listItemMap[filePath]  = QStandardItem(filePath)
            self.listItemMap[filePath].setCheckable(True)
            #   QStandardItem().checkState().Checked == Qt.CheckState.Checked
            self.fileListModel.appendRow(self.listItemMap[filePath])
        self.listViewFiles.setModel(self.fileListModel)
        self.fileListModel.itemChanged.connect(self.fileListSelectionEvent)

        self.imageScroller = QScrollArea(parent=self.contentFrame)
        self.imageScroller.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.imageScroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.imageScroller.setWidgetResizable(True)

        self.labelImage = QLabel("Selected Image", parent=self.imageScroller)
        self.imageScroller.setWidget(self.labelImage)

        self.labelMessages = QLabel("messages", parent=self.contentFrame)

        self.contentGridLayout.addWidget(self.labelMessages, 0, 0, 1, 2)
        self.contentGridLayout.addWidget(self.listViewFiles, 1, 0, 1, 1)
        self.contentGridLayout.addWidget(self.imageScroller, 1, 1, 1, 1)
        self.setCentralWidget(self.contentFrame)

        self.getDimensions()

    def getDimensions(self):
        self.dialogHeight = self.height()
        self.dialogWidth = self.width()
        self.imageScrollerHeight = self.imageScroller.height()
        self.imageScrollerWidth = self.imageScroller.width()

    def toggleHelp(self):
        if DEBUG:
            print(("ImageManager.toggleHelp"))
        if self.helpDialog is None:
            config = {
                'title':    'PictureTextCrop Help',
                'helpTopics': {
                    'About':   HELP_DOCS_FOLDER + '/' + HELP_ABOUT_FILE,
                    "Quick Start": HELP_DOCS_FOLDER + '/' + HELP_QUICK_START_FILE,
                    'Files Menu': HELP_DOCS_FOLDER + '/' + HELP_FILES_MENU_FILE,
                    'Run Menu':  HELP_DOCS_FOLDER + '/' + HELP_RUN_MENU_FILE,
                    'View Menu': HELP_DOCS_FOLDER + '/' + HELP_VIEW_MENU_FILE,
                    'Admin Menu': HELP_DOCS_FOLDER + '/' + HELP_ADMIN_MENU_FILE,
                },
            }
            self.helpDialog = HelpDialog(config=config, listener=self.messageReceiver)
            self.helpDialog.setGeometry(QRect(150, 150, 700, 550))
            self.helpDialog.show()
        self.helpDialog.setVisible(self.buttonHelp.isChecked())

    def buildToolBar(self):
        toolBar = QToolBar(parent=self)
        #           self.buttonSelectFolder.clicked.connect(lambda: self.selectImageFolder(initialFolder=None))
        #   self.destActionMap[destination].triggered.connect(partial(self.storeToDestination, destination))

        scanFolderRecursive = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/address-book.png'), 'scan', toolBar)
        scanFolderRecursive.triggered.connect(lambda: self.selectImageFolder(initialFolder=None))
        #   actionAnalysisLocate.setCheckable(True)
        scanRecursiveHelpText   = "Select folder to scan for image files - entire tree"
        scanFolderRecursive.setToolTip(scanRecursiveHelpText)
        scanFolderRecursive.setStatusTip(scanRecursiveHelpText)
        toolBar.addAction(scanFolderRecursive)

        self.iconActionSelectAllFiles = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/asterisk.png'), 'select all', toolBar)
        self.iconActionSelectAllFiles.triggered.connect(lambda: self.selectAllImages('Icon Button'))
        self.iconActionSelectAllFiles.setCheckable(True)
        selectAllFilesHelpText = "Select all images in the current list"
        self.iconActionSelectAllFiles.setToolTip(selectAllFilesHelpText)
        self.iconActionSelectAllFiles.setStatusTip(selectAllFilesHelpText)
        toolBar.addAction(self.iconActionSelectAllFiles)

        actionCropSequence = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/control-double.png'), 'Sequence', toolBar)
        actionCropSequence.triggered.connect(partial(self.runImageFileCropSelectionList))
        self.sequenceCropHelpText    = "Display each selected image in turn in the text cropping dialog and store " \
                                       "its cropped text in the CropLog table"
        actionCropSequence.setToolTip(self.sequenceCropHelpText)
        actionCropSequence.setStatusTip(self.sequenceCropHelpText)
        toolBar.addAction(actionCropSequence)

        actionAnalysisScannedFolders = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/arrow-circle-135-left.png'), 'Batch Process', toolBar)
        actionAnalysisScannedFolders.triggered.connect(lambda: self.toolBarAction("Batch Process"))
        batchHelpText   = 'Extract all text from all files in the list and store it in the BatchMaster table'
        actionAnalysisScannedFolders.setToolTip(batchHelpText)
        actionAnalysisScannedFolders.setStatusTip(batchHelpText)
        toolBar.addAction(actionAnalysisScannedFolders)

        actionRunJobs = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/arrow.png'), 'Run Job', toolBar)
        actionRunJobs.triggered.connect(lambda: self.toolBarAction("Run Job"))
        runJobHelpText   = 'Select and run jobs you defined using the job definition dialog or job manager'
        actionRunJobs.setToolTip(runJobHelpText)
        actionRunJobs.setStatusTip(runJobHelpText)
        toolBar.addAction(actionRunJobs)

        actionLaunchJobsDialog = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/toolbox.png'), 'Jobs', toolBar)
        actionLaunchJobsDialog.triggered.connect(lambda: self.toolBarAction("Jobs"))
        launchJobsDialogHelpText = "Launch the Job Management dialog to add, edit and manage jobs."
        actionLaunchJobsDialog.setStatusTip(launchJobsDialogHelpText)
        actionLaunchJobsDialog.setToolTip(launchJobsDialogHelpText)
        toolBar.addAction(actionLaunchJobsDialog)

        actionExit = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/control-power.png'), 'Exit', toolBar)
        actionExit.triggered.connect(lambda: self.toolBarAction("Exit"))
        actionExit.setStatusTip("Exit this application")
        toolBar.addAction(actionExit)

        return toolBar

    def toolBarAction(self, actionId: str):
        if DEBUG:
            print("ImageManager.toolBarAction:\t" + actionId)
        if actionId == 'Exit':
            if self.listener is not None:
                self.listener({'source': 'ImageManager.toolBarAction', 'actionId': actionId})
        elif actionId == 'Jobs':
            if self.jobDefinitionView is None:
                self.jobDefinitionView = JobDefinitionView(job=Job(FileCollectionOrdered()), identifier='jobDefinitionView', config=None,
                                                           listener=self.messageReceiver)
                self.jobDefinitionView.setGeometry(QRect(200, 100, 700, 400))

            self.jobDefinitionView.show()

        elif actionId == 'Batch Process':
            self.batchProcessAll(repeat=True)

        elif actionId == 'Run Job':
            self.selectAndRunJob()


    def initMenuBar(self):
        #   menu = QMenuBar()
        menu = self.menuBar()

        #       Using icons in menu items:
        #   action  = QAction(QIcon(ICON_FOLDER + '/' + ICON_FILE_LOAD), "&Load",
        #                     self, shortcut="Ctrl+L", triggered=self.loadFile)
        #   self.fileMenu.addAction(QAction("&Select Folder", self, shortcut="Ctrl+L", triggered=self.selectFolder))

        #   Presence of some of these, like 'View Folder Text' and 'Export',  will depend on whether the
        #       application is in ADMIN mode.

        fileMenu = menu.addMenu("Files")

        menuScanFolder  = fileMenu.addMenu("Scan Folder")

        actionWalkFolder = QAction("&Walk", self, shortcut="Ctrl+W", triggered=partial(self.fileMenuAction, "Walk"))
        actionWalkFolder.setStatusTip("Traverse (Walk) s selected folder's subfolders to list the files in its folder tree")
        menuScanFolder.addAction(actionWalkFolder)

        actionListFolder = QAction("&List", self, shortcut="Ctrl+S", triggered=partial(self.fileMenuAction, "List"))
        actionListFolder.setStatusTip("List the contents of a selected folder")
        menuScanFolder.addAction(actionListFolder)

        actionSelectText = QAction("&Select Text", self, shortcut="Ctrl+S", triggered=partial(self.fileMenuAction, "Select Text"))
        actionSelectText.setStatusTip("Display the selected image in the text selection dialog to extract text you select")
        fileMenu.addAction(actionSelectText)

        self.menuActionSelectAll     = QAction("&Select All", self, shortcut="Ctrl+S", triggered=partial(self.fileMenuAction, "Select All"))
        self.menuActionSelectAll.setCheckable(True)
        selectAllFilesHelpText = "Select all images in the current list"
        self.menuActionSelectAll.setStatusTip(selectAllFilesHelpText)
        self.menuActionSelectAll.triggered.connect(lambda: self.selectAllImages('Menu Button'))
        fileMenu.addAction(self.menuActionSelectAll)

        actionExit  = QAction("E&xit", self, shortcut="Ctrl+X", triggered=partial(self.fileMenuAction, "Exit"))
        actionExit.setStatusTip("Exit this application")
        fileMenu.addAction(actionExit)

        runMenu = menu.addMenu("Run")

        actionRunSequence   = QAction("&Sequence", self, shortcut="Ctrl+S", triggered=partial(self.runMenuAction, "Sequence"))
        actionRunSequence.setStatusTip(self.sequenceCropHelpText)
        runMenu.addAction(actionRunSequence)

        actionRunBatch  = QAction("&Batch", self, shortcut="Ctrl+B", triggered=partial(self.runMenuAction, "Batch"))
        actionRunBatch.setStatusTip("Extract all the text from each file in the selected folder's contents list and "
                                    "store it in the BatchMaster table")
        runMenu.addAction(actionRunBatch)

        actionRunBatch  = QAction("&Job", self, shortcut="Ctrl+J", triggered=partial(self.toolBarAction, "Run Job"))
        actionRunBatch.setStatusTip("Run jobs you defined using the job definition dialog or job manager")
        runMenu.addAction(actionRunBatch)

        viewMenu = menu.addMenu("View")
        imageSizeMenu = viewMenu.addMenu("Image Size")

        actionSmall = QAction("Fit Frame", self, triggered=partial(self.setImageSize, "Fit Frame"))
        actionSmall.setStatusTip("Fit the image to its view frame")
        imageSizeMenu.addAction(actionSmall)

        actionLarge     = QAction("Original", self, triggered=partial(self.setImageSize, "Original"))
        actionLarge.setStatusTip("View image in its normal, original size in the scrollable frame")
        imageSizeMenu.addAction(actionLarge)

        actionSizeToFrame   = QAction("Larger", self, triggered=partial(self.setImageSize, "Larger"))
        actionSizeToFrame.setStatusTip("View the image 10% larger")
        imageSizeMenu.addAction(actionSizeToFrame)

        actionSizeToFrame   = QAction("Smaller", self, triggered=partial(self.setImageSize, "Smaller"))
        actionSizeToFrame.setStatusTip("View the image 10% smaller")
        imageSizeMenu.addAction(actionSizeToFrame)

        actionSizeToFrame   = QAction("to Dialog", self, triggered=partial(self.setImageSize, "to Dialog"))
        actionSizeToFrame.setStatusTip("View the image in its own dialog")
        imageSizeMenu.addAction(actionSizeToFrame)

        toolBarMenu = viewMenu.addMenu("ToolBars")

        self.actionIcons = QAction("Icons", self, triggered=partial(self.toggleToolbar, "Icons"))
        self.actionIcons.setCheckable(True)
        self.actionIcons.setChecked(True)
        self.actionIcons.setStatusTip("Toggle the toolbar with icon buttons on or off")
        toolBarMenu.addAction(self.actionIcons)

        self.actionText = QAction("Text", self, triggered=partial(self.toggleToolbar, "Text"))
        self.actionText.setCheckable(True)
        self.actionText.setChecked(True)
        self.actionText.setStatusTip("Toggle the toolbar with text buttons on or off")
        toolBarMenu.addAction(self.actionText)


        if AppConfig._adminEnabled:
            adminMenu = menu.addMenu("Admin")

            actionConfiguration     = QAction("&Configuration", self, shortcut="Ctrl+A", triggered=partial(self.adminMenuAction, "Configuration"))
            actionConfiguration.setStatusTip("Set configuration settings in a multi-tab window")
            adminMenu.addAction(actionConfiguration)

            actionUsers     = QAction("&Jobs", self, shortcut="Ctrl+J", triggered=partial(self.toolBarAction, "Jobs"))
            actionUsers.setStatusTip("Define, add, and edit Jobs, e.g. image file crop sequence")
            adminMenu.addAction(actionUsers)

        return menu

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.getDimensions()
        if DEBUG:
            print("resizeEvent:\theight:\t" + str(self.dialogHeight) + "\twidth:\t" + str(self.dialogWidth))
            print("\tscroller height:\t" + str(self.imageScrollerHeight) +
                  "\tscroller width:\t" + str(self.imageScrollerWidth))

    def launchTextSelector(self):
        if DEBUG:
            print("ImageManager.launchTextSelector")
        hPos = 200
        yPos = 100
        for filePath in self.fileCheckedList:
            if filePath not in self.pixMapImages or self.pixMapImages[filePath] is None:
                #   self.loadImage(filePath)
                #   self.pixMapImages[filePath] = Image.open(filePath).toqpixmap()
                #   self.pixMapImages[filePath]     = QPixmap(filePath)
                self.pixMapImages[filePath] = Scan.readImage(filePath)

            if filePath not in self.textSelectorMap:
                config = { 'topLeft': QPoint(hPos, yPos)}
                self.textSelectorMap[filePath] = TextSelector(pixMapImage=self.pixMapImages[filePath],
                                                              imagePath=filePath, config=config,
                                                              listener=self.messageReceiver, parent=self)
                hPos += 50
                yPos += 50
            self.textSelectorMap[filePath].exec()

    def setImageSize(self, sizeName: str):
        if DEBUG:
            print("ImageManager.setImageSize:\t" + sizeName)
        if self.selectedPixMap is None:
            return

        if sizeName == "Fit Frame":
            if DEBUG:
                print("resizeEvent:\theight:\t" + str(self.dialogHeight) + "\twidth:\t" + str(self.dialogWidth))
                print("\tscroller height:\t" + str(self.imageScrollerHeight) +
                      "\tscroller width:\t" + str(self.imageScrollerWidth))
            self.scaleImageToFit()

        elif sizeName == "Original":
            self.viewPixMap = self.selectedPixMap
            self.labelImage.setPixmap(self.viewPixMap)

        elif sizeName == "Larger":          #   previously "Large"
            self.getDimensions()
            self.viewPixMap = self.viewPixMap.scaledToHeight(floor(self.viewPixMap.height() * 1.1))
            self.labelImage.setPixmap(self.viewPixMap)

        elif sizeName == "Smaller":
            self.getDimensions()
            self.viewPixMap = self.viewPixMap.scaledToHeight(floor(self.viewPixMap.height() * 1/1.1))
            self.labelImage.setPixmap(self.viewPixMap)

        elif sizeName == "to Dialog":
            if self.selectedImgFilePath not in self.textSelectorMap:
                config = { 'topLeft': QPoint(200, 100)}
                self.textSelectorMap[self.selectedImgFilePath] = \
                    TextSelector(identifier=self.selectedImgFilePath,
                                 pixMapImage=self.pixMapImages[self.selectedImgFilePath],
                                 imagePath=self.selectedImgFilePath, config=config,
                                 listener=self.messageReceiver, parent=self)

                width = self.displayDimensions['width'] - config['topLeft'].x() - 100
                height = self.displayDimensions['height'] - config['topLeft'].y() - 100

                imageWidth = self.pixMapImages[self.selectedImgFilePath].width()
                imageHeight = self.pixMapImages[self.selectedImgFilePath].height()
                if imageWidth < width:
                    width = imageWidth
                if imageHeight < height:
                    height = imageHeight

                self.textSelectorMap[self.selectedImgFilePath].setMinimumWidth(width)
                self.textSelectorMap[self.selectedImgFilePath].setMinimumHeight(height)
            self.textSelectorMap[self.selectedImgFilePath].show()


    def toggleToolbar(self, toolBarId: str):
        if not isinstance(toolBarId, str):
            return
        if toolBarId == "Icons":
            self.toolBarIcon.setVisible(self.actionIcons.isChecked())
        elif toolBarId == "Text":
            self.toolBarMain.setVisible(self.actionText.isChecked())


    def scaleImageToFit(self):
        self.getDimensions()
        scaled = False
        pixMap = self.selectedPixMap
        if pixMap.height() != self.imageScrollerHeight:
            pixMap = pixMap.scaledToHeight(self.imageScrollerHeight)
            scaled = True
        if pixMap.width() > self.imageScrollerWidth - 15:  # -15 for scroller frame width adjustment
            pixMap = pixMap.scaledToWidth(self.imageScrollerWidth - 15)
            scaled = True
        if scaled:
            self.viewPixMap = pixMap
            self.labelImage.setPixmap(self.viewPixMap)

    def runImageFileCropSelectionList(self):
        for filePath, selected in self.fileSelectionList.items():
            if selected:
                if DEBUG:
                    print("ImageManager.runImageFileCropSelectionList:\n\t" + filePath)
                if self.pixMapImages[filePath] is None:
                    self.pixMapImages[filePath] = Scan.readImage(filePath)
                config = {'topLeft': QPoint(200, 100), 'exitOnSelect': True}
                self.textSelector = TextSelector(identifier='sequenceTextSelector',
                                                 pixMapImage=self.pixMapImages[filePath],
                                                 imagePath=filePath, config=config,
                                                 listener=self.messageReceiver, parent=self)
                self.textSelector.exec()

    def runCropDialogSequence(self, flatFileSequence: tuple=None):
        if flatFileSequence is None:
            if self.iconActionSelectAllFiles.isChecked():
                for filePath in self.pixMapImages:
                    if self.pixMapImages[filePath] is None:
                        self.pixMapImages[filePath] = Scan.readImage(filePath)
                    config = {'topLeft': QPoint(200, 100), 'exitOnSelect': True}
                    self.textSelector = TextSelector(identifier='sequenceTextSelector', pixMapImage=self.pixMapImages[filePath],
                                                  imagePath=filePath, config=config,
                                                  listener=self.messageReceiver, parent=self)
                    self.textSelector.exec()
                return True
            else:
                for filePath in self.fileCheckedList:
                    if filePath not in self.pixMapImages or self.pixMapImages[filePath] is None:
                        #   self.loadImage(filePath)
                        #   self.pixMapImages[filePath] = Image.open(filePath).toqpixmap()
                        #   self.pixMapImages[filePath] = QPixmap(filePath)
                        self.pixMapImages[filePath] = Scan.readImage(filePath)
                    config = {'topLeft': QPoint(200, 100), 'exitOnSelect': True}
                    self.textSelector = TextSelector(identifier='sequenceTextSelector', pixMapImage=self.pixMapImages[filePath],
                                                  imagePath=filePath, config=config,
                                                  listener=self.messageReceiver, parent=self)
                    self.textSelector.exec()
                return True
        else:
            if not isinstance(flatFileSequence, tuple):
                return False
            for filePath in flatFileSequence:
                if not isinstance(filePath, str) or not isfile(filePath):
                    raise Exception("ImageManager.runCropDialogSequence:  filePath does not reference a file:  " + str(filePath))
                pixMapImage = Scan.readImage(filePath)
                config = {'topLeft': QPoint(200, 100), 'exitOnSelect': True}
                self.textSelector = TextSelector(identifier='sequenceTextSelector', pixMapImage=pixMapImage,
                                                 imagePath=filePath, config=config,
                                                 listener=self.messageReceiver, parent=self)
                self.textSelector.exec()
            return True

    def batchProcessAll(self, repeat: bool=False, flatFileSequence: tuple=None):
        if DEBUG:
            print("ImageManager.batchProcessAll")
        if DEBUG:
            ImageTextDB.dumpContent()

        if flatFileSequence is None:
            if repeat:
                Extractor.batchProcessAll(self.imageFolder, self.pixMapImages)
        else:
            if not isinstance(flatFileSequence, tuple):
                return
            Extractor.batchProcessJob(flatFileSequence)

    def selectAndRunJob(self):
        """
        Show job selection dialog with one variation: selection of batch mode or crop sequence mode.
        Batch mode can take time so a warning should be displayed in a configurable help area at the bottom.
        Using QTextEdit in read-only mode allows formatting of the help text with HTML.
        Once the job is selected and the mode is set, run the job.
        :return:
        """
        if DEBUG:
            print("ImageManager.selectAndRunJob")
        #   textInput = QTextEdit()
        if self.jobSelectionDialog is None:
            self.jobSelectionDialog = JobSelectionDialog(identifier='jobSelectionDialog',
                                                         config={'mode': 'select for run'},
                                                         listener=self.messageReceiver)
            self.jobSelectionDialog.setWindowTitle("Select and RUN Job")
        self.jobSelectionDialog.exec()


    def selectImageFolder(self, initialFolder: str=None, scanType: ScanType=None):
        if initialFolder is not None and (not isinstance(initialFolder, str) or not isdir(initialFolder)):
            raise Exception("ImageManager.selectImageFolder - Invalid initialFolder argument:  " + str(initialFolder))
        if scanType is not None and not isinstance(scanType, ScanType):
            raise Exception("ImageManager.selectImageFolder - Invalid scanType argument:  " + str(scanType))

        if initialFolder is not None:
            self.imageFolder = initialFolder
        elif self.imageFolder is None:
            self.imageFolder = environ['HOME']
        config = {'selectable': True,
                  'title': "Select Folder to Scan for Image Files",
                  'foldersOnly': True,
                  'showCurrentPath': True,
                  'selectionMode': 'extended'}
        self.scanTypeOverride = scanType
        self.imageFolderSelector = FileDialog(identifier='imageFolderSelector',
                                              initialFolder=self.imageFolder, config=config,
                                              listener=self.messageReceiver, parent=None)
        self.imageFolderSelector.setGeometry(QRect(300, 200, 550, 450))
        self.imageFolderSelector.exec()

    def selectAllImages(self, controlId: str):
        if not isinstance(controlId, str) or not controlId in ('Icon Button', 'Menu Button'):
            return
        if controlId == 'Icon Button':
            self.menuActionSelectAll.setChecked(self.iconActionSelectAllFiles.isChecked())
        else:
            self.iconActionSelectAllFiles.setChecked(self.menuActionSelectAll.isChecked())
        row = 0
        model = self.listViewFiles.selectionModel()
        if self.iconActionSelectAllFiles.isChecked() or self.menuActionSelectAll.isChecked():
            for filePath in self.pixMapImages.keys():
                #   self.listItemMap[filePath].setCheckState(True)
                #   self.listItemMap[filePath].checkState().Checked = Qt.CheckState.Checked
                index   = self.fileListModel.index(row, 0)
                model.select(index, QItemSelectionModel.Select)
                self.fileSelectionList[filePath] = True
                row += 1
            self.iconActionSelectAllFiles.setToolTip("Deselect all images in the current list")
            self.iconActionSelectAllFiles.setStatusTip("Deselect all images in the current list")
        else:
            for filePath in self.pixMapImages.keys():
                index   = self.fileListModel.index(row, 0)
                model.select(index, QItemSelectionModel.Deselect)
                row += 1
            self.fileSelectionList = OrderedDict()

            self.iconActionSelectAllFiles.setToolTip("Select all images in the current list")
            self.iconActionSelectAllFiles.setStatusTip("Select all images in the current list")

    def messageReceiver(self, message: dict):
        if not isinstance(message, dict):
            return
        if DEBUG:
            print("ImageManager.messageReceiver:\t" + str(message))

        if 'source' in message:

            #   {'source': "TextSelector.closeEvent", 'action': 'close requested' }
            if message['source'] == "TextSelector.closeEvent":
                if 'action' in message:
                    if message['action'] == 'close requested':
                        if 'fileName' in message:
                            if message['fileName'] in self.textSelectorMap:
                                self.textSelectorMap[message['fileName']].destroy()
                                del(self.textSelectorMap[message['fileName']])
                            self.listItemMap[message['fileName']].setCheckState(Qt.CheckState.Unchecked)

            #   {'source': 'FileListView.mousePressEvent', 'selectionText': self.currentImageFilePath}
            elif message['source'] == 'FileListView.mousePressEvent':
                if 'selectionText' in message and isinstance(message['selectionText'], str):
                    if self.selectedImgFilePath != message['selectionText']:
                        self.selectedImgFilePath = message['selectionText']
                        self.labelMessages.setText(self.selectedImgFilePath)

                        if self.selectedImgFilePath in self.pixMapImages:
                            self.loadImage(self.selectedImgFilePath)
                            self.selectedPixMap = self.viewPixMap  = self.pixMapImages[self.selectedImgFilePath]
                            self.scaleImageToFit()

            #   {'source': 'FileViewFrame.setSelection', 'selected': self.currentSelections}
            elif message['source'] == 'FileViewFrame.setSelection':
                if 'identifier' in message and message['identifier'] == 'imageFolderSelector':
                    if 'selected' in message and isinstance(message['selected'], tuple) and isdir(message['selected'][0]):
                        self.folderPath = self.imageFolder     = message['selected'][0]
                        self.imageFolderSelector.close()
                        self.imageFolderSelector = None
                        self.pixMapImages = OrderedDict()

                        if AppConfig._folderScanType != self.scanType:
                            self.scanType = AppConfig._folderScanType

                        if self.scanTypeOverride is not None:
                            scanType = self.scanTypeOverride
                            self.scanTypeOverride = None
                        else:
                            scanType = self.scanType

                        if scanType == ScanType.LIST:
                            Scan.listFolder(self.imageFolder, self.pixMapImages)
                        elif scanType == ScanType.WALK:
                            Scan.walkFolder(self.imageFolder, self.pixMapImages)

                        self.fileListModel = QStandardItemModel()
                        self.listItemMap = OrderedDict()
                        for fileName in self.pixMapImages:
                            self.listItemMap[fileName]  = QStandardItem(fileName)
                            self.listItemMap[fileName].setCheckable(True)
                            self.fileListModel.appendRow(self.listItemMap[fileName])
                        self.fileListModel.itemChanged.connect(self.fileListSelectionEvent)
                        self.listViewFiles.setModel(self.fileListModel)

                        self.selectedPixMap = None
                        self.viewPixMap = None
                        self.labelImage = QLabel("Selected Image", parent=self.imageScroller)
                        self.imageScroller.setWidget(self.labelImage)

            #   {'source': "PixMapLabel.mouseReleaseEvent", 'selectedText': text, 'filePath': filePath,
            #               'identifier': self.identifier}
            elif message['source'] == "PixMapLabel.mouseReleaseEvent":
                if 'identifier' in message and isinstance(message['identifier'], str):
                    if message['identifier'] == 'sequenceTextSelector':
                        self.textSelector.deleteLater()
                        self.textSelector = None

            #   {'source': 'ConfigurationDialog.handleButtonClick', 'buttonId': buttonId}
            elif message['source'] == 'ConfigurationDialog.handleButtonClick':
                if 'buttonId' in message:
                    if message['buttonId'] == "Exit":
                        if AppConfig.isChanged():
                            AppDatabase.updateConfig(AppConfig.getCurrent())
                        self.configurationDialog.close()
                        self.configurationDialog = None
                    elif message['buttonId'] == "Cancel":
                        self.configurationDialog.close()
                        self.configurationDialog = None

            #   {'source': "FileViewFrame.closeFrame", 'identifier': self.identifier}
            elif message['source'] == "FileViewFrame.closeFrame":
                if 'identifier' in message and message['identifier'] == 'imageFolderSelector':
                    self.imageFolderSelector.close()
                    self.imageFolderSelector = None

            #   {'source': 'JobDefinitionView.menuAction', 'actionId': actionId}
            elif message['source'] == 'JobDefinitionView.menuAction':
                if 'actionId' in message and message['actionId'] == "Exit":
                    self.jobDefinitionView.close()
                    self.jobDefinitionView = None

            #   {'source': 'JobDefinitionView.exitDialog'}
            elif message['source'] == 'JobDefinitionView.exitDialog':
                self.jobDefinitionView.close()
                self.jobDefinitionView = None

            #   {'source': 'JobDefinitionView.saveJob'}
            elif message['source'] == 'JobDefinitionView.saveJob':
                pass

            #   {'source': 'JobSelectionDialog.cancel', 'identifier': self.identifier}
            elif message['source'] == 'JobSelectionDialog.cancel':
                if 'identifier' in message and isinstance(message['identifier'], str):
                    if message['identifier'] == 'jobSelectionDialog':
                        self.jobSelectionDialog.close()
                        self.jobSelectionDialog = None

            #   {'source': 'JobSelectionDialog.selectJob',  'selection': self.currentJobTable[self.currentSelection],
            #           'runMode': self.runMode,    'consoleOutputConfig': consoleOutputConfig,
            #           'identifier': self.identifier}
            elif message['source'] == 'JobSelectionDialog.selectJob':
                if 'identifier' in message and isinstance(message['identifier'], str):
                    if message['identifier'] == 'jobSelectionDialog':
                        if 'selection' in message and isinstance(message['selection'], dict):
                            selection = message['selection']
                        else:
                            return
                        if 'FileSequence' in selection and isinstance(selection['FileSequence'], FileCollectionOrdered):
                            fileSequence = selection['FileSequence']
                        else:
                            return
                        if DEBUG:
                            print("Job selected to run:\t" + str(message['selection']['JobName']))
                        self.jobSelectionDialog.close()
                        self.jobSelectionDialog = None

                        if 'runMode' in message and message['runMode'] == RunMode.BATCH:
                             if 'consoleOutputConfig' in message and isinstance(message['consoleOutputConfig'], dict):
                                 Extractor.batchProcessJob(fileSequence, message['consoleOutputConfig'])

                        else:
                            self.runCropDialogSequence(fileSequence.getFileSequence())

            #   {'source': 'EvidenceHelpDialog.closeEvent'}
            elif message['source'] == 'EvidenceHelpDialog.closeEvent':
                self.buttonHelp.setChecked(False)

            #   {'source': 'FileListView.selectionChanged', 'identifier': self.identifier,
            #           'selection': selection, 'selectionList': tuple(self.selectionList)}
            elif message['source'] == 'FileListView.selectionChanged':
                if 'identifier' in message and message['identifier'] == 'listViewFiles':
                    if 'selectionList' in message and isinstance(message['selectionList'], tuple):
                        self.fileSelectionList = OrderedDict()
                        for filePath in message['selectionList']:
                            if isinstance(filePath, str) and isfile(filePath):
                                self.fileSelectionList[filePath] = True


    def closeEvent(self, event: QCloseEvent) -> None:
        if self.listener is not None:
            self.listener({'source': "ImageManager.closeEvent",
                           'action': 'close requested'})

    def loadImage(self, filePath: str):
        #   pixmap = QPixmap(filePath)  2023-12-23
        pixmap = Scan.readImage(filePath)
        self.pixMapImages[filePath] = pixmap
        #   image = Image.open(filePath)
        #   self.pixMapImages[filePath] = image.toqpixmap()

    def fileMenuAction(self, actionId: str):
        if DEBUG:
            print("ImageManager.fileManuAction:\t" + actionId)

        if actionId == "Select Text":
            self.launchTextSelector()
        if actionId == 'Walk':
            self.selectImageFolder(initialFolder=None, scanType=ScanType.WALK)
        elif actionId == 'List':
            self.selectImageFolder(initialFolder=None, scanType=ScanType.LIST)
        elif actionId == 'Exit':
            if self.listener is not None:
                self.listener({'source': 'ImageManager.toolBarAction', 'actionId': actionId})

    def runMenuAction(self, actionId: str):
        if DEBUG:
            print("ImageManager.runMenuAction:\t" + actionId)

        if actionId == "Sequence":
            self.runCropDialogSequence()

        elif actionId == "Batch":
            fileCount = 0
            timeStart = datetime.now()
            records = []
            for filePath in self.fileCheckedList:
                fileCount += 1
                if filePath not in self.pixMapImages or self.pixMapImages[filePath] is None:
                    #   self.loadImage(filePath)
                    #   self.pixMapImages[filePath] = Image.open(filePath).toqpixmap()
                    #   self.pixMapImages[filePath] = QPixmap(filePath)
                        self.pixMapImages[filePath] = Scan.readImage(filePath)
                newRecord = Extractor.makeTextExtractionRecord(filePath)
                records.append(newRecord)
            timeEnd = datetime.now()
            elapsedTime = timeEnd - timeStart
            ImageTextDB.addRecords(records)

    def adminMenuAction(self, actionId: str):
        if DEBUG:
            print("ImageManager.adminMenuAction:\t" + actionId)
        if actionId == "Configuration":
            if self.configurationDialog is None:
                self.configurationDialog = ConfigurationDialog(config={}, listener=self.messageReceiver)
                self.configurationDialog.setWindowTitle("Configuration")
            self.configurationDialog.show()

    def fileListSelectionEvent(self, listItem):
        if DEBUG:
            print("\nImageManager.fileListSelectionEvent:\t" + str(listItem.text()))
            print("\tcheckState:\t" + str(listItem.checkState() == Qt.CheckState.Checked))
        if listItem.checkState() == Qt.CheckState.Checked:
            self.fileCheckedList[listItem.text()]  = {}
        elif listItem.checkState() == Qt.CheckState.Unchecked:
            del(self.fileCheckedList[listItem.text()])
        if DEBUG:
            print("self.selectionList:\t" + str(self.fileCheckedList))

    def launchTextSelector(self):
        if DEBUG:
            print("ImageManager.launchTextSelector")
        hPos = 200
        yPos = 100
        for filePath in self.fileCheckedList:
            if filePath not in self.pixMapImages or self.pixMapImages[filePath] is None:
                #   self.loadImage(filePath)
                #   self.pixMapImages[filePath] = Image.open(filePath).toqpixmap()
                #   self.pixMapImages[filePath] = QPixmap(filePath)
                self.pixMapImages[filePath] = Scan.readImage(filePath)

            if filePath not in self.textSelectorMap:
                config = { 'topLeft': QPoint(hPos, yPos)}
                self.textSelectorMap[filePath] = TextSelector(identifier=filePath,
                                                              pixMapImage=self.pixMapImages[filePath],
                                                              imagePath=filePath, config=config,
                                                              listener=self.messageReceiver, parent=self)
                hPos += 50
                yPos += 50
            self.textSelectorMap[filePath].show()


class JobSelectionDialog(QDialog):

    DEFAULT_ID  = 'JobSelectionDialog'
    DEFAULT_CONFIG  = {}

    def __init__(self, identifier: str=None, config: dict=None, listener=None, parent=None):
        if identifier is None:
            self.identifier = JobSelectionDialog.DEFAULT_ID
        else:
            if not isinstance(identifier, str):
                raise Exception("JobSelectionDialog constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        if config is None:
            self.config = JobSelectionDialog.DEFAULT_CONFIG
        else:
            if not isinstance(config, dict):
                raise Exception("JobSelectionDialog constructor - Invalid config argument:  " + str(config))
            self.config = config
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(JobSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Job")

        if 'mode' in self.config and self.config['mode'] == 'select for run':
            self.setGeometry(QRect(600, 125, 300, 300))
        else:
            self.setGeometry(QRect(400, 75, 300, 300))

        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)

        self.currentSelection = None
        self.runMode = RunMode.SEQUENCE     #   The default

        #   Get Job table records from database, ...
        self.currentJobTable = AppDatabase.getJobTable()

        if 'mode' in self.config and self.config['mode'] == 'select for run':
            #    identifier: str=None,  text: str=None, config: dict=None, listener=None, parent=None
            labelRunMode = FieldLabel(identifier='labelRunMode', text='Run Mode:', listener=self.messageReceiver)
            labelRunMode.setMaximumWidth(100)
            labelRunMode.setAlignment(Qt.AlignRight)

            self.menuButtonRunMode = QPushButton("Run Mode")
            menuRunMode    = QMenu("Run Mode")
            self.menuButtonRunMode.setMenu(menuRunMode)
            self.actionSelectSequence   = QAction(text="Sequence", triggered=partial(self.setRunMode, RunMode.SEQUENCE))
            menuRunMode.addAction(self.actionSelectSequence)
            self.actionSelectBatch      = QAction(text="Batch", triggered=partial(self.setRunMode, RunMode.BATCH))
            menuRunMode.addAction(self.actionSelectBatch)

            self.menuButtonRunMode.setText(str(AppConfig.getJobsConfig()['DefaultRunMode']))

            batchModeHelpText = 'Batch mode can take a considerable amount of time on image file sets of ten or more.\n' \
                                'You can track progress in the console, and can select the items you want included below.'
            self.textEditBatchHelp = QTextEdit(parent=self)
            self.textEditBatchHelp.setText(batchModeHelpText)
            self.textEditBatchHelp.setReadOnly(True)
            self.textEditBatchHelp.setVisible(False)

            self.consoleOutConfigView = ConsoleOutConfigView(identifier='', listener=self.messageReceiver)
            self.consoleOutConfigView.setVisible(False)

        self.jobNameListView = \
            KeyListView(keyList=tuple(self.currentJobTable.keys()), config=None, identifier='jobNameListView',
                        listener=self.messageReceiver, parent=None)
        #   self.jobNameListView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.jobListModel = QStandardItemModel()
        self.jobListItemMap = OrderedDict()
        for jobName in self.currentJobTable.keys():
            self.jobListItemMap[jobName] = QStandardItem(jobName)
            #   self.listItemMap[year].setCheckable(True)
            self.jobListModel.appendRow(self.jobListItemMap[jobName])
        self.jobNameListView.setModel(self.jobListModel)

        buttonBar = QFrame(parent=self)
        buttonBar.setLayout(QHBoxLayout())
        buttonBar.setFrameStyle(QFrame.Panel | QFrame.Raised)
        buttonBar.setLineWidth(2)

        buttonSelect    = QPushButton('Select')
        buttonSelect.setMaximumWidth(100)
        textHelpSelect = 'Select the currently highlighted job'
        buttonSelect.setToolTip(textHelpSelect)
        buttonSelect.setStatusTip(textHelpSelect)
        buttonBar.layout().addWidget(buttonSelect)
        buttonSelect.clicked.connect(self.selectJob)

        buttonDetails   = QPushButton('Details')
        buttonDetails.setCheckable(True)
        buttonDetails.setMaximumWidth(100)
        textHelpDetails = 'View the details of the highlighted job'
        buttonDetails.setToolTip(textHelpDetails)
        buttonDetails.setStatusTip(textHelpDetails)
        buttonBar.layout().addWidget(buttonDetails)

        buttonCancel    = QPushButton('Cancel')
        buttonCancel.setMaximumWidth(100)
        textHelpCancel = 'Cancel job selection'
        buttonCancel.setToolTip(textHelpCancel)
        buttonCancel.setStatusTip(textHelpCancel)
        buttonCancel.clicked.connect(self.cancel)
        buttonBar.layout().addWidget(buttonCancel)

        self.gridLayout.addWidget(self.jobNameListView, 1, 0, 1, 2)
        self.gridLayout.addWidget(buttonBar, 2, 0, 1, 2)
        if 'mode' in self.config and self.config['mode'] == 'select for run':
            self.gridLayout.addWidget(labelRunMode, 0, 0, 1, 1)
            self.gridLayout.addWidget(self.menuButtonRunMode, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.textEditBatchHelp, 3, 0, 1, 2)
            self.gridLayout.addWidget(self.consoleOutConfigView, 4, 0, 1, 2)

    def getIdentifier(self):
        return self.identifier

    def getConfig(self):
        return self.config

    def getJobTable(self):
        return self.currentJobTable

    def getRunMode(self):
        return self.runMode

    def setRunMode(self, runMode: RunMode):
        if not isinstance(runMode, RunMode):
            return
        self.menuButtonRunMode.setText(str(runMode))
        self.textEditBatchHelp.setVisible(runMode == RunMode.BATCH)
        self.consoleOutConfigView.setVisible(runMode == RunMode.BATCH)
        if runMode == RunMode.SEQUENCE:
            self.setGeometry(QRect(600, 125, 300, 300))
        else:
            self.setGeometry(QRect(600, 125, 300, 500))
        self.runMode    = runMode

    def messageReceiver(self, message: dict):
        if not isinstance(message, dict):
            return
        if 'source' in message:
            #   {'source': 'KeyListView.selectionChanged', 'identifier': self.identifier, 'selection': selection}
            if message['source'] == 'KeyListView.selectionChanged':
                if 'identifier' in message and message['identifier'] == 'jobNameListView':
                    if 'selection' in message and isinstance(message['selection'], str):
                        self.currentSelection = message['selection']

    def selectJob(self):
        if self.currentSelection is None:
            messageDialog = QMessageBox(text="You must first select a job name in the list.\n")
            messageDialog.setWindowTitle("No Job Selected")
            messageDialog.setGeometry(QRect(450, 200, 500, 150))
            messageDialog.setStandardButtons(QMessageBox.Ok)
            messageDialog.exec()
            return
        if self.listener is not None:
            consoleOutputConfig = {}
            if self.runMode == RunMode.BATCH:
                consoleOutputConfig = self.consoleOutConfigView.getSettings()
            self.listener({'source': 'JobSelectionDialog.selectJob',
                           'selection': self.currentJobTable[self.currentSelection],
                           'runMode': self.runMode, 'consoleOutputConfig': consoleOutputConfig,
                           'identifier': self.identifier})

    def toggleJobDetails(self):
        pass

    def cancel(self):
        if self.listener is not None:
            self.listener({'source': 'JobSelectionDialog.cancel', 'identifier': self.identifier})


class ConsoleOutConfigView(QFrame):

    DEFAULT_ID      = 'ConsoleOutConfigView'
    DEFAULT_SETTINGS    = {
        'filePath': True,
        'times': True,
        'stats': False,
        'textExtracted': False
    }
    DEFAULT_CONFIG  = {}

    def __init__(self, identifier: str=None, initialSettings: dict=None, config: dict=None, listener=None, parent=None):
        if identifier is None:
            self.identifier = ConsoleOutConfigView.DEFAULT_ID
        elif isinstance(identifier, str):
            self.identifier = identifier
        else:
            raise Exception("ConsoleOutConfigView constructor - Invalid identifier argument:  " + str(identifier))
        if initialSettings is None:
            self.settings = ConsoleOutConfigView.DEFAULT_SETTINGS
        else:
            if not isinstance(initialSettings, dict):
                raise Exception("ConsoleOutConfigView constructor - Invalid initialSettings argument:  " + str(initialSettings))
            self.settings = deepcopy(initialSettings)
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("ConsoleOutConfigView constructor - Invalid config argument:  " + str(config))
            self.config = config
        else:
            self.config = ConsoleOutConfigView.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(ConsoleOutConfigView, self).__init__(parent)

        gridLayout = QGridLayout()
        self.setLayout(gridLayout)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(3)

        self.initialSettings = deepcopy(self.settings)

        labelTitle  = FieldLabel(identifier='labelTitle', text="Console Output", listener=self.messageReceiver)
        labelTitle.setAlignment(Qt.AlignCenter)
        labelTitle.setFrameStyle(QFrame.Panel | QFrame.Raised)
        labelTitle.setLineWidth(2)

        self.checkBoxFilePath    = QCheckBox("File Path")
        self.checkBoxTimes       = QCheckBox("Times and Durations")
        self.checkBoxStats       = QCheckBox("Statistics")
        self.checkBoxTextExtracted   = QCheckBox("Text Extracted")

        if 'buttonBar' in self.config and self.config['buttonBar']:
            buttonBar = QFrame(parent=self)
            buttonBar.setFrameStyle(QFrame.Panel | QFrame.Raised)
            buttonBar.setLineWidth(2)
            buttonBar.setLayout(QHBoxLayout())

            buttonCommit    = QPushButton("Commit")
            buttonCommit.setMaximumWidth(100)
            buttonCommit.setToolTip("Save settings")
            buttonCommit.clicked.connect(self.commit)
            buttonBar.layout().addWidget(buttonCommit)

            buttonCancel    = QPushButton("Cancel")
            buttonCancel.setMaximumWidth(100)
            buttonCancel.setToolTip("Reset to default settings")
            buttonCancel.clicked.connect(self.cancel)
            buttonBar.layout().addWidget(buttonCancel)

        gridLayout.addWidget(labelTitle)
        gridLayout.addWidget(self.checkBoxFilePath)
        gridLayout.addWidget(self.checkBoxTimes)
        gridLayout.addWidget(self.checkBoxStats)
        gridLayout.addWidget(self.checkBoxTextExtracted)
        if 'buttonBar' in self.config and self.config['buttonBar']:
            gridLayout.addWidget(buttonBar)

        self.setState(self.settings)

    def getSettings(self):
        return {
            'filePath': self.checkBoxFilePath.isChecked(),
            'times': self.checkBoxTimes.isChecked(),
            'stats': self.checkBoxStats.isChecked(),
            'textExtracted': self.checkBoxTextExtracted.isChecked()
        }

    def setState(self, settings: dict):
        if not isinstance(settings, dict):
            return
        if 'filePath' in settings:
            self.checkBoxFilePath.setChecked(settings['filePath'])
        if 'times' in settings:
            self.checkBoxTimes.setChecked(settings['times'])
        if 'stats' in settings:
            self.checkBoxStats.setChecked(settings['stats'])
        if 'textExtracted' in settings:
            self.checkBoxTextExtracted.setChecked(settings['textExtracted'])
        self.settings = deepcopy(settings)

    def messageReceiver(self, message: dict):
        if not isinstance(message, dict):
            return
        if 'source' in message:
            pass

    def commit(self):
        pass

    def cancel(self):
        self.setState(self.initialSettings)


class JobDefinitionView(QMainWindow):
    """
    History option can include the activity log for use of this dialog to design and manage Jobs, i.e. when and who
    entered it initially and any changes made during its life.
    """

    DEFAULT_ID      = 'JobDefinitionView'
    DEFAULT_CONFIG  = {}
    DEFAULT_TITLE   = 'Job Definition'

    def __init__(self, job: Job, identifier: str=None, config: dict=None, listener=None, parent=None):
        if not isinstance(job, Job):
            raise Exception("JobDefinitionView constructor - Invalid job argument:  " + str(job))
        if identifier is None:
            self.identifier = JobDefinitionView.DEFAULT_ID
        elif isinstance(identifier, str):
            self.identifier = identifier
        else:
            raise Exception("JobDefinitionView constructor - Invalid identifier argument:  " + str(identifier))
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("JobDefinitionView constructor - Invalid config argument:  " + str(config))
            self.config = config
        else:
            self.config = JobDefinitionView.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(JobDefinitionView, self).__init__(parent)
        self.setWindowTitle(JobDefinitionView.DEFAULT_TITLE)
        self.mostRecentFileSequence = None
        self.mostRecentJob = None

        self.currentJob = job
        self.currentRootFolder  = environ['HOME']
        self.currentPathSelection = None

        self.fileMultiSelector  = None
        self.popupViewJobSelect = None

        self.initMenuBar()
        self.addToolBar(self.buildToolBar())
        statusBar = QStatusBar()
        self.setStatusBar(statusBar)
        self.addToolBar(self.buildButtonBar())

        contentPane = QFrame(parent=self)
        self.setCentralWidget(contentPane)

        gridLayout = QGridLayout()
        contentPane.setLayout(gridLayout)

        labelJobName    = FieldLabel(identifier='labelJobName', text="Job Name:", parent=contentPane)
        labelJobName.setAlignment(Qt.AlignRight)
        labelJobName.setMinimumWidth(100)
        self.editorJobName = EditorLine(config=None, initialText='', identifier='editorJobName', validator=None,
                                        listener=self.messageReceiver)
        #   editorJobName.setText("Enter the name of this job")
        self.editorJobName.setToolTip("Enter the name of this job")
        self.editorJobName.setMinimumWidth(250)

        labelJobType    = FieldLabel(identifier='labelJobType', text="Job Type:", parent=contentPane)
        labelJobType.setAlignment(Qt.AlignRight)
        labelJobType.setMinimumWidth(100)
        self.editorJobType   = EditorLine(config=None, initialText='', identifier='editorJobType', validator=None,
                                          listener=self.messageReceiver)
        #   editorJobType.setText("Enter the job type")
        self.editorJobType.setToolTip("Enter the job type")
        self.editorJobType.setMinimumWidth(150)

        #   keyList:tuple, config: dict=None, identifier: str=None, listener=None, parent=None
        pathList = tuple(self.currentJob.getFileCollection().getFilePathMap().keys())
        self.pathListView = KeyListView(keyList=pathList, config={}, identifier='pathList', listener=self.messageReceiver)
        self.pathListView.setStatusTip("This is the list of folders and files which are included in the Job.\n"
                                       "The contents of folders are included as scanned.")
        self.refreshListView()

        sideButtonBar = self.buildSideButtonBar()

        buttonSave      = QPushButton("Save")
        buttonSave.setMaximumWidth(100)
        helpTextSave    = 'Save this job definition'
        buttonSave.setToolTip(helpTextSave)
        buttonSave.setStatusTip(helpTextSave)
        buttonSave.clicked.connect(lambda: self.saveJob())

        buttonExit    = QPushButton("Exit")
        buttonExit.setMaximumWidth(100)
        helpTextExit     = "Exit dialog; does not save job definition"
        buttonExit.setToolTip(helpTextExit)
        buttonExit.setStatusTip(helpTextExit)
        buttonExit.clicked.connect(lambda: self.exitDialog())

        gridLayout.addWidget(labelJobName, 0, 0, 1, 1)
        gridLayout.addWidget(self.editorJobName, 0, 1, 1, 2)
        gridLayout.addWidget(labelJobType, 0, 3, 1, 1)
        gridLayout.addWidget(self.editorJobType, 0, 4, 1, 2)
        gridLayout.addWidget(self.pathListView, 1, 0, 10, 5)
        gridLayout.addWidget(sideButtonBar, 1, 5, 10, 1)
        gridLayout.addWidget(buttonExit, 11, 3, 1, 1)
        gridLayout.addWidget(buttonSave, 11, 4, 1, 1)

    def getCurrentJob(self):
        return self.currentJob

    def getIdentifier(self):
        return self.identifier

    def refreshListView(self):
        pathList = tuple(self.currentJob.getFileCollection().getFilePathMap().keys())
        self.pathListModel = QStandardItemModel()
        self.pathListItemMap = OrderedDict()
        for pathName in pathList:
            self.pathListItemMap[pathName] = QStandardItem(pathName)
            #   self.listItemMap[year].setCheckable(True)
            self.pathListModel.appendRow(self.pathListItemMap[pathName])
        self.pathListView.setModel(self.pathListModel)

    def messageReceiver(self, message: dict):
        if not isinstance(message, dict):
            return
        if 'source' in message:

            #   {'source': 'KeyListView.mousePressEvent', 'action': 'selection', 'point': event.pos(),
            #       'selectionText': self.currentKey, 'multiSelect': len(selectedItems) > 1,
            #       'selectionList': selectedItems, 'button': event.button(),
            #       'row': selectionIdx.row(), 'identifier': self.identifier}
            if message['source'] == 'KeyListView.mousePressEvent':
                if 'action' in message and isinstance(message['action'], str):
                    if message['action'] == 'selection':
                        pass

            #   {'source': 'KeyListView.selectionChanged', 'identifier': self.identifier, 'selection': selection}
            elif message['source'] == 'KeyListView.selectionChanged':
                if 'identifier' in message and message['identifier'] == 'pathList':
                    if 'selection' in message and isinstance(message['selection'], str):
                        self.currentPathSelection = message['selection']

            #   {'source': 'FileViewFrame.setSelection', 'selected': self.currentSelections}
            elif message['source'] == 'FileViewFrame.setSelection':
                if 'identifier' in message and message['identifier'] == 'fileMultiSelector':
                    if 'selected' in message and isinstance(message['selected'], tuple):
                        selections = message['selected']
                        for pathName in selections:


                            if isfile(pathName):
                                #   Not already present in the list?
                                if pathName not in self.currentJob.getFileCollection().getFilePathMap():
                                    #   Check to see if it is QImageReader compatible
                                    fileName = pathName.split('/')[-1]
                                    fileNameParts = fileName.split('.')
                                    if len(fileNameParts) > 1 and fileNameParts[-1] in QT5_IMAGE_FILE_EXTS:
                                        self.currentJob.getFileCollection().addFile(pathName)

                            elif isdir(pathName):
                                #   Include only those files that are QImageReader compatible
                                #   If none present, message user and do not include folder in list
                                #   Folder popup menu item: "Show Image Files"
                                compatibleImageFiles = []

                                scanType = ScanType.WALK if self.buttonFolderScanMode.text() == 'Walk' else ScanType.LIST
                                if scanType == ScanType.LIST:
                                    fileList = listdir(pathName)
                                    for fileName in fileList:
                                        fileNameParts = fileName.split('.')
                                        if len(fileNameParts) > 1 and fileNameParts[-1] in QT5_IMAGE_FILE_EXTS:
                                            compatibleImageFiles.append(pathName + '/' + fileName)
                                else:
                                    for dirName, subdirList, fileList in walk(pathName):
                                        if islink(dirName):
                                            continue
                                        for fileName in fileList:
                                            filePath = dirName + '/' + fileName
                                            if not isfile(filePath):
                                                continue
                                            fileNameParts = fileName.split('.')
                                            if len(fileNameParts) > 1 and fileNameParts[-1] in QT5_IMAGE_FILE_EXTS:
                                                compatibleImageFiles.append(filePath)

                                if len(compatibleImageFiles) > 0:
                                    self.currentJob.getFileCollection().addFolder(pathName, tuple(compatibleImageFiles),
                                                                                  scanType, force=True)
                        self.refreshListView()

                        self.fileMultiSelector.close()
                        self.fileMultiSelector = None

            #   {'source': "FileViewFrame.closeFrame"}
            elif message['source'] == 'FileViewFrame.closeFrame':
                self.fileMultiSelector.close()
                self.fileMultiSelector = None

            #   {'source': 'JobSelectionDialog.cancel', 'identifier': self.identifier}
            elif message['source'] == 'JobSelectionDialog.cancel':
                if 'identifier' in message and isinstance(message['identifier'], str):
                    if message['identifier'] == 'popupViewJobSelect':
                        self.popupViewJobSelect.close()
                        self.popupViewJobSelect = None

            #   {'source': 'JobSelectionDialog.selectJob', 'selection': self.currentJobTable[self.currentSelection],
            #           'identifier': self.identifier}
            elif message['source'] == 'JobSelectionDialog.selectJob':
                if 'identifier' in message and isinstance(message['identifier'], str):
                    if message['identifier'] == 'popupViewJobSelect':
                        if 'selection' in message and isinstance(message['selection'], dict):
                            #   Format database return structure to local format for interface with view:
                            selection = {
                                'jobName': message['selection']['JobName'],
                                'jobType': message['selection']['Config']['jobType'],
                                'pathMap': message['selection']['FileSequence'].getFilePathMap()
                            }

                            self.currentJob = Job(FileCollectionOrdered(selection['jobName'], selection['pathMap']),
                                                  selection['jobName'], message['selection']['Config'])

                            self.setState(selection)
                        self.popupViewJobSelect.close()
                        self.popupViewJobSelect = None

            #   {'source': 'EditorLine.focusOutEvent', 'identifier': self.identifier, 'newValue': self.text()}
            elif message['source'] == 'EditorLine.focusOutEvent':
                if 'identifier' in message and isinstance(message['identifier'], str):
                    if message['identifier'] == 'editorJobName':
                        self.currentJob.setIdentifier(self.editorJobName.text())
                    elif message['identifier'] == 'editorJobType':
                        self.currentJob.setJobType(self.editorJobType.text())

    def initMenuBar(self):
        menu = self.menuBar()

        menuJobs = menu.addMenu("Jobs")
        #   Select, Manage, History, Exit
        actionSelectJob = QAction("&Select", self, shortcut="Ctrl+S", triggered=partial(self.menuAction, "Select"))
        actionSelectJob.setStatusTip("Select a job to edit, run, view run log and stats, ...")
        menuJobs.addAction(actionSelectJob)

        #   Planned for future release:
        """
        actionManageJob = QAction("&Manage", self, shortcut="Ctrl+M", triggered=partial(self.menuAction, "Manage"))
        actionManageJob.setStatusTip("Manage defined jobs")
        menuJobs.addAction(actionManageJob)
        """
        """
        actionJobHistory = QAction("&History", self, shortcut="Ctrl+H", triggered=partial(self.menuAction, "History"))
        actionJobHistory.setStatusTip("Job activity history generally, including definition, edits, and runs")
        menuJobs.addAction(actionJobHistory)
        """

        actionExit = QAction("&Exit", self, shortcut="Ctrl+E", triggered=partial(self.menuAction, "Exit"))
        actionExit.setStatusTip("Exit this dialog")
        menuJobs.addAction(actionExit)

        menuFiles   = menu.addMenu('Files')

        actionAddFiles  = QAction("Add", self, triggered=partial(self.menuAction, "Add Files"))
        actionAddFiles.setStatusTip("Add one or more files to the list of files to process when job is launched")
        menuFiles.addAction(actionAddFiles)

    def buildToolBar(self):
        toolBar = QToolBar(parent=self)

        toolFileFolder = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/address-book.png'), 'Address', toolBar)
        toolFileFolder.triggered.connect(partial(self.menuAction, "Add Files"))
        #   actionAnalysisLocate.setCheckable(True)
        toolFileFolder.setToolTip("Add one or more files to the list of files to process when job is launched")
        toolFileFolder.setStatusTip("Add one or more files to the list of files to process when job is launched")
        toolBar.addAction(toolFileFolder)

        self.toolAsterisk = QAction(QIcon(TOOLBAR_ICON_FOLDER + '/asterisk.png'), 'Select All', toolBar)
        self.toolAsterisk.triggered.connect(lambda: self.toolBarAction('Select All'))
        self.toolAsterisk.setCheckable(True)
        self.toolAsterisk.setToolTip("Toggle selection of all files / folders in the current Job's list")
        self.toolAsterisk.setStatusTip("Toggle selection of all files / folders in the current Job's list")
        toolBar.addAction(self.toolAsterisk)

        return toolBar

    def buildButtonBar(self):
        buttonBar = QToolBar()

        buttonSelectFolder = QPushButton("Add Files")
        helpTextNewJob = "Add one or more files or folder contents to the list of files to process when job is launched"
        buttonSelectFolder.setToolTip(helpTextNewJob)
        buttonSelectFolder.setStatusTip(helpTextNewJob)
        buttonSelectFolder.clicked.connect(lambda: self.menuAction('Add Files'))
        buttonBar.addWidget(buttonSelectFolder)

        buttonNewJob = QPushButton("New Job")
        helpTextNewJob = "Clear all fields to start a new job definition"
        buttonNewJob.setToolTip(helpTextNewJob)
        buttonNewJob.setStatusTip(helpTextNewJob)
        buttonNewJob.clicked.connect(lambda: self.buttonBarAction('New Job'))
        buttonBar.addWidget(buttonNewJob)

        labelScanMode   = QLabel('     Scan Mode: ')
        labelScanMode.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        labelScanMode.setMaximumWidth(125)
        buttonBar.addWidget(labelScanMode)

        self.buttonFolderScanMode    = QPushButton('Scan Mode')
        if AppConfig.getJobsConfig()['DefaultFolderScanMode'] == ScanType.WALK:
            self.buttonFolderScanMode.setText('Walk')
        elif AppConfig.getJobsConfig()['DefaultFolderScanMode'] == ScanType.LIST:
            self.buttonFolderScanMode.setText('List')
        helpTextScanMode = "Set the mode of scanning a folder for image files: List for the folder only, Walk for all folders under it"
        self.buttonFolderScanMode.setToolTip(helpTextScanMode)
        self.buttonFolderScanMode.setStatusTip(helpTextScanMode)
        menuScanMode = QMenu('Scan Mode')
        menuScanMode.addAction(QAction(text="List", parent=self.buttonFolderScanMode, triggered=partial(self.setScanMode, 'List')))
        menuScanMode.addAction(QAction(text="Walk", parent=self.buttonFolderScanMode, triggered=partial(self.setScanMode, 'Walk')))
        self.buttonFolderScanMode.setMenu(menuScanMode)
        buttonBar.addWidget(self.buttonFolderScanMode)

        return buttonBar

    def setScanMode(self, scanModeId: str):
        self.buttonFolderScanMode.setText(scanModeId)

    def buildSideButtonBar(self):
        buttonBar   = QFrame()
        buttonBar.setLayout(QVBoxLayout())

        buttonMoveUp    = QPushButton("Move Up")
        buttonMoveUp.setToolTip("Move the selected file or folder up one position in order")
        buttonMoveUp.setStatusTip("Move the selected file or folder up one position in order")
        buttonMoveUp.clicked.connect(lambda: self.buttonBarAction('Move Up'))
        buttonBar.layout().addWidget(buttonMoveUp)

        buttonMoveDown  = QPushButton("Move Down")
        buttonMoveDown.setToolTip("Move the selected file or folder down one position in order")
        buttonMoveDown.setStatusTip("Move the selected file or folder down one position in order")
        buttonMoveDown.clicked.connect(lambda: self.buttonBarAction('Move Down'))
        buttonBar.layout().addWidget(buttonMoveDown)

        buttonDelete    = QPushButton("Delete")
        buttonDelete.setToolTip("Delete the selected file or folder from the list")
        buttonDelete.setStatusTip("Delete the selected file or folder from the list")
        buttonDelete.clicked.connect(lambda: self.buttonBarAction('Delete'))
        buttonBar.layout().addWidget(buttonDelete)

        return buttonBar

    def menuAction(self, actionId: str):
        if not isinstance(actionId, str):
            return
        if actionId == 'Select':
            if self.popupViewJobSelect is None:
                self.popupViewJobSelect = JobSelectionDialog(identifier='popupViewJobSelect',
                                                             listener=self.messageReceiver)
            self.popupViewJobSelect.show()
        elif actionId == 'Exit':
            if self.listener is not None:
                self.listener({'source': 'JobDefinitionView.menuAction', 'actionId': actionId})
        elif actionId == 'Add Files':
            self.fileMultiSelector = FileDialog(identifier='fileMultiSelector',
                                                initialFolder=self.currentRootFolder, config={'selectionMode': 'extended'},
                                                listener=self.messageReceiver, parent=None)
            self.fileMultiSelector.setGeometry(QRect(300, 200, 550, 450))
            self.fileMultiSelector.exec()


    def toolBarAction(self, actionId: str):
        if not isinstance(actionId, str):
            return
        """
        "Select All" can be used for two operations:
            Deleting all from the list
            Clicking 'New' copies the list to a new Job Definition with blank name and type.
                When the user has saved the current new or edited job definition they can then
                use the list as a template in a new job definition which will be saved under a
                new name.
                If, for instance, they want to do a batch extraction of all text in every file but also
                want to do a sequence of clippings from each file, they do not have to re-select a large
                list correctly to accomplish this.
        """
        if actionId == 'Select All':
            print("toolBarAction:\t" + actionId)

            row = 0
            model = self.pathListView.selectionModel()
            if self.toolAsterisk.isChecked():
                for pathName in self.pathListItemMap:
                    #   self.listItemMap[filePath].setCheckState(True)
                    #   self.listItemMap[filePath].checkState().Checked = Qt.CheckState.Checked
                    index   = self.pathListModel.index(row, 0)
                    model.select(index, QItemSelectionModel.Select)
                    row += 1
            else:
                for pathName in self.pathListItemMap:
                    index   = self.pathListModel.index(row, 0)
                    model.select(index, QItemSelectionModel.Deselect)
                    row += 1


    def buttonBarAction(self, actionId: str):
        if not isinstance(actionId, str):
            return
        if actionId == 'Move Up':
            if self.currentPathSelection is None:
                self.showSelectFirstMessage()
            else:
                currentLoc = list(self.currentJob.getFileCollection().getFilePathMap().keys()).index(self.currentPathSelection)
                if currentLoc > 0:
                    if self.currentJob.getFileCollection().moveEntry(self.currentPathSelection, currentLoc-1):
                        self.refreshListView()

        elif actionId == 'Move Down':
            if self.currentPathSelection is None:
                self.showSelectFirstMessage()
            else:
                keyList = list(self.currentJob.getFileCollection().getFilePathMap().keys())
                currentLoc = keyList.index(self.currentPathSelection)
                if currentLoc < len(keyList):
                    if self.currentJob.getFileCollection().moveEntry(self.currentPathSelection, currentLoc+1):
                        self.refreshListView()

        elif actionId == 'Delete':
            if self.currentPathSelection is None:
                self.showSelectFirstMessage()
            else:
                self.currentJob.getFileCollection().removeFolder(self.currentPathSelection)
                #   redisplay
                self.refreshListView()

        elif actionId == 'New Job':
            self.clearFields()
        """
        elif actionId == 'Add Files':
            self.fileMultiSelector = FileDialog(identifier='fileMultiSelector',
                                                initialFolder=self.currentRootFolder, config={},
                                                listener=self.messageReceiver, parent=None)
            self.fileMultiSelector.setGeometry(QRect(300, 200, 550, 450))
            self.fileMultiSelector.exec()
        """

    def clearFields(self):
        self.editorJobName.setText('')
        self.editorJobType.setText('')
        self.pathListModel = QStandardItemModel()
        self.pathListItemMap = OrderedDict()
        self.pathListView.setModel(self.pathListModel)
        self.currentJob     = Job()


    def getState(self):
        return {
            'jobName': self.editorJobName.text(),
            'jobType': self.editorJobType.text(),
            'pathMap': self.filePathMap
        }

    def setState(self, state: dict):
        if not isinstance(state, dict):
            return
        if 'jobName' in state and isinstance(state['jobName'], str):
            self.editorJobName.setText(state['jobName'])
        if 'jobType' in state and isinstance(state['jobType'], str):
            self.editorJobType.setText(state['jobType'])
        if 'pathMap' in state and isinstance(state['pathMap'], dict):
            self.pathListModel = QStandardItemModel()
            self.pathListItemMap = OrderedDict()
            for pathName in state['pathMap']:
                self.pathListItemMap[pathName] = QStandardItem(pathName)
                #   self.listItemMap[year].setCheckable(True)
                self.pathListModel.appendRow(self.pathListItemMap[pathName])
            self.pathListView.setModel(self.pathListModel)

    def getEntryErrors(self):
        return {
            'jobName'   : self.currentJob.getIdentifier().strip() == '',
            'fileList': len(self.currentJob.getFileCollection().getFilePathMap()) == 0,
        }

    def saveJob(self):
        #   self.currentJob
        #   currentDefinition = self.getState()

        dataEntryErrors = self.getEntryErrors()
        if dataEntryErrors['jobName'] or dataEntryErrors['fileList']:
            errorMessages = ''
            if dataEntryErrors['jobName']:
                errorMessages += 'The job name is invalid\n'
            if dataEntryErrors['fileList']:
                errorMessages += 'The file list is empty\n'
            messageDialog = QMessageBox(text="Invalid Entry in Job Definition.\n\n" + errorMessages + '\n' +
                                             "Launch the Help dialog for details.\n")
            messageDialog.setWindowTitle("Invalid Entry")
            messageDialog.setGeometry(QRect(450, 200, 500, 150))
            messageDialog.setStandardButtons(QMessageBox.Ok)
            messageDialog.exec()
            return

        AppDatabase.saveJobDefinition(self.currentJob)

        if self.listener is not None:
            self.listener({'source': 'JobDefinitionView.saveJob'})

    def exitDialog(self):
        if self.listener is not None:
            self.listener({'source': 'JobDefinitionView.exitDialog'})

    def showSelectFirstMessage(self):
        messageDialog = QMessageBox(text="You must first select an item from the list.\n")
        messageDialog.setWindowTitle("No Selection Made")
        messageDialog.setGeometry(QRect(450, 200, 500, 150))
        messageDialog.setStandardButtons(QMessageBox.Ok)
        messageDialog.exec()
        return


def messageReceiver(message: dict):
    if not isinstance(message, dict):
        return
    if 'source' in message:
        #   {'source': 'SelectedTextDialog.cancelClicked'}
        if message['source'] == 'SelectedTextDialog.cancelClicked':
            app.exit()
        #   {'source': 'SelectedTextDialog.nextClicked'}
        elif message['source'] == 'SelectedTextDialog.nextClicked':
            app.exit()
        #   {'source': 'ImageManager.toolBarAction', 'actionId': actionId}
        elif message['source'] == 'ImageManager.toolBarAction':
            if 'actionId' in message and message['actionId'] == "Exit":
                app.exit()


if __name__ == "__main__":
    print("Running:\t" + MODULE_NAME)
    #   guiApp = QGuiApplication(argv)
    app = QApplication(argv)
    #   selectedTextDialog = SelectedTextDialog(identifier="", text='Extracted text to store and bill for', config={},
    #                                           listener=messageReceiver)
    #   selectedTextDialog.show()

    AppDatabase.initializeDatabase()

    compatibility = 'PixMap'
    currentImageFolder = AppConfig._defaultImageFolder

    imageManager = ImageManager(config={'imageFileFolder': currentImageFolder,
                                             'scanType': ScanType.LIST,
                                             'extSet': compatibility},
                                displayDimensions={'width': app.primaryScreen().size().width(),
                                                   'height': app.primaryScreen().size().height()},
                                listener=messageReceiver)
    imageManager.setGeometry(QRect(100,100,800,500))
    imageManager.show()

    app.exec()