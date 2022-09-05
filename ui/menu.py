from PySide6.QtWidgets import QMenu, QMenuBar
from PySide6.QtGui import QAction, QKeySequence

def createMenuBar(parent):
        menuBar = parent.menuBar()
        menuBar.setNativeMenuBar(False)

        fileMenu = menuBar.addMenu("File")
        editMenu = menuBar.addMenu("Edit")

        createFileMenu(fileMenu, parent)
        createEditMenu(editMenu, parent)

def createFileMenu(menu, parent):
    openAction = QAction("Open video...", parent)
    openAction.setShortcut(QKeySequence.Open)

    checkAction = QAction("Check for updates...", parent)

    exportAction = QAction("Export Collection...", parent)
    exportAction.setShortcut(QKeySequence("Ctrl+E"))

    settingsAction = QAction("Preferences...", parent)
    settingsAction.setShortcut(QKeySequence.Preferences)

    quitAction = QAction("\0Quit", parent)
    quitAction.setShortcut(QKeySequence.Quit)

    menu.addAction(openAction)
    menu.addAction(checkAction)
    menu.addAction(exportAction)
    menu.addSeparator()
    menu.addAction(settingsAction)
    menu.addSeparator()
    menu.addAction(quitAction)

def createEditMenu(menu, parent):
    changeCameraAction = QAction("Change camera...", parent)
    menu.addAction(changeCameraAction)
