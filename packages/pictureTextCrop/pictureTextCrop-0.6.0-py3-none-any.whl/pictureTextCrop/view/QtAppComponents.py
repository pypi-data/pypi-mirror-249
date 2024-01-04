#   Project:        PictureTextCrop
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   Copyright:      (c) Copyright 2022, 2023 George Keith Watson
#   Module:         view.QtAppComponents.py
#   Purpose:        Extensions of PySide Qt widgets.
#   Development:
#
from sys import stderr, argv

from PyQt5.QtCore import QEvent, QByteArray, Qt, QItemSelection
from PyQt5.QtGui import QEnterEvent, QMouseEvent, QContextMenuEvent, QImageReader, QImage, QPixmap, QFont, QKeyEvent, \
    QFocusEvent
from PyQt5.QtWidgets import QPushButton, QTabWidget, QApplication, QLabel, QListView, QLineEdit

from model.HelpContent import HelpContent

MODULE_NAME    = "Qt Derived Components"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONSOLE_LOGGING = True


class AppButton(QPushButton):

    def __init__(self, text: str, identifier=None, listener=None, parent=None):
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(AppButton, self).__init__(text=text, parent=parent)
        self.identifier = identifier

    def enterEvent(self, event: QEnterEvent) -> None:
        super(AppButton, self).enterEvent(event)
        if self.listener is not None:
            self.listener({'source': "AppButton.enterEvent", 'identifier': self.identifier})

    def leaveEvent(self, event: QEvent) -> None:
        super(AppButton, self).leaveEvent(event)
        #   if self.listener is not None:
        #       self.listener({'source': "AppButton.leaveEvent", 'identifier': self.identifier})

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(AppButton, self).mousePressEvent(event)
        if DEBUG:
            print("AppButton.mousePressEvent")

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super(AppButton, self).mouseReleaseEvent(event)
        if self.listener is not None:
            self.listener({'source': "AppButton.mouseReleaseEvent", 'identifier': self.identifier, 'button': event.button()})


class TabbedView(QTabWidget):
    DEFAULT_ID = 'TabbedView'
    DEFAULT_CONFIG = {}

    def checkArguments(config: dict, initialContent: tuple, listener=None, parent=None):
        if config is not None and not isinstance(config, dict):
            raise Exception("TabbedView.checkArguments - Invalid config argument:  " + str(config))
        #   also check config for raquired fields and for correct types / values of its fields
        if initialContent is not None:
            if not isinstance(initialContent, tuple):
                raise Exception("TabbedView.checkArguments - Invalid initialTabs argument:  " + str(initialContent))
            for tabFrame in initialContent:
                if not isinstance(tabFrame, HelpContent):
                    raise Exception(
                        "TabbedView.checkArguments - Invalid tabFrame in initialTabs argument:  " + str(tabFrame))
        if listener is not None and not callable(listener):
            raise Exception("TabbedView.checkArguments - Invalid listener argument:  " + str(listener))
        return True

    def __init__(self, identifier: str = None, config: dict = None, initialTabs: tuple = None, listener=None,
                 parent=None):
        if identifier is not None and isinstance(identifier, str):
            self.identifier = identifier
        else:
            self.identifier = TabbedView.DEFAULT_ID
        TabbedView.checkArguments(config, initialTabs, listener, parent)
        super(TabbedView, self).__init__(parent)
        self.config = config
        self.initialTabs = initialTabs
        self.listener = listener
        self.setTabsClosable(False)


    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        super().contextMenuEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)


