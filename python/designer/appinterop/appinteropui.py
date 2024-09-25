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

from .appinterop import AppInterop
from .sbsarpublishdialog import SBSARPublishDialog

import shiboken6
from PySide6 import QtCore, QtGui, QtWidgets, QtSvg

import sd
from sd.api.sdapplication import SDApplicationPath
from sd.api.sdgraph import SDGraph
from sd.api.sdpackage import SDPackage
from sd.api.sdresource import SDResource, EmbedMethod

import collections
from functools import partial
import logging
import os
import tempfile


logger = logging.getLogger("AppInterop")


class AppInteropActions(object):
    """
    Interop and publishing UI.
    There is one instance of this class for each explorer panel.
    """

    __icons = {}

    class InteropHistory(object):
        """
        InteropHistory Keep tracks of the last interop
        action used on a package (sending or publishing).
        """

        def __init__(self):
            self.__entries = {}
            self.__sendToEntries = {}

        def lastActionForPackage(self, pkg):
            if self.__isTemporaryPackage(pkg):
                return None

            key = (pkg.getFilePath(), pkg.getUID())
            return self.__entries.get(key, None)

        def lastSendToActionForPackage(self, pkg):
            if self.__isTemporaryPackage(pkg):
                return None

            key = (pkg.getFilePath(), pkg.getUID())
            return self.__sendToEntries.get(key, None)

        def updateLastAction(self, pkg, action):
            if self.__isTemporaryPackage(pkg):
                return

            key = (pkg.getFilePath(), pkg.getUID())
            self.__entries[key] = action

            if action.isSendToAction:
                self.__sendToEntries[key] = action

        def packageClosed(self, pkg):
            key = (pkg.getFilePath(), pkg.getUID())

            if key in self.__entries:
                del self.__entries[key]

            if key in self.__sendToEntries:
                del self.__sendToEntries[key]

        def packageSaved(self, pkgMgr):
            '''
            Update the entries list after packages are saved.
            If the user saved a package with a new path using Save as
            we need to remove it from the interop history.
            '''
            pkgList = pkgMgr.getUserPackages()

            allPkgFilePaths = set()
            for pkg in pkgList:
                path = pkg.getFilePath()
                if path != '':
                    allPkgFilePaths.add(path)

            for key in list(self.__entries.keys()):
                if not key[0] in allPkgFilePaths:
                    del self.__entries[key]

            for key in list(self.__sendToEntries.keys()):
                if not key[0] in allPkgFilePaths:
                    del self.__sendToEntries[key]

        @staticmethod
        def __isTemporaryPackage(pkg):
            return pkg.getFilePath() == ''

    class ActionEntry(object):
        """
        ActionEntry wraps a QAction and allows to
        update actions icons, enabled state and callbacks easily.
        """

        def __init__(
                self,
                label,
                objectName,
                icon,
                shortcut,
                callback,
                isSendToAction,
                showInSendContextMenu,
                appName,
                parent):
            self.action = QtGui.QAction(label, parent=parent)
            self.action.setObjectName(objectName)
            self.action.triggered.connect(self.__onActionTriggered)
            self.setCallback(callback)
            self.isSendToAction = isSendToAction
            self.showInSendContextMenu = showInSendContextMenu
            self.appName = appName
            self.setEnabled(False)

            if icon:
                self.setIcon(icon)

            if shortcut:
                self.action.setShortcut(shortcut)

            self.updateToolTip()

        @property
        def label(self):
            return self.action.text()

        def setLabel(self, label):
            self.action.setText(label)

        @property
        def icon(self):
            return self.__icon

        @property
        def enabled(self):
            return self.action.isEnabled()

        def setEnabled(self, enabled):
            self.action.setEnabled(enabled)

        def setIcon(self, icon):
            self.__icon = icon
            self.action.setIcon(self.__icon)

        def updateToolTip(self):
            if not self.action.shortcut().isEmpty():
                self.action.setToolTip(
                    '{0}    {1}'.format(
                        self.label, self.action.shortcut().toString(QtGui.QKeySequence.NativeText)))
            else:
                self.action.setToolTip(self.label)

        def copyPropertiesFromAction(self, act):
            self.setLabel(act.label)
            self.updateToolTip()
            self.setIcon(act.icon)

        @property
        def callback(self):
            return self.__callback

        def setCallback(self, callback):
            self.__callback = callback

        def __onActionTriggered(self):
            self.__callback()

    def __init__(self, explorerID, sdApp, uiMgr, appInterop, pkgMgr):
        logger.debug("Creating Interop actions for explorer %s" % explorerID)

        self.__explorerID = explorerID
        self.__uiMgr = uiMgr
        self.__appInterop = appInterop
        self.__interopHistory = AppInteropActions.InteropHistory()
        self.__pkgMgr = pkgMgr
        self.__tempDir = sdApp.getPath(SDApplicationPath.DefaultTemporaryDir)

        # Load icons from SVG if needed.
        self.__loadIcons()

        #
        # Create actions and add them to the UI.
        #

        self.__actions = collections.OrderedDict()

        act = AppInteropActions.ActionEntry(
            label=QtCore.QCoreApplication.translate(
                "PyAppInterop", "Publish .sbsar file"),
            objectName='explorerToolbar.publishAction',
            icon=self.__icons['publish'],
            shortcut=QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_P),
            callback=self.__onPublish,
            isSendToAction=False,
            showInSendContextMenu=False,
            appName=None,
            parent=self.__uiMgr.getMainWindow()
        )
        self.__actions['publish'] = act

        act = AppInteropActions.ActionEntry(
            label=QtCore.QCoreApplication.translate(
                "PyAppInterop", "Republish .sbsar file"),
            objectName='explorerToolbar.republishAction',
            icon=self.__icons['republish'],
            shortcut=None,
            callback=self.__onRepublish,
            isSendToAction=False,
            showInSendContextMenu=False,
            appName=None,
            parent=self.__uiMgr.getMainWindow()
        )
        self.__actions['republish'] = act

        if appInterop.isSamplerInstalled():
            act = AppInteropActions.ActionEntry(
                label=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Send to Substance 3D Sampler"),
                objectName='explorerToolbar.sendToSampler',
                icon=self.__icons['send_to_sampler'],
                shortcut=None,
                callback=self.__onSendToSampler,
                isSendToAction=True,
                showInSendContextMenu=True,
                appName=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Substance 3D Sampler"),
                parent=self.__uiMgr.getMainWindow()
            )
            self.__actions['send_to_sampler'] = act

        if appInterop.isPainterInstalled():
            act = AppInteropActions.ActionEntry(
                label=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Send to Substance 3D Painter"),
                objectName='explorerToolbar.sendToPainter',
                icon=self.__icons['send_to_painter'],
                shortcut=None,
                callback=self.__onSendToPainter,
                isSendToAction=True,
                showInSendContextMenu=True,
                appName=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Substance 3D Painter"),
                parent=self.__uiMgr.getMainWindow()
            )
            self.__actions['send_to_painter'] = act

        if appInterop.isStagerInstalled():
            act = AppInteropActions.ActionEntry(
                label=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Send to Substance 3D Stager"),
                objectName='explorerToolbar.sendToStager',
                icon=self.__icons['send_to_stager'],
                shortcut=None,
                callback=self.__onSendToStager,
                isSendToAction=True,
                showInSendContextMenu=True,
                appName=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Substance 3D Stager"),
                parent=self.__uiMgr.getMainWindow()
            )
            self.__actions['send_to_stager'] = act

        if appInterop.isPlayerInstalled():
            act = AppInteropActions.ActionEntry(
                label=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Send to Player"),
                objectName='explorerToolbar.sendToPlayer',
                icon=self.__icons['send_to_player'],
                shortcut=None,
                callback=self.__onSendToPlayer,
                isSendToAction=True,
                showInSendContextMenu=True,
                appName=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Player"),
                parent=self.__uiMgr.getMainWindow()
            )
            self.__actions['send_to_player'] = act

        if appInterop.isBridgeInstalled():
            act = AppInteropActions.ActionEntry(
                label=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Show in Bridge..."),
                objectName='explorerToolbar.showInBridge',
                icon=None,
                shortcut=None,
                callback=self.__onShowInBridge,
                isSendToAction=False,
                showInSendContextMenu=False,
                appName=QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Bridge"),
                parent=self.__uiMgr.getMainWindow()
            )
            self.__actions['show_in_bridge'] = act

        # Send To drop menu / tool button.
        self.__sendToMenu = QtWidgets.QMenu(parent=uiMgr.getMainWindow())
        self.__sendToMenu.setObjectName(
            "explorerToolbar.publishSendToMenu")

        # Add actions to send to menu.
        self.__sendToMenu.addAction(self.__actions['publish'].action)
        self.__sendToMenu.addAction(self.__actions['republish'].action)

        self.__sendToMenu.addSeparator()

        if 'send_to_sampler' in self.__actions:
            self.__sendToMenu.addAction(
                self.__actions['send_to_sampler'].action)
        if 'send_to_painter' in self.__actions:
            self.__sendToMenu.addAction(
                self.__actions['send_to_painter'].action)
        if 'send_to_stager' in self.__actions:
            self.__sendToMenu.addAction(
                self.__actions['send_to_stager'].action)
        if 'send_to_player' in self.__actions:
            self.__sendToMenu.addAction(
                self.__actions['send_to_player'].action)

        self.__sendToButton = QtWidgets.QToolButton(
            parent=uiMgr.getMainWindow())
        self.__sendToButton.setObjectName(
            "explorerToolbar.publishSendToButton")
        self.__sendToButton.setDefaultAction(self.__sendToMenu.menuAction())
        self.__sendToButton.defaultAction().setIcon(
            self.__icons['publish_drop'])
        self.__sendToButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.__sendToButtonAction = QtWidgets.QWidgetAction(
            uiMgr.getMainWindow())
        self.__sendToButtonAction.setObjectName(
            "explorerToolbar.publishSendToMenuAction")

        self.__sendToButtonAction.setDefaultWidget(self.__sendToButton)
        uiMgr.addActionToExplorerToolbar(explorerID, self.__sendToButtonAction)

        # Repeat last interop action.
        act = AppInteropActions.ActionEntry(
            label=QtCore.QCoreApplication.translate(
                "PyAppInterop", "Repeat last interop action"),
            objectName='explorerToolbar.repeatInteropAction',
            icon=self.__icons['republish'],
            shortcut=QtGui.QKeySequence(
                QtCore.Qt.CTRL | QtCore.Qt.SHIFT | QtCore.Qt.Key_P),
            callback=self.__onRepeatLastAction,
            isSendToAction=False,
            showInSendContextMenu=False,
            appName=None,
            parent=self.__uiMgr.getMainWindow()
        )
        self.__actions['repeat_last'] = act
        uiMgr.addActionToExplorerToolbar(explorerID, act.action)

        # Register selection changed callback.
        self.__selectionChangedCallbackID = uiMgr.registerExplorerSelectionChangedCallback(
            self.__explorerSelectionChanged)

        self.__updateActionsState()

    def uninitialize(self):
        if self.__selectionChangedCallbackID:
            self.__uiMgr.unregisterCallback(self.__selectionChangedCallbackID)

    #
    # Action methods.
    #

    def addActionsToSendToMenu(self, explorerID, menu):
        if self.__explorerID != explorerID:
            return

        for act in self.__actions.values():
            if act.isSendToAction and act.showInSendContextMenu:
                menu.addAction(act.action)

    def addPublishSBSARActionsToMenu(self, explorerID, menu):
        if self.__explorerID == explorerID:
            menu.addAction(self.__actions['publish'].action)
            menu.addAction(self.__actions['republish'].action)

    def addShowInBridgeActionToMenu(self, explorerID, menu):
        if 'show_in_bridge' in self.__actions and self.__explorerID == explorerID:
            menu.addAction(self.__actions['show_in_bridge'].action)

    def __updateActionsState(self):
        self.__explorerSelectionChanged(self.__explorerID)

    def __disableAllActions(self):
        # Reset context dependent actions.
        self.__actions['repeat_last'].copyPropertiesFromAction(
            self.__actions['republish'])

        for act in self.__actions.values():
            act.setEnabled(False)

    #
    # Callbacks.
    #

    def __explorerSelectionChanged(self, explorerID):
        # Ignore callbacks for other explorers.
        if explorerID != self.__explorerID:
            return

        self.__disableAllActions()

        selection = self.__uiMgr.getExplorerSelection(explorerID)
        if len(selection) != 1:
            return

        if isinstance(selection[0], SDPackage):
            pkg = selection[0]
            if self.__appInterop.canSendOrPublishPackage(pkg):
                for act in self.__actions.values():
                    act.setEnabled(True)

                isSBSARPkg = self.__appInterop.isSBSARPackage(pkg)
                canRepublish = self.__appInterop.canRepublishPackage(pkg)

                self.__actions['publish'].setEnabled(not isSBSARPkg)
                self.__actions['republish'].setEnabled(
                    not isSBSARPkg and canRepublish)

                # Handle repeat last interop actions.
                lastPkgAction = self.__interopHistory.lastActionForPackage(pkg)
                if lastPkgAction != None:
                    self.__actions['repeat_last'].copyPropertiesFromAction(
                        lastPkgAction)
                    self.__actions['repeat_last'].setEnabled(
                        lastPkgAction.enabled)
                else:
                    self.__actions['repeat_last'].setEnabled(False)

            if 'show_in_bridge' in self.__actions:
                self.__actions['show_in_bridge'].setEnabled(
                    not self.__appInterop.isTemporaryPackage(pkg))

        elif isinstance(selection[0], SDGraph):
            # Ignore graphs.
            return

        elif isinstance(selection[0], SDResource):
            if 'show_in_bridge' in self.__actions and selection[0].getEmbedMethod() == EmbedMethod.Linked:
                self.__actions['show_in_bridge'].setEnabled(True)

    def __onPublish(self):
        pkg = self.__uiMgr.getExplorerSelection(self.__explorerID)[0]
        publishParams = self.__appInterop.getPublishExportParams(pkg)
        dialog = SBSARPublishDialog(
            pkg, publishParams, self.__uiMgr.getMainWindow())
        if dialog.exec():
            self.__doPublishPackage(
                pkg, dialog.exportParameters(), checkForUnsavedDeps=False)

    def __onRepublish(self):
        pkg = self.__uiMgr.getExplorerSelection(self.__explorerID)[0]
        self.__doPublishPackage(
            pkg, self.__appInterop.getPublishExportParams(pkg), checkForUnsavedDeps=True)

    def __onSendToSampler(self):
        self.__doSendPackageToApp(
            pkg=self.__uiMgr.getExplorerSelection(self.__explorerID)[0],
            action=self.__actions['send_to_sampler'],
            sendCallback=self.__appInterop.sendToSampler,
            errorMessage=QtCore.QCoreApplication.translate(
                "PyAppInterop",
                "Error sending package to Substance 3D Sampler. Check the console for details."),
            updateInteropHistory=True
        )

    def __onSendToPainter(self):
        self.__doSendPackageToApp(
            pkg=self.__uiMgr.getExplorerSelection(self.__explorerID)[0],
            action=self.__actions['send_to_painter'],
            sendCallback=self.__appInterop.sendToPainter,
            errorMessage=QtCore.QCoreApplication.translate(
                "PyAppInterop",
                "Error sending package to Substance 3D Painter. Check the console for details."),
            updateInteropHistory=True
        )

    def __onSendToPlayer(self):
        self.__doSendPackageToApp(
            pkg=self.__uiMgr.getExplorerSelection(self.__explorerID)[0],
            action=self.__actions['send_to_player'],
            sendCallback=self.__appInterop.sendToPlayer,
            errorMessage=QtCore.QCoreApplication.translate(
                "PyAppInterop", "Error sending package to Substance Player. Check the console for details."),
            updateInteropHistory=False
        )

    def __onSendToStager(self):
        try:
            sel = self.__uiMgr.getExplorerSelection(self.__explorerID)[0]
            self.__appInterop.sendToStager(sel)
        except:
            if isinstance(sel, SDPackage):
                errorMessage = QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Error sending package to Substance 3D Stager. Check the console for details."),
            else:
                errorMessage = QtCore.QCoreApplication.translate(
                    "PyAppInterop",
                    "Error sending model graph.")

            fullMessage = errorMessage + '\n' + self.__appInterop.getLastErrorMessage()
            QtWidgets.QMessageBox.critical(
                self.__uiMgr.getMainWindow(),
                errorMessage,
                fullMessage,
                QtWidgets.QMessageBox.Ok)

    def __onShowInBridge(self):
        sel = self.__uiMgr.getExplorerSelection(self.__explorerID)[0]
        errorMessage = ''

        try:
            if isinstance(sel, SDPackage):
                errorMessage = QtCore.QCoreApplication.translate(
                    "PyAppInterop",
                    "Error showing package in Bridge.")
                self.__appInterop.showPackageInBridge(sel)
            elif isinstance(sel, SDResource):
                errorMessage = QtCore.QCoreApplication.translate(
                    "PyAppInterop",
                    "Error showing resource in Bridge.")
                self.__appInterop.showResourceInBridge(sel)
        except:
            fullMessage = errorMessage + '\n' + self.__appInterop.getLastErrorMessage()
            QtWidgets.QMessageBox.critical(
                self.__uiMgr.getMainWindow(),
                QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Error launching Bridge"),
                fullMessage,
                QtWidgets.QMessageBox.Ok)

    def __onResend(self):
        pkg = self.__uiMgr.getExplorerSelection(self.__explorerID)[0]

        if AppInterop.isAnyDependencyModified(pkg):
            if not self.__showUnsavedDependenciesWarning():
                return

        if pkg.isModified():
            if self.__appInterop.saveSBSBeforePublishingOrSending():
                self.__savePackageIfNeeded(pkg)
                if pkg.isModified():
                    # If the package is still modified, the user cancelled
                    # the save dialog or something went wrong.
                    return

        try:
            self.__appInterop.resendPackage(pkg)
        except:
            QtWidgets.QMessageBox.critical(
                self.__uiMgr.getMainWindow(),
                QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Error sending package"),
                QtCore.QCoreApplication.translate(
                    "PyAppInterop",
                    "Error resending package. Check the console for details."),
                QtWidgets.QMessageBox.Ok)

    def __onRepeatLastAction(self):
        pkg = self.__uiMgr.getExplorerSelection(self.__explorerID)[0]
        lastPkgAction = self.__interopHistory.lastActionForPackage(pkg)
        if lastPkgAction.isSendToAction:
            self.__onResend()
        else:
            self.__onRepublish()

    def onPackageClosed(self, pkg):
        self.__appInterop.onPackageClosed(pkg)
        self.__interopHistory.packageClosed(pkg)

    def onPackageSaved(self):
        self.__appInterop.onPackageSaved()
        self.__interopHistory.packageSaved(self.__pkgMgr)
        self.__updateActionsState()

    #
    # Utility methods.
    #

    def __savePackageIfNeeded(self, pkg):
        if not self.__packageHasFilePath(pkg):
            # If the package has never been saved, show the save file dialog
            # and save the package if the user accepted.
            filename = self.__getSavePackageFileName()
            if filename != '':
                self.__pkgMgr.savePackageAs(pkg, filename)
        elif pkg.isModified():
            # Save the package if it is modified.
            self.__pkgMgr.savePackageAs(pkg, pkg.getFilePath())

    def __doPublishPackage(self, pkg, exportParams, checkForUnsavedDeps=False):
        sbsFilePath = pkg.getFilePath()
        sbsTmpFilePath = None

        if checkForUnsavedDeps and AppInterop.isAnyDependencyModified(pkg):
            if not self.__showUnsavedDependenciesWarning():
                return

        try:
            if pkg.isModified():
                if self.__appInterop.saveSBSBeforePublishingOrSending():
                    self.__savePackageIfNeeded(pkg)
                    if pkg.isModified():
                        # If the package is still modified, the user cancelled
                        # the save dialog or something went wrong.
                        return

                    sbsFilePath = pkg.getFilePath()
                else:
                    sbsFilePath = self.__appInterop.saveTemporaryPackage(pkg)
                    sbsTmpFilePath = sbsFilePath

            self.__appInterop.publishPackage(pkg, sbsFilePath, exportParams)
            self.__interopHistory.updateLastAction(
                pkg, self.__actions['republish'])
            self.__updateActionsState()
        except:
            QtWidgets.QMessageBox.critical(
                self.__uiMgr.getMainWindow(),
                QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Error publishing package"),
                QtCore.QCoreApplication.translate(
                    "PyAppInterop",
                    "Error publishing package. Check the console for details."),
                QtWidgets.QMessageBox.Ok)
        finally:
            # If we created a temporary file to publish, remove it.
            if sbsTmpFilePath:
                os.remove(sbsTmpFilePath)

    def __doSendPackageToApp(self, pkg, action, sendCallback, errorMessage, updateInteropHistory):
        if AppInterop.isAnyDependencyModified(pkg):
            if not self.__showUnsavedDependenciesWarning():
                return

        if pkg.isModified():
            if self.__appInterop.saveSBSBeforePublishingOrSending():
                self.__savePackageIfNeeded(pkg)
                if pkg.isModified():
                    # If the package is still modified, the user cancelled
                    # the save dialog or something went wrong.
                    return

        try:
            sendCallback(pkg)
            if updateInteropHistory:
                self.__interopHistory.updateLastAction(pkg, action)
            self.__updateActionsState()
        except:
            fullMessage = errorMessage + '\n' + self.__appInterop.getLastErrorMessage()
            QtWidgets.QMessageBox.critical(
                self.__uiMgr.getMainWindow(),
                QtCore.QCoreApplication.translate(
                    "PyAppInterop", "Error sending package"),
                fullMessage,
                QtWidgets.QMessageBox.Ok)

    @staticmethod
    def __packageHasFilePath(pkg):
        return pkg.getFilePath() != ''

    def __getSavePackageFileName(self):
        return QtWidgets.QFileDialog.getSaveFileName(
            parent=self.__uiMgr.getMainWindow(),
            caption=QtCore.QCoreApplication.translate(
                "PyAppInterop", "Save package 'New_Graph'?"),
            filter=QtCore.QCoreApplication.translate(
                "PyAppInterop", "Substance 3D Designer files (*.sbs)"))[0]

    def __showUnsavedDependenciesWarning(self):
        retcode = QtWidgets.QMessageBox.warning(
            self.__uiMgr.getMainWindow(),
            QtCore.QCoreApplication.translate(
                "PyAppInterop", "Unsaved depdendencies"),
            QtCore.QCoreApplication.translate(
                "PyAppInterop", "One or more package dependencies are not saved. The saved file will be used for this action. Do you want to continue anyway?"),
            QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes)
        if retcode == QtWidgets.QMessageBox.Yes:
            return True

        return False

    @classmethod
    def __loadIcons(cls):
        thisDir = os.path.abspath(os.path.dirname(__file__))
        iconsDir = os.path.join(thisDir, '..', 'icons')
        iconList = [
            'send_to_sampler',
            'send_to_painter',
            'send_to_player',
            'send_to_stager',
            'republish',
            'publish_drop',
            'publish'
        ]

        for iconName in iconList:
            if not iconName in cls.__icons:
                cls.__icons[iconName] = QtGui.QIcon(
                    os.path.join(iconsDir, iconName + '.svg'))


