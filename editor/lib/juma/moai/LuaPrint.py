
import sys

from colorama import Fore, Back, Style

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

def printSeparator(runningFile, colored):
    if colored:
        print(Style.RESET_ALL + Style.NORMAL + Fore.GREEN)
    
    print(5 * '\n' + 30 * '%%%')
    print('\t' + strftime('%H:%M:%S') + '\t' + runningFile)
    print(30 * '%%%')
    
    if colored:
        print(Style.RESET_ALL + Style.DIM)