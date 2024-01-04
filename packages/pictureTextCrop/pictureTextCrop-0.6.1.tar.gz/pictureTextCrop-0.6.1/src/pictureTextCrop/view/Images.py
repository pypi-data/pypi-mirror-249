#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           Images.py
#   Language:       Python 3.0+
#   Copyright:      Copyright 2022 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#

from sys import argv, stderr
from os import listdir, stat, environ, walk
from os.path import isfile, isdir, islink
from collections import OrderedDict
from datetime import datetime
from pickle import dumps as convertToBytes
from sqlite3 import connect, Binary
from pickle import loads as convertFromBinary


from PIL import Image
#   from PIL import ImageQt
#   Error:  Cannot mix incompatible Qt library (6.3.2) with this library (6.3.1)
import pytesseract

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QCoreApplication, Qt, QRect, QSize, QPoint
from PySide6.QtGui import QAction, QStandardItemModel, QStandardItem, QPixmap, QCloseEvent, QImage, QMouseEvent, \
    QPainter, QFont, QPen, QResizeEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QPushButton, QListView, QGridLayout, QLabel, \
    QScrollArea, QWidget, QDialog, QMenu, QHBoxLayout, QStatusBar, QFrame

from model.Installation import TEXT_EXTRACTION_DB_FILE
from model.Exif import PhotoFolder

MODULE_NAME    = "Images"
INSTALLING      = False
TESTING         = True
DEBUG           = False

IMAGE_PIXMAP_EXTS = ('bmp', 'gif', 'jpeg', 'jpg', 'pbm', 'pgm', 'png', 'ppm', 'xbm', 'xpm')
PillowFileExtensions = ('ALL', 'apng', 'blp', 'blp1', 'blp2', 'bmp', 'dds', 'dib', 'dxt1', 'dxt3', 'dxt5', 'eps',
                        'gif', 'icns', 'ico', 'im', 'jfif', 'jpeg', 'jpg', 'msp', 'pbm', 'pcx', 'pgm', 'png',
                        'pnm', 'ppm', 'sgi', 'spi', 'tga', 'tiff', 'webp', 'xbm')

class PixMapLabel(QLabel):

    def __init__(self, pixMapImage, imageFilePath, parent=None):
        super(PixMapLabel, self).__init__(parent=parent)
        self.pixmap = pixMapImage
        self.imageFilePath = imageFilePath
        pilImage = Image.fromqpixmap(self.pixmap)
        if DEBUG:
            pilImage.show()

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
        if TESTING:
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
        image = clippedPixMap.toImage()
        PilImage = Image.fromqimage(image)
        #   PilImage.show(title="Cropped Image")
        text = pytesseract.image_to_string(PilImage)
        if TESTING:
            print("\nExtracted Text:\t" + text)

        #   Log to DB:
        timeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        filePath = self.imageFilePath
        coordinates = convertToBytes({ "startX": startX,
                        "endX": endX,
                        'startY': startY,
                        'endY': endY,
                        'pixMapProps': self.pixMapProps,
                        'scaledPixmapProps': self.scaledPixmapProps })
        connection = connect(TEXT_EXTRACTION_DB_FILE)
        connection.cursor().execute("""INSERT INTO CropLog (timeStamp, filePath, coordinates, text)
                                        values(?, ?, ?, ?)""",
                                    (timeStamp, filePath, Binary(coordinates), text))
        connection.commit()
        connection.close()
        self.startPos = None
        self.endPos = None
        self.endingDraw = True
        self.update()


class TextSelector(QMainWindow):

    DEFAULT_CONFIG  = {}

    def __init__(self, pixMapImage, imagePath,  config: dict=None, listener=None, parent=None):
        self.listener = None
        if listener is not None and callable(listener):
            self.listener = listener
        if isinstance(config, dict):
            self.config = config
        else:
            self.config = TextSelector.DEFAULT_CONFIG
        super(TextSelector, self).__init__(parent)
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
        self.label = PixMapLabel(self.pixMapImage, self.imageFilePath, parent=self)

        #   self.label.setPixmap(self.imageMap[self.imageFilePath])
        self.scroller.setWidget(self.label)

        self.setCentralWidget(self.scroller)
        #   self.resize(pixmap.width(), pixmap.height())
        pixMapProps = self.label.getScaledPixMapProps()
        #   self.setGeometry(QRect(QPoint(200, 100), QPoint(200+pixMapProps['width'], 100+pixMapProps['height'])))
        self.setGeometry(QRect(QPoint(200, 100), QPoint(900, 600)))


    def getImageFileName(self):
        return self.imageFileName

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.listener is not None:
            self.listener({'source': "TextSelector.closeEvent", 'action': 'close requested', 'fileName': self.imageFileName })


