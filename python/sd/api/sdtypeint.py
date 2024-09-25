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
from .sdtypebasetype import SDTypeBaseType
from .sdapiobject import SDAPIObject
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDTypeInt(SDTypeBaseType):
    """
    Class representing the int type
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDTypeInt
        """
        super(SDTypeInt, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew() -> SDTypeInt:
        """
        Create new SDTypeInt

        """
        outSDTypeInt = ctypes.c_void_p()
        _res = sd.getContext().SDTypeInt_sNew(ctypes.byref(outSDTypeInt))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDTypeInt, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDTypeInt.value, ownHandle=True)

