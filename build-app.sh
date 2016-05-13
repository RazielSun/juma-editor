#!/bin/bash

d=`dirname $0`

rm -rf build JumaEditor.app

python setup.py py2app --dist-dir ${d}