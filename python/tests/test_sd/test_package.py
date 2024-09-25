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
import shutil
import sys
import unittest
import xml.etree.ElementTree as ET

import sd
from sd.api import sdapiobject, apiexception
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph

from tests import tools


class TestPackage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        context = sd.getContext()

        # Load the reference package
        cls.sdPackage = tools.loadSDPackage(context, 'test_sdpackage.sbs')

        # Load some other packages
        cls.sdPackageTestNewContent = tools.loadSDPackage(context, 'test_write_content.sbs')

    def testPackagesLoaded(self):
        self.assertTrue(self.sdPackage, 'Fail to load package')
        self.assertTrue(self.sdPackageTestNewContent, 'Fail to load package')

    def test_SDPackage_getChildrenResources(self):
        # Check Non Recursive mode
        sbsResourceArray = self.sdPackage.getChildrenResources(False)
        self.assertEqual(len(sbsResourceArray), 3)

        # Check Recursive Mode
        sbsResourceArray = self.sdPackage.getChildrenResources(True)
        self.assertEqual(len(sbsResourceArray), 5)

    def test_SDPackage_findResourceFromUrl(self):
        # Check that a resource of the reference package can be retrieved
        sbMDLSubGraph = self.sdPackage.findResourceFromUrl('folder0/mdl_sub_graph')
        self.assertTrue(sbMDLSubGraph)

        # Check that a resource in another can't be found in the reference package
        sbPBRGraph = self.sdPackage.findResourceFromUrl('pbr_graph')
        self.assertFalse(sbPBRGraph)

    def test_SDPackage_getDependencies(self):
        pkgDeps = self.sdPackage.getDependencies()
        self.assertEqual(len(pkgDeps), 1)
        firstPkgDep = pkgDeps[0]
        self.assertTrue(len(firstPkgDep.getFilePath())>0)
        self.assertTrue(firstPkgDep.getPackage())

    def test_SDPackage_isModified(self):
        context = sd.getContext()
        app = context.getSDApplication()
        pkgMgr = app.getPackageMgr()
        pkg = pkgMgr.newUserPackage()
        self.assertFalse(pkg.isModified())

        graph = SDSBSCompGraph.sNew(pkg)
        self.assertTrue(pkg.isModified())

        graph.delete()
        self.assertTrue(pkg.isModified())

        dstFileAbsPath = os.path.join(tools.getTestOutputDir(__file__), 'test_package_is_modified.sbs')
        pkgMgr.savePackageAs(pkg, dstFileAbsPath)
        self.assertFalse(pkg.isModified())

    def test_SDPackage_Save(self):
        context = sd.getContext()
        app = context.getSDApplication()
        pkgMgr = app.getPackageMgr()
        pkg = pkgMgr.newUserPackage()
        graph = SDSBSCompGraph.sNew(pkg)
        self.assertTrue(pkg.isModified())
        self.assertEqual(pkg.getFilePath(), '')

        with self.assertRaises(sd.api.APIException) as error:
            pkgMgr.savePackage(pkg)
            self.assertEqual(error.exception.mErrorCode,
                             sd.api.SDApiError.InvalidArgument, "Package file path is empty")
            self.assertTrue(pkg.isModified())

        dstFileAbsPath = os.path.join(tools.getTestOutputDir(
            __file__), 'test_package_save.sbs')
        pkgMgr.savePackageAs(pkg, dstFileAbsPath)
        self.assertFalse(pkg.isModified())

        graph2 = SDSBSCompGraph.sNew(pkg)
        self.assertTrue(pkg.isModified())

        pkgMgr.savePackage(pkg)
        self.assertFalse(pkg.isModified())

    @staticmethod
    def __collectAllFilePathsFromSBSDocument(xmlFileName):
        filePathXMLTags = {'filepath', 'filename'}
        pathList = []

        docRoot = ET.parse(xmlFileName).getroot()
        for elem in docRoot.iter():
            name = elem.tag
            if name in filePathXMLTags:
                value = elem.get('v')
                if value:
                    value = value.replace('\\', '/')
                    pathList.append(value)

        return pathList

    def test_SDPackage_SaveCopyAs(self):
        context = sd.getContext()
        app = context.getSDApplication()
        pkgMgr = app.getPackageMgr()

        outputTestDir = os.path.join(
            tools.getTestOutputDir(__file__),
            'test_save_copy_as')

        # Cleanup the test dir if it exists and create a new one.
        shutil.rmtree(outputTestDir, ignore_errors=True)
        self.assertFalse(os.path.exists(outputTestDir))

        os.makedirs(outputTestDir)
        self.assertTrue(os.path.exists(outputTestDir))

        # Load test package and save as to another path.
        pkg = tools.loadSDPackage(context, os.path.join('test_save_copy_as', 'test_save_copy_as.sbs'))
        savedAsFileAbsPath = os.path.join(outputTestDir, 'test_py_save_as.sbs').replace('\\', '/')
        pkgMgr.savePackageAs(pkg, savedAsFileAbsPath)
        savedPackageFilePath = pkg.getFilePath().replace('\\', '/')

        self.assertTrue(os.path.exists(savedAsFileAbsPath))
        self.assertEqual(savedPackageFilePath, savedAsFileAbsPath)
        self.assertFalse(pkg.isModified())

        savedAsFilePaths = self.__collectAllFilePathsFromSBSDocument(savedAsFileAbsPath)

        # Modify the package.
        graph = SDSBSCompGraph.sNew(pkg)
        self.assertTrue(pkg.isModified())

        # Save a copy of the package in a diferent dir.
        copyOutputTestDir = os.path.join(outputTestDir, 'save_copy')
        self.assertFalse(os.path.exists(copyOutputTestDir))

        os.makedirs(copyOutputTestDir)
        self.assertTrue(os.path.exists(copyOutputTestDir))

        savedCopyAsFileAbsPath = os.path.join(copyOutputTestDir, 'test_py_save_copy_as.sbs')
        pkgMgr.saveCopyOfPackageAs(pkg, savedCopyAsFileAbsPath)

        # Check that the package was saved, it is still modified and filepath did not change.
        self.assertTrue(os.path.exists(savedCopyAsFileAbsPath))
        self.assertTrue(pkg.isModified())
        self.assertEqual(pkg.getFilePath().replace('\\', '/'), savedPackageFilePath)

        # Check that we saved the external copy resources with the package.
        self.assertTrue(os.path.exists(os.path.join(
            copyOutputTestDir, 'test_py_save_copy_as.resources', 'XXXXXX-substance-128x128.png'
        )))

        # Undo the changes, delete the previous saved file and save the package.
        graph.delete()
        os.remove(savedAsFileAbsPath)
        pkgMgr.savePackage(pkg)

        # Check that the package was saved
        self.assertTrue(os.path.exists(savedAsFileAbsPath))
        newSavedAsFilePaths = self.__collectAllFilePathsFromSBSDocument(savedAsFileAbsPath)

        # Check that the paths in the new sbs package match the previously saved paths.
        self.assertEqual(savedAsFilePaths, newSavedAsFilePaths)

if __name__ == '__main__':
    unittest.main()
