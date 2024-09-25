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

from .sdvalue import SDValue
from .sdapiobject import SDAPIObject
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDGraphPresetInput(SDAPIObject):
    """
    Class managing a Substance graph preset input
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDGraphPresetInput
        """
        super(SDGraphPresetInput, self).__init__(APIContext, handle, *args, **kwargs)

    def getIdentifier(self) -> str:
        """
        Get the identifier of this preset input

        """
        outId = ctypes.c_char_p()
        _res = self.mAPIContext.SDGraphPresetInput_getIdentifier(self.mHandle, ctypes.byref(outId))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outId.value.decode('utf-8') # type: ignore

    def getValue(self) -> SDValue:
        """
        Get the value of the specified input

        """
        outSDValue = ctypes.c_void_p()
        _res = self.mAPIContext.SDGraphPresetInput_getValue(self.mHandle, ctypes.byref(outSDValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = self.mAPIContext.mTypeMap[SDAPIObject(self.mAPIContext, outSDValue, ownHandle=False).getClassName()]
        return constructor(self.mAPIContext, outSDValue.value, ownHandle=True)

    def setValue(self, sdValue : SDValue) -> None:
        """
        Set the value of the specified input

        :param sdValue: The new input value
        """
        _res = self.mAPIContext.SDGraphPresetInput_setValue(self.mHandle, sdValue.mHandle)
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

