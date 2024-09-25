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

from enum import Enum
from .sdarray import SDArray
from .sdtype import SDType
from .sdvalue import SDValue
from .sdapiobject import SDAPIObject
from .sdtype import SDTypeModifier
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDPropertyCategory(Enum):
    Annotation = 0
    Input = 1
    Output = 2

class SDPropertyInheritanceMethod(Enum):
    """Property value is relative to the node that is connected to this input property"""
    RelativeToInput = 0
    """Property value is relative to the graph containing the node of this input property"""
    RelativeToParent = 1
    """Property value is not relative"""
    Absolute = 2

class SDProperty(SDAPIObject):
    """
    Description of property defined by an identifier, a type, and some additional information
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDProperty
        """
        super(SDProperty, self).__init__(APIContext, handle, *args, **kwargs)

    def getId(self) -> str:
        """
        Get the identifier of the property. The identifier is unique in the current category.

        """
        outId = ctypes.c_char_p()
        _res = self.mAPIContext.SDProperty_getId(self.mHandle, ctypes.byref(outId))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outId.value.decode('utf-8') # type: ignore

    def getTypes(self) -> SDArray[SDType]:
        """
        Get all types supported by this property

        """
        outSDArrayOfSDType = ctypes.c_void_p()
        _res = self.mAPIContext.SDProperty_getTypes(self.mHandle, ctypes.byref(outSDArrayOfSDType))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = self.mAPIContext.mTypeMap[SDAPIObject(self.mAPIContext, outSDArrayOfSDType, ownHandle=False).getClassName()]
        return constructor(self.mAPIContext, outSDArrayOfSDType.value, ownHandle=True)

    def getType(self) -> Optional[SDType]:
        """
        Get the first type of all available types returned by getTypes() (defined for convenience)

        """
        outType = ctypes.c_void_p()
        _res = self.mAPIContext.SDProperty_getType(self.mHandle, ctypes.byref(outType))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = self.mAPIContext.mTypeMap[SDAPIObject(self.mAPIContext, outType, ownHandle=False).getClassName()]
        return constructor(self.mAPIContext, outType.value, ownHandle=True)

    def getDefaultValue(self) -> Optional[SDValue]:
        """
        Get the default value of the property

        """
        outValue = ctypes.c_void_p()
        _res = self.mAPIContext.SDProperty_getDefaultValue(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = self.mAPIContext.mTypeMap[SDAPIObject(self.mAPIContext, outValue, ownHandle=False).getClassName()]
        return constructor(self.mAPIContext, outValue.value, ownHandle=True)

    def getLabel(self) -> str:
        """
        Get the label of the property

        """
        outLabel = ctypes.c_char_p()
        _res = self.mAPIContext.SDProperty_getLabel(self.mHandle, ctypes.byref(outLabel))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outLabel.value.decode('utf-8') # type: ignore

    def getDescription(self) -> str:
        """
        Get the description of the property

        """
        outDescription = ctypes.c_char_p()
        _res = self.mAPIContext.SDProperty_getDescription(self.mHandle, ctypes.byref(outDescription))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outDescription.value.decode('utf-8') # type: ignore

    def getCategory(self) -> SDPropertyCategory:
        """
        Get the category of the property (see SDPropertyCategory)

        """
        outSDPropertyCategory = ctypes.c_int()
        _res = self.mAPIContext.SDProperty_getCategory(self.mHandle, ctypes.byref(outSDPropertyCategory))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return SDPropertyCategory(outSDPropertyCategory.value)

    def isConnectable(self) -> bool:
        """
        Indicates whether the property is connectable (i.e. if another node's property can be connected to it)

        """
        outValue = ctypes.c_bool()
        _res = self.mAPIContext.SDProperty_isConnectable(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

    def isReadOnly(self) -> bool:
        """
        Indicates whether the property is readonly

        """
        outValue = ctypes.c_bool()
        _res = self.mAPIContext.SDProperty_isReadOnly(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

    def isVariadic(self) -> bool:
        """
        Indicates whether the property is variadic. If True, this parameter will be represented as multiple properties on the instance

        """
        outValue = ctypes.c_bool()
        _res = self.mAPIContext.SDProperty_isVariadic(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

    def isPrimary(self) -> bool:
        """
        Indicates whether the property is the primary property in its category

        """
        outValue = ctypes.c_bool()
        _res = self.mAPIContext.SDProperty_isPrimary(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

    def isFunctionOnly(self) -> bool:
        """
        Indicates if the property value is only controlled by a function. If so calling getPropertyValue/setPropertyValue is not allowed

        """
        outValue = ctypes.c_bool()
        _res = self.mAPIContext.SDProperty_isFunctionOnly(self.mHandle, ctypes.byref(outValue))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outValue.value

