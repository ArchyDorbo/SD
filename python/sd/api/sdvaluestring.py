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

class SDValueString(SDValueBaseType):
    """
    Class representing a string Value
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDValueString
        """
        super(SDValueString, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew(value : str) -> SDValueString:
        """
        Create new SDValueString

        :param value: The name of the enum type
        """
        outSDValueString = ctypes.c_void_p()
        _res = sd.getContext().SDValueString_sNew(ctypes.create_string_buffer(value.encode('utf-8')), ctypes.byref(outSDValueString))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDValueString, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDValueString.value, ownHandle=True)

    def get(self) -> str:
        """
        Get the base type value as string

        """
        outValue = ctypes.c_char_p()
        _res = self.mAPIContext.SDValueString_get(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value.decode('utf-8') # type: ignore

