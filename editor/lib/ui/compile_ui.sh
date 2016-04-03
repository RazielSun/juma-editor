#!/bin/bash

pyside-uic -o statsdock_ui.py statsdock.ui
pyside-uic -o runstring_dock_ui.py runstring_dock.ui
pyside-uic -o object_container_ui.py object_container.ui
pyside-uic -o color_picker_ui.py color_picker.ui
pyside-uic -o search_view_ui.py search_view.ui
pyside-uic -o debug_draw_item_ui.py debug_draw_item.ui