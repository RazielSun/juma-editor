#!/usr/bin/env python
##----------------------------------------------------------------##
import os
import os.path
import platform
import sys

rootPath = os.path.dirname(os.path.abspath(__file__))
libpath = rootPath + '/lib'
sys.path.insert( 0, libpath )

import juma

def main():
    juma.startup()

if __name__ == '__main__':
    main()