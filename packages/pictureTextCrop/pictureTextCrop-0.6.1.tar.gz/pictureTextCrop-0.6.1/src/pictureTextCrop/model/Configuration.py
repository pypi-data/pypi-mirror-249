#   Project:        PictureTextCrop
#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   Copyright:      (c) Copyright 2022, 2023 George Keith Watson
#   Module:         model.Config.py
#   Date Started:   November 12, 2023
#   Purpose:        Configuration record-keeping including class level access to settings.
#   Development:

from collections import OrderedDict
from enum import Enum
from os import environ, stat
from os.path import isfile, isdir

MODULE_NAME    = "Configuration"
INSTALLING      = False
TESTING         = True
DEBUG           = False
CONSOLE_LOGGING = True


class CropMode(Enum):
    SEQUENCE    = 'Sequence'
    LIST        = 'List'

    def __str__(self):
        return self.value

    @staticmethod
    def valueToConst(value: str):
        if value == 'Sequence':
            return CropMode.SEQUENCE
        elif value == 'List':
            return CropMode.LIST


class TimeStampFormat(Enum):
    SORTABLE        = 'Sortable'
    PYTHON_NATIVE   = 'Python Native'   #   datetime.ctime()
    BUSINESS        = 'Business'
    SECONDS         = 'Seconds'
    MICRO_SECONDS   = 'Micro-Seconds'

    def __str__(self):
        return self.value

    @staticmethod
    def valueToConst(value: str):
        if value == 'Sortable':
            return TimeStampFormat.SORTABLE
        elif value == 'Python Native':
            return TimeStampFormat.PYTHON_NATIVE
        elif value == 'Business':
            return TimeStampFormat.BUSINESS
        elif value == 'Seconds':
            return TimeStampFormat.SECONDS
        elif value == 'Micro-Seconds':
            return TimeStampFormat.MICRO_SECONDS


class ScanType(Enum):
    LIST            = 'List'
    WALK            = 'Walk'

    def __str__(self):
        return self.value

    @staticmethod
    def valueToConst(value: str):
        if value == 'lIST':
            return ScanType.LIST
        elif value == 'Walk':
            return ScanType.WALK


class CropMode(Enum):
    SEQUENCE    = 'Sequence'
    LIST        = 'List'

    def __str__(self):
        return self.value

    @staticmethod
    def valueToConst(value: str):
        if value == 'Sequence':
            return CropMode.SEQUENCE
        elif value == 'List':
            return CropMode.LIST


class TimeStampFormat(Enum):
    SORTABLE        = 'Sortable'
    PYTHON_NATIVE   = 'Python Native'   #   datetime.ctime()
    BUSINESS        = 'Business'
    SECONDS         = 'Seconds'
    MICRO_SECONDS   = 'Micro-Seconds'

    def __str__(self):
        return self.value

    @staticmethod
    def valueToConst(value: str):
        if value == 'Sortable':
            return TimeStampFormat.SORTABLE
        elif value == 'Python Native':
            return TimeStampFormat.PYTHON_NATIVE
        elif value == 'Business':
            return TimeStampFormat.BUSINESS
        elif value == 'Seconds':
            return TimeStampFormat.SECONDS
        elif value == 'Micro-Seconds':
            return TimeStampFormat.MICRO_SECONDS


class Operation(Enum):
    EXTRACT_ALL     = "Extract All"
    CROP_SEQUENCE   = "Crop Sequence"
    INDEX_FILES     = "Index Files"
    INDEX_TEXT      = "Index Text"
    INDEX_GEN       = 'Generate Indexes'


class StartMode(Enum):
    INSTALL         = "Install"
    ADMIN           = "Admin"
    USER            = "User"


class RunMode(Enum):
    SEQUENCE        = 'Sequence'
    BATCH           = 'Batch'

    def __str__(self):
        return self.value


