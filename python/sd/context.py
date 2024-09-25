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

import logging
import os
from sd.api.sdapplication import SDApplication
from sd import capi, logger
from sd.api import APIContext
import tempfile

gIsVerbose = True

# =======================================================================================
class Context(APIContext):
    def __init__(self):
        self.mCAPI = capi.getCAPI()
        APIContext.__init__(self, self.getCTypesBinary())

        # Initialized the first time getSDApplication() is called.
        self.mSDApplication = None

    def getCTypesBinary(self):
        """
        :rtype: ctypes.CDLL
        """
        return self.mCAPI.getCTypesBinary()

    def getCTypesFct(self, aFctName):
        return self.mCAPI.getCTypesFct(aFctName)

    def getSDApplication(self):
        """
        :rtype: sd.api.sdapplication.SDApplication
        """
        if not self.mSDApplication:
            self.mSDApplication = SDApplication(self, 0)
        return self.mSDApplication

    def isVerbose(self):
        return gIsVerbose

    def getTempDir(self, aSubDirName = ''):
        """
        :rtype: string
        """
        dirAbsPath = os.path.join(os.path.abspath(tempfile.gettempdir()), 'Allegorithmic', 'Substance Designer Python API')
        if aSubDirName:
            dirAbsPath = os.path.join(dirAbsPath, aSubDirName)
        if not os.path.isdir(dirAbsPath):
            os.makedirs(dirAbsPath)
        return dirAbsPath

    def createRuntimeLogHandler(self, channelName = None):
        """
        Creates a log handler that redirects logs to Designer's console.

        :rtype: logger.SDRuntimeLogHandler
        """
        return logger.SDRuntimeLogHandler(self.mCAPI, channelName)

    def getLogger(self):
        """
        :rtype: logging.Logger
        """
        return self.mCAPI.getLogger()
