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

from .sdmdlnode import SDMDLNode
from ..sdapiobject import SDAPIObject
from ..sdapiobject import SDApiError
from ..apiexception import APIException

class SDMDLConstantNode(SDMDLNode):
    """
    Class managing a MDL constant node
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDMDLConstantNode
        """
        super(SDMDLConstantNode, self).__init__(APIContext, handle, *args, **kwargs)

    def setExposed(self, isExposed : bool) -> None:
        """
        Exposed or Unexpose the current node

        :param isExposed: Indicates whether the node is exposed
        """
        _res = self.mAPIContext.SDMDLConstantNode_setExposed(self.mHandle, isExposed)
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

    def isExposed(self) -> bool:
        """
        Determine whether the current node is exposed

        """
        outIsExposed = ctypes.c_bool()
        _res = self.mAPIContext.SDMDLConstantNode_isExposed(self.mHandle, ctypes.byref(outIsExposed))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return outIsExposed.value

