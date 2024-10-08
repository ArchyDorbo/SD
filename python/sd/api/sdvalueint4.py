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

class SDValueInt4(SDValueVector):
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDValueInt4
        """
        super(SDValueInt4, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew(value : int4) -> SDValueInt4:
        """
        Create new SDValueInt4

        :param value: The name of the enum type
        """
        outSDValueInt4 = ctypes.c_void_p()
        _res = sd.getContext().SDValueInt4_sNew(ctypes.byref(value), ctypes.byref(outSDValueInt4))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDValueInt4, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDValueInt4.value, ownHandle=True)

    def get(self) -> int4:
        """
        Get the base type value as int4

        """
        outValue = int4()
        _res = self.mAPIContext.SDValueInt4_get(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue

