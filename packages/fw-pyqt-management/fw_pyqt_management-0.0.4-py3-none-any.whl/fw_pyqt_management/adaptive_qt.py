"""Adaptive import of PyQt5 or PyQt6."""
# ruff: noqa
from importlib.util import find_spec

# fmt: off
"""Import the available version of PyQt."""
# Check if PyQt6 is installed
if find_spec("PyQt6"):
    from PyQt6 import QtGui, QtWidgets
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QDialogButtonBox,
        QMenu,
        QMessageBox,
    )
    NoEditTriggers = QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
    ExtendedSelection = QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
    CustomContextMenu = Qt.ContextMenuPolicy.CustomContextMenu
    WaitCursor = Qt.CursorShape.WaitCursor
    Ok_btn = QMessageBox.StandardButton.Ok
# Else, check if PyQt5 is installed
elif find_spec("PyQt5"):
    from PyQt5 import QtGui, QtWidgets
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QAbstractItemView,
        QApplication,
        QDialogButtonBox,
        QMenu,
        QMessageBox,
    )
    NoEditTriggers = QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
    ExtendedSelection = QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection
    CustomContextMenu = Qt.ContextMenuPolicy.CustomContextMenu
    WaitCursor = Qt.CursorShape.WaitCursor
    Ok_btn = QMessageBox.StandardButton.Ok
# Else, use the 3D Slicer alias for PyQt
else:
    from PythonQt import QtGui
    from PythonQt.QtCore import Qt
    from qt import QAbstractItemView, QApplication, QMenu, QMessageBox
    NoEditTriggers = QAbstractItemView.NoEditTriggers
    ExtendedSelection = QAbstractItemView.ExtendedSelection
    CustomContextMenu = Qt.CustomContextMenu
    WaitCursor = Qt.WaitCursor
    Ok_btn = QMessageBox.Ok
# fmt: on
