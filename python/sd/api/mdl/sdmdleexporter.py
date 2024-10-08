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
from .sdmdlgraph import SDMDLGraph
from ..sdapiobject import SDAPIObject
from ..sdapiobject import SDApiError
from ..apiexception import APIException

class SDMDLEExporter(SDAPIObject):
    """
    Utility to export MDLE file
    """
    def __init__(self, APIContext, handle, *args, **kwargs):
        """
        Constructor

        :rtype: SDMDLEExporter
        """
        super(SDMDLEExporter, self).__init__(APIContext, handle, *args, **kwargs)

    @staticmethod
    def sExportGraph(sdMDLGraph : SDMDLGraph, mdleFilePath : str) -> None:
        """
        Export the specified SDMDLGraph as a .mdle file

        :param sdMDLGraph: The SDMDLGraph to export
        :param mdleFilePath: The file path of the .mdle that will be generated
        """
        _res = sd.getContext().SDMDLEExporter_sExportGraph(sdMDLGraph.mHandle, ctypes.create_string_buffer(mdleFilePath.encode('utf-8')))
        if _res != SDApiError.NoError.value:
            if _res == SDApiError.NoErrorOutputParamNotSet.value:
                return None # type: ignore
            raise APIException(SDApiError(_res))
        return None

