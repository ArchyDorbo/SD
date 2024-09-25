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
from sd.tools import io
from sd.api import sdbasetypes, sdgraph, sdvalue, sdtexture, sdarray

from sd.api import sdvaluebool, sdvaluebool2, sdvaluebool3, sdvaluebool4
from sd.api import sdvalueint, sdvalueint2, sdvalueint3, sdvalueint4
from sd.api import sdvaluefloat, sdvaluefloat2, sdvaluefloat3, sdvaluefloat4
from sd.api import sdvaluedouble, sdvaluedouble2, sdvaluedouble3, sdvaluedouble4
from sd.api import sdvaluestring, sdvaluecolorrgb, sdvaluecolorrgba, sdvaluetexture, sdvaluearray
from sd.api import sdvalueenum, sdvaluestruct, sdvaluematrix

from sd.api.sdnode import SDNode
from sd.api.sdproperty import SDPropertyCategory
from sd.api.sdvalueserializer import SDValueSerializer
from sd.api.mdl import sdmdlvalue, sdmdlvaluecall, sdmdlvaluereference, sdmdlvaluetexturereference, sdmdlvalueparameterreference
from sd.api.mdl import sdmdltypetexturereference

from tests import tools
from tests import data_serializer

import logging
logger = logging.getLogger(__name__)


