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

class SDValueBool(SDValueBaseType):
    """
    Class representing a bool Value
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDValueBool
        """
        super(SDValueBool, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew(value : bool) -> SDValueBool:
        """
        Create new SDValueBool

        :param value: The name of the enum type
        """
        outSDValueBool = ctypes.c_void_p()
        _res = sd.getContext().SDValueBool_sNew(value, ctypes.byref(outSDValueBool))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDValueBool, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDValueBool.value, ownHandle=True)

    def get(self) -> bool:
        """
        Get the base type value as bool

        """
        outValue = ctypes.c_bool()
        _res = self.mAPIContext.SDValueBool_get(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

