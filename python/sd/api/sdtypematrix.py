# ADOBE CONFIDENTIAL
#
# Copyright 2010-2024 Adobe
# All Rights Reserved.
#
# NOTICE:  Adobe permits you to use, modify, and distribute this file in
# accordance with the terms of the Adobe license agreement accompanying it.
# If you have received this file from a source other than Adobe,
# then your use, modification, or distribution of it requires the prior
# written permission of Adobe.
#
# Autogenerated by ipa. Don't edit directly, edit the definitions and regenerate it when changing
#

from __future__ import annotations

import ctypes
import base64

from typing import Any, Optional

from .sdtype import SDType
from .sdapiobject import SDAPIObject
from .sdtype import SDTypeModifier
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDTypeMatrix(SDType):
    """
    Class used to store information about a matrix type
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDTypeMatrix
        """
        super(SDTypeMatrix, self).__init__(APIContext, handle, *args, **kwargs)

    def getItemType(self) -> SDType:
        """
        Get the type of items

        """
        outType = ctypes.c_void_p()
        _res = self.mAPIContext.SDTypeMatrix_getItemType(self.mHandle, ctypes.byref(outType))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = self.mAPIContext.mTypeMap[SDAPIObject(self.mAPIContext, outType, ownHandle=False).getClassName()]
        return constructor(self.mAPIContext, outType.value, ownHandle=True)

    def getColumnCount(self) -> int:
        """
        Get the number of column of the matrix

        """
        outValue = ctypes.c_size_t()
        _res = self.mAPIContext.SDTypeMatrix_getColumnCount(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

    def getRowCount(self) -> int:
        """
        Get the number of row of the matrix

        """
        outValue = ctypes.c_size_t()
        _res = self.mAPIContext.SDTypeMatrix_getRowCount(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