class TestReadContent(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()
        srcPackageFileName = 'test_read_content.sbs'
        sdPackage = tools.loadSDPackage(context, srcPackageFileName)

        # Check Serialization
        logFileDir = tools.getAssetsDir()
        currentFileBaseName = io.getFileBaseName(__file__)
        srcDumpFile = os.path.join(logFileDir, currentFileBaseName + '.txt')

        dumpLines = data_serializer.DataSerializer().serializeSDPackage(sdPackage)

        # ------------------------------------------------
        # For development only
        createSrcDumpFile = False
        if createSrcDumpFile:
            # test with file
            with open(srcDumpFile, 'wt', encoding='utf-8') as f:
                for line in dumpLines:
                    f.write(line + '\n')
                f.close()
        # ------------------------------------------------

        # Read src Dump File
        srcDumpFileLines = []

        with open(srcDumpFile, 'rt', encoding='utf-8') as rf:
            srcDumpFileLines = rf.readlines()
            rf.close()

        # Compare Lines
        for i in range(0, len(dumpLines)):
            srcLine = srcDumpFileLines[i]
            line = dumpLines[i]
            self.__compareLines(line, srcLine)

        # Check data coherency
        self.__checkSDPackage(sdPackage)

        # Check some MDL Data
        self.__checkMDL(sdPackage)

        # Check some Properties
        self.__checkGetProperties(sdPackage)

    def __compareLines(self, aLine0, aLine1):
        # Remove whitespace.
        a = aLine0.strip()
        b = aLine1.strip()

        # Check if both lines contains paths.
        if a.startswith('FilePath:') and b.startswith('FilePath:'):
            a = a.replace('FilePath:', '').strip()
            b = b.replace('FilePath:', '').strip()

            # TODO: can we do better than comparing filenames here?
            self.assertEqual(os.path.basename(a), os.path.basename(b))
        else:
            self.assertEqual(a, b)

    def __checkSDValue(self, aSDValue):
        if not aSDValue:
            return

        propertyValueType = aSDValue.getType()
        if not propertyValueType:
            return

        propertyValueTypeName = propertyValueType.getId()

        if issubclass(type(aSDValue), sdmdlvalue.SDMDLValue):
            if issubclass(type(aSDValue), sdmdlvaluereference.SDMDLValueReference):
                v = aSDValue.getValue()
                self.assertTrue(type(v) is type(''))
            elif issubclass(type(aSDValue), sdmdlvaluecall.SDMDLValueCall):
                v = aSDValue.getValue()
                self.assertTrue(type(v) is type(''))
            elif issubclass(type(aSDValue), sdmdlvalueparameterreference.SDMDLValueParameterReference):
                v = aSDValue.getReferencedType()

            if issubclass(type(aSDValue), sdmdlvaluetexturereference.SDMDLValueTextureReference):
                textureShape = propertyValueType.getTextureShape()
                self.assertTrue(
                    textureShape == sdmdltypetexturereference.TextureShape.TwoDim or
                    textureShape == sdmdltypetexturereference.TextureShape.ThreeDim or
                    textureShape == sdmdltypetexturereference.TextureShape.Cube or
                    textureShape == sdmdltypetexturereference.TextureShape.Ptex)
        elif issubclass(type(aSDValue), sdvaluestruct.SDValueStruct):
            pass
        elif issubclass(type(aSDValue), sdvalueenum.SDValueEnum):
            v = aSDValue.get()
            self.assertTrue(type(v) is int)
        elif issubclass(type(aSDValue), sdvaluearray.SDValueArray):
            sdArray = aSDValue.get()
            self.assertTrue(sdArray is not None)
            self.assertTrue(type(sdArray) is sdarray.SDArray)
            for itemValue in sdArray:
                if type(itemValue) is sdvalue.SDValue:
                    self.__checkSDValue(itemValue)
        elif issubclass(type(aSDValue), sdvaluetexture.SDValueTexture):
            sdTexture = aSDValue.get()
            self.assertTrue(sdTexture)
            self.assertTrue(type(sdTexture) is sdtexture.SDTexture)
            sdTextureSize = sdTexture.getSize()
            self.assertTrue(sdTextureSize.x >= 0)
            self.assertTrue(sdTextureSize.y >= 0)
        elif issubclass(type(aSDValue), sdvaluematrix.SDValueMatrix):
            sdTypeMatrix = propertyValueType
            columnCount = sdTypeMatrix.getColumnCount()
            rowCount = sdTypeMatrix.getRowCount()
            itemType = sdTypeMatrix.getItemType()
            self.assertTrue(itemType)
            itemTypeName = itemType.getId()
            for columnIndex in range(0,columnCount):
                for rowIndex in range(0, rowCount):
                    itemValue = aSDValue.getItem(columnIndex, rowIndex)
                    itemValueType = itemValue.getType()
                    self.assertTrue(itemValueType)
                    itemValueTypeName = itemValueType.getId()
                    self.assertEqual(itemValueTypeName, itemTypeName)
                    self.__checkSDValue(itemValue)
        elif issubclass(type(aSDValue), sdvaluestring.SDValueString):
            v = aSDValue.get()
            self.assertTrue(type(v) is type(''))
        elif issubclass(type(aSDValue), sdvaluebool.SDValueBool):
            v = aSDValue.get()
            self.assertTrue(type(v) is bool)
        elif issubclass(type(aSDValue), sdvaluebool2.SDValueBool2):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.bool2)
            self.assertTrue(type(v.x) is bool)
            self.assertTrue(type(v.y) is bool)
        elif issubclass(type(aSDValue), sdvaluebool3.SDValueBool3):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.bool3)
            self.assertTrue(type(v.x) is bool)
            self.assertTrue(type(v.y) is bool)
            self.assertTrue(type(v.z) is bool)
        elif issubclass(type(aSDValue), sdvaluebool4.SDValueBool4):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.bool4)
            self.assertTrue(type(v.x) is bool)
            self.assertTrue(type(v.y) is bool)
            self.assertTrue(type(v.z) is bool)
            self.assertTrue(type(v.w) is bool)
        elif issubclass(type(aSDValue), sdvalueint.SDValueInt):
            v = aSDValue.get()
            self.assertTrue(type(v) is int)
        elif issubclass(type(aSDValue), sdvalueint2.SDValueInt2):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.int2)
            self.assertTrue(type(v.x) is int)
            self.assertTrue(type(v.y) is int)
        elif issubclass(type(aSDValue), sdvalueint3.SDValueInt3):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.int3)
            self.assertTrue(type(v.x) is int)
            self.assertTrue(type(v.y) is int)
            self.assertTrue(type(v.z) is int)
        elif issubclass(type(aSDValue), sdvalueint4.SDValueInt4):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.int4)
            self.assertTrue(type(v.x) is int)
            self.assertTrue(type(v.y) is int)
            self.assertTrue(type(v.z) is int)
            self.assertTrue(type(v.w) is int)
        elif issubclass(type(aSDValue), sdvaluefloat.SDValueFloat):
            v = aSDValue.get()
            self.assertTrue(type(v) is float)
        elif issubclass(type(aSDValue), sdvaluefloat2.SDValueFloat2):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.float2)
            self.assertTrue(type(v.x) is float)
            self.assertTrue(type(v.y) is float)
        elif issubclass(type(aSDValue), sdvaluefloat3.SDValueFloat3):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.float3)
            self.assertTrue(type(v.x) is float)
            self.assertTrue(type(v.y) is float)
            self.assertTrue(type(v.z) is float)
        elif issubclass(type(aSDValue), sdvaluefloat4.SDValueFloat4):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.float4)
            self.assertTrue(type(v.x) is float)
            self.assertTrue(type(v.y) is float)
            self.assertTrue(type(v.z) is float)
            self.assertTrue(type(v.w) is float)
        elif issubclass(type(aSDValue), sdvaluedouble.SDValueDouble):
            v = aSDValue.get()
            self.assertTrue(type(v) is float)
        elif issubclass(type(aSDValue), sdvaluedouble2.SDValueDouble2):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.double2)
            self.assertTrue(type(v.x) is float)
            self.assertTrue(type(v.y) is float)
        elif issubclass(type(aSDValue), sdvaluedouble3.SDValueDouble3):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.double3)
            self.assertTrue(type(v.x) is float)
            self.assertTrue(type(v.y) is float)
            self.assertTrue(type(v.z) is float)
        elif issubclass(type(aSDValue), sdvaluedouble4.SDValueDouble4):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.double4)
            self.assertTrue(type(v.x) is float)
            self.assertTrue(type(v.y) is float)
            self.assertTrue(type(v.z) is float)
            self.assertTrue(type(v.w) is float)
        elif issubclass(type(aSDValue), sdvaluecolorrgb.SDValueColorRGB):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.ColorRGB)
            self.assertTrue(type(v.r) is float)
            self.assertTrue(type(v.g) is float)
            self.assertTrue(type(v.b) is float)
        elif issubclass(type(aSDValue), sdvaluecolorrgba.SDValueColorRGBA):
            v = aSDValue.get()
            self.assertTrue(type(v) is sdbasetypes.ColorRGBA)
            self.assertTrue(type(v.r) is float)
            self.assertTrue(type(v.g) is float)
            self.assertTrue(type(v.b) is float)
            self.assertTrue(type(v.a) is float)
        else:
            # Custom type
            logger.debug('Unchecked type "%s" (%s)' % (propertyValueTypeName, str(propertyValueType)))
            e = 0

    def __checkSDProperty(self, aSDItem, aSDProperty):
        propertyId = aSDProperty.getId()
        self.assertTrue(propertyId)

        propertyType = aSDProperty.getType()
        # self.assertTrue(propertyType)

        propertyCategory = aSDProperty.getCategory()
        self.assertTrue(propertyCategory)

        propertySDValue = aSDItem.getPropertyValue(aSDProperty)
        self.__checkSDValue(propertySDValue)

        foundProperty = aSDItem.getPropertyFromId(propertyId, propertyCategory)
        self.assertTrue(foundProperty)
        foundPropertyId = foundProperty.getId()
        self.assertEqual(foundPropertyId, propertyId)
        foundPropertyCategory = foundProperty.getCategory()
        self.assertEqual(foundPropertyCategory, propertyCategory)

    def __checkSDPropertyArray(self, aSDItem, aSDPropertyArray):
        usedPropNames = {}
        for sdProperty in aSDPropertyArray:
            propertyId = sdProperty.getId()
            self.assertTrue(propertyId)
            if propertyId in usedPropNames:
                raise Exception('Property "%s" already defined' % propertyId)
            usedPropNames[propertyId] = True

            self.__checkSDProperty(aSDItem, sdProperty)

    def __checkSDDefinition(self, aSDNode, aSDDefinition):
        if not aSDDefinition:
            return
        self.__checkSDPropertyArray(aSDNode, aSDDefinition.getProperties(SDPropertyCategory.Annotation))
        self.__checkSDPropertyArray(aSDNode, aSDDefinition.getProperties(SDPropertyCategory.Input))
        self.__checkSDPropertyArray(aSDNode, aSDDefinition.getProperties(SDPropertyCategory.Output))

    def __checkSDNode(self, aSDNode):
        nodeDefinition = aSDNode.getDefinition()
        self.assertTrue(nodeDefinition)
        self.__checkSDDefinition(aSDNode, nodeDefinition)

    def __checkSDGraph(self, aSDGraph):
        # Check Properties
        self.__checkSDPropertyArray(aSDGraph, aSDGraph.getProperties(SDPropertyCategory.Annotation))
        self.__checkSDPropertyArray(aSDGraph, aSDGraph.getProperties(SDPropertyCategory.Input))
        self.__checkSDPropertyArray(aSDGraph, aSDGraph.getProperties(SDPropertyCategory.Output))

        # Check Nodes
        sdNodeArray = aSDGraph.getNodes()
        for sdNode in sdNodeArray:
            # Check SDGraph.getNodeFromId()
            sdNodeId = sdNode.getIdentifier()
            sdNode2 = aSDGraph.getNodeFromId(sdNodeId)
            self.assertEqual(sdNode2.getIdentifier(), sdNodeId)
            self.assertEqual(sdNode2.getDefinition().getId(), sdNode.getDefinition().getId())

            self.__checkSDNode(sdNode)

    def __checkSDResource(self, sdResource):
        aSDGraphIdentifier = sdResource.getIdentifier()
        # self.assertTrue(aSDGraphIdentifier)

        sdGraphResourceUrl = sdResource.getUrl()
        # self.assertTrue(sdGraphResourceUrl, 'Resource Url not defined for \'%s\'' % aSDGraphIdentifier)

        sdGraphResourceType = sdResource.getType()
        # self.assertTrue(sdGraphResourceType, 'Resource Type not defined for \'%s\'' % aSDGraphIdentifier)

        # Check if the resource is a SDGraph
        if issubclass(type(sdResource), sdgraph.SDGraph):
            self.__checkSDGraph(sdResource)

    def __checkSDPackage(self, aSDPackage):
        sbsResourceArray = aSDPackage.getChildrenResources(True)
        self.assertTrue(sbsResourceArray)
        for sdResource in sbsResourceArray:
            self.__checkSDResource(sdResource)

        # Specific tests
        self.__specificCheck(aSDPackage)

    def __specificCheckFindResource(self, aSDPackage):
        url = 'pkg:///sbs/compositing/sbs_comp_graph_property_function'
        sdResourceFromUrl = aSDPackage.findResourceFromUrl(url)
        self.assertTrue(sdResourceFromUrl, 'Resource not found for url \'%s\'' % url)

        shortUrl = '/sbs/compositing/sbs_comp_graph_property_function'
        sdResourceFromShortUrl = aSDPackage.findResourceFromUrl(shortUrl)
        self.assertTrue(sdResourceFromShortUrl, 'Resource not found for short url \'%s\'' % shortUrl)

    def __specificCheck(self, aSDPackage):
        self.__specificCheckFindResource(aSDPackage)

    def __checkMDL(self, aSDPackage):
        mdlGraphResource = aSDPackage.findResourceFromUrl('mdl/mdl_graph')
        self.assertTrue(mdlGraphResource)
        sdNodes = mdlGraphResource.getNodes()
        for sdNode in sdNodes:
            nodeDefinition = sdNode.getDefinition()
            if not nodeDefinition:
                continue
            nodeTypeName = nodeDefinition.getId()
            logger.debug('Type: \'%s\'' % nodeTypeName)
            if not nodeTypeName.startswith('mdl::material_surface('):
                continue

            tab = '\t'
            sdproperties = nodeDefinition.getProperties(SDPropertyCategory.Input)
            for sdProperty in sdproperties:
                sdPropertyId = sdProperty.getId()
                logger.debug(tab + 'identifier: \'%s\'' % sdPropertyId)

                sdPropertyType = sdProperty.getType()
                sdPropertyTypeStr = ''
                if sdPropertyType:
                    sdPropertyTypeStr = sdPropertyType.getId()
                logger.debug(tab + 'type: \'%s\'' % sdPropertyTypeStr)

                if sdPropertyId == 'emission':
                    sdPropertyMembers = sdPropertyType.getMembers()
                    self.assertEqual(len(sdPropertyMembers), 3)

                    sdPropertyValue = sdNode.getPropertyValue(sdProperty)
                    self.assertTrue(sdPropertyValue)

                    for sdPropertyMember in sdPropertyMembers:
                        memberName = sdPropertyMember.getId()
                        memberType = sdPropertyMember.getType()
                        if memberType:
                            memberTypeStr = memberType.getId()
                        else:
                            memberTypeStr = 'None'
                        memberValue = sdPropertyValue.getPropertyValueFromId(memberName)
                        if memberValue:
                            memberValueStr = SDValueSerializer.sToString(memberValue)
                        else:
                            memberValueStr = 'None'

                        if memberName == 'emission':
                            # TODO
                            self.assertEqual(memberTypeStr, 'mdl::edf')
                            self.assertEqual(memberValueStr, 'SDMDLValueEDF()')
                        elif memberName == 'intensity':
                            self.assertEqual(memberTypeStr, 'ColorRGB')
                            self.assertEqual(memberValueStr, 'SDValueColorRGB(ColorRGB(0.050875999,0.214040995,0.522521973))')
                        elif memberName == 'mode':
                            self.assertEqual(memberTypeStr, 'mdl::intensity_mode')
                            self.assertEqual(memberValue.get(), 0)
                            self.assertEqual(memberValueStr, 'SDValueEnum("mdl::intensity_mode",0)')
                        else:
                            self.assertTrue(False, 'Not tested member')

    def __checkGetProperties(self, aSDPackage):
        def __isEqual(aValue0F, aValue1F):
            delta = aValue0F - aValue1F
            aa = abs(delta)
            return aa < 0.000001
        sbsGraph = aSDPackage.findResourceFromUrl('sbs/compositing/sbs_comp_graph_all_nodes')
        self.assertTrue(sbsGraph)
        sdNodes = sbsGraph.getNodes()
        for sdNode in sdNodes:
            nodeDefinition = sdNode.getDefinition()
            if not nodeDefinition:
                continue
            nodeTypeName = nodeDefinition.getId()
            if nodeTypeName == 'uniform':
                propertyId = 'outputcolor'
                sdValue = sdNode.getPropertyValueFromId(propertyId, SDPropertyCategory.Input)
                self.assertTrue(sdValue)

                colorRGBA = sdValue.get()
                self.assertTrue(colorRGBA)

                self.assertTrue(__isEqual(colorRGBA.r, 0.3))
                self.assertTrue(__isEqual(colorRGBA.g, 0.5))
                self.assertTrue(__isEqual(colorRGBA.b, 0.7))
                self.assertTrue(__isEqual(colorRGBA.a, 1.0))

        sbsGraph = aSDPackage.findResourceFromUrl('sbs/compositing/sbs_comp_graph_sub')
        self.assertTrue(sbsGraph)
        propertyId = 'myGraphInput'
        sdValue = sbsGraph.getPropertyValueFromId(propertyId, SDPropertyCategory.Input)
        self.assertTrue(sdValue)
        sdValueAsFloat3 = sdValue.get()
        self.assertTrue(sdValueAsFloat3)
        self.assertTrue(__isEqual(sdValueAsFloat3.x, 0.5))
        self.assertTrue(__isEqual(sdValueAsFloat3.y, 0.7))
        self.assertTrue(__isEqual(sdValueAsFloat3.z, 0.3))

if __name__ == '__main__':
    unittest.main()