class AppInteropUI(object):
    """
    Handles module initialization, uninitialization,
    application callbacks and creation of interop actions when
    explorer panels are created.
    """

    PKG_UPDATE_CHECK_DELAY = 100  # 2 seconds.

    __uiMgr = None
    __pkgMgr = None
    __appInterop = None
    __explorerCreatedCallbackID = None
    __beforeFileClosedCallbackID = None
    __interopActions = []

    @classmethod
    def initialize(cls):
        ctx = sd.getContext()
        cls.__app = ctx.getSDApplication()
        cls.__uiMgr = cls.__app.getQtForPythonUIMgr()
        cls.__pkgMgr = cls.__app.getPackageMgr()

        if cls.__uiMgr:
            cls.__appInterop = AppInterop(cls.__app)
            logger.info("Initializing App Interop")

            cls.__explorerCreatedCallbackID = cls.__uiMgr.registerExplorerCreatedCallback(
                cls.__explorerCreated)
            cls.__beforeFileClosedCallbackID = cls.__app.registerBeforeFileClosedCallback(
                cls.__onBeforeFileClosedCallback)
            cls.__afterFileSavedCallbackID = cls.__app.registerAfterFileSavedCallback(
                cls.__onAfterFileSavedCallback)

    @classmethod
    def uninitialize(cls):
        if cls.__uiMgr:
            if cls.__explorerCreatedCallbackID:
                logger.info("Uninitializing App Interop")
                cls.__uiMgr.unregisterCallback(cls.__explorerCreatedCallbackID)

            if cls.__beforeFileClosedCallbackID:
                cls.__app.unregisterCallback(cls.__beforeFileClosedCallbackID)

            if cls.__afterFileSavedCallbackID:
                cls.__app.unregisterCallback(cls.__afterFileSavedCallbackID)

            for iopAction in cls.__interopActions:
                iopAction.uninitialize()

    #
    # Action methods.
    #

    @classmethod
    def addActionsToSendToMenu(cls, explorerID, menuPtr):
        for act in cls.__interopActions:
            act.addActionsToSendToMenu(
                explorerID, shiboken6.wrapInstance(menuPtr, QtWidgets.QMenu))

    @classmethod
    def addPublishSBSARActionsToMenu(cls, explorerID, menuPtr):
        for act in cls.__interopActions:
            act.addPublishSBSARActionsToMenu(
                explorerID, shiboken6.wrapInstance(menuPtr, QtWidgets.QMenu))

    @classmethod
    def addShowInBridgeActionToMenu(cls, explorerID, menuPtr):
        for act in cls.__interopActions:
            act.addShowInBridgeActionToMenu(
                explorerID, shiboken6.wrapInstance(menuPtr, QtWidgets.QMenu))

    #
    # Callbacks.
    #

    @classmethod
    def __explorerCreated(cls, explorerID):
        cls.__interopActions.append(
            AppInteropActions(explorerID, cls.__app, cls.__uiMgr, cls.__appInterop, cls.__pkgMgr))

    @classmethod
    def __onBeforeFileClosedCallback(cls, filePath):
        pkg = cls.__findPackageFromFilePath(filePath)
        if pkg:
            for act in cls.__interopActions:
                act.onPackageClosed(pkg)

    @classmethod
    def __onAfterFileSavedCallback(cls, filePath, succeed):
        if not succeed:
            return

        '''
        Currently save file related callbacks in SD are triggered too early (a bug?).
        We need to execute the callback using a timer to make sure
        that the package list is properly up to date.
        '''
        QtCore.QTimer.singleShot(
            cls.PKG_UPDATE_CHECK_DELAY,
            partial(cls.__doOnAfterFileSavedCallback, filePath=filePath))

    @classmethod
    def __doOnAfterFileSavedCallback(cls, filePath):
        for act in cls.__interopActions:
            act.onPackageSaved()

    #
    # Utility methods.
    #

    @classmethod
    def __findPackageFromFilePath(cls, filePath):
        filePath = filePath.decode('utf-8')
        for pkg in cls.__app.getPackageMgr().getUserPackages():
            if pkg.getFilePath() == filePath:
                return pkg
