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

import sys
import os
import logging
import unittest


# Add the path to the Python API to sys.path if needed.
thisDir = os.path.abspath(os.path.dirname(__file__))
apiDir = os.path.join(thisDir, '..')
if not apiDir in sys.path:
    sys.path.append(apiDir)


def runTests():
    # set the log level for all tests.
    logging.basicConfig(level=logging.WARNING)

    loader = unittest.TestLoader()
    tests = loader.discover(thisDir)
    testRunner = unittest.runner.TextTestRunner(verbosity=3)
    result = testRunner.run(tests)
    return result

if __name__ == '__main__':
    returnCode = 0 if runTests().wasSuccessful() else 1
    sys.exit(returnCode)
