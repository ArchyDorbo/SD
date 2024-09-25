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

import ctypes
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDCallbackMap(object):
    """
    Class used to store functions used as callbacks.
    If we don't keep a reference to them, they are garbage collected
    by Python and we crash when trying to call them.
    For internal use, don't use it directly.
    """

    __mLastCallbackIndex = 0
    __mCallbacksMap = {}

    @classmethod
    def _registerCallback(cls, f, registerFunc):
        # We need to keep a reference to the ctypes callable wrapper.
        cls.__mLastCallbackIndex += 1
        cls.__mCallbacksMap[cls.__mLastCallbackIndex] = f

        _res = registerFunc(f, ctypes.c_size_t(cls.__mLastCallbackIndex))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None
            raise APIException(SDApiError(_res))

        # Return our callbackID.
        return cls.__mLastCallbackIndex

    @classmethod
    def _unregisterCallback(cls, callbackID, unregisterFunc):
        if not callbackID in cls.__mCallbacksMap:
            raise APIException(SDApiError(SDApiError.InvalidArgument))

        _res = unregisterFunc(callbackID)
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None
            raise APIException(SDApiError(_res))

        # Remove our reference to the ctypes callable wrapper.
        del cls.__mCallbacksMap[callbackID]
