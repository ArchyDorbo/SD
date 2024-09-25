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
import os
import sd
from tests import tools
from tests.data_serializer import *
from sd.tools import io
from sd.api.mdl.sdmdlgraph import *

import logging
logger = logging.getLogger(__name__)


class TestModuleRootPaths(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()

        sdPkgMgr = context.getSDApplication().getPackageMgr()
        sdModuleMgr = context.getSDApplication().getModuleMgr()

        # Display Root paths
        originalRootPaths = self.__getMDLRootPaths()
        for path in originalRootPaths:
            logger.debug('Root Path: %s' % path)

        # Add root path
        assetsDir = tools.getAssetsDir()
        newMdlRootPath = os.path.join(assetsDir, 'mdl')
        sdModuleMgr.addRootPath('mdl', newMdlRootPath)

        # Check path exist in the root paths
        self.assertTrue(newMdlRootPath in self.__getMDLRootPaths())

        # Create New Package
        sdPkg = sdPkgMgr.newUserPackage()
        sdMDLGraph = SDMDLGraph.sNew(sdPkg)
        sdMDLNode = sdMDLGraph.newNode('mdl::test::test_function()')

        # Check the node has been properly created
        self.assertTrue(sdMDLNode)

        # Remove root path
        sdModuleMgr.removeRootPath('mdl', newMdlRootPath)
        self.assertTrue(newMdlRootPath not in self.__getMDLRootPaths())

    def __getMDLRootPaths(self):
        context = sd.getContext()
        sdModuleMgr = context.getSDApplication().getModuleMgr()

        newRootPaths = []
        for p in sdModuleMgr.getRootPaths('mdl'):
            newRootPaths.append(p.get())
        return newRootPaths

if __name__ == '__main__':
    unittest.main()

