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
from .sdapiobject import SDAPIObject
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDUsage(SDAPIObject):
    """
    Description of an input or output usage
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDUsage
        """
        super(SDUsage, self).__init__(APIContext, handle, *args, **kwargs)

    def getName(self) -> str:
        """
        Get the usage name

        """
        outValue = ctypes.c_char_p()
        _res = self.mAPIContext.SDUsage_getName(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value.decode('utf-8') # type: ignore

    def getComponents(self) -> str:
        """
        Get the components associated to the current usage (R, G, B, A, RGB or RGBA)

        """
        outValue = ctypes.c_char_p()
        _res = self.mAPIContext.SDUsage_getComponents(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value.decode('utf-8') # type: ignore

    def getColorSpace(self) -> str:
        """
        Get the color space associated to the current usage (sRGB, linear, ...)

        """
        outValue = ctypes.c_char_p()
        _res = self.mAPIContext.SDUsage_getColorSpace(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value.decode('utf-8') # type: ignore

    @staticmethod
    def sNew(name : str, components : str, colorSpace : str) -> SDUsage:
        """
        Create a new SDUsage

        :param name: The name of the usage
        :param components: The components of the usage
        :param colorSpace: The color space of the usage
        """
        outSDUsage = ctypes.c_void_p()
        _res = sd.getContext().SDUsage_sNew(ctypes.create_string_buffer(name.encode('utf-8')), ctypes.create_string_buffer(components.encode('utf-8')), ctypes.create_string_buffer(colorSpace.encode('utf-8')), ctypes.byref(outSDUsage))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDUsage, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDUsage.value, ownHandle=True)