if __name__ == "__main__":
    print("Running:\t" + MODULE_NAME)

    filePath = "/home/keithcollins/Clippings.me/Uploads/2022-09-23/Screenshot_2022-09-23_07-50-51.png"

    try:
        imageReader     = QImageReader(filePath)
        imageReader.setAutoDetectImageFormat(True)

        print("QImageReader scan of file:\t" + filePath)
        if imageReader.canRead():
            print("\tThe file can be read")
        imageRef = imageReader.read()
        if imageRef is not None:
            print("\tThe file WAS read")
        else:
            print("\tThe file WAS NOT read")

    #   These will need a QMessageBox to report error to GUI application user:
    except QImageReader.FileNotFoundError:
        print("Exception on attempt to load file:\t" + filePath, file=stderr)
        print("\tFileNotFoundError" + filePath, file=stderr)
    except QImageReader.DeviceError:
        print("Exception on attempt to load file:\t" + filePath, file=stderr)
        print("\tDeviceError" + filePath, file=stderr)
    except QImageReader.UnsupportedFormatError:
        print("Exception on attempt to load file:\t" + filePath, file=stderr)
        print("\tUnsupportedFormatError" + filePath, file=stderr)
    except QImageReader.InvalidDataError:
        print("Exception on attempt to load file:\t" + filePath, file=stderr)
        print("\tInvalidDataError" + filePath, file=stderr)
    except QImageReader.UnknownError:
        print("Exception on attempt to load file:\t" + filePath, file=stderr)
        print("\tUnknownError" + filePath, file=stderr)

    print("Type of image object returned by read():\t" + str(type(imageRef)))
    #   pixImage = imageRef.toPixelFormat(QImage)

    app = QApplication(argv)
    pixImage = QPixmap(imageRef)

    print("Type of image object returned by toPixelFormat():\t" + str(type(pixImage)))

    #   pixMap  = imageRef.toPixelFormat()
    #   print("Type of imageRef.toPixelFormat():\t" + str(type(pixMap)))

    """
    print('\nSupported Image Formats:\t')
    for imageFormat in imageLoader.supportedImageFormats():
        print(str(imageFormat.data().decode('utf-8')))
    """
    print('\nSupported MIME Types:\t')
    #   Use:    QFileDialog::setMimeTypeFilters()
    for mimeType in imageReader.supportedMimeTypes():
        print(str(mimeType.data().decode('utf-8')))


