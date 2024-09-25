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
from .sdvaluevector import *
from .sdapiobject import *
from .sdbasetypes import *
from .sdapiobject import *
from .apiexception import APIException

class SDValueBool3(SDValueVector):
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDValueBool3
        """
        super(SDValueBool3, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew(value : bool3) -> SDValueBool3:
        """
        Create new SDValueBool3

        :param value: The name of the enum type
        """
        outSDValueBool3 = ctypes.c_void_p()
        _res = sd.getContext().SDValueBool3_sNew(ctypes.byref(value), ctypes.byref(outSDValueBool3))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDValueBool3, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDValueBool3.value, ownHandle=True)

    def get(self) -> bool3:
        """
        Get the base type value as bool3

        """
        outValue = bool3()
        _res = self.mAPIContext.SDValueBool3_get(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue

