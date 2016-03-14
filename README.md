# Juma MOAI Editor

### Based on
Vavius IDE https://github.com/Vavius/moai-ide
Tommo IDE https://github.com/pixpil/gii

### Features
* Host for latest MOAI SDK (currently 1.7)

### Running
    cd juma-editor
    ./juma
    ./juma ide

    Use file->open or cmd+O to open any moai main.lua file. 

### Roadmap
* Create DebugDraw DockWidget
* Create RunString DockWidget

### RobotStyle Theme
* Top Color - #323232
* Widget Color - #282828
* Dark Color - #1E1E1E
* Label - #f0f0f0
* Disabled - #999999
* Mint - #00af95
* Yellow(select) - #eda900
* Red(close) - #b70000
* Red - #ff0a0c



# About Vavius version Editor
This editor is a Python-Qt based host for MOAI SDK. 
The main idea behind all this is pretty easy: 
* I wanted to add editor features to MOAI SDK with live game preview - like most of 3d AAA engines have
* Editors tend to have pretty complicated GUI - coding all this in Lua with MOAI classes is a pain, also some performance issues could arise, so better to look at existing frameworks and run MOAI as GL View
* Qt is one of the most complete frameworks for crossplatform GUI applications
* GUI stuff is easier to code and tune with dynamic language such as Python (may consider QtScript as well)

### Setup
Since all used technologies are cross platform in nature this thing should work on Windows, Linux, OS X without problems. 
However, I've only tested this on OS X 10.8 and 10.9. To build on other platforms you'll need to compile MOAI as python module, read [Technical details](#technical-details) for more info. 

### There are tons of dependencies: 
* Qt 4.8.5 and PySide 1.2.1: https://qt-project.org/wiki/PySide_Binaries_MacOSX (sometimes 1.2.1 does not work, then 1.1.1 can be used with Qt 4.8.5)
* hanappe/flower based lua framework from here: https://github.com/Vavius/moai-framework
* PyOpenGL-3.0.2 and Cython-0.19.2 - included in this repo as archives

### Installation
1. Install Qt, then PySide bindings
2. Unzip and install include/PyOpenGL-3.0.2.zip (python setup.py install)
3. Clone Lua framework https://github.com/Vavius/moai-framework, then link or copy src/ folder from it to editor/lua/moai-framework/src/

### Technical details
MOAI is compiled as python module with Cython. Lua communication implemented with Lupa. There are some modifications to Lupa in order to make it use existing lua_State from MOAI. 
Python module sources located in dev/moaipy:
* static moai libs - I suppose they need to be recompiled for your current platform
* cmoai.pxd - cython header file for AKU calls
* moaipy.pyx - here we wrap AKU functions to be called from python
* _lupa.pyx - modified lupa

# About Tommo version Editor
This editor is a Python-Qt based host for MOAI SDK.

### Technical details