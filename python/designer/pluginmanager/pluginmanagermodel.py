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

import sd
from sd.api.sdplugin import SDPluginStatus

import shiboken6
from PySide6 import QtCore, QtGui, QtWidgets, QtSvg

# Constants.

DEFAULT_ICON_SIZE = 20
PLUGIN_STATE_UPDATE_DELAY = 250  # in microseconds.


def _loadSvgIcon(iconName, size):
    svgRenderer = QtSvg.QSvgRenderer(iconName)
    if svgRenderer.isValid():
        pixmap = QtGui.QPixmap(QtCore.QSize(size, size))

        if not pixmap.isNull():
            pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pixmap)
            svgRenderer.render(painter)
            painter.end()

        return QtGui.QIcon(pixmap)

    return None


class PluginTreeItem(QtCore.QObject):
    """
    Represents an item in the model. It can be
    the root item, a plugin directory or a plugin.
    """

    __failedIcon = _loadSvgIcon(
        os.path.join(os.path.dirname(__file__), "..",
                     "icons", "warning_red.svg"),
        DEFAULT_ICON_SIZE)
    __progressIcon = _loadSvgIcon(
        os.path.join(os.path.dirname(__file__), "..",
                     "icons", "icon_reloading.svg"),
        DEFAULT_ICON_SIZE)

    def __init__(self, header=None, pluginDir=None, plugin=None, parent=None):
        super(PluginTreeItem, self).__init__()

        self.__children = []
        self.__parent = parent

        if header:  # root item.
            assert(pluginDir == None)
            assert(plugin == None)
            assert(parent == None)
            self.__header = header
        elif pluginDir:
            assert(header == None)
            assert(plugin == None)
            assert(parent != None)
            self.__pluginDir = pluginDir
        elif plugin:
            assert(header == None)
            assert(pluginDir == None)
            assert(parent != None)
            self.__plugin = plugin
            self.__updating = False
        else:
            # We shouldn't get here.
            assert(False)

        if parent:
            parent.addChild(self)

    #
    # Root item methods.
    #

    def findItemForDirectory(self, pluginDir):
        assert(self.isRoot())

        for child in self.__children:
            if child.pluginDirectory() == pluginDir:
                return child

        return None

    def findItemForPlugin(self, plugin):
        assert(self.isRoot())

        for child in self.__children:
            for item in child.__children:
                if item.plugin().getName() == plugin.getName():
                    if item.plugin().getDirectory() == plugin.getDirectory():
                        return item

        return None

    #
    # Plugin directory methods.
    #

    def pluginDirectory(self):
        return self.__pluginDir

    #
    # Plugin methods.
    #

    def plugin(self):
        return self.__plugin

    def isLoaded(self):
        if self.__plugin:
            return self.__plugin.getStatus() == SDPluginStatus.Loaded

        return False

    def loadFailed(self):
        if self.__plugin:
            return self.__plugin.getStatus() == SDPluginStatus.LoadFailed

        return False

    def setUpdating(self, updating):
        self.__updating = updating

    #
    # Hierarchy related methods.
    #

    def parent(self):
        return self.__parent

    def addChild(self, child):
        self.__children.append(child)

    def childCount(self):
        return len(self.__children)

    def child(self, row):
        return self.__children[row]

    def isRoot(self):
        return self.__parent == None

    def isLeaf(self):
        # We cannot test for childCount == 0 here because for a short amount of time
        # when adding new plugin directories to the model, they don't have any children.
        try:
            return self.__plugin != None
        except:
            return False

    def isInternal(self):
        if self.isRoot() or self.isLeaf():
            return False

        return True

    #
    # AbstractItemModel related methods.
    #

    def columnCount(self):
        return 2

    def data(self, column, role):
        # Tree Header.
        if self.isRoot():
            if column < len(self.__header):
                return self.__header[column]

        if role == QtCore.Qt.DisplayRole:
            if column == 0:
                if self.isLeaf():
                    return self.plugin().getName()
                else:
                    return self.pluginDirectory()

        elif role == QtCore.Qt.CheckStateRole:
            if column == 1 and self.isLeaf():
                if self.isLoaded():
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

        elif role == QtCore.Qt.DecorationRole:
            if column == 1 and self.isLeaf():
                if self.__updating:
                    return self.__progressIcon
                elif self.loadFailed():
                    return self.__failedIcon

        elif role == QtCore.Qt.ToolTipRole:
            if column == 0 and self.isInternal():
                return self.pluginDirectory()
            if self.isLeaf():
                if self.loadFailed():
                    return self.plugin().getLastErrorMessage()
                elif self.isLoaded():
                    return self.tr("Loaded.")
                else:
                    return self.tr("Not loaded.")

        return None

    def parent(self):
        return self.__parent

    # Return the index of this item into its parent children list.
    def parentRowIndex(self):
        if self.__parent:
            return self.__parent.__children.index(self)

        return 0

    #
    # Utility methods.
    #

    def showInFileBrowser(self):
        if self.isRoot():
            return

        if self.isLeaf():
            dirToShow = self.parent().pluginDirectory()
        else:
            dirToShow = self.pluginDirectory()

        import webbrowser
        webbrowser.open("file://" + dirToShow)