class FieldLabel(QLabel):
    """
    A QLabel with visible and contained mouse event response methods.
    """
    DEFAULT_ID  = ''
    DEFAULT_CONFIG = {}
    DEFAULT_TEXT = 'enter text'

    def __init__(self, identifier: str=None,  text: str=None, config: dict=None, listener=None, parent=None):
        if identifier is not None:
            if not isinstance(identifier, str):
                raise Exception("FieldLabel constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        else:
            self.identiier = FieldLabel.DEFAULT_ID
        if text is not None:
            if not isinstance(text, str):
                raise Exception("FieldLabel constructor - Invalid text argument:  " + str(text))
            else:
                self.text = text
        else:
            self.text = FieldLabel.DEFAULT_TEXT
        if config is not None:
            if not isinstance(config, dict):
                raise Exception("FieldLabel constructor - Invalid config argument:  " + str(config))
            self.config = config
        else:
            self.config = FieldLabel.DEFAULT_CONFIG
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None

        super(FieldLabel, self).__init__(text=text, parent=parent)
        self.identifier = identifier
        self.text = text

        if 'font' in self.config and 'face' in self.config['font'] and 'size' in self.config['font']:
            #   self.setFont(QFont("Arial", 10))
            self.setFont(QFont(self.config['font']['face'], self.config['font']['size']))


    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(FieldLabel, self).mousePressEvent(event)
        if self.listener is not None:
            self.listener({'source': 'FieldLabel.mousePressEvent', 'identifier': self.identifier,
                           'position': self.mapToGlobal(event.pos())})

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super(FieldLabel, self).mouseReleaseEvent(event)
        if self.listener is not None:
            self.listener({'source': 'FieldLabel.mouseReleaseEvent', 'identifier': self.identifier})

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super(FieldLabel, self).mouseDoubleClickEvent(event)
        if self.listener is not None:
            self.listener({'source': 'FieldLabel.mouseDoubleClickEvent', 'identifier': self.identifier})


class KeyListView(QListView):
    """
    This needs to display a scaled image or thumbnail on the right when an image is made the current one.
    It should also have the option of displaying a thumbnail as an icon for each list item.
    """
    DEFAULT_CONFIG  = {}
    DEFAULT_ID  = "KeyListView"

    def __init__(self, keyList:tuple, config: dict=None, identifier: str=None, listener=None, parent=None):
        if not isinstance(keyList, tuple) and not isinstance(keyList, list):
            raise Exception("KeyListView constructor - Invalid keyList argument:  " + str(keyList))
        if identifier is not None:
            if not isinstance(identifier, str):
                raise Exception("KeyListView constructor - Invalid identifier argument:  " + str(identifier))
            else:
                self.identifier = identifier
        else:
            self.identifier = KeyListView.DEFAULT_ID
        if config is None or not isinstance(config, dict):
            self.config = KeyListView.DEFAULT_CONFIG
        else:
            self.config = config
        if listener is not None and callable(listener):
            self.listener = listener
        else:
            self.listener = None
        super(KeyListView, self).__init__(parent)
        self.keyList = keyList
        self.config = config
        self.currSelectionIdx = None

        #   self.setStyleSheet("border-radius: 5px; font-size: 11pt; padding: 5px 5px 5px 5px")

    def __setattr__(self, key, value):
        if key == 'listener':
            if 'listener' not in self.__dict__:
                self.__dict__[key] = value
            return
        self.__dict__[key] = value

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super(KeyListView, self).mousePressEvent(event)
        if DEBUG:
            print("KeyListView.mousePressEvent:\t" + str(event))

        if self.selectionModel() is None:
            return
        selectedItems = []
        for index in self.selectionModel().selectedIndexes():
            if index.column() == 0:
                selectedItems.append(self.model().itemData(index)[0])
        selectedItems = tuple(selectedItems)

        self.currSelectionIdx = None
        self.currentKey = None
        selectionIdx = self.indexAt(event.pos())
        if selectionIdx is not None:
            selectedItem = self.model().item(selectionIdx.row(), selectionIdx.column())
            if selectedItem is not None:
                self.currSelectionIdx = selectionIdx
                self.currentKey = selectedItem.text()

        if self.listener is not None:
            self.listener({'source': 'KeyListView.mousePressEvent',
                           #   Popup menu if right click
                           'action': 'popupMenu' if event.button() == Qt.MouseButton.RightButton else "selection",
                           'point': event.pos(),
                           'selectionText': self.currentKey,
                           'multiSelect': len(selectedItems) > 1,
                           'selectionList': selectedItems,
                           'button': event.button(),
                           'row': selectionIdx.row(),
                           'identifier': self.identifier})

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super(KeyListView, self).mouseDoubleClickEvent(event)
        if self.listener is not None:
            self.listener({'source': 'KeyListView.mouseDoubleClickEvent', 'identifier': self.identifier,
                           'selection': self.currentKey})

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super(KeyListView, self).keyPressEvent(event)
        if DEBUG:
            print("KeyListView.keyPressEvent:\t" + str(event.key()))
        if self.listener is not None:
            if event.key() == 16777216:      #   [esc] key pressed
                self.listener({'source': 'KeyListView.keyPressEvent', 'identifier': self.identifier, 'keyId': 'esc'})
            elif event.key() == 16777220:    #   [enter] key pressed
                self.listener({'source': 'KeyListView.keyPressEvent', 'identifier': self.identifier, 'keyId': 'enter'})

    def selectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
        super(KeyListView, self).selectionChanged(selected, deselected)
        if self.listener is not None:
            if len(selected.indexes()) > 0:
                selection = self.model().itemData(selected.indexes()[0])[0]
            else:
                selection = None
            self.listener({'source': 'KeyListView.selectionChanged', 'identifier': self.identifier,
                           'selection': selection})


class EditorLine(QLineEdit):

    DEFAULT_CONFIG = {
        'maxLength': 100,
        'history': ('First URL', 'Second URL', 'Third URL')
    }

    @staticmethod
    def validateArgs(config: dict, initialText: str, identifier: str=None, validator=None, listener=None):
        pass

    def __init__(self, config: dict, initialText: str, identifier: str=None, validator=None, listener=None, parent=None):
        self.validateArgs(config, initialText, validator, listener)
        super(EditorLine, self).__init__(parent)
        if config is not None:
            self.config = config
        else:
            self.config = EditorLine.DEFAULT_CONFIG
        self.initialText = initialText
        self.identifier = identifier
        self.validator = validator
        self.listener = listener
        if 'maxLength' in self.config and isinstance(self.config['maxLength'], int):
            self.setMaxLength(self.config['maxLength'])
        if self.initialText is None:
            self.setPlaceholderText("Enter URL or search terms")
        else:
            self.setPlaceholderText(self.initialText)
        self.setText(self.initialText)

        self.setEnabled(True)
        self.setReadOnly(False)

    def __setattr__(self, key, value):
        if key == 'listener':
            if 'listener' not in self.__dict__:
                self.__dict__[key] = value
            return
        self.__dict__[key] = value

    def setText(self, text: str) -> None:
        if DEBUG:
            print("EditorLine.setText:\t" + text)
        super(EditorLine, self).setText(text)

    def changeEvent(self, event: QEvent) -> None:
        super(EditorLine, self).changeEvent(event)
        if 'suggestions' in self.config:
            for candidate in self.config['suggestions']:
                if self.text() in candidate:
                    self.setText(candidate)
                    break

    def keyPressEvent(self, keyEvent: QKeyEvent) -> None:
        super(EditorLine, self).keyPressEvent(keyEvent)
        if DEBUG:
            print("EditorLine.keyPressEvent:\t" + str(keyEvent.key()))

        if keyEvent.key() == 16777220:  # Enter pressed
            if self.listener is not None:
                self.listener({'source': 'EditorLine.keyPressEvent', 'keyCode': keyEvent.key(), 'keyId': "Enter"})

        elif keyEvent.key() == 16777219: # Backspace pressed
            pass
        elif keyEvent.key() == 16777248: # Shift pressed
            pass
        else:
            if DEBUG:
                print(str(keyEvent.key()))
            if 'suggestions' in self.config:
                for candidate in self.config['suggestions']:
                    if self.text() in candidate:
                        self.setText(candidate)
                        break

    def mouseReleaseEvent(self, mouseEvent: QMouseEvent) -> None:
        super(EditorLine, self).mouseReleaseEvent(mouseEvent)

    def mousePressEvent(self, mouseEvent: QMouseEvent) -> None:
        super(EditorLine, self).mousePressEvent(mouseEvent)

    def focusInEvent(self, focusEvent: QFocusEvent) -> None:
        super(EditorLine, self).focusInEvent(focusEvent)
        if DEBUG:
            print("EditorLine.focusInEvent")
        self.selectAll()
        if self.listener is not None:
            self.listener({'source': 'EditorLine.focusInEvent', 'identifier': self.identifier})

    def focusOutEvent(self, focusEvent: QFocusEvent) -> None:
        super(EditorLine, self).focusOutEvent(focusEvent)
        if self.listener is not None:
            self.listener({'source': 'EditorLine.focusOutEvent', 'identifier': self.identifier, 'newValue': self.text()})

    def enterEvent(self, event: QEnterEvent) -> None:
        super(EditorLine, self).enterEvent(event)
        if self.listener is not None:
            self.listener({'source': 'EditorLine.enterEvent', 'identifier': self.identifier})

    def leaveEvent(self, event: QEvent) -> None:
        super(EditorLine, self).leaveEvent(event)
        if self.listener is not None:
            self.listener({'source': 'EditorLine.leaveEvent', 'identifier': self.identifier})

    def changeEvent(self, event: QEvent) -> None:
        super(EditorLine, self).changeEvent(event)
        if self.listener is not None:
            self.listener({'source': 'EditorLine.changeEvent', 'identifier': self.identifier,
                           'newValue': self.text()})

    def popupMenuAction(self, actionName):
        if DEBUG:
            print("EditorLine.popupMenuAction:\t" + str(actionName))

