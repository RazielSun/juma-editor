
rm -rf build dist

python setup.py py2app -A

# cp -r dist/JumaEditor.app JumaEditor.app

./dist/JumaEditor.app/Contents/MacOS/JumaEditor ide

# The first .icns file, if any, will be used as the application’s icon (equivalent to using the --iconfile option).