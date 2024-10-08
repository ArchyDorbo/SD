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
from .sdtypevector import SDTypeVector
from .sdapiobject import SDAPIObject
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDTypeDouble3(SDTypeVector):
    """
    Class representing the double3 type
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDTypeDouble3
        """
        super(SDTypeDouble3, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew() -> SDTypeDouble3:
        """
        Create new SDTypeDouble3

        """
        outSDTypeDouble3 = ctypes.c_void_p()
        _res = sd.getContext().SDTypeDouble3_sNew(ctypes.byref(outSDTypeDouble3))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDTypeDouble3, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDTypeDouble3.value, ownHandle=True)