class AppConfig:
    """
    These are default values only.
    The values are set from the database every time the application starts.
    """
    _changed  = False

    _adminEnabled                   = True
    _startMode                      = StartMode.USER

    _openWithFolderSelection        = False
    _folderScanType                 = ScanType.LIST

    _autoCacheTextExtraction        = True
    _autoIndexTextExtraction        = False

    _defaultImageFolder             = environ['HOME']

    _cropMode                       = CropMode.LIST

    _timeStampFormat                = TimeStampFormat.SORTABLE

    _jobDefaultFolderScanMode       = ScanType.WALK
    _jobDefaultRunMode               = RunMode.SEQUENCE

    @staticmethod
    def getCurrent():
        return {
            'adminEnabled': AppConfig._adminEnabled,
            'startMode': AppConfig._startMode,
            'openWithFolderSelection': AppConfig._openWithFolderSelection,
            'folderScanType': AppConfig._folderScanType,
            'autoCacheTextExtraction': AppConfig._autoCacheTextExtraction,
            'autoIndexTextExtraction': AppConfig._autoIndexTextExtraction,
            'defaultImageFolder': AppConfig._defaultImageFolder,
            'cropMode': AppConfig._cropMode,
            'timeStampFormat': AppConfig._timeStampFormat,
            'jobDefaultFolderScanMode': AppConfig._jobDefaultFolderScanMode,
            'jobDefaultRunMode': AppConfig._jobDefaultRunMode
        }

    @staticmethod
    def isChanged():
        return AppConfig._changed

    @staticmethod
    def setConfig(config: dict):
        if not isinstance(config, dict):
            raise Exception("AppConfig.setConfig - Invalid config argument:  " + str(config))
        if 'adminEnabled' in config and isinstance(config['adminEnabled'], bool):
            AppConfig._adminEnabled = config['adminEnabled']
        if 'startMode' in config and isinstance(config['startMode'], StartMode):
            AppConfig._startMode = config['startMode']
        if 'openWithFolderSelection' in config and isinstance(config['openWithFolderSelection'], bool):
            AppConfig._openWithFolderSelection = config['openWithFolderSelection']
        if 'folderScanType' in config and isinstance(config['folderScanType'], ScanType):
            AppConfig._folderScanType = config['folderScanType']
        if 'autoCacheTextExtraction' in config and isinstance(config['autoCacheTextExtraction'], bool):
            AppConfig._autoCacheTextExtraction = config['autoCacheTextExtraction']
        if 'autoIndexTextExtraction' in config and isinstance(config['autoIndexTextExtraction'], bool):
            AppConfig._autoIndexTextExtraction = config['autoIndexTextExtraction']
        if 'defaultImageFolder' in config and isinstance(config['defaultImageFolder'], str):
            AppConfig._defaultImageFolder = config['defaultImageFolder']
        if 'cropMode' in config and isinstance(config['cropMode'], CropMode):
            AppConfig._cropMode = config['cropMode']
        if 'timeStampFormat' in config and isinstance(config['timeStampFormat'], TimeStampFormat):
            AppConfig._timeStampFormat = config['timeStampFormat']
        if 'jobDefaultFolderScanMode' in config and isinstance(config['jobDefaultFolderScanMode'], ScanType):
            AppConfig._jobDefaultFolderScanMode = config['jobDefaultFolderScanMode']
        if 'jobDefaultRunMode' in config and isinstance(config['jobDefaultRunMode'], RunMode):
            AppConfig._jobDefaultRunMode = config['jobDefaultRunMode']

        AppConfig._changed = True

    @staticmethod
    def getJobsConfig():
        return {
            'DefaultFolderScanMode': AppConfig._jobDefaultFolderScanMode,
            'DefaultRunMode': AppConfig._jobDefaultRunMode,
        }

    @staticmethod
    def setJobsDefaultFolderScanMode(scanMode: ScanType):
        if not isinstance(scanMode, ScanType):
            return
        AppConfig._jobDefaultFolderScanMode = scanMode
        AppConfig._changed = True

    @staticmethod
    def setJobsDefaultRunMode(runMode: RunMode):
        if not isinstance(runMode, RunMode):
            return
        AppConfig._jobDefaultRunMode = runMode
        AppConfig._changed  = True

    @staticmethod
    def getOpenWithFolderSelection():
        return AppConfig._openWithFolderSelection

    @staticmethod
    def setOpenWithFolderSelection(value: bool):
        if not isinstance(value, bool):
            return
        AppConfig._openWithFolderSelection = value
        AppConfig._changed   = True

    @staticmethod
    def getFolderScanType():
        return AppConfig._folderScanType

    @staticmethod
    def setFolderScanType(scanType: ScanType):
        if not isinstance(scanType, ScanType):
            return
        AppConfig._folderScanType = scanType
        AppConfig._changed = True

    #   _defaultImageFolder
    @staticmethod
    def getDefaultImageFolder():
        return AppConfig._defaultImageFolder

    @staticmethod
    def setDefaultImageFolder(folderPath: str):
        if not isinstance(folderPath, str) or not isdir(folderPath):
            return
        AppConfig._defaultImageFolder = folderPath
        AppConfig._changed = True