class FileListView(QListView):
    """
    This needs to display a scaled image or thumbnail on the right when an image is made the current one.
    It should also have the option of displaying a thumbnail as an icon for each list item.
    """

    def __init__(self, imageMap=None, config: dict=None, listener=None, parent=None):
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(FileListView, self).__init__(parent)
        self.imageMap = imageMap
        self.config = config
        self.currSelectionIdx = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(FileListView, self).mousePressEvent(event)
        if DEBUG:
            print("FileListView.mousePressEvent:\t" + str(event))
        #   Popup menu if right click
        selectionIdx = self.indexAt(event.pos())
        if selectionIdx is not None:
            #   self.currentImageFileName = self.projectListModel.item(row, col).text()
            selectedItem = self.model().item(selectionIdx.row(), selectionIdx.column())
            if selectedItem is not None:
                self.currSelectionIdx = selectionIdx
                self.currentImageFileName = selectedItem.text()
                if self.listener is not None:
                    self.listener({'source': 'FileListView.mousePressEvent',
                                   'selectionText': self.currentImageFileName,
                                   'listType': 'walk'})


    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super(FileListView, self).mouseReleaseEvent(event)
        if DEBUG:
            print("FileListView.mouseReleaseEvent:\t" + str(event))
        #   Popup menu if right click

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super(FileListView, self).mouseDoubleClickEvent(event)
        if DEBUG:
            print("FileListView.mouseDoubleClickEvent:\t" + str(event))


