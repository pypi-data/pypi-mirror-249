#   Project:        EvidenceExplorer
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   Copyright:      (c) Copyright 2022 George Keith Watson
#   Module:         view.Help.py
#   Date Started:   December 20, 2022
#   Purpose:        Dialog for help specific to the subject matter and work flows involved in use of the
#                   Evidence Explorer application.
#   Development:
#

from sys import argv
from os.path import isfile
from collections import OrderedDict

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont, QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFrame, QGridLayout, QTextEdit

from model.HelpContent import HelpText
from model.Installation import HELP_DOCS_FOLDER, HELP_ABOUT_FILE, HELP_QUICK_START_FILE, HELP_FILES_MENU_FILE, \
                            HELP_RUN_MENU_FILE, HELP_VIEW_MENU_FILE, HELP_ADMIN_MENU_FILE
from view.QtAppComponents import TabbedView

MODULE_NAME     = "PictureTextCrop Help"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONDOLE_OUTPUT  = False


class HelpDialog(QMainWindow):

    DEFAULT_TITLE   = "General Help"
    DEFAULT_CONFIG  = {
        'helpTopics': {
            'About': HELP_DOCS_FOLDER + '/' + HELP_ABOUT_FILE,
        },
        'dialogHelp':   {
            HelpText.FolderIndexAndArchive.value[2]:  HelpText.FolderIndexAndArchive.value[1],
            HelpText.FolderArchiveAndIndex.value[2]: HelpText.FolderArchiveAndIndex.value[1],
            HelpText.VerifyFolderWithIndex.value[2]: HelpText.VerifyFolderWithIndex.value[1]
        }
    }

    def __init__(self, config: dict=None, dispatcher=None, listener=None, parent=None):
        if isinstance(config, dict) and 'helpTopics' in config:
            self.config = config
        else:
            self.config = HelpDialog.DEFAULT_CONFIG
        if dispatcher is not None and callable(dispatcher):
            self.dispatcher = dispatcher
        else:
            self.dispatcher = None
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(HelpDialog, self).__init__(parent=parent)

        if 'title' in self.config:
            self.setWindowTitle(self.config['title'])
        else:
            self.setWindowTitle(HelpDialog.DEFAULT_TITLE)

        self.contentFrame = QFrame(self)
        self.contentLayout    = QGridLayout()
        self.contentFrame.setLayout(self.contentLayout)
        self.setCentralWidget(self.contentFrame)

        self.tabIndexMap = OrderedDict()
        self.viewFrames = OrderedDict()
        self.helpNotebook = TabbedView(listener=self.messageReceiver, parent=self)
        self.helpNotebook.setStatusTip("PictureTextCrop Help / Instructions for Use")

        self.htmlViewMap = OrderedDict()
        self.textEditMap = OrderedDict()

        if 'helpTopics' in self.config:
            for topic, htmlFile in self.config['helpTopics'].items():
                if isinstance(htmlFile, str) and isfile(htmlFile):
                    textFile = open(htmlFile, 'r')
                    htmlText = textFile.read()
                    textFile.close()
                    self.textEditMap[topic] = QTextEdit(parent=self.contentFrame)
                    #   self.textEditMap[topic].setStatusTip("About the Evidence Explorer Application")
                    self.textEditMap[topic].setMinimumHeight(85)
                    self.textEditMap[topic].setText(htmlText)
                    self.textEditMap[topic].setFont(QFont('Sanserif', 10))
                    self.textEditMap[topic].setReadOnly(True)
                    self.tabIndexMap[self.textEditMap[topic]] = self.helpNotebook.addTab(self.textEditMap[topic], topic)
                    self.viewFrames[topic] = self.textEditMap[topic]

        if 'dialogHelp' in self.config:
            for topic, text in self.config['dialogHelp'].items():
                self.textEditMap[topic] = QTextEdit(parent=self.contentFrame)
                self.textEditMap[topic].setMinimumHeight(85)
                self.textEditMap[topic].setText(text)
                self.textEditMap[topic].setFont(QFont('Sanserif', 10))
                self.textEditMap[topic].setReadOnly(True)
                self.tabIndexMap[self.textEditMap[topic]] = self.helpNotebook.addTab(self.textEditMap[topic], topic)
                self.viewFrames[topic] = self.textEditMap[topic]
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.contentLayout.addWidget(self.helpNotebook, 0, 0, 1, 1)

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

    def messageReceiver(self, message: dict):
        if DEBUG:
            print("EvidenceHelpDialog.messageReceiver:\t" + str(message))
        if not isinstance(message, dict):
            return

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.listener is not None:
            self.listener({'source': 'EvidenceHelpDialog.closeEvent'})


if __name__ == "__main__":
    print("Running:\t" + MODULE_NAME)