class Task:
    """
    Task Configuration
        A Task is a sequence of files or other object on which a particular operation is to be performed on
        each in order.
    """
    pass


class User:
    """
    This is planned for a future release.
    """

    DEFAULT_NAME    = 'User'

    def __init__(self, userName: str):
        if userName is not None:
            if not isinstance(userName, str):
                raise Exception("User constructor - Invalid userName argument:  " + str(userName))
            self._userName = userName
        else:
            self._userName = User.DEFAULT_NAME
        self._assignedTasks = None

    def getUserName(self):
        return self._userName

    def addTask(self, task: Task):
        if self._assignedTasks is None:
            self._assignedTasks = []
        else:
            self._assignedTasks = list(self._assignedTasks)
        self._assignedTasks.append(task)
        self._assignedTasks = tuple(self._assignedTasks)

    def getAssignedTasks(self):
        return self._assignedTasks


class File:
    """
    This is planned for a future release.
    """

    def __init__(self, filePath: str):
        if not isinstance(filePath, str) or not isfile(filePath):
            raise Exception("File constructor - Invalid filePath argument:  " + str(filePath))
        self._filePath = filePath
        self._info = stat(filePath)

    def getFilePath(self):
        return self._filePath

    def getFileInfo(self):
        return self._info


class FileList:
    """
    This is planned for a future release.
    """

    def __init__(self, filePathList: tuple):
        self._fileMap = OrderedDict()
        self._addFiles(filePathList)

    def _addFiles(self, filePathList: tuple):
        if not (isinstance(filePathList, tuple) or isinstance(filePathList, list)):
            raise Exception("FileList.addFiles - Invalid filePathList argument:  " + str(filePathList))
        for filePath in filePathList:
            self._fileMap[filePath] = File(filePath)

    def getFile(self, filePath):
        if filePath in self._fileMap:
            return self._fileMap[filePath]
        return None


class Task:
    """
    This is planned for a future release.
    """

    DEFAULT_ID      = "Current File List Task"

    def __init__(self, identifier: str, fileList: FileList, operation: Operation):
        if identifier is not None:
            if not isinstance(identifier, str):
                raise Exception("Task constructor - Invalid identifier argument:  " + str(identifier))
            self.identifier = identifier
        else:
            self.identifier = Task.DEFAULT_ID
        if not isinstance(fileList, FileList):
            raise Exception("Task constructor - Invalid fileList argument:  " + str(fileList))
        if not isinstance(operation, Operation):
            raise Exception("Task constructor - Invalid operation argument:  " + str(operation))
        self._fileList = fileList
        self._operation = operation
        self._user = None

    def getIdentifier(self):
        return self.identifier

    def getFileList(self):
        return self._fileList

    def getOperation(self):
        return self._operation

    def getUser(self):
        return self._user

    def assignTo(self, user: User):
        if not isinstance(user, User):
            raise Exception("Task.assignTo - Invalid user argument:  " + str(user))
        self._user = user


if __name__ == "__main__":
    print("Running:\t" + MODULE_NAME)
    AppConfig._adminEnabled = False
