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

from typing import Sequence, Iterator, Iterable, TypeVar, overload

import sd
from .sdapiobject import SDAPIObject
from .sdapiobject import SDApiError
from .apiexception import APIException

T = TypeVar("T", bound=SDAPIObject)
class SDArray(SDAPIObject, Sequence[T], Iterable[T]):
    """
    General-purpose, untyped, ordered collection of SDAPIObject
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDArray[T]
        """
        super(SDArray, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sNew() -> SDArray[SDAPIObject]:
        """
        Create a new SDArray

        """
        outArray = ctypes.c_void_p()
        _res = sd.getContext().SDArray_sNew(ctypes.byref(outArray))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = sd.getContext().mTypeMap[SDAPIObject(sd.getContext(), outArray, ownHandle=False).getClassName()]
        return constructor(sd.getContext(), outArray.value, ownHandle=True)

    def getSize(self) -> int:
        """
        Get the size of the array

        """
        outSize = ctypes.c_size_t()
        _res = self.mAPIContext.SDArray_getSize(self.mHandle, ctypes.byref(outSize))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outSize.value

    def getItem(self, index : int) -> T:
        """
        Get the item located at a specified index

        :param index: The index of the item to retrieve
        """
        outItem = ctypes.c_void_p()
        _res = self.mAPIContext.SDArray_getItem(self.mHandle, index, ctypes.byref(outItem))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        constructor = self.mAPIContext.mTypeMap[SDAPIObject(self.mAPIContext, outItem, ownHandle=False).getClassName()]
        return constructor(self.mAPIContext, outItem.value, ownHandle=True)

    def pushBack(self, item : SDAPIObject) -> None:
        """
        Add the specified item to the end of the array

        :param item: The item to push
        """
        _res = self.mAPIContext.SDArray_pushBack(self.mHandle, item.mHandle)
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None
    # Manually written code patched in by IPA begins
    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[T]: ...

    def __getitem__(self, index) -> T | Sequence[T]:
        """
        :rtype: T
        """
        if isinstance(index, slice):
            raise APIException(SDApiError.NotSupported)
        return self.getItem(index)

    def __len__(self) -> int:
        """
        :rtype: int
        """
        return self.getSize()

    def __iter__(self) -> Iterator[T]:
        class _Iter(Iterator):
            def __init__(self, array):
                self.array = array
                self.current = 0
                self.size = len(array)

            def __next__(self):
                if self.current >= self.size:
                    raise StopIteration
                else:
                    res = self.array[self.current]
                    self.current += 1
                    return res

        return _Iter(self)
    # Manually written code patched in by IPA ends

