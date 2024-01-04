#   Author:         George Keith Watson
#   Date Started:   November 4, 2022
#   File:           Installation.py
#   Language:       Python 3.6+
#   Copyright:      Copyright 2022 by George Keith Watson
#   License:        GNU LGPL 3.0 (GNU Lesser General Public License)
#                   at: www.gnu.org/licenses/lgpl-3.0.html
#
from enum import Enum
from os import environ

USER_HOME = environ['HOME']
INSTALLED_PY_MODULES    = None
ALL_PY_MODULES          = None

#   PROJECTS_FOLDER         = USER_HOME + "/PycharmProjects/Publishing"
#   INSTALLATION_FOLDER     = PROJECTS_FOLDER + "/PictureTextCrop"
INSTALLATION_FOLDER     = '.'
TOOLBAR_ICON_FOLDER     =  INSTALLATION_FOLDER + '/view/icons'

DOCS_FOLDER             = INSTALLATION_FOLDER + '/docs'
HELP_DOCS_FOLDER        = DOCS_FOLDER + '/help'
HTML_DOCS_FOLDER        = DOCS_FOLDER + '/html'


HELP_FOLDER_ICON        = 'folder--arrow.png'
HELP_FOLDER_HORIZONTAL_ICON = 'folder-horizontal.png'

HELP_ABOUT_FILE                     = 'About.html'
HELP_QUICK_START_FILE               = 'QuickStart.html'
HELP_FILES_MENU_FILE                = 'Files.html'
HELP_RUN_MENU_FILE                  = 'Run.html'
HELP_VIEW_MENU_FILE                 = 'View.html'
HELP_ADMIN_MENU_FILE                = 'Admin.html'

FILE_SYSTEM_TECH                    = "Replaying the Journal.html"


TEXT_EXTRACTION_DB_FILE = 'TextExtraction.db'

#   Loadable with QImageReader, which is image file loader currently used:
QT5_IMAGE_FILE_EXTS   = ('bmp', 'cur', 'gif', 'icns', 'ico', 'jpeg', 'jpg', 'mng', 'pbm', 'pgm', 'png', 'ppm',
                       'svg', 'svgz', 'tga', 'tif', 'tiff', 'wbmp', 'webp', 'xbm', 'xpm')

QT5_MIME_TYPES = ( 'image/bmp', 'image/gif', 'image/jpeg', 'image/png', 'image/svg+xml', 'image/svg+xml-compressed',
                   'image/tiff', 'image/vnd.microsoft.icon', 'image/vnd.wap.wbmp', 'image/webp', 'image/x-icns',
                   'image/x-mng', 'image/x-portable-bitmap', 'image/x-portable-graymap', 'image/x-portable-pixmap',
                   'image/x-tga', 'image/x-xbitmap', 'image/x-xpixmap')

#   Formats loadable from files:
IMAGE_PIXMAP_EXTS = ('bmp', 'gif', 'jpeg', 'jpg', 'pbm', 'pgm', 'png', 'ppm', 'xbm', 'xpm')
PillowFileExtensions = ('ALL', 'apng', 'blp', 'blp1', 'blp2', 'bmp', 'dds', 'dib', 'dxt1', 'dxt3', 'dxt5', 'eps',
                        'gif', 'icns', 'ico', 'im', 'jfif', 'jpeg', 'jpg', 'msp', 'pbm', 'pcx', 'pgm', 'png',
                        'pnm', 'ppm', 'sgi', 'spi', 'tga', 'tiff', 'webp', 'xbm')


class PixmapMimeType(Enum):
    BMP         = ("image/bmp", 'bmp')
    GIF         = ("image/gif", 'gif')
    JPEG        = ("image/jpeg", 'jpeg')

    PNG         = ("image/png", 'png')

    TIFF        = ("image-tiff", 'tiff')
    AVIF        = ("image/avif", 'avif')
    G3FAX       = ("image/g3fax", 'g3fax')
    SVG_XML     = ("image/svg+xml", 'svg+xml')
    ADOBE_SHOP  = ("image/vnd.adobe.photoshop", 'vnd.adobe.photoshop')
    MS_ICON     = ("image/vnd.microsoft.icon", 'vnd.microsoft.icon')
    WEBP        = ("image/webp", 'webp')
    X_ICNS      = ("image/x-icns", 'x-icns')
    SONY_TIM    = ("image/x-sony-tim", 'x-sony-tim')

    ALL_TYPES   = ("image-tiff", "image/avif", "image/bmp", "image/g3fax", "image/gif", "image/jpeg", "image/png",
                   "image/svg+xml", "image/vnd.adobe.photoshop", "image/vnd.microsoft.icon", "image/webp",
                   "image/x-icns", "image/x-sony-tim")



class PageType(Enum):
    WEB_PAGE        = "Web Page"
    WEB_XML         = "Web XML Document"
    WEB_XML_GZ      = "Web XML Document - GZIP"
    WEB_MATHML      = "Web MathML Document"

    XML_WORD_DOC    = "MS Open XML Document"

    PYSIDE_LAYOUT   = "PySide Layout"
    PYSIDE_WIDGET   = "PySide Widget"
    PYSIDE_SVG      = "Scalable Vector Graphics"
    WEB_PDF         = "Web PDF Document"

    WEB_TEXT        = "Web Text"
    WEB_IMAGE       = "Web Image"
    WEB_AUDIO       = "Web Audio"
    WEB_VIDEO       = "Web Video"

    def __str__(self):
        return self.value