class PluginTreeModel(QtCore.QAbstractItemModel):
    """
    Model for the PluginManagerDialog QTreeView.
    """

    def __init__(self, pluginMgr, parent=None):
        super(PluginTreeModel, self).__init__(parent)
        self.__pluginMgr = pluginMgr
        self.refreshModel()

    #
    # Methods reimplemented from QAbstractItemModel
    #

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.__rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()
        return item.data(index.column(), role)

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        indexFlags = super(PluginTreeModel, self).flags(index)

        if index.column() == 1:
            item = index.internalPointer()

            if item.isLeaf():
                indexFlags |= QtCore.Qt.ItemIsUserCheckable

        return indexFlags

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.__rootItem.data(section, None)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.__rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.__rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.parentRowIndex(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.__rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False

        if role == QtCore.Qt.CheckStateRole:
            item = index.internalPointer()
            if item.isLeaf():
                if value == QtCore.Qt.Checked:
                    self.__loadPlugin(
                        item,
                        index,
                        item.plugin().getName(),
                        item.plugin().getDirectory())
                else:
                    self.__unloadPlugin(item, index)

        return False

    #
    # Utility methods.
    #

    def reloadPlugin(self, index):
        if not index.isValid():
            return

        item = index.internalPointer()
        assert(item.isLeaf())
        assert(item.isLoaded())

        self.__pluginMgr.unloadPlugin(item.plugin())
        parentItem = item.parent()
        pluginDir = parentItem.pluginDirectory()

        self.__pluginMgr.loadPlugin(item.plugin().getName(), pluginDir)
        self.dataChanged.emit(index, index)

    # Called after a new plugin has been loaded, updates the model.
    def newPluginLoaded(self, plugin):
        item = self.__rootItem.findItemForPlugin(plugin)

        if item:
            # We loaded this plugin before, find and update the item.
            parentItem = item.parent()
            parentIndex = self.index(
                parentItem.parentRowIndex(), 0, QtCore.QModelIndex())
            index = self.index(item.parentRowIndex(), 0, parentIndex)
            self.dataChanged.emit(index, index)
        else:
            # This is a new plugin.
            pluginDir = plugin.getDirectory()
            parentItem = self.__rootItem.findItemForDirectory(pluginDir)

            if not parentItem:
                # Create new plugin directory item.
                self.beginInsertRows(QtCore.QModelIndex(
                ), self.__rootItem.childCount(), self.__rootItem.childCount())
                parentItem = PluginTreeItem(
                    pluginDir=pluginDir, parent=self.__rootItem)
                self.endInsertRows()

            # Create a new plugin item.
            parentIndex = self.index(
                parentItem.parentRowIndex(), 0, QtCore.QModelIndex())
            self.beginInsertRows(
                parentIndex, parentItem.childCount(), parentItem.childCount())
            pluginItem = PluginTreeItem(plugin=plugin, parent=parentItem)
            self.endInsertRows()

        # Return the index to the plugin directory.
        return parentIndex

    # Reset the model and re-create all items.
    def refreshModel(self):
        self.beginResetModel()

        self.__rootItem = PluginTreeItem(
            header=[self.tr("Plugins"), self.tr("Loaded")])

        plugins = self.__pluginMgr.getPlugins()

        for p in plugins:
            pluginDir = p.getDirectory()
            parentItem = self.__rootItem.findItemForDirectory(pluginDir)

            if not parentItem:
                parentItem = PluginTreeItem(
                    pluginDir=pluginDir, parent=self.__rootItem)

            PluginTreeItem(plugin=p, parent=parentItem)

        self.endResetModel()

    #
    # Internal (private) methods.
    #

    def __loadPlugin(self, item, index, pluginName, pluginDir):
        item.setUpdating(True)
        self.dataChanged.emit(index, index)
        self.__pluginMgr.loadPlugin(pluginName, pluginDir)
        self.__schedulePluginStateUpdate(item, index)

    def __unloadPlugin(self, item, index):
        item.setUpdating(True)
        self.dataChanged.emit(index, index)
        self.__pluginMgr.unloadPlugin(item.plugin())
        self.__schedulePluginStateUpdate(item, index)

    def __schedulePluginStateUpdate(self, item, index):
        QtCore.QTimer.singleShot(
            PLUGIN_STATE_UPDATE_DELAY, lambda: self.__updatePluginState(item, index))

    def __updatePluginState(self, item, index):
        item.setUpdating(False)
        self.dataChanged.emit(index, index)
