
rm -rf build dist

./Python.app/Contents/MacOS/Python setup.py py2app -A

cp dist/JumaEditor.app JumaEditor.app

./JumaEditor.app/Contents/MacOS/JumaEditor ide

# The first .icns file, if any, will be used as the application’s icon (equivalent to using the --iconfile option).