#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           Exif.py
#   Language:       Python 3.0+
#   Copyright:      Copyright 2022 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#

from os.path import isfile, isdir
from os import listdir
from sys import stderr
from pathlib import Path
from enum import Enum

from exif import Image      #   Excellent, apparently thorough results on jpeg format.
import Exif                 #   tested and works on jpg, digital camera photographs, not on png, screenshots
from PIL import Image as PilImage
import exifread

MODULE_NAME    = "Exif"
INSTALLING      = False
TESTING         = True
DEBUG           = False


class ExifService(Enum):
    EXIFREAD        = 'exifread'
    EXIF_IMAGE      = 'from exif import Image'

    def __str__(self):
        return self.value


class PhotoFolder:

    def __init__(self, folderPath: str, extensions: tuple, service: ExifService):
        self.photoDataMap = {}
        if isdir(folderPath):
            fileList = listdir(folderPath)
            for fileName in fileList:
                path = Path(folderPath + '/' + fileName)
                print("Extracting meta data from:\t" + str(path))
                if path.suffix in extensions:
                    try:
                        if service == ExifService.EXIF_IMAGE:
                            image = Image(str(path))
                            self.photoDataMap[str(path)]    = { 'image': image, 'exif': image.get_all() }
                        elif service == ExifService.EXIFREAD:
                            image = PilImage.open(str(path))
                            with open(path, 'rb') as imageFile:
                                tags = exifread.process_file(imageFile, details=True)
                                self.photoDataMap[str(path)]    = { 'image': image, 'exif': tags }

                    except:     #   Report failure and write it to log
                        print("\tCould not get meta-data from file:\t" + str(path), file=stderr)

    @staticmethod
    def getExif(filePath: str):
        if not isfile(filePath):
            return None
        path = Path(filePath)
        if TESTING:
            print("Extracting meta data from:\t" + filePath)
        info = {}
        if path.suffix != '.png':
            #   image = Image(str(filePath))
            #   info['imageExig'] = image.get_all()
            #   image = Image(str(filePath))
            info['imageExig'] = None
        with open(filePath, 'rb') as imageFile:
            info['tags'] = exifread.process_file(imageFile, details=True)
            info['imageExig'] = None
        return info


def testExifImage():
    photoFilePath  = TEST_SAMPLE_FILES + "/IMG_20221127_123600802.jpg"
    if not isfile(photoFilePath):
        print("File does not exist:\t" + photoFilePath, file=stderr)
    print("Screenshot File:\t" + photoFilePath)
    with open(photoFilePath, 'rb') as screenshotFile:
        screenshot = Image(screenshotFile)
    if screenshot.has_exif:
        print("\tHAS EXIF META DATA")
        screenshot.list_all()
        exifObj = screenshot.get_all()
        #   NOW SAVE TO TABLE ROW WITH THE FILE"S PATH AND STAT IN IT AS exitInfo: BLOB
    else:
        print("\tHAS NO EXIF", file=stderr)
