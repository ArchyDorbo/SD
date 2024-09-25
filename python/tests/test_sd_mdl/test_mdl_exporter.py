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

import unittest
import os, shutil
import sd
from sd.api.mdl.sdmdlexporter import *
from sd.api.mdl.sdmdlgraph import *
from tests import tools

import logging
logger = logging.getLogger(__name__)


class TestMDLExporter(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()

        packageFiles = []
        # packageFiles.append(['test_mdl_exporter.sbs', ['0.exr', '1.png']])
        packageFiles.append(['test_mdl_texture2d.sbs', ['0.png']])
        # packageFiles.append(['test_mdl_mbsdf.sbs', []])
        # packageFiles.append(['test_mdl_lightprofile.sbs', []])

        for packageFile in packageFiles:
            self.__test_File(context, packageFile[0], packageFile[1])

    def __test_File(self, aContext, aPackageFile, aResourceSuffixList):
        # Load Package
        sdPackage = tools.loadSDPackage(aContext, aPackageFile)
        self.assertTrue(sdPackage, 'Fail to load package')
        self.__test_SDMDLExporter_sExportPackage(sdPackage, aResourceSuffixList)
        self.__test_SDMDLExporter_sExportPreset(sdPackage, aResourceSuffixList)



    def __test_SDMDLExporter_sExportPackage(self, aSDPackage, aResourceSuffixList):
        packageFilePath = aSDPackage.getFilePath()
        packageFileName = os.path.split(packageFilePath)[1]
        packageFileBaseName = packageFileName[0:packageFileName.rfind('.')]
        outputMDLFile = os.path.join(tools.getTestOutputDir(__file__), 'exportModule', packageFileBaseName + '.mdl')
        outputMDLFileResourcesDir = outputMDLFile[:-4] # Remove '.mdl'

        # Remove file if any
        if os.path.isfile(outputMDLFile):
            os.remove(outputMDLFile)
        if os.path.isdir(outputMDLFileResourcesDir):
            shutil.rmtree(outputMDLFileResourcesDir)

        # Export to MDL Module
        SDMDLExporter.sExportPackage(aSDPackage, outputMDLFile)

        # Check results
        self.assertTrue(os.path.isfile(outputMDLFile))
        self.assertTrue(os.path.isdir(outputMDLFileResourcesDir))
        for resourceSuffix in aResourceSuffixList:
            resourceFileName = packageFileBaseName + '_resource_' + resourceSuffix
            self.assertTrue(os.path.isfile(os.path.join(outputMDLFileResourcesDir, resourceFileName)))

        logger.debug('SDPackage exported to MDL Module %s' % outputMDLFile)


    def __test_SDMDLExporter_sExportPreset(self, aSDPackage, aResourceSuffixList):
        # Find first MDL Graph
        mdlGraph = None
        for sdResource in aSDPackage.getChildrenResources(False):
            if isinstance(sdResource, SDMDLGraph):
                mdlGraph = sdResource
                break

        self.assertTrue(mdlGraph)

        packageFilePath = aSDPackage.getFilePath()
        packageFileName = os.path.split(packageFilePath)[1]
        packageFileBaseName = packageFileName[0:packageFileName.rfind('.')]
        outputMDLFile = os.path.join(tools.getTestOutputDir(__file__), 'exportPreset', packageFileBaseName + '.mdl')
        outputMDLFileResourcesDir = outputMDLFile[:-4] # Remove '.mdl'

        # Remove file if any
        if os.path.isfile(outputMDLFile):
            os.remove(outputMDLFile)
        if os.path.isdir(outputMDLFileResourcesDir):
            shutil.rmtree(outputMDLFileResourcesDir)

        # Export to MDL Module
        SDMDLExporter.sExportPreset(mdlGraph, outputMDLFile)

        # Check results
        self.assertTrue(os.path.isfile(outputMDLFile))
        self.assertTrue(os.path.isdir(outputMDLFileResourcesDir))
        for resourceSuffix in aResourceSuffixList:
            resourceFileName = packageFileBaseName + '_resource_' + resourceSuffix
            self.assertTrue(os.path.isfile(os.path.join(outputMDLFileResourcesDir, resourceFileName)))

        logger.debug('SDPackage exported to MDL Module %s' % outputMDLFile)


if __name__ == '__main__':
    unittest.main()

