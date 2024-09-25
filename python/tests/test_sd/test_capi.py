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


class TestCAPI(unittest.TestCase):

    def runTest(self):
        self.testCAPI_getVersion()

    def testCAPI_getVersion(self):
        context = sd.getContext()
        capi = sd.capi.getCAPI()

        capiVersionStr = capi.getVersion()

        # Check version number string: MAJOR.MINOR.PATCH[.releaseName]
        tokens = capiVersionStr.split('.')
        self.assertTrue(len(tokens) == 3)

        # Check all the tokens are numbers
        for token in tokens:
            number = int(token)

        self.assertTrue(int(tokens[0]) >= 1)


if __name__ == '__main__':
    unittest.main()

