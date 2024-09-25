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
import unittest
import sd

from sd.api.sbs.sdsbsarexporter import *

from tests import tools

import logging
logger = logging.getLogger(__name__)


class TestSDSBSExporter(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()
        srcPackageFileName = 'test_export.sbs'
        sdPackage = tools.loadSDPackage(context, srcPackageFileName)
        self.assertTrue(sdPackage, 'Fail to load package')

        sbsarFilePath = os.path.join(tools.getTestOutputDir(__file__), 'test_new_content_output.sbsar')

        if os.path.isfile(sbsarFilePath):
            logger.debug('Remove existing file: ' + sbsarFilePath)
            os.remove(sbsarFilePath)
            self.assertFalse(os.path.isfile(sbsarFilePath))


        logger.debug('Export package to: ' + sbsarFilePath)
        sdSBSARExporter = SDSBSARExporter.sNew()
        sdSBSARExporter.setExposeRandomSeed(False)
        sdSBSARExporter.exportPackageToSBSAR(sdPackage, sbsarFilePath)

        # Check that sbsar file exist
        self.assertTrue(os.path.isfile(sbsarFilePath))

        # Check file size
        statinfo = os.stat(sbsarFilePath)
        self.assertTrue(statinfo.st_size > 0)

if __name__ == '__main__':
    unittest.main()

