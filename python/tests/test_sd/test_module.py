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

import logging
logger = logging.getLogger(__name__)


class TestModule(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()

        moduleMgr = context.getSDApplication().getModuleMgr()
        self.assertTrue(moduleMgr)

        # Check Serialization
        logFileDir = tools.getAssetsDir()
        currentFileBaseName = io.getFileBaseName(__file__)
        referenceFile = os.path.join(logFileDir, currentFileBaseName + '.txt')

        # Serialize All SDModules
        dumpLines = DataSerializer().serializeSDModules(moduleMgr)

        # Convert To Lines
        newLines = tools.createFileLines(dumpLines)

        # ------------------------------------------------
        # For development only
        # createReferenceFile = False
        createReferenceFile = True
        if createReferenceFile:
            # Write lines to reference file
            tools.writeLinesToFile(referenceFile, newLines)
        # ------------------------------------------------

        # Read reference file lines
        referenceLines = tools.readLinesFromFile(referenceFile)

        # Compare Lines
        tools.compareLines(self, referenceLines, newLines)


    def __test_SDModuleMgr_getModules(self, aModuleMgr):
        sdModuleSBSCompositing = aModuleMgr.getModuleFromId('sbs::compositing')
        self.assertTrue(sdModuleSBSCompositing)
        functionCount = len(sdModuleSBSCompositing)
        for functionDefinition in sdModuleSBSCompositing:
            logger.debug(functionDefinition.getId())

if __name__ == '__main__':
    unittest.main()

