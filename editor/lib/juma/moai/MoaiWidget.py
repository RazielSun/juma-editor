
# MOAI OpenGL qt widget

import os, sys
import moaipy

from PySide import QtCore, QtGui, QtOpenGL
from moaipy import *
from OpenGL.GL import *
from OpenGL.GLU import *

import LuaInterface
from FileDialog import FileDialog
from ColoredLog import ColoredLog

# input sensors IDs
KEYBOARD, POINTER, MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT, MOUSE_WHEEL, TOTAL = range(0, 7)

KeyCodes = moaipy.KeyCodesDict()

class MOAIWidget( QtOpenGL.QGLWidget ):
    _context = 0
    timer = None
    windowReady = False
    contextReady = False
    initReady = False


    def __init__(self, parent=None):
        fmt = QtOpenGL.QGLFormat()
        fmt.setSwapInterval(1)

        QtOpenGL.QGLWidget.__init__(self, fmt, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)

        self.refreshContext()

    # Qt callbacks and overrides
    def resizeGL(self, w, h):
        if self.windowReady and self.contextReady:
            AKUSetScreenSize(w, h)
            AKUSetViewSize(w, h)

    def initializeGL(self):
        self.glReady = True
        glClearColor(0, 0, 0, 1)

    def paintGL(self):
        if self.windowReady and self.contextReady:
            AKURender()
        elif self.glReady:
            glClear(GL_COLOR_BUFFER_BIT)

    def timerEvent(self, event):
        if self.windowReady and self.contextReady:
            AKUModulesUpdate()
            self.updateGL()

    # Input
    # def wheelEvent(self, event):
    #     AKUEnqueueWheelEvent ( 0, MOUSE_WHEEL, event.delta() )
    #     event.accept()

    # def mouseMoveEvent(self, event):
    #     x, y = event.x(), event.y()
    #     AKUEnqueuePointerEvent ( 0, POINTER, x, y )

    # def mousePressEvent(self, event):
    #     button = event.button()

    #     if button == QtCore.Qt.LeftButton:
    #         AKUEnqueueButtonEvent ( 0, MOUSE_LEFT, True)
    #     elif button == QtCore.Qt.RightButton:
    #         AKUEnqueueButtonEvent ( 0, MOUSE_RIGHT, True)
    #     elif button == QtCore.Qt.MidButton:
    #         AKUEnqueueButtonEvent ( 0, MOUSE_MIDDLE, True)

    # def mouseReleaseEvent(self, event):
    #     button = event.button()

    #     if button == QtCore.Qt.LeftButton:
    #         AKUEnqueueButtonEvent ( 0, MOUSE_LEFT, False)
    #     elif button == QtCore.Qt.RightButton:
    #         AKUEnqueueButtonEvent ( 0, MOUSE_RIGHT, False)
    #     elif button == QtCore.Qt.MidButton:
    #         AKUEnqueueButtonEvent ( 0, MOUSE_MIDDLE, False)

    # def keyPressEvent(self, event):
    #     key = event.key()
        
    #     if key == QtCore.Qt.Key_Shift:
    #         AKUEnqueueKeyboardKeyEvent(0, KEYBOARD, KeyCodes["MOAI_KEY_SHIFT"], True)
    #     elif key == QtCore.Qt.Key_Control:
    #         AKUEnqueueKeyboardKeyEvent(0, KEYBOARD, KeyCodes["MOAI_KEY_CONTROL"], True)
    #     elif key == QtCore.Qt.Key_Alt:
    #         AKUEnqueueKeyboardKeyEvent(0, KEYBOARD, KeyCodes["MOAI_KEY_ALT"], True)
    #     else:
    #         key = self.normalizeKeyCode(key)
    #         if key:
    #             AKUEnqueueKeyboardKeyEvent(0, KEYBOARD, key, False)


    # def keyReleaseEvent(self, event):
    #     key = event.key()

    #     if key == QtCore.Qt.Key_Shift:
    #         AKUEnqueueKeyboardKeyEvent(0, KEYBOARD, KeyCodes["MOAI_KEY_SHIFT"], False)
    #     elif key == QtCore.Qt.Key_Control:
    #         AKUEnqueueKeyboardKeyEvent(0, KEYBOARD, KeyCodes["MOAI_KEY_CONTROL"], False)
    #     elif key == QtCore.Qt.Key_Alt:
    #         AKUEnqueueKeyboardKeyEvent(0, KEYBOARD, KeyCodes["MOAI_KEY_ALT"], False)
    #     else:
    #         key = self.normalizeKeyCode(key)
    #         if key:
    #             AKUEnqueueKeyboardKeyEvent(0, KEYBOARD, key, False)

    # Wrap key code to MOAI accepted range [0, 511]
    def normalizeKeyCode(self, key):
        if key >= 0x01000000:
            key = 0x100 + (key & ~0x01000000)
        if key >= 512:
            return False
        return key

    # Game Management API
    def setupContext(self):
        if self._context != 0:
            AKUSetContext ( self._context )
            # AKUPause( False )

    def deleteContext(self):
        if self._context != 0:
            AKUDeleteContext ( self._context )
            self._context = 0
        self.contextReady = False

    def refreshContext(self):
        self.deleteContext()

        AKUAppInitialize ()
        AKUModulesAppInitialize ()

        self._context = AKUCreateContext ()
        AKUModulesContextInitialize ()
        self.contextReady = True

        AKUInitializeCallbacks ()

        AKUSetInputConfigurationName ( "AKUQtEditor" );

        AKUReserveInputDevices          ( 1 );
        AKUSetInputDevice               ( 0, "device" );
        
        AKUReserveInputDeviceSensors    ( 0, TOTAL );
        AKUSetInputDeviceKeyboard       ( 0, KEYBOARD,     "keyboard" );
        AKUSetInputDevicePointer        ( 0, POINTER,      "pointer" );
        AKUSetInputDeviceWheel          ( 0, MOUSE_WHEEL,  "wheel" );
        AKUSetInputDeviceButton         ( 0, MOUSE_LEFT,   "mouseLeft" );
        AKUSetInputDeviceButton         ( 0, MOUSE_MIDDLE, "mouseMiddle" );
        AKUSetInputDeviceButton         ( 0, MOUSE_RIGHT,  "mouseRight" );

        self.runString("os.setlocale('C')")
        AKUModulesRunLuaAPIWrapper ()
        AKUInitParticlePresets ()
        self.runString("MOAIEnvironment.setValue('horizontalResolution', %d) MOAIEnvironment.setValue('verticalResolution', %d)" %
            ( int ( self.size().width() ), int ( self.size().height()) ) )
        
        self.lua = LuaRuntime()
        self.lua.init()

        moaipy.callback_SetSimStep = self.setSimStep
        moaipy.callback_OpenWindow = self.openWindow

        self.windowReady = False
        self.initReady = False

        if not self.timer:
            timer = QtCore.QBasicTimer()
            timer.start(1000 * AKUGetSimStep(), self)
            self.timer = timer

    def loadEditorFramework(self):
        luaEditorFrameworkPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../lua/editor/?.lua")        
        self.runString("package.path = '%s;' .. package.path" % luaEditorFrameworkPath)
        self.runString("""
            MOAIApp = MOAIApp or require ('MOAIApp')
            MOAINotificationsIOS = MOAINotifications or require('MOAINotifications')
        """)

    def loadLuaFramework(self, dir_path):
        if dir_path:
            luaFrameworkPath = os.path.join(dir_path, "framework/?.lua")
            if os.path.exists(luaFrameworkPath):
                self.runString("package.path = '%s;' .. package.path" % luaFrameworkPath)
                self.runString("""  require ('include')""" )
                self.coloredlog = ColoredLog(self.lua)
                self.fileDialog = FileDialog(self.lua, self)

    def openWindow(self, title, width, height):
        AKUDetectGfxContext()

        w = self.size().width()
        h = self.size().height()
        AKUSetScreenSize(w, h)
        AKUSetViewSize(w, h)

        self.windowReady = True

    def pause(self, value):
        AKUPause ( value )

    def finalize(self):
        self.windowReady = False
        self.glReady = False
        self.timer.stop()
        AKUModulesAppFinalize()
        # AKUAppFinalize()

    def setSimStep(self, step):
        self.timer.start(step * 1000, self)

    def setWorkingDirectory(self, path):
        AKUSetWorkingDirectory(path)

    def runScript(self, fileName):
        AKURunScript(fileName)

    def runString(self, luaStr):
        AKURunString(luaStr)

    def setTraceback(self, func):
        setFunc = self.lua.eval("function(func) _G.pythonLogFunc = func end")
        setFunc(func)
        self.lua.execute("MOAISim.setTraceback(function(err) _G.pythonLogFunc(debug.traceback(err, 2)) return 'hello from python' end)")

    def setPrint(self, before, after):
        setFunc = self.lua.eval("""function(before, after) 
            _print = print
            print = function(...)
                before()
                _print(...)
                after()
            end
        end""")
        setFunc(before, after)