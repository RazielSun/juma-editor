#!/bin/bash

pyside-uic -o statsdock_ui.py statsdock.ui
pyside-uic -o object_container_ui.py object_container.ui
pyside-uic -o color_picker_ui.py color_picker.ui
pyside-uic -o debugdock_ui.py debugdock.ui
pyside-uic -o search_view_ui.py search_view.ui