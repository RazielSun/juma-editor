import sys
import traceback

from colorama import Fore, Back, Style

from time import strftime

def printTraceBack(colored=True):
    if colored:
        print(Style.RESET_ALL + Style.NORMAL + Fore.RED)

    traceback.print_stack()

    if colored:
        print(Style.RESET_ALL + Style.DIM)

def tracebackFunc(trace):
    print(Style.RESET_ALL + Fore.RED + Style.BRIGHT + trace + Style.RESET_ALL + Style.DIM)

def luaBeforePrint():
    style = strftime("%H:%M:%S")
    style = style + Style.RESET_ALL + Style.NORMAL
    style = style + '  '
    print style,
    
def luaAfterPrint():
    style = Style.RESET_ALL + Style.DIM
    sys.stdout.write(style)

def printSeparator(path, file, colored=True):
    if colored:
        print(Style.RESET_ALL + Style.NORMAL + Fore.GREEN)
    
    print(5 * '\n' + 40 * '%%%')
    print('\t' + strftime('%H:%M:%S') + '\t Folder: ' + path + '\t File: ' + file)
    print(40 * '%%%')
    
    if colored:
        print(Style.RESET_ALL + Style.DIM)