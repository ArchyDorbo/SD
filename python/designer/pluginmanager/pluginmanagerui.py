##########################################################################
# ADOBE CONFIDENTIAL
# ___________________
#  Copyright 2010-2024 Adobe
#  All Rights Reserved.
# * NOTICE:  Adobe permits you to use, modify, and distribute this file in
# accordance with the terms of the Adobe license agreement accompanying it.
# If you have received this file from a source other than Adobe,
# then your use, modification, or distribution of it requires the prior
# written permission of Adobe.
##########################################################################

import os
import sys
import json

import sd
from PySide6 import QtCore, QtGui, QtWidgets

from .pluginmanagermodel import PluginTreeModel
from .installpackage import installPackage


class PluginManagerDialog(QtWidgets.QDialog):
    """
    Plugin manager dialog.
    """

    def __init__(self, pluginMgr, parent=None):
        super(PluginManagerDialog, self).__init__(parent=parent)

        self.__pluginMgr = pluginMgr

        self.setWindowTitle(self.tr("Plugin Manager"))
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        # Create the widgets.
        dialogLayout = QtWidgets.QVBoxLayout(self)

        filterEntry = QtWidgets.QLineEdit()
        filterEntry.setPlaceholderText(self.tr("Filter"))
        dialogLayout.addWidget(filterEntry)

        self.__model = PluginTreeModel(pluginMgr, self)
        self.__proxyModel = QtCore.QSortFilterProxyModel(self)
        self.__proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.__proxyModel.setSourceModel(self.__model)
        self.__proxyModel.setFilterKeyColumn(0)
        self.__proxyModel.setRecursiveFilteringEnabled(True)

        self.__treeView = QtWidgets.QTreeView()
        self.__treeView.setUniformRowHeights(True)
        self.__treeView.setTextElideMode(QtCore.Qt.ElideLeft)
        self.__treeView.setModel(self.__proxyModel)
        self.__treeView.header().setStretchLastSection(False)
        self.__treeView.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.__treeView.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.__treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.__treeView.setSortingEnabled(True)
        self.__treeView.expandAll()
        dialogLayout.addWidget(self.__treeView)

        buttonBox = QtWidgets.QDialogButtonBox()
        browseBtn = QtWidgets.QPushButton(self.tr("BROWSE..."))
        buttonBox.addButton(browseBtn, QtWidgets.QDialogButtonBox.ActionRole)

        installBtn = QtWidgets.QPushButton(self.tr("INSTALL..."))
        buttonBox.addButton(installBtn, QtWidgets.QDialogButtonBox.ActionRole)

        refreshBtn = QtWidgets.QPushButton(self.tr("REFRESH"))
        buttonBox.addButton(refreshBtn, QtWidgets.QDialogButtonBox.ActionRole)
        dialogLayout.addWidget(buttonBox)

        # Connect signals.
        filterEntry.textChanged.connect(self.__proxyModel.setFilterFixedString)
        browseBtn.pressed.connect(self.__onBrowsePlugin)
        installBtn.pressed.connect(self.__onInstallPlugin)
        refreshBtn.pressed.connect(self.__onRefreshModel)

        self.__treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.__treeView.customContextMenuRequested.connect(
            self.__onShowContextMenu)

    #
    # Callbacks.
    #

    def __onShowContextMenu(self, point):
        index = self.__treeView.indexAt(point)
        index = self.__proxyModel.mapToSource(index)

        if not index.isValid() or index.column() != 0:
            return

        item = index.internalPointer()
        if item.isRoot():
            return

        menu = QtWidgets.QMenu()
        menu.addAction(
            self.tr("Show in File Browser..."),
            lambda: item.showInFileBrowser())

        if item.isLeaf() and item.isLoaded():
            menu.addAction(
                self.tr("Reload"),
                lambda: self.__model.reloadPlugin(index))

        menu.exec(self.__treeView.viewport().mapToGlobal(point))

    def __onBrowsePlugin(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open Plugin"),
            None,
            self.tr("Plugin Package (pluginInfo.json);;Python Module (__init__.py);;Python Files (*.py)"))[0]

        if fileName != "":
            # Find the plugin name and the directory.
            pluginDir = os.path.dirname(fileName)
            fileName = os.path.basename(fileName)

            if fileName == "pluginInfo.json":
                # The user picked a plugin installed from a package.
                pluginName = os.path.basename(pluginDir)
            elif fileName == "__init__.py":
                # The user picked a module. Adjust the plugin name and dir.
                pluginName = os.path.basename(pluginDir)
                pluginDir = os.path.dirname(pluginDir)
            else:
                # The user picked a python file. Simply remove the python extension.
                pluginName = fileName.replace(".py", "")

            # Add the plugin dir to the path, so that it can be imported.
            if not pluginDir in sys.path:
                sys.path.append(pluginDir)

            # Load the plugin and update the model.
            plugin = self.__pluginMgr.loadPlugin(pluginName, pluginDir)
            index = self.__model.newPluginLoaded(plugin)

            # Expand the plugin directory group (by default new groups are not expanded).
            proxyIndex = self.__proxyModel.mapFromSource(index)
            self.__treeView.setExpanded(proxyIndex, True)

    def __onInstallPlugin(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Install Plugin Package"),
            None,
            self.tr("Plugin Package (*.sdplugin)"))[0]

        if fileName != "":
            try:
                index = installPackage(
                    fileName, self.__pluginMgr, self.__model)

                # Expand the new plugin directory group (by default new groups are not expanded).
                proxyIndex = self.__proxyModel.mapFromSource(index)
                self.__treeView.setExpanded(proxyIndex, True)
            except Exception as err:
                QtWidgets.QMessageBox.critical(
                    self,
                    self.tr("Error installing plugin package:"),
                    str(err),
                    QtWidgets.QMessageBox.Ok)

    def __onRefreshModel(self):
        self.__model.refreshModel()
        self.__treeView.expandAll()


class PluginManagerUI(object):
    __pluginMgr = None
    __uiMgr = None
    __menu = None
    __pluginMgrAct = None
    __dialog = None

    @classmethod
    def initialize(cls):
        ctx = sd.getContext()
        app = ctx.getSDApplication()

        cls.__uiMgr = app.getQtForPythonUIMgr()
        cls.__pluginMgr = app.getPluginMgr()

        if cls.__uiMgr:
            cls.__menu = cls.__uiMgr.findMenuFromObjectName(
                "Pfx.Editor.Menu.Tools")
            if cls.__menu:
                cls.__menu.addSeparator()

                cls.__pluginMgrAct = QtGui.QAction(
                    QtCore.QCoreApplication.translate(
                        "PluginManagerUI", "Plugin Manager..."),
                    cls.__menu)
                cls.__pluginMgrAct.triggered.connect(cls.__onShowPluginManager)
                cls.__menu.addAction(cls.__pluginMgrAct)

    @classmethod
    def uninitialize(cls):
        if cls.__pluginMgrAct:
            cls.__menu.removeAction(cls.__pluginMgrAct)

    #
    # Callbacks.
    #

    @classmethod
    def __onShowPluginManager(cls):
        if not cls.__dialog:
            cls.__dialog = PluginManagerDialog(
                cls.__pluginMgr, parent=cls.__uiMgr.getMainWindow())
            cls.__dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose, False)
            cls.__dialog.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
            cls.__dialog.resize(550, 350)

        cls.__dialog.show()
