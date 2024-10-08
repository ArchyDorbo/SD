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

import sd
from .sdvaluebasetype import SDValueBaseType
from .sdapiobject import SDAPIObject
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDValueFloat(SDValueBaseType):
    """
    Class representing a float Value
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDValueFloat
        """
        super(SDValueFloat, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew(value : float) -> SDValueFloat:
        """
        Create new SDValueFloat

        :param value: The name of the enum type
        """
        outSDValueFloat = ctypes.c_void_p()
        _res = sd.getContext().SDValueFloat_sNew(value, ctypes.byref(outSDValueFloat))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDValueFloat, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDValueFloat.value, ownHandle=True)

    def get(self) -> float:
        """
        Get the base type value as float

        """
        outValue = ctypes.c_float()
        _res = self.mAPIContext.SDValueFloat_get(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