class ImageManager(QMainWindow):

    DEFAULT_CONFIG = {'imageFileFolder': environ['HOME'], 'scanType': 'walk', 'extSet': 'Pillow'}

    def __init__(self, config: dict=None, listener=None, parent=None):
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        if isinstance(config, dict):
            self.config = config
        else:
            self.config = ImageManager.DEFAULT_CONFIG
        if 'extSet' in config:
            self.extSet = config['extSet']
        else:
            self.extSet = 'Pillow'
        super(ImageManager, self).__init__(parent)
        #   self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.contentFrame = QFrame(parent=self)
        self.contentGridLayout = QGridLayout()
        self.contentFrame.setLayout(self.contentGridLayout)

        self.pixMapImages = OrderedDict()
        self.textSelectors = OrderedDict()
        self.imageFolder = None
        self.selImgFilePath = None
        self.selPixMap = None

        if 'imageFileFolder' in self.config and isdir(self.config['imageFileFolder']):
            self.imageFolder = self.config['imageFileFolder']
            self.scanType = 'list'
            if 'scanType' in self.config:
                self.scanType   = self.config['scanType']
            if self.scanType == 'list':
                self.listFolder()
            elif self.scanType == 'walk':
                self.walkFolder()

        self.setStatusBar(QStatusBar())

        self.mainToolBar = QToolBar()
        self.addToolBar(self.mainToolBar)

        self.buttonImageText = QPushButton(" Select Image Text ", self)
        self.buttonImageText.clicked.connect(self.launchTextSelector)
        self.buttonImageText.setToolTip("Display the selected image in the text selection dialog to extract text you select")
        self.buttonImageText.setStatusTip("Display the selected image in the text selection dialog to extract text you select")
        self.mainToolBar.addWidget(self.buttonImageText)

        self.buttonBatchProcess = QPushButton(" Batch Process ", self)
        self.buttonBatchProcess.setToolTip("Extract all text from each image in the list below and record their text content and meta-data in the database")
        self.buttonBatchProcess.setStatusTip("Extract all text from each image in the list below and record their text content and meta-data in the database")
        self.buttonBatchProcess.clicked.connect(lambda: self.batchProcessAll(repeat=True))
        self.mainToolBar.addWidget(self.buttonBatchProcess)

        self.buttonSelectFolder = QPushButton(" Select Folder ", self)
        self.buttonSelectFolder.setToolTip("Select a new folder")
        self.buttonSelectFolder.setStatusTip("Select a new folder")
        self.buttonSelectFolder.clicked.connect(lambda: self.selectImageFolder(initialFolder=None))
        self.mainToolBar.addWidget(self.buttonSelectFolder)

        #   Menu button for view mode: large or small, could also include a slider for size setting.
        self.buttonImageSize = QPushButton(" Image Size ", self)
        self.imageSizeMenu = QMenu(self.buttonImageSize)
        self.imageSizeMenu.addAction("Small", lambda:  self.setImageSize("Small"))
        self.imageSizeMenu.addAction("Large", lambda: self.setImageSize("Large"))
        self.imageSizeMenu.addAction("FULL", lambda: self.setImageSize("FULL"))
        self.buttonImageSize.setMenu(self.imageSizeMenu)
        self.mainToolBar.addWidget(self.buttonImageSize)

        self.selectionList  = {}
        self.listViewFiles = FileListView(imageMap=self.pixMapImages, config={'listType': self.config['scanType']},
                                          listener=self.messageReceiver, parent=self.contentFrame)
        self.listViewFiles.setWindowTitle("Image File List")
        self.fileListModel = QStandardItemModel()
        self.listItemMap = OrderedDict()
        for fileName in self.pixMapImages:
            self.listItemMap[fileName]  = QStandardItem(fileName)
            self.listItemMap[fileName].setCheckable(True)
            self.fileListModel.appendRow(self.listItemMap[fileName])

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

    def listFolder(self):
        fileList = listdir(self.imageFolder)
        fileCount = 0
        for fileName in fileList:
            nameParts = fileName.split('.')
            if nameParts[-1].lower() in IMAGE_PIXMAP_EXTS:
                #   self.loadImage(self.imageFolder + '/' + fileName)
                self.pixMapImages[self.imageFolder + '/' + fileName] = True
                fileCount += 1
        return fileCount

    def walkFolder(self):
        fileCount = 0
        for dirName, subdirList, fileList in walk(self.imageFolder):
            if islink(dirName):
                continue
            for fileName in fileList:
                if islink(dirName + '/' + fileName):
                    continue
                nameParts = fileName.split('.')
                if nameParts[-1].lower() in IMAGE_PIXMAP_EXTS:
                    #   self.loadImage(dirName + '/' + fileName)
                    self.pixMapImages[dirName + '/' + fileName] = True
                    fileCount += 1
        return fileCount

    def loadImage(self, filePath: str):
        self.pixMapImages[filePath] = Image.open(filePath).toqpixmap()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super(ImageManager, self).resizeEvent(event)
        if DEBUG:
            print("ImageManager.resizeEvent:\t" + str(event.oldSize()))
            print("\told size::\t" + str(event.size()))
        newWidth = event.size().width()
        newHeight = event.size().height()
        #   self.labelImage.setMinimumHeight(350)
        #   self.labelImage.setMinimumWidth(250)

    def setImageSize(self, sizeName: str):
        if TESTING:
            print("ImageManager.setImageSize:\t" + sizeName)
        if sizeName == "Small":
            pass
        if sizeName == "Large":
            labelWidth = self.labelImage.width()
            labelHeight = self.labelImage.height()
            dialogWidth = self.width()
            dialogHeight = self.height()
            listWidth = self.listViewFiles.width()

            newWidth = dialogWidth - listWidth - 40
            newHeight = dialogHeight - 40

            scaled = False
            if self.selPixMap.height() != newHeight:
                pixMap = self.selPixMap.scaledToHeight(newHeight)
                scaled = True
            if self.selPixMap.width() != newWidth:
                pixMap = self.selPixMap.scaledToWidth(newWidth)
                scaled = True
            if scaled:
                self.labelImage.setMinimumWidth(pixMap.width())
                self.labelImage.setMinimumHeight(pixMap.height())
                self.imageScroller.setMinimumWidth(min(pixMap.width()+25, dialogWidth-listWidth-60))
                self.imageScroller.setMinimumHeight(min(pixMap.height()+25, dialogHeight-60))
                self.selPixMap = pixMap
                self.labelImage.setPixmap(self.selPixMap)

        if sizeName == "FULL":
            pass

    def fileListSelectionEvent(self, listItem):
        if TESTING:
            print("\nImageManager.fileListSelectionEvent:\t" + str(listItem.text()))
            print("\tcheckState:\t" + str(listItem.checkState()))
        if listItem.checkState() == Qt.CheckState.Checked:
            self.selectionList[listItem.text()]  = {}
        elif listItem.checkState() == Qt.CheckState.Unchecked:
            del(self.selectionList[listItem.text()])
        print("self.selectionList:\t" + str(self.selectionList))

    def launchTextSelector(self):
        if TESTING:
            print("ImageManager.launchTextSelector")
        for filePath in self.selectionList:
            if filePath not in self.textSelectors:
                config = {}
                self.textSelectors[filePath] = TextSelector(pixMapImage=self.pixMapImages[filePath],
                                                             imagePath=filePath, config=config,
                                                             listener=self.messageReceiver, parent=self)
            self.textSelectors[filePath].show()

    def batchProcessAll(self, repeat: bool=False):
        if TESTING:
            print("ImageManager.batchProcessAll")
        if DEBUG:
            ImageTextDB.dumpContent()

        if repeat:
            records = []
            timeStart = datetime.now()
            for filePath in self.pixMapImages:
                newRecord = {}
                newRecord['TimeStamp'] = datetime.now()
                newRecord['FolderPath'] = self.imageFolder
                newRecord['FileName'] = filePath
                print("Getting text from:\t" + filePath)
                (mode, inode, dev, nlink, uid, gid, size, atime, mtime, ctime)  = stat(filePath)
                aTime   = datetime.fromtimestamp(atime).strftime('%Y-%m-%d %H:%M:%S.%f')
                mTime   = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S.%f')
                cTime   = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S.%f')
                info = {
                    'mode': mode,                     'inode': inode,                     'dev': dev,
                    'nlink': nlink,                     'uid': uid,                    'gid': gid,
                    'size': size,                    'atime': aTime,                    'mtime': mTime,
                    'ctime': cTime
                }
                newRecord['Text'] = pytesseract.image_to_string(Image.open(filePath))
                newRecord['Info'] = convertToBytes(info)
                exif = PhotoFolder.getExif(filePath)
                newRecord['Exif'] = convertToBytes(exif)
                records.append(newRecord)
            timeEnd = datetime.now()
            elapsedTime = timeEnd - timeStart
            ImageTextDB.addRecords(records)
            print("ALL DONE in :\t" + str(elapsedTime))

    def selectImageFolder(self, initialFolder: str=None):
        if TESTING:
            print("ImageManager.selectImageFolder")
        if initialFolder is not None and (not isinstance(initialFolder, str) or not isdir(initialFolder)):
            raise Exception("ImageManager.selectImageFolder - Invalid initialFolder argument:  " + str(initialFolder))
        initialFolder = initialFolder if initialFolder is not None else environ['HOME']
        fileDialog = QFileDialog(parent=self, directory=initialFolder)
        fileDialog.setFileMode(QFileDialog.FileMode.Directory)
        #   fileDialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        fileDialog.setOption(QFileDialog.Option.ShowDirsOnly)
        fileDialog.setOption(QFileDialog.Option.DontUseNativeDialog)
        fileDialog.setOption(QFileDialog.Option.DontResolveSymlinks)
        fileDialog.setOption(QFileDialog.Option.ReadOnly)
        fileDialog.setViewMode(QFileDialog.Detail)
        fileDialog.exec()
        selections = fileDialog.selectedFiles()
        if TESTING:
            print(str(selections))

        self.folderPath = self.imageFolder  = selections[0]

        self.pixMapImages = OrderedDict()
        if self.scanType == 'list':
            self.listFolder()
        elif self.scanType == 'walk':
            self.walkFolder()
        self.fileListModel = QStandardItemModel()
        self.listItemMap = OrderedDict()
        for fileName in self.pixMapImages:
            self.listItemMap[fileName]  = QStandardItem(fileName)
            self.listItemMap[fileName].setCheckable(True)
            self.fileListModel.appendRow(self.listItemMap[fileName])
        self.listViewFiles.setModel(self.fileListModel)


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
                            self.textSelectors[message['fileName']].destroy()
                            del(self.textSelectors[message['fileName']])
                            self.listItemMap[message['fileName']].setCheckState(Qt.CheckState.Unchecked)
            #   {'source': 'FileListView.mousePressEvent', 'selectionText': self.currentImageFileName}
            elif message['source'] == 'FileListView.mousePressEvent':
                if 'selectionText' in message:
                    self.selImgFilePath = filePath = message['selectionText']
                    if self.pixMapImages[filePath] == True:
                        self.loadImage(filePath)
                    self.selPixMap = pixMapSelected  = self.pixMapImages[filePath]
                    if self.labelImage.height() < pixMapSelected.height():
                        pixMapSelected = pixMapSelected.scaledToHeight(self.labelImage.height())
                    if self.labelImage.width() < pixMapSelected.width():
                        pixMapSelected = pixMapSelected.scaledToWidth(self.labelImage.width())
                    self.labelImage.setPixmap(pixMapSelected)
                    self.labelMessages.setText(self.selImgFilePath)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.listener is not None:
            self.listener({'source': "ImageManager.closeEvent",
                           'action': 'close requested'})

class ImageTextDB:

    @staticmethod
    def addRecords(records: list):
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

