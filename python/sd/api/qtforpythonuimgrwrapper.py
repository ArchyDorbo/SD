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

from __future__ import annotations

import sd
from sd.api import SDArray, SDGraph, SDGraphObject, SDNode
from sd.api.sdapiobject import SDAPIObject
from sd.api.sdtexture import SDTexture
from sd.api.sduimgr import SDUIMgr

import shiboken6
from PySide6 import QtGui, QtWidgets

from typing import Callable, Optional


class QtForPythonUIMgrWrapper(object):
    def __init__(self, uiMgr):
        self.__mUiMgr = uiMgr

    def getMainWindow(self) -> Optional[QtWidgets.QMainWindow]:
        """
        Get the main window
        """
        return shiboken6.wrapInstance(self.__mUiMgr.getMainWindowPtr(), QtWidgets.QMainWindow)

    def newMenu(self, menuTitle: str, objectName: str) -> QtWidgets.QMenu:
        """
        Create a new menu in the application menu bar

        :param menuTitle: The menu title
        :param objectName: The internal object name of the menu
        """
        return shiboken6.wrapInstance(self.__mUiMgr.newMenu(menuTitle, objectName), QtWidgets.QMenu)

    def findMenuFromObjectName(self, objectName: str) -> Optional[QtWidgets.QMenu]:
        """
        Return an existing menu in the application menu bar

        :param objectName: The internal object name of the menu
        """
        menuPtr = self.__mUiMgr.findMenuFromObjectName(objectName)
        if menuPtr:
            return shiboken6.wrapInstance(menuPtr, QtWidgets.QMenu)

    def deleteMenu(self, objectName: str) -> None:
        """
        Remove a menu from the application menu bar

        :param objectName: The internal object name of the menu
        """
        self.__mUiMgr.deleteMenu(objectName)

    def newDockWidget(self, identifier: str, title: str) -> QtWidgets.QWidget:
        """
        Create a new dock widget

        :param identifier: Dock internal identifier (must be unique)
        :param title: Dock title
        """
        return shiboken6.wrapInstance(self.__mUiMgr.newDockWidget(identifier, title), QtWidgets.QWidget)

    def addToolbarToGraphView(
            self,
            graphViewID: int,
            toolbar: QtWidgets.QToolBar,
            icon: Optional[QtGui.QIcon] = None,
            tooltip: Optional[str] = None) -> None:
        """
        Add a toolbar to a graph view

        :param graphViewID: Graph view identifier
        :param toolbar: Toolbar to add to the widget
        :param toolbar: The toolbar icon
        :param tooltip: The toolbar tooltip
        """

        action = toolbar.toggleViewAction()

        if icon:
            action.setIcon(icon)

        if tooltip:
            action.setToolTip(tooltip)

        return self.__mUiMgr.addToolbarToGraphView(
            graphViewID,
            shiboken6.getCppPointer(toolbar)[0],
            shiboken6.getCppPointer(action)[0])

    def addActionToGraphViewToolbar(self, graphViewID : int, action : QtGui.QAction) -> None:
        """
        Add an action to a graph view toolbar

        :param graphViewID: Graph view identifier
        :param action: QAction to add to the toolbar
        """
        return self.__mUiMgr.addActionToGraphViewToolbar(
            graphViewID,
            shiboken6.getCppPointer(action)[0])

    def getCurrentGraph(self) -> Optional[SDGraph]:
        """
        Get the current graph (can be null)
        """
        return self.__mUiMgr.getCurrentGraph()

    @sd.deprecatedMethod("QtForPythonUIMgrWrapper", "This method is deprecated. Please use QtForPythonUIMgrWrapper.getCurrentGraphSelectedNodes instead")
    def getCurrentGraphSelection(self) -> Optional[SDArray[SDNode]]:
        """
        Get the selected nodes in the current graph
        """
        return self.__mUiMgr.getCurrentGraphSelectedNodes()

    def getCurrentGraphSelectedNodes(self) -> Optional[SDArray[SDNode]]:
        """
        Get the selected nodes in the current graph
        """
        return self.__mUiMgr.getCurrentGraphSelectedNodes()

    def getCurrentGraphSelectedObjects(self) -> Optional[SDArray[SDGraphObject]]:
        """
        Get the selected graph objects in the current graph
        """
        return self.__mUiMgr.getCurrentGraphSelectedObjects()

    def getGraphFromGraphViewID(self, graphViewID: int) -> Optional[SDGraph]:
        """
        Get the graph from a Graph View ID (can be null)

        :param graphViewID: The Graph View ID
        """
        return self.__mUiMgr.getGraphFromGraphViewID(graphViewID)

    @sd.deprecatedMethod("QtForPythonUIMgrWrapper", "This method is deprecated. Please use QtForPythonUIMgrWrapper.getGraphSelectedNodesFromGraphViewID instead")
    def getCurrentGraphSelectionFromGraphViewID(self, graphViewID: int) -> Optional[SDGraph]:
        """
        Get the selected nodes in a graph from a Graph View ID (can be null)

        :param graphViewID: The Graph View ID
        """
        return self.__mUiMgr.getGraphSelectedNodesFromGraphViewID(graphViewID)

    def getGraphSelectedNodesFromGraphViewID(self, graphViewID: int) -> Optional[SDArray[SDNode]]:
        """
        Get the selected nodes in a graph from a Graph View ID (can be null)

        :param graphViewID: The Graph View ID
        """
        return self.__mUiMgr.getGraphSelectedNodesFromGraphViewID(graphViewID)

    def getGraphSelectedObjectsFromGraphViewID(self, graphViewID: int) -> Optional[SDArray[SDGraphObject]]:
        """
        Get the selected graph objects in the current graph

        :param graphViewID: The Graph View ID
        """
        return self.__mUiMgr.getGraphSelectedObjectsFromGraphViewID(graphViewID)

    def addActionToExplorerToolbar(self, explorerID: int, action: QtGui.QAction) -> None:
        """
        Add an action to an explorer toolbar

        :param explorerID: Explorer identifier
        :param action: action
        """
        return self.__mUiMgr.addActionToExplorerToolbar(
            explorerID,
            shiboken6.getCppPointer(action)[0])

    def getExplorerSelection(self, explorerID: int) -> SDArray[SDAPIObject]:
        """
        Return the currently selected items in the explorer panel

        :param explorerID: Explorer identifier
        """
        return self.__mUiMgr.getExplorerSelection(explorerID)

    def registerGraphViewCreatedCallback(self, callable: Callable[[int], None]) -> int:
        """
        Register a callback to be called when a new graph view is created
        Returns a callback ID that can be used later to unregister the callback

        :param callable: Function to call when a new graph view is created
        """
        return self.__mUiMgr.registerGraphViewCreatedCallback(callable)

    def registerExplorerCreatedCallback(self, callable: Callable[[int], None]) -> int:
        """
        Register a callback to be called when a new explorer is created
        Returns a callback ID that can be used later to unregister the callback

        :param callable: Function to call when a new explorer is created
        """
        return self.__mUiMgr.registerExplorerCreatedCallback(callable)

    def registerExplorerSelectionChangedCallback(self, callable: Callable[[int], None]) -> int:
        """
        Register a callback to be called when the explorer selection changed
        Returns a callback ID that can be used later to unregister the callback

        :param callable: Function to call when the explorer selection changed
        """
        return self.__mUiMgr.registerExplorerSelectionChangedCallback(callable)

    def unregisterCallback(self, callbackID: int) -> None:
        """
        Unregister a callback

        :param callbackID: The callback ID of the callback to unregister
        """
        self.__mUiMgr.unregisterCallback(callbackID)

    @staticmethod
    def convertSDTextureToQImage(sdTexture: SDTexture) -> QtGui.QImage:
        """
        Convert a SDTexture into a QImage

        :param sdTexture: The texture that will be converted
        """
        image = QtGui.QImage()
        SDUIMgr.convertSDTextureToQImage(
            sdTexture, shiboken6.getCppPointer(image)[0])
        return image

    def getGraphView(self, graphViewID : int) -> QtWidgets.QWidget:
        """
        Return the Widget that match the specified graphViewID

        :param graphViewID: Graph view identifier
        """
        return shiboken6.wrapInstance(graphViewID, QtWidgets.QWidget)
