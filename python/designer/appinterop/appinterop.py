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

from sd.api.sdapplication import SDApplicationPath
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph
from sd.api.sdpackage import SDPackage

import collections
import os
import tempfile


class AppInterop(object):
    """
    Utility class that handles all non UI aspects
    of publishing and sending packages to other apps.
    """

    class PublishHistory(object):
        """
        PublishHistory Keep tracks of packages published and
        settings used to publish them.
        """

        def __init__(self):
            self.__entries = {}

        def hasPackageBeenPublished(self, pkg):
            key = (pkg.getFilePath(), pkg.getUID())
            return key in self.__entries

        def getPublishExportParams(self, pkg):
            key = (pkg.getFilePath(), pkg.getUID())
            return self.__entries.get(key, None)

        def packagePublished(self, pkg, exportParams):
            key = (pkg.getFilePath(), pkg.getUID())
            self.__entries[key] = exportParams

        def packageClosed(self, pkg):
            key = (pkg.getFilePath(), pkg.getUID())
            if key in self.__entries:
                del self.__entries[key]

        def packageSaved(self, pkgMgr):
            '''
            Update the entries list after packages are saved.
            If the user saved a package with a new path using Save as
            we need to remove it from the publish history.
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

    def __init__(self, app):
        self.__interopMgr = app.getAppInteropMgr()
        self.__pkgMgr = app.getPackageMgr()
        self.__tempDir = app.getPath(SDApplicationPath.DefaultTemporaryDir)
        self.__publishHistory = AppInterop.PublishHistory()

    #
    # Queries.
    #

    def isSamplerInstalled(self):
        return self.__interopMgr.isSamplerInstalled()

    def isPainterInstalled(self):
        return self.__interopMgr.isPainterInstalled()

    def isPlayerInstalled(self):
        # Player is always bundled with Designer.
        return True

    def isBridgeInstalled(self):
        return self.__interopMgr.isBridgeInstalled()

    def isStagerInstalled(self):
        return self.__interopMgr.isStagerInstalled()

    def saveSBSBeforePublishingOrSending(self):
        return self.__interopMgr.saveSBSBeforePublishingOrSending()

    @staticmethod
    def isSBSARPackage(pkg):
        return pkg.getFilePath().endswith('.sbsar')

    @staticmethod
    def isTemporaryPackage(pkg):
        return pkg.getFilePath() == ''

    @staticmethod
    def __anyDependencyModified(pkg, visitedPackages):
        # If we have seen this package before, do not recurse.
        # If not, add it to the set of visited packages.
        key = (pkg.getFilePath(), pkg.getUID())
        if key in visitedPackages:
            return False
        else:
            visitedPackages.add(key)

        if pkg.isModified():
            return True

        for dep in pkg.getDependencies():
            if AppInterop.__anyDependencyModified(dep.getPackage(), visitedPackages):
                return True

        return False

    @staticmethod
    def isAnyDependencyModified(pkg):
        key = (pkg.getFilePath(), pkg.getUID())
        visitedPackages = {key}
        for dep in pkg.getDependencies():
            if AppInterop.__anyDependencyModified(dep.getPackage(), visitedPackages):
                return True

        return False

    @staticmethod
    def canSendOrPublishPackage(pkg):
        # Check if there is any exposed SBSCompGraph inside the package.
        for res in pkg.getChildrenResources(isRecursive=True):
            if isinstance(res, SDSBSCompGraph):
                if res.getExposedInSBSAR():
                    return True
        return False

    def canRepublishPackage(self, pkg):
        return not self.isTemporaryPackage(pkg) and self.__publishHistory.hasPackageBeenPublished(pkg)

    #
    # SBSAR publish.
    #

    def publishPackage(self, pkg, sbsFilePath, exportParams):
        self.__interopMgr.publishSBSARWithProgressDialog(
            sbsFilePath, exportParams['sbsar_file_path'], exportParams['compression_mode'])

        # Update package history.
        if not self.isTemporaryPackage(pkg):
            self.__publishHistory.packagePublished(pkg, exportParams)

    def getPublishExportParams(self, pkg):
        if self.isTemporaryPackage(pkg):
            return None

        return self.__publishHistory.getPublishExportParams(pkg)

    #
    # Send to methods.
    #

    def sendToSampler(self, pkg):
        return self.__interopMgr.sendPackageToSampler(pkg)

    def sendToPainter(self, pkg):
        return self.__interopMgr.sendPackageToPainter(pkg)

    def sendToPlayer(self, pkg):
        return self.__interopMgr.sendPackageToPlayer(pkg)

    def showPackageInBridge(self, pkg):
        return self.__interopMgr.showPackageInBridge(pkg)

    def showResourceInBridge(self, res):
        return self.__interopMgr.showResourceInBridge(res)

    def resendPackage(self, pkg):
        return self.__interopMgr.resendPackage(pkg)

    def sendToStager(self, pkgOrModelGraph):
        if isinstance(pkgOrModelGraph, SDPackage):
            return self.__interopMgr.sendPackageToStager(pkgOrModelGraph)
        else:
            return self.__interopMgr.sendModelGraphToStager(pkgOrModelGraph)

    #
    # Utility methods.
    #

    def onPackageSaved(self):
        self.__publishHistory.packageSaved(self.__pkgMgr)
        self.__interopMgr.updateSentToHistory()

    def onPackageClosed(self, pkg):
        self.__publishHistory.packageClosed(pkg)

    def getLastErrorMessage(self):
        return self.__interopMgr.getLastErrorMessage()

    def saveTemporaryPackage(self, pkg):
        fd, sbsFilePath = tempfile.mkstemp(suffix='.sbs', dir=self.__tempDir)
        os.close(fd)
        self.__pkgMgr.saveCopyOfPackageAs(pkg, sbsFilePath)
        return sbsFilePath
