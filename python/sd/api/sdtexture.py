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
from enum import Enum
from .sdapiobject import SDAPIObject
from .sdbasetypes import int2
from .sdapiobject import SDApiError
from .apiexception import APIException

class SBSPixelFormat(Enum):
    Unknown = 0
    LUM8 = 1
    LUMALPHA8 = 2
    RGB8 = 3
    BGR8 = 4
    RGBA8 = 5
    BGRA8 = 6
    LUM16 = 7
    LUMALPHA16 = 8
    RGB16 = 9
    RGBA16 = 10
    LUM16F = 11
    LUMALPHA16F = 12
    RGB16F = 13
    RGBA16F = 14
    LUM32F = 15
    LUMALPHA32F = 16
    RGB32F = 17
    RGBA32F = 18

class SDTexture(SDAPIObject):
    """
    Common 2D texture object (i.e. a 2d array of pixels)
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDTexture
        """
        super(SDTexture, self).__init__(APIContext, handle, *args, **kwargs)

    def getSize(self) -> int2:
        """
        Get the size of the texture

        """
        outSize = int2()
        _res = self.mAPIContext.SDTexture_getSize(self.mHandle, ctypes.byref(outSize))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outSize

    def getPixelFormat(self) -> SBSPixelFormat:
        """
        Get the pixel format of the texture (see SBSPixelFormat)

        """
        outPixelFormat = ctypes.c_int()
        _res = self.mAPIContext.SDTexture_getPixelFormat(self.mHandle, ctypes.byref(outPixelFormat))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return SBSPixelFormat(outPixelFormat.value)

    def getBytesPerPixel(self) -> int:
        """
        Get the bytes count per pixel

        """
        outSize = ctypes.c_size_t()
        _res = self.mAPIContext.SDTexture_getBytesPerPixel(self.mHandle, ctypes.byref(outSize))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outSize.value

    def save(self, filename : str, outputColorSpace : str = "") -> None:
        """
        Save the current texture to the specified file

        :param filename: The absolute file path used to save the texture
        :param outputColorSpace: The destination color space name. If empty, no color transform is applied
        """
        _res = self.mAPIContext.SDTexture_save(self.mHandle, ctypes.create_string_buffer(filename.encode('utf-8')), ctypes.create_string_buffer(outputColorSpace.encode('utf-8')))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

    @staticmethod
    def sFromFile(filename : str) -> Optional[SDTexture]:
        """
        Create a new texture from the specified file

        :param filename: The image absolute file path
        """
        outSDTexture = ctypes.c_void_p()
        _res = sd.getContext().SDTexture_sFromFile(ctypes.create_string_buffer(filename.encode('utf-8')), ctypes.byref(outSDTexture))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDTexture, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDTexture.value, ownHandle=True)

    def getPixelBufferAddress(self) -> int:
        """
        Get the address of the pixel buffer in memory. Take in account the Row pitch that can be negative. In this case the pixel values will be located before this address in memory.

        """
        outPixelBufferAddress = ctypes.c_size_t()
        _res = self.mAPIContext.SDTexture_getPixelBufferAddress(self.mHandle, ctypes.byref(outPixelBufferAddress))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outPixelBufferAddress.value

    def getRowPitch(self) -> int:
        """
        Get the offset between adjacent scanlines, in bytes. This Value can be negative. In this case, all the pixel values will be located before the pixel buffer address.

        """
        outRowPitch = ctypes.c_long()
        _res = self.mAPIContext.SDTexture_getRowPitch(self.mHandle, ctypes.byref(outRowPitch))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outRowPitch.value

