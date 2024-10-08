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
from .sdgraph import SDGraph
from .sdgraphobject import SDGraphObject
from .sdapiobject import SDAPIObject
from .sdbasetypes import ColorRGBA
from .sdbasetypes import float2
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDGraphObjectFrame(SDGraphObject):
    """
    Class managing a Frame object in the graph
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDGraphObjectFrame
        """
        super(SDGraphObjectFrame, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew(sdGraph : SDGraph) -> SDGraphObjectFrame:
        """
        Create a new SDGraphObjectFrame instance in the specified graph

        :param sdGraph: The SDGraph that should contains the new outSDGraphObjectFrame
        """
        outSDGraphObjectFrame = ctypes.c_void_p()
        _res = sd.getContext().SDGraphObjectFrame_sNew(sdGraph.mHandle, ctypes.byref(outSDGraphObjectFrame))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDGraphObjectFrame, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDGraphObjectFrame.value, ownHandle=True)

    def getTitle(self) -> str:
        """
        Get the SDGraphObjectFrame title

        """
        outValue = ctypes.c_char_p()
        _res = self.mAPIContext.SDGraphObjectFrame_getTitle(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value.decode('utf-8') # type: ignore

    def setTitle(self, value : str) -> None:
        """
        Set the SDGraphObjectFrame title

        :param value: The new title
        """
        _res = self.mAPIContext.SDGraphObjectFrame_setTitle(self.mHandle, ctypes.create_string_buffer(value.encode('utf-8')))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

    def getColor(self) -> ColorRGBA:
        """
        Get the SDGraphObjectFrame color

        """
        outValue = ColorRGBA()
        _res = self.mAPIContext.SDGraphObjectFrame_getColor(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue

    def setColor(self, value : ColorRGBA) -> None:
        """
        Set the SDGraphObjectFrame color

        :param value: The new color
        """
        _res = self.mAPIContext.SDGraphObjectFrame_setColor(self.mHandle, ctypes.byref(value))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

    def getSize(self) -> float2:
        """
        Get the SDGraphObjectFrame size

        """
        outSize = float2()
        _res = self.mAPIContext.SDGraphObjectFrame_getSize(self.mHandle, ctypes.byref(outSize))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outSize

    def setSize(self, value : float2) -> None:
        """
        Set the SDGraphObjectFrame size

        :param value: The new size
        """
        _res = self.mAPIContext.SDGraphObjectFrame_setSize(self.mHandle, ctypes.byref(value))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

