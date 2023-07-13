
import os
import platform
import sys

VERSION = "VERSION: 1.0.0"

SITE = "https://github.com/duibu/downloader"

TYPE = "dev" if VERSION.count('.') > 2 and VERSION.split('.')[-1] != '0' else "stable"

TYPE_COLORS = {"dev": 33, "stable": 90, "pip": 34}

BANNER = """\033[01;33m\

    ########   #######  ##      ## ##    ## ##        #######     ###    ########  ######## ########            \033[01;37m{\033[01;%dm%s\033[01;37m}\033[01;33m
    ##     ## ##     ## ##  ##  ## ###   ## ##       ##     ##   ## ##   ##     ## ##       ##     ## 
    ##     ## ##     ## ##  ##  ## ####  ## ##       ##     ##  ##   ##  ##     ## ##       ##     ## 
    ##     ## ##     ## ##  ##  ## ## ## ## ##       ##     ## ##     ## ##     ## ######   ########  
    ##     ## ##     ## ##  ##  ## ##  #### ##       ##     ## ######### ##     ## ##       ##   ##   
    ##     ## ##     ## ##  ##  ## ##   ### ##       ##     ## ##     ## ##     ## ##       ##    ##  
    ########   #######   ###  ###  ##    ## ########  #######  ##     ## ########  ######## ##     ##           \033[0m\033[4;37m%s\033[0m\n
    """ % (TYPE_COLORS.get(TYPE, 31), VERSION, SITE)


PLATFORM = os.name
OS_NAME = platform.system()
PYVERSION = sys.version.split()[0]
IS_WIN = PLATFORM == "nt"
IS_LINUX = OS_NAME == "Linux"

ABS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

DEFAULT_DOWNLOAD_PATH = ABS_PATH + os.sep + 'data'