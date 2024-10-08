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
from .sdsbscompgraph import SDSBSCompGraph
from ..sdapiobject import SDAPIObject
from ..sdapiobject import SDApiError
from ..apiexception import APIException

class SDSBSGraphThumbnailGenerator(SDAPIObject):
    """
    Utility to generate thumbnails for Substance compositing graphs
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDSBSGraphThumbnailGenerator
        """
        super(SDSBSGraphThumbnailGenerator, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew() -> SDSBSGraphThumbnailGenerator:
        """
        Create a new SDSBSGraphThumbnailGenerator instance

        """
        outSDSBSGraphThumbnailGenerator = ctypes.c_void_p()
        _res = sd.getContext().SDSBSGraphThumbnailGenerator_sNew(ctypes.byref(outSDSBSGraphThumbnailGenerator))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outSDSBSGraphThumbnailGenerator, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outSDSBSGraphThumbnailGenerator.value, ownHandle=True)

    def generateThumbnail(self, sdGraph : SDSBSCompGraph) -> None:
        """
        Generate a thumbnail for a Substance compositing graph

        :param sdGraph: The graph to generate the thumbnail for
        """
        _res = self.mAPIContext.SDSBSGraphThumbnailGenerator_generateThumbnail(self.mHandle, sdGraph.mHandle)
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

    def isFinished(self) -> bool:
        """
        Generate a thumbnail for a Substance compositing graph

        """
        outIsFinished = ctypes.c_bool()
        _res = self.mAPIContext.SDSBSGraphThumbnailGenerator_isFinished(self.mHandle, ctypes.byref(outIsFinished))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outIsFinished.value

    def cancel(self) -> None:
        """
        Cancel the current thumbnail generation

        """
        _res = self.mAPIContext.SDSBSGraphThumbnailGenerator_cancel(self.mHandle)
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

    def getLastError(self) -> Optional[str]:
        """
        Return the last error message. None if no error ocurred

        """
        outMessage = ctypes.c_char_p()
        _res = self.mAPIContext.SDSBSGraphThumbnailGenerator_getLastError(self.mHandle, ctypes.byref(outMessage))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outMessage.value.decode('utf-8') # type: ignore

