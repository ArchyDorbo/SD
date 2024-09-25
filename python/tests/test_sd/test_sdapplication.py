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
import sd

import logging
logger = logging.getLogger(__name__)


class TestSDApplication(unittest.TestCase):

    def runTest(self):
        self.testSDApplication_getVersion()

    def testSDApplication_getVersion(self):
        context = sd.getContext()
        sdApp = context.getSDApplication()
        sdAppVersionStr = sdApp.getVersion()

        # Check version number string: MAJOR.MINOR.PATCH[.releaseName]
        tokens = sdAppVersionStr.split('.')
        self.assertTrue(len(tokens) >= 3)

        # Check all the tokens are numbers
        for token in tokens:
            number = int(token)


if __name__ == '__main__':
    unittest.main()
