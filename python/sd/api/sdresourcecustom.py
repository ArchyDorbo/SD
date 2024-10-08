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

from .sdresource import SDResource
from .sdapiobject import SDAPIObject
from .sdresource import EmbedMethod
from .sdapiobject import SDApiError
from .apiexception import APIException

class SDResourceCustom(SDResource):
    """
    A valid resource whose type is not natively supported
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDResourceCustom
        """
        super(SDResourceCustom, self).__init__(APIContext, handle, *args, **kwargs)

    def getFileContent(self) -> Optional[bytes]:
        """
        Get the content of the file used by the SDResourceCustom

        """
        outFileContent = ctypes.c_char_p()
        _res = self.mAPIContext.SDResourceCustom_getFileContent(self.mHandle, ctypes.byref(outFileContent))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return base64.b64decode(outFileContent.value) # type: ignore

