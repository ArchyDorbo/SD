##########################################################################
# ADOBE CONFIDENTIAL
# ___________________
#  Copyright 2010-2024 Adobe
#  All Rights Reserved.
# * NOTICE:  Adobe permits you to use, modify, and distribute this file in
# accordance with the terms of the Adobe license agreement accompanying it.
# If you have received this file from a source other than Adobe,
# then your use, modification, or distribution of it requires the prior
# written permission of Adobe.
##########################################################################

import os
import unittest
import sd

from sd.api.sdproperty import *
from sd.api.sdvaluebool import *
from sd.api.sdvalueint import *
from sd.api.sdvalueint2 import *
from sd.api.sdvalueint3 import *
from sd.api.sdvalueint4 import *
from sd.api.sdvaluefloat import *
from sd.api.sdvaluefloat2 import *
from sd.api.sdvaluefloat3 import *
from sd.api.sdvaluefloat4 import *

from sd.api.sdvalueserializer import *

from tests import tools
from tests.sdvaluetools import *


class TestSDSBSGraphComputation(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()
        srcPackageFileName = 'test_read_content.sbs'
        sdPackage = tools.loadSDPackage(context, srcPackageFileName)
        self.assertTrue(sdPackage, 'Fail to load package')

        # Get the graph
        sdSBSCompGraph = sdPackage.findResourceFromUrl('sbs/compositing/sbs_comp_graph_outputs')
        self.assertTrue(sdSBSCompGraph)

        sdSBSCompGraph.compute()

        self.__checkValueProcessorNode(sdSBSCompGraph, '1343239036', SDValueBool.sNew(False))

        self.__checkValueProcessorNode(sdSBSCompGraph, '1343238354', SDValueInt.sNew(10))
        self.__checkValueProcessorNode(sdSBSCompGraph, '1343238355', SDValueInt2.sNew(int2(8, 4)))
        self.__checkValueProcessorNode(sdSBSCompGraph, '1343238353', SDValueInt3.sNew(int3(10, 8, 6)))
        self.__checkValueProcessorNode(sdSBSCompGraph, '1343238356', SDValueInt4.sNew(int4(18, 12, 8, 4)))

        self.__checkValueProcessorNode(sdSBSCompGraph, '1343233566', SDValueFloat.sNew(1.2))
        self.__checkValueProcessorNode(sdSBSCompGraph, '1343238020', SDValueFloat2.sNew(float2(0.552, 0.308)))
        self.__checkValueProcessorNode(sdSBSCompGraph, '1343238028', SDValueFloat3.sNew(float3(0.699, 0.401940047, 0.24966)))
        self.__checkValueProcessorNode(sdSBSCompGraph, '1343238035', SDValueFloat4.sNew(float4(0.81172, 0.58140003, 0.45955, 0.41952)))

        # Check Output that return a texture
        self.__checkOutputTexture(sdSBSCompGraph, '1343386302')


    def __getNodeFromId(self, aSDGraph, aNodeId):
        for sdNode in aSDGraph.getNodes():
            if sdNode.getIdentifier() == aNodeId:
                return sdNode
        return None

    def __getSDSBSCompNodeOutputValue(self, aSDNode):
        sdNodeOutputProperty = aSDNode.getProperties(SDPropertyCategory.Output)[0]
        self.assertTrue(sdNodeOutputProperty)

        outputValue = aSDNode.getPropertyValue(sdNodeOutputProperty)
        self.assertTrue(outputValue)

        return outputValue

    def __getOutputConnectedNode(self, aSDNode):
        sdNodeOutputProperty = aSDNode.getProperties(SDPropertyCategory.Output)[0]
        self.assertTrue(sdNodeOutputProperty)

        outputConnections = aSDNode.getPropertyConnections(sdNodeOutputProperty)
        outputConnection = outputConnections[0]

        node = outputConnection.getInputPropertyNode()
        return node


    def __checkValueProcessorNode(self, aSDGraph, aNodeId, aExpectedValue):
        sdNode = self.__getNodeFromId(aSDGraph, aNodeId)
        self.assertTrue(sdNode)
        sdNodeOutputValue = self.__getSDSBSCompNodeOutputValue(sdNode)
        assertSDValueEqual(self, sdNodeOutputValue, aExpectedValue)

        sdOutputNode = self.__getOutputConnectedNode(sdNode)
        self.assertTrue(sdOutputNode)
        sdOutputNodeOutputValue = self.__getSDSBSCompNodeOutputValue(sdOutputNode)
        assertSDValueEqual(self, sdOutputNodeOutputValue, aExpectedValue)

    def __checkOutputTexture(self, aSDGraph, aNodeId):
        sdNode = self.__getNodeFromId(aSDGraph, aNodeId)
        self.assertTrue(sdNode)
        sdNodeOutputValue = self.__getSDSBSCompNodeOutputValue(sdNode)
        self.assertTrue(isinstance(sdNodeOutputValue, SDValueTexture))

        sdOutputNode = self.__getOutputConnectedNode(sdNode)
        self.assertTrue(sdOutputNode)
        sdOutputNodeOutputValue = self.__getSDSBSCompNodeOutputValue(sdOutputNode)
        self.assertTrue(isinstance(sdOutputNodeOutputValue, SDValueTexture))

if __name__ == '__main__':
    unittest.main()

