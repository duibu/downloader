
import os
import sys

VERSION = "VERSION: 1.0.0"

SITE = "https://github.com/duibu/downlonder"

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
PYVERSION = sys.version.split()[0]
IS_WIN = PLATFORM == "nt"