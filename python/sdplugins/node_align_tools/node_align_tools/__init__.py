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

from functools import partial
import os
import weakref

import sd
from sd.api import SDArray, SDNode
from sd.api.sdhistoryutils import SDHistoryUtils
from sd.api.qtforpythonuimgrwrapper import QtForPythonUIMgrWrapper
from sd.tools import graphlayout

from PySide6 import QtCore, QtGui, QtWidgets, QtSvg

import typing
from typing import ClassVar, Optional

DEFAULT_ICON_SIZE = 24


def loadSvgIcon(iconName: str, size: int) -> Optional[QtGui.QIcon]:
    currentDir = os.path.dirname(__file__)
    iconFile = os.path.abspath(os.path.join(currentDir, iconName + '.svg'))

    svgRenderer = QtSvg.QSvgRenderer(iconFile)
    if svgRenderer.isValid():
        pixmap = QtGui.QPixmap(QtCore.QSize(size, size))

        if not pixmap.isNull():
            pixmap.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(pixmap)
            svgRenderer.render(painter)
            painter.end()

        return QtGui.QIcon(pixmap)

    return None


class NodeAlignmentToolBar(QtWidgets.QToolBar):
    # Ideally, here we should use typings.Self instead of
    # QtWidgets.QToolBar as the value type of the array.
    # Unfortunately, typings.Self is not available in the
    # Python version we use.
    __toolbarList: ClassVar[dict[int,
                                 weakref.ReferenceType[QtWidgets.QToolBar]]] = {}

    def __init__(self, graphViewID: int, uiMgr: QtForPythonUIMgrWrapper):
        super(NodeAlignmentToolBar, self).__init__(
            parent=uiMgr.getMainWindow())

        self.setObjectName("allegorithmic.com.node_alignment_toolbar")

        self.__graphViewID = graphViewID
        self.__uiMgr = uiMgr

        act = self.addAction(loadSvgIcon(
            "align_horizontal", DEFAULT_ICON_SIZE), "HAlign")
        act.setShortcut(QtGui.QKeySequence('H'))
        act.setToolTip(self.tr("Align the selected nodes horizontally"))
        act.triggered.connect(self.__onHorizAlignNodes)

        act = self.addAction(loadSvgIcon(
            "align_vertical", DEFAULT_ICON_SIZE), "VAlign")
        act.setShortcut(QtGui.QKeySequence('V'))
        act.setToolTip(self.tr("Align the selected nodes vertically"))
        act.triggered.connect(self.__onVertAlignNodes)

        act = self.addAction(loadSvgIcon(
            "align_snap", DEFAULT_ICON_SIZE), "Snap")
        act.setShortcut(QtGui.QKeySequence('S'))
        act.setToolTip(self.tr("Snap the selected nodes on grid"))
        act.triggered.connect(self.__onSnapNodes)

        # We need this cast because we cannot use typings.Self. See comment above.
        self.__toolbarList[graphViewID] = weakref.ref(
            typing.cast(QtWidgets.QToolBar, self))

        self.destroyed.connect(
            partial(NodeAlignmentToolBar.__onToolbarDeleted, graphViewID=graphViewID))

    def tooltip(self) -> str:
        return self.tr("Align Tools")

    def __onHorizAlignNodes(self) -> None:
        selectedNodes = self.__getSelectedNodes()
        if not selectedNodes or len(selectedNodes) < 2:
            return

        with SDHistoryUtils.UndoGroup(self.tr("Align nodes")):
            graphlayout.alignSDNodes(
                selectedNodes,
                graphlayout.AlignmentDirection.Horizontal)

    def __onVertAlignNodes(self) -> None:
        selectedNodes = self.__getSelectedNodes()
        if not selectedNodes or len(selectedNodes) < 2:
            return

        with SDHistoryUtils.UndoGroup(self.tr("Align nodes")):
            graphlayout.alignSDNodes(
                selectedNodes,
                graphlayout.AlignmentDirection.Vertical)

    def __onSnapNodes(self) -> None:
        selectedNodes = self.__getSelectedNodes()
        if not selectedNodes or len(selectedNodes) == 0:
            return

        with SDHistoryUtils.UndoGroup(self.tr("Snap node(s) to grid")):
            graphlayout.snapSDNodes(selectedNodes)

    def __getSelectedNodes(self) -> Optional[SDArray[SDNode]]:
        return self.__uiMgr.getGraphSelectedNodesFromGraphViewID(self.__graphViewID)

    @classmethod
    def __onToolbarDeleted(cls, graphViewID: int) -> None:
        del cls.__toolbarList[graphViewID]

    @classmethod
    def removeAllToolbars(cls) -> None:
        for toolbarRef in cls.__toolbarList.values():
            toolbar = toolbarRef()
            if toolbar:
                toolbar.deleteLater()


def onNewGraphViewCreated(graphViewID: int, uiMgr: QtForPythonUIMgrWrapper) -> None:
    # Ignore graph types not supported by the Python API.
    if not uiMgr.getCurrentGraph():
        return

    toolbar = NodeAlignmentToolBar(graphViewID, uiMgr)
    uiMgr.addToolbarToGraphView(
        graphViewID,
        toolbar,
        icon=loadSvgIcon("align_tools", DEFAULT_ICON_SIZE),
        tooltip=toolbar.tooltip())


graphViewCreatedCallbackID: int = 0


def initializeSDPlugin() -> None:
    ctx = sd.getContext()
    app = ctx.getSDApplication()
    uiMgr = app.getQtForPythonUIMgr()

    if uiMgr:
        global graphViewCreatedCallbackID
        graphViewCreatedCallbackID = uiMgr.registerGraphViewCreatedCallback(
            partial(onNewGraphViewCreated, uiMgr=uiMgr))


def uninitializeSDPlugin() -> None:
    ctx = sd.getContext()
    app = ctx.getSDApplication()
    uiMgr = app.getQtForPythonUIMgr()

    if uiMgr:
        global graphViewCreatedCallbackID
        uiMgr.unregisterCallback(graphViewCreatedCallbackID)
        NodeAlignmentToolBar.removeAllToolbars()
