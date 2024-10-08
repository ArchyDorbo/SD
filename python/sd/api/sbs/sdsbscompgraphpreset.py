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

from ..sdarray import SDArray
from ..sdgraphpresetinput import SDGraphPresetInput
from ..sdvalue import SDValue
from ..sdapiobject import SDAPIObject
from ..sdapiobject import SDApiError
from ..apiexception import APIException

class SDSBSCompGraphPreset(SDAPIObject):
    """
    Class managing a Substance compositing graph preset
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDSBSCompGraphPreset
        """
        super(SDSBSCompGraphPreset, self).__init__(APIContext, handle, *args, **kwargs)

    def getLabel(self) -> str:
        """
        Get the label of this preset

        """
        outLabel = ctypes.c_char_p()
        _res = self.mAPIContext.SDSBSCompGraphPreset_getLabel(self.mHandle, ctypes.byref(outLabel))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outLabel.value.decode('utf-8') # type: ignore

    def getUserTags(self) -> str:
        """
        Get the user tags of this preset

        """
        outTags = ctypes.c_char_p()
        _res = self.mAPIContext.SDSBSCompGraphPreset_getUserTags(self.mHandle, ctypes.byref(outTags))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outTags.value.decode('utf-8') # type: ignore

    def setUserTags(self, tags : str) -> None:
        """
        Set the user tags of this preset

        :param tags: The user tags
        """
        _res = self.mAPIContext.SDSBSCompGraphPreset_setUserTags(self.mHandle, ctypes.create_string_buffer(tags.encode('utf-8')))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

    def getInputs(self) -> SDArray[SDGraphPresetInput]:
        """
        Get all inputs of this preset

        """
        outArray = ctypes.c_void_p()
        _res = self.mAPIContext.SDSBSCompGraphPreset_getInputs(self.mHandle, ctypes.byref(outArray))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = self.mAPIContext.mTypeMap[SDAPIObject(self.mAPIContext, outArray, ownHandle=False).getClassName()]
        return constructor(self.mAPIContext, outArray.value, ownHandle=True)

    def addInput(self, inputIdentifier : str, sdValue : SDValue) -> SDGraphPresetInput:
        """
        Create a new preset input

        :param inputIdentifier: The identifier of the input to add
        :param sdValue: The new input value
        """
        outInput = ctypes.c_void_p()
        _res = self.mAPIContext.SDSBSCompGraphPreset_addInput(self.mHandle, ctypes.create_string_buffer(inputIdentifier.encode('utf-8')), sdValue.mHandle, ctypes.byref(outInput))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = self.mAPIContext.mTypeMap[SDAPIObject(self.mAPIContext, outInput, ownHandle=False).getClassName()]
        return constructor(self.mAPIContext, outInput.value, ownHandle=True)

