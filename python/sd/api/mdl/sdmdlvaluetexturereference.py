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

from .sdmdlvalueresourcereference import SDMDLValueResourceReference
from ..sdapiobject import SDAPIObject
from ..sdapiobject import SDApiError
from ..apiexception import APIException

class SDMDLValueTextureReference(SDMDLValueResourceReference):
    """
    Class used to store information about a MDL Texture Reference value
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDMDLValueTextureReference
        """
        super(SDMDLValueTextureReference, self).__init__(APIContext, handle, *args, **kwargs)

