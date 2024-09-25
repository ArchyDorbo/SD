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

class SDIndexException(IndexError):
    def __init__(self, *args, **kwargs):
        IndexError.__init__(self, *args, **kwargs)

class SDAPIErrorMsg(BaseException):
    def __init__(self, aErrorMsg):
        self.mErrorMsg = aErrorMsg

class SDAPIErrorCode(BaseException):
    def __init__(self, aErrorCode):
        self.mErrorCode = aErrorCode
