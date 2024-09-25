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
import sd.api.sdvalue
from sd.api.sdnode import *
from sd.tools import io
from tests.sdvaluetools import *

from sd.api.sdtypebool import *
from sd.api.sdtypebool2 import *
from sd.api.sdtypebool3 import *
from sd.api.sdtypebool4 import *
from sd.api.sdtypeint import *
from sd.api.sdtypeint2 import *
from sd.api.sdtypeint3 import *
from sd.api.sdtypeint4 import *
from sd.api.sdtypefloat import *
from sd.api.sdtypefloat2 import *
from sd.api.sdtypefloat3 import *
from sd.api.sdtypefloat4 import *
from sd.api.sdtypedouble import *
from sd.api.sdtypedouble2 import *
from sd.api.sdtypedouble3 import *
from sd.api.sdtypedouble4 import *
from sd.api.sdtypestring import *
from sd.api.sdtypecolorrgb import *
from sd.api.sdtypecolorrgba import *
from sd.api.sdtypetexture import *
from sd.api.sdtypearray import *
from sd.api.sdtypestruct import *
from sd.api.sdtypematrix import *
from sd.api.sdtypeenum import *
from sd.api.sdtypeusage import *
from sd.api.mdl.sdmdltype import *

from sd.api.sdvaluebool import *
from sd.api.sdvaluebool2 import *
from sd.api.sdvaluebool3 import *
from sd.api.sdvaluebool4 import *
from sd.api.sdvalueint import *
from sd.api.sdvalueint2 import *
from sd.api.sdvalueint3 import *
from sd.api.sdvalueint4 import *
from sd.api.sdvaluefloat import *
from sd.api.sdvaluefloat2 import *
from sd.api.sdvaluefloat3 import *
from sd.api.sdvaluefloat4 import *
from sd.api.sdvaluedouble import *
from sd.api.sdvaluedouble2 import *
from sd.api.sdvaluedouble3 import *
from sd.api.sdvaluedouble4 import *
from sd.api.sdvaluestring import *
from sd.api.sdvaluecolorrgb import *
from sd.api.sdvaluecolorrgba import *
from sd.api.sdvaluetexture import *
from sd.api.sdvaluearray import *
from sd.api.sdvaluestruct import *
from sd.api.sdvaluematrix import *
from sd.api.sdvalueenum import *
from sd.api.sdvalueusage import *

from sd.api.sdtexture import SDTexture
from sd.api.sdusage import SDUsage
from sd.api.sdarray import SDArray
from sd.api.sdresource import EmbedMethod
from sd.api.sdresourcebitmap import SDResourceBitmap
from sd.api.sdresourcesvg import SDResourceSVG
from sd.api.sdresourcescene import SDResourceScene
from sd.api.sdresourcefont import SDResourceFont
from sd.api.sdresourcefolder import SDResourceFolder
from sd.api.sdresourcelightprofile import SDResourceLightProfile
from sd.api.sdresourcebsdfmeasurement import SDResourceBSDFMeasurement
from sd.api.sdresourcecustom import SDResourceCustom
from sd.api.sdresourcefont import SDResourceFont
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph
from sd.api.sbs.sdsbsfunctiongraph import SDSBSFunctionGraph
from sd.ui import graphgrid
from sd.api.sdproperty import SDPropertyCategory
from sd.api.sdproperty import SDPropertyInheritanceMethod
from tests import tools
from sd.api.sdbasetypes import *
from sd.api.sdvaluematrix import SDValueMatrix
from sd.api.sdvalueserializer import SDValueSerializer
from sd.api.sdmetadatadict import *
from sd.api.sdapiobject import *
from sd.api.apiexception import *

from sd.api.mdl.sdmdlgraph import *
from sd.api.mdl.sdmdlvalue import *
from sd.api.mdl.sdmdlconstantnode import *

import logging
logger = logging.getLogger(__name__)


class TestWriteContent(unittest.TestCase):

    def runTest(self):
        self.mUID = 0
        self.mDebugTestSBS = True
        # self.mDebugTestSBS = False

        self.mDebugTestMDL = True
        # self.mDebugTestMDL = False

        context = sd.getContext()

        pkgMgr = context.getSDApplication().getPackageMgr()
        sdPackage = pkgMgr.newUserPackage()

        self.__testNewResources(sdPackage)
        self.__testSDResource_delete(sdPackage)
        self.__testSDResource_newProperty(sdPackage)
        self.__testSDResource_deleteProperty(sdPackage)
        self.__testSDResource_setPropertyValue(sdPackage)
        self.__testSDResource_setPropertyAnnotationValueFromId(sdPackage)
        self.__testSDNode_newProperty(sdPackage)
        self.__testSDNode_deleteProperty(sdPackage)

        self.__testSDGraph_newNode(sdPackage)
        self.__testSDGraph_newInstanceNode(context, sdPackage)
        self.__testSDGraph_deleteNode(sdPackage)
        self.__testSDGraph_setOutputNode(sdPackage)

        self.__testSDSBSCompGraph_setPropertyInheritanceMethod(sdPackage)

        self.__testSDNode_newPropertyConnection(sdPackage)
        self.__testSDNode_deletePropertyConnection(sdPackage)

        self.__testSDNode_newPropertyGraph(sdPackage)
        self.__testSDNode_deletePropertyGraph(sdPackage)
        self.__testSDNode_setPropertyValue(sdPackage)

        self.__testSDConnection_disconnect(sdPackage)

        if self.mDebugTestMDL:
            self.__testMDLConstantNode_exposition(sdPackage)

        dstFileAbsPath = os.path.join(tools.getTestOutputDir(__file__), 'test_new_content_output.sbs')
        logger.debug('Save output file to ' + dstFileAbsPath)
        pkgMgr.savePackageAs(sdPackage, dstFileAbsPath)

    def __testIsEqual(self, aSDValue0, aSDValue1):
        assertSDValueEqual(self, aSDValue0, aSDValue1)

    def __isCheckValue(self, aSDObject, aSDProperty, aSDValue):
        sdValue = aSDObject.getPropertyValue(aSDProperty)
        self.__testIsEqual(sdValue, aSDValue)

        # Test the getPropertyValueFromId
        sdValueFromId = aSDObject.getPropertyValueFromId(aSDProperty.getId(), aSDProperty.getCategory())
        self.__testIsEqual(sdValueFromId, aSDValue)

    def __setSDObjectPropertyValue(self, aSDObject, aSDProperty, aSDValue):
        if aSDProperty.isFunctionOnly():
            return

        valueStr = SDValueSerializer.sToString(aSDValue)
        logger.debug('        Set value \'%s\' (type:\'%s\') ...' % (valueStr, type(aSDValue).__name__))
        aSDObject.setPropertyValue(aSDProperty, aSDValue)
        self.__isCheckValue(aSDObject, aSDProperty, aSDValue)

        if aSDProperty.getCategory() == SDPropertyCategory.Input:
            aSDObject.setInputPropertyValueFromId(aSDProperty.getId(), aSDValue)
            self.__isCheckValue(aSDObject, aSDProperty, aSDValue)

        elif aSDProperty.getCategory() == SDPropertyCategory.Annotation:
            aSDObject.setAnnotationPropertyValueFromId(aSDProperty.getId(), aSDValue)
            self.__isCheckValue(aSDObject, aSDProperty, aSDValue)

    def __getTestSDValues(self, aSDType):
        values = []
        if isinstance(aSDType, SDTypeBool):
            values.append(SDValueBool.sNew(True))
            values.append(SDValueBool.sNew(False))
        elif isinstance(aSDType, SDTypeBool2):
            boolValues = [True, False]
            for x in boolValues:
                for y in boolValues:
                    values.append(SDValueBool2.sNew(bool2(x, y)))
        elif isinstance(aSDType, SDTypeBool3):
            boolValues = [True, False]
            for x in boolValues:
                for y in boolValues:
                    for z in boolValues:
                        values.append(SDValueBool3.sNew(bool3(x, y, z)))
        elif isinstance(aSDType, SDTypeBool4):
            boolValues = [True, False]
            for x in boolValues:
                for y in boolValues:
                    for z in boolValues:
                        for w in boolValues:
                            values.append(SDValueBool4.sNew(bool4(x, y, z, w)))
        elif isinstance(aSDType, SDTypeInt):
            for v in [0, 1]:
                values.append(SDValueInt.sNew(v))
        elif isinstance(aSDType, SDTypeInt2):
            for v in [int2(0, 1), int2(5, 8)]:
                values.append(SDValueInt2.sNew(v))
        elif isinstance(aSDType, SDTypeInt3):
            for v in [int3(0, 1, 3), int3(5, 8, 4)]:
                values.append(SDValueInt3.sNew(v))
        elif isinstance(aSDType, SDTypeInt4):
            for v in [int4(0, 1, 3, 4), int4(5, 8, 4, 8)]:
                values.append(SDValueInt4.sNew(v))
        elif isinstance(aSDType, SDTypeFloat):
            for v in [0.21, -1.3]:
                values.append(SDValueFloat.sNew(v))
        elif isinstance(aSDType, SDTypeFloat2):
            for v in [float2(0.21, 1.43), float2(5.21, 8.21)]:
                values.append(SDValueFloat2.sNew(v))
        elif isinstance(aSDType, SDTypeFloat3):
            for v in [float3(0.43, 1.21, 3.21), float3(5.21, 8.43, 4.21)]:
                values.append(SDValueFloat3.sNew(v))
        elif isinstance(aSDType, SDTypeFloat4):
            for v in [float4(0.5, -1, 0.8, 0.43), float4(-0.43, 0, -0.5, 0)]:
                values.append(SDValueFloat4.sNew(v))
        elif isinstance(aSDType, SDTypeDouble):
            for v in [0.21, -1.3]:
                values.append(SDValueDouble.sNew(v))
        elif isinstance(aSDType, SDTypeDouble2):
            for v in [double2(0.21, 1.43), double2(5.21, 8.21)]:
                values.append(SDValueDouble2.sNew(v))
        elif isinstance(aSDType, SDTypeDouble3):
            for v in [double3(0.43, 1.21, 3.21), double3(5.21, 8.43, 4.21)]:
                values.append(SDValueDouble3.sNew(v))
        elif isinstance(aSDType, SDTypeDouble4):
            for v in [double4(0.5, -1, 0.8, 0.43), double4(-0.43, 0, -0.5, 0)]:
                values.append(SDValueDouble4.sNew(v))
        elif isinstance(aSDType, SDTypeColorRGBA):
            for v in [ColorRGBA(0.5, 1, 0.8, 0.43), ColorRGBA(0.43, 0, 0.5, 0)]:
                values.append(SDValueColorRGBA.sNew(v))
        elif isinstance(aSDType, SDTypeColorRGB):
            for v in [ColorRGB(0.5, 1, 0.8)]:
                values.append(SDValueColorRGB.sNew(v))
        elif isinstance(aSDType, SDTypeString):
            v = 'test_string_' + str(self.mUID)
            self.mUID += 1
            values.append(SDValueString.sNew(v))
        elif isinstance(aSDType, SDTypeTexture):
            textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'substance-128x128.png')
            sdTexture = SDTexture.sFromFile(textureFileAbsPath)
            self.assertTrue(sdTexture)
            values.append(SDValueTexture.sNew(sdTexture))
        elif isinstance(aSDType, SDTypeArray):
            itemType = aSDType.getItemType()
            arraySize = aSDType.getSize()

            # Fill Array
            sdValueArray = SDValueArray.sNew(itemType, arraySize)
            self.assertTrue(sdValueArray)
            for i in range(arraySize):
                sdValue = self.__getTestSDValues(itemType)
                if sdValue:
                    sdValueArray.setItem(i, sdValue[0])

            values.append(sdValueArray)
        elif isinstance(aSDType, SDTypeStruct):
            sdValueStruct = SDValueStruct.sNew(aSDType)
            self.assertTrue(sdValueStruct)

            sdValueStructType = sdValueStruct.getType()
            self.assertTrue(sdValueStructType)
            self.assertTrue(sdValueStructType.getId() == aSDType.getId())

            # Test SDValueStruct.sNew()
            sdTypeStruct = SDTypeStruct.sNew(sdValueStructType.getId())
            sdValueStructFromName = SDValueStruct.sNew(sdTypeStruct)
            self.assertTrue(sdValueStructFromName)

            # Fill the structure members values
            for structProperty in sdValueStructType.getMembers():
                sdValues = self.__getTestSDValues(structProperty.getType())
                if sdValues:
                    sdValue = sdValues[0]
                    sdValueStruct.setPropertyValue(structProperty, sdValue)

            values.append(sdValueStruct)
        elif isinstance(aSDType, SDTypeMatrix):
            sdValueMatrix = SDValueMatrix.sNewFromSDTypeMatrix(aSDType)
            # Set some values
            columnCount = sdValueMatrix.getColumnCount()
            rowCount = sdValueMatrix.getRowCount()
            sdValues = self.__getTestSDValues(aSDType.getItemType())
            self.assertTrue(sdValues)
            sdValuesIndex = 0
            for columnIndex in range(columnCount):
                for rowIndex in range(rowCount):
                    if sdValuesIndex >= len(sdValues):
                        sdValuesIndex = 0
                    sdValue = sdValues[sdValuesIndex]
                    self.assertTrue(sdValue)
                    sdValuesIndex += 1
                    sdValueMatrix.setItem(columnIndex, rowIndex, sdValue)
            values.append(sdValueMatrix)
        elif isinstance(aSDType, SDTypeEnum):
            # Get members
            availableIntValues = []
            for enumerator in aSDType.getEnumerators():
                availableIntValues.append(int(enumerator.getDefaultValue().get()))

            for value in availableIntValues:
                values.append(SDValueEnum.sFromValue(aSDType.getId(), value))
        elif isinstance(aSDType, SDTypeUsage):
            values.append(SDValueUsage.sNew(SDUsage.sNew('baseColor', 'RGBA', 'sRGB')))
            values.append(SDValueUsage.sNew(SDUsage.sNew('normal', 'RGBA', 'linear')))
        elif isinstance(aSDType, SDMDLType):
            # TODO: do some specific test for specific MLD types
            return []
        else:
            raise Exception('Can\'t instantiate value from an unknown type: \'%s\' (%s)' % (aSDType.getId(), type(aSDType).__name__))

        if not values:
            raise Exception('No test values generated from the following type: \'%s\' (%s)' % (aSDType.getId(), type(aSDType).__name__))
        return values

    def __testSDPropertyValue(self, aSDObject, aSDProperty):
        def __getId(aSDObject):
            if isinstance(aSDObject, SDNode):
                return aSDObject.getDefinition().getId()
            return aSDObject.getType().getId()

        logger.debug('Test Property modification for %s(\'%s\').%s (category:%s)...' % (
            type(aSDObject).__name__,
            __getId(aSDObject),
            aSDProperty.getId(),
            str(aSDProperty.getCategory().name)))
        if aSDProperty.isReadOnly():
            logger.debug('    Property is ReadOnly')
            return

        propertyTypes = aSDProperty.getTypes()
        for sdPropertyType in propertyTypes:
            if not sdPropertyType:
                continue

            if sdPropertyType:
                sdPropertyTypeName = sdPropertyType.getId()
            else:
                sdPropertyTypeName = ''
            logger.debug('    Test Type: \'%s\'' % sdPropertyTypeName)

            sdTestValues = self.__getTestSDValues(sdPropertyType)
            if not sdTestValues:
                logger.debug('    No test values defined for type: \'%s\' (%s)' % (sdPropertyType.getId(), type(sdPropertyType).__name__))
                return

            for sdValue in sdTestValues:
                self.assertTrue(sdValue)
                self.__setSDObjectPropertyValue(aSDObject, aSDProperty, sdValue)

    def __testSDProperties(self, aSDObject, aSDPropertyCategory):
        sdPropertyArray = aSDObject.getProperties(aSDPropertyCategory)
        for sdProperty in sdPropertyArray:
            self.__testSDPropertyValue(aSDObject, sdProperty)

            # Test the getPropertyFromId method
            sdPropertyFromId = aSDObject.getPropertyFromId(sdProperty.getId(), aSDPropertyCategory)
            self.assertTrue(sdPropertyFromId)

    def __testAllSDProperties(self, aSDObject):
        self.__testSDProperties(aSDObject, SDPropertyCategory.Input)
        self.__testSDProperties(aSDObject, SDPropertyCategory.Output)
        self.__testSDProperties(aSDObject, SDPropertyCategory.Annotation)

    def __testSDResource_getPackage(self, aSDResource, aSDPackage):
        sdResourcePackage = aSDResource.getPackage()
        self.assertTrue(sdResourcePackage, 'Fail to get the SDPackage from the SDResource')
        self.assertEqual(sdResourcePackage.getFilePath(), aSDPackage.getFilePath())
        resourceFound = False
        for sdResource in sdResourcePackage.getChildrenResources(True):
            if sdResource.getUrl() == aSDResource.getUrl():
                resourceFound = True
                break
        self.assertTrue(resourceFound, 'The specified SDResource has not been found in the package returned by SDResource.getPackage()')

    def __testNewResources(self, aSDPackage):
        # SDSBSCompGraph
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        self.assertTrue(sdSBSCompGraph, 'Fail to create new Resource')
        sdSBSCompGraph.setIdentifier('test_new_resources_sbs_comp_graph')
        self.assertEqual(sdSBSCompGraph.getIdentifier(), 'test_new_resources_sbs_comp_graph', 'Fail to set identifier')
        self.assertEqual(sdSBSCompGraph.getType().getId(), 'SDSBSCompGraph')
        self.assertTrue(sdSBSCompGraph.getUrl().startswith('pkg:///test_new_resources_sbs_comp_graph?dependency='))
        self.__testAllSDProperties(sdSBSCompGraph)
        self.__testSDResource_getPackage(sdSBSCompGraph, aSDPackage)

        # SDSBSFunctionGraph
        sdSBSFuncGraph = SDSBSFunctionGraph.sNew(aSDPackage)
        self.assertTrue(sdSBSFuncGraph, 'Fail to create new Resource')
        sdSBSFuncGraph.setIdentifier('test_new_resources_sbs_function_graph')
        self.assertEqual(sdSBSFuncGraph.getIdentifier(), 'test_new_resources_sbs_function_graph', 'Fail to set identifier')
        self.assertEqual(sdSBSFuncGraph.getType().getId(), 'SDSBSFunctionGraph')
        self.assertTrue(sdSBSFuncGraph.getUrl().startswith('pkg:///test_new_resources_sbs_function_graph?dependency='))
        self.__testAllSDProperties(sdSBSFuncGraph)
        self.__testSDResource_getPackage(sdSBSFuncGraph, aSDPackage)

        sdResourceFolder = SDResourceFolder.sNew(aSDPackage)
        self.assertTrue(sdResourceFolder, 'Fail to create new Resource')
        sdResourceFolder.setIdentifier('test_new_resources_folder')
        self.assertEqual(sdResourceFolder.getIdentifier(), 'test_new_resources_folder', 'Fail to set identifier')
        self.assertEqual(sdResourceFolder.getType().getId(), 'SDResourceFolder')
        self.assertTrue(sdResourceFolder.getUrl().startswith('pkg:///test_new_resources_folder?dependency='))
        self.__testAllSDProperties(sdResourceFolder)
        self.__testSDResource_getPackage(sdResourceFolder, aSDPackage)

        # SDSBSFunctionGraph under a folder
        sdSBSFuncGraph1 = SDSBSFunctionGraph.sNew(sdResourceFolder)
        self.assertTrue(sdSBSFuncGraph1, 'Fail to create new Resource')

        # SDSBSCompGraph under a folder
        sdSBSCompGraph1 = SDSBSCompGraph.sNew(sdResourceFolder)
        self.assertTrue(sdSBSCompGraph1, 'Fail to create new Resource')

        #
        # Resources
        #

        # Check identifier uniqueness
        sdSBSCompGraph2 = SDSBSCompGraph.sNew(sdResourceFolder)
        self.assertTrue(sdSBSCompGraph2, 'Fail to create new Resource')

        sdSBSCompGraph2.setIdentifier(sdSBSCompGraph1.getIdentifier())
        self.assertEqual(sdSBSCompGraph2.getIdentifier(), sdSBSCompGraph1.getIdentifier() + '_1', 'Fail to set identifier')

        # Bitmap
        newSDResourceBitmap = SDResourceBitmap.sNew(sdResourceFolder, int2(512, 512), ColorRGBA(0.2, 0.3, 0.4, 0.8))
        self.assertTrue(newSDResourceBitmap, 'Fail to create new Resource')
        self.__testAllSDProperties(newSDResourceBitmap)
        newSDResourceBitmap.setIdentifier('new_bitmap_resource')
        self.__testSDResource_getPackage(newSDResourceBitmap, aSDPackage)

        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'substance-128x128.png')
        linkedSDResourceBitmap = SDResourceBitmap.sNewFromFile(sdResourceFolder, textureFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceBitmap, 'Fail to create new Resource')
        self.__testAllSDProperties(linkedSDResourceBitmap)
        linkedSDResourceBitmap.setIdentifier('linked_bitmap_resource')
        self.__testSDResource_getPackage(linkedSDResourceBitmap, aSDPackage)

        importedSDResourceBitmap = SDResourceBitmap.sNewFromFile(sdResourceFolder, textureFileAbsPath, EmbedMethod.CopiedAndLinked)
        self.assertTrue(importedSDResourceBitmap, 'Fail to create new Resource')
        self.__testAllSDProperties(importedSDResourceBitmap)
        importedSDResourceBitmap.setIdentifier('imported_bitmap_resource')
        self.__testSDResource_getPackage(importedSDResourceBitmap, aSDPackage)

        # SVG
        newSDResourceSVG = SDResourceSVG.sNew(sdResourceFolder, int2(512, 512))
        self.assertTrue(newSDResourceSVG, 'Fail to create new Resource')
        self.__testAllSDProperties(newSDResourceSVG)
        newSDResourceSVG.setIdentifier('new_svg_resource')
        self.__testSDResource_getPackage(newSDResourceSVG, aSDPackage)

        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'sbs.svg')
        linkedSDResourceSVG = SDResourceSVG.sNewFromFile(sdResourceFolder, textureFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceSVG, 'Fail to create new Resource')
        self.__testAllSDProperties(linkedSDResourceSVG)
        linkedSDResourceSVG.setIdentifier('linked_svg_resource')

        importedSDResourceSVG = SDResourceSVG.sNewFromFile(sdResourceFolder, textureFileAbsPath, EmbedMethod.CopiedAndLinked)
        self.assertTrue(importedSDResourceSVG, 'Fail to create new Resource')
        self.__testAllSDProperties(importedSDResourceSVG)
        importedSDResourceSVG.setIdentifier('imported_svg_resource')
        self.__testSDResource_getPackage(importedSDResourceSVG, aSDPackage)

        # Font From file
        fontFileAbsPath = os.path.join(tools.getAssetsDir(), 'AdobeClean-Regular.ttf')
        linkedSDResourceFont = SDResourceFont.sNewFromFile(sdResourceFolder, fontFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceFont, 'Fail to create new Resource')
        self.__testAllSDProperties(linkedSDResourceFont)
        linkedSDResourceFont.setIdentifier('linked_font_resource')
        self.__testSDResource_getPackage(linkedSDResourceFont, aSDPackage)

        # Scene Primitives
        for scenePrimitiveDefinition in SDResourceScene.sGetAvailablePrimitiveDefinitions():
            scenePrimitiveId = scenePrimitiveDefinition.getId()
            if scenePrimitiveId == 'plane_hires':
                continue # Skipped for performance reasons
            logger.debug('Create new SDResourceScene from primitive Id \'%s\'...' % scenePrimitiveId)
            sdResourceScenePrimitive = SDResourceScene.sNewFromPrimitiveId(sdResourceFolder, scenePrimitiveId)
            self.assertTrue(sdResourceScenePrimitive, 'Fail to create new Scene Resource from primitive "%s"' % scenePrimitiveId)
            self.__testAllSDProperties(sdResourceScenePrimitive)
            sdResourceScenePrimitive.setIdentifier('primitive_scene_resource_' + scenePrimitiveId)
            self.__testSDResource_getPackage(sdResourceScenePrimitive, aSDPackage)

        # Scene From file
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'Rounded Cylinder.fbx')
        linkedSDResourceScene = SDResourceScene.sNewFromFile(sdResourceFolder, sceneFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceScene, 'Fail to create new Resource')
        self.__testAllSDProperties(linkedSDResourceScene)
        linkedSDResourceScene.setIdentifier('linked_scene_resource')
        self.__testSDResource_getPackage(linkedSDResourceScene, aSDPackage)

        # Light Profile from file
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'example_modules.ies')
        linkedSDResourceLightProfile = SDResourceLightProfile.sNewFromFile(sdResourceFolder, sceneFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceLightProfile, 'Fail to create new Resource')
        self.__testAllSDProperties(linkedSDResourceLightProfile)
        linkedSDResourceLightProfile.setIdentifier('linked_light_profile_resource')
        self.__testSDResource_getPackage(linkedSDResourceLightProfile, aSDPackage)

        # BSDF Measurement
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'carpaint_blue.mbsdf')
        linkedSDResourceBSDFMeasurement = SDResourceBSDFMeasurement.sNewFromFile(sdResourceFolder, sceneFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceBSDFMeasurement, 'Fail to create new Resource')
        self.__testAllSDProperties(linkedSDResourceBSDFMeasurement)
        linkedSDResourceBSDFMeasurement.setIdentifier('linked_bsdf_measurement_resource')
        self.__testSDResource_getPackage(linkedSDResourceBSDFMeasurement, aSDPackage)

        # Custom Resource
        customFileAbsPath = os.path.join(tools.getAssetsDir(), 'TEXT.txt')
        linkedSDResourceCustom = SDResource.sNewFromFile(sdResourceFolder, customFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceCustom, 'Fail to create new Resource')
        self.assertIsInstance(linkedSDResourceCustom, SDResourceCustom, 'Custom resource was not created as such')
        self.__testAllSDProperties(linkedSDResourceCustom)
        linkedSDResourceCustom.setIdentifier('linked_custom_resource')
        self.__testSDResource_getPackage(linkedSDResourceCustom, aSDPackage)

    def __testSDResource_delete(self, aSDPackage):
        def __testResourceDeletion(aSDResource, aIndex = 0):
            className = type(aSDResource).__name__
            aSDResource.setIdentifier('test_sdresource_delete_' + className + '_' + str(aIndex))

            resourcePath = aSDResource.getUrl()
            self.assertTrue(aSDPackage.findResourceFromUrl(resourcePath))
            aSDResource.delete()
            self.assertFalse(aSDPackage.findResourceFromUrl(resourcePath))

            return aIndex + 1

        index = 0
        index = __testResourceDeletion(SDResourceFolder.sNew(aSDPackage), index)
        index = __testResourceDeletion(SDSBSCompGraph.sNew(aSDPackage), index)
        index = __testResourceDeletion(SDSBSFunctionGraph.sNew(aSDPackage), index)

        # SDSBSFunctionGraph under a folder
        sdResourceFolder = SDResourceFolder.sNew(aSDPackage)
        sdResourceFolder.setIdentifier('test_sdresource_delete_folder')
        index = __testResourceDeletion(SDSBSCompGraph.sNew(sdResourceFolder), index)
        index = __testResourceDeletion(SDSBSFunctionGraph.sNew(sdResourceFolder), index)
        index = __testResourceDeletion(SDResourceBitmap.sNew(sdResourceFolder, int2(512, 512), ColorRGBA(0.2, 0.3, 0.4, 0.8)), index)

        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'substance-128x128.png')
        index = __testResourceDeletion(SDResourceBitmap.sNewFromFile(sdResourceFolder, textureFileAbsPath, EmbedMethod.Linked), index)
        index = __testResourceDeletion(SDResourceBitmap.sNewFromFile(sdResourceFolder, textureFileAbsPath, EmbedMethod.CopiedAndLinked), index)

        # SVG
        index = __testResourceDeletion(SDResourceSVG.sNew(sdResourceFolder, int2(512, 512)), index)

        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'sbs.svg')
        index = __testResourceDeletion(SDResourceSVG.sNewFromFile(sdResourceFolder, textureFileAbsPath, EmbedMethod.Linked), index)
        index = __testResourceDeletion(SDResourceSVG.sNewFromFile(sdResourceFolder, textureFileAbsPath, EmbedMethod.CopiedAndLinked), index)

        # Font From file
        fontFileAbsPath = os.path.join(tools.getAssetsDir(), 'AdobeClean-Regular.ttf')
        index = __testResourceDeletion(SDResourceFont.sNewFromFile(sdResourceFolder, fontFileAbsPath, EmbedMethod.Linked), index)

        # Scene Primitives
        for scenePrimitiveDefinition in SDResourceScene.sGetAvailablePrimitiveDefinitions():
            scenePrimitiveId = scenePrimitiveDefinition.getId()
            if scenePrimitiveId == 'plane_hires':
                continue # Skipped for performance reasons
            logger.debug('Create new SDResourceScene from primitive Id \'%s\'...' % scenePrimitiveId)
            index = __testResourceDeletion(SDResourceScene.sNewFromPrimitiveId(sdResourceFolder, scenePrimitiveId), index)

        # Scene From file
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'Rounded Cylinder.fbx')
        index = __testResourceDeletion(SDResourceScene.sNewFromFile(sdResourceFolder, sceneFileAbsPath, EmbedMethod.Linked), index)

        # Light Profile from file
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'example_modules.ies')
        index = __testResourceDeletion(SDResourceLightProfile.sNewFromFile(sdResourceFolder, sceneFileAbsPath, EmbedMethod.Linked), index)

        # BSDF Measurement
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'carpaint_blue.mbsdf')
        index = __testResourceDeletion(SDResourceBSDFMeasurement.sNewFromFile(sdResourceFolder, sceneFileAbsPath, EmbedMethod.Linked), index)

        # Custom Resource
        customFileAbsPath = os.path.join(tools.getAssetsDir(), 'TEXT.txt')
        index = __testResourceDeletion(SDResource.sNewFromFile(sdResourceFolder, customFileAbsPath, EmbedMethod.Linked), index)

    def __layoutNodes(self, aNodeList):
        posX = 0
        posY = 0
        nodeSize = graphgrid.GraphGrid.sGetFirstLevelSize() * 2
        for node in aNodeList:
            # Set position
            node.setPosition(float2(posX * nodeSize, posY * nodeSize))
            posX = posX + 1
            if posX > 20:
                posX = 0
                posY = posY + 1

    def __testGraphNodeCreation(self, aGraph):
        # Create all available nodes
        nodes = []
        nodeDefinitions = aGraph.getNodeDefinitions()
        nodeDefinitionsSize = len(nodeDefinitions)
        for i in range(nodeDefinitionsSize):
            nodeDefinition = nodeDefinitions[i]
            nodeDefinitionId = nodeDefinition.getId()

            # if i < 927:
            #     continue

            # Create Node
            logger.debug('[%d/%d] Create Node of type %s...' % (i, nodeDefinitionsSize, nodeDefinitionId))
            node = aGraph.newNode(nodeDefinitionId)
            self.assertTrue(node, 'Fail to create new node')
            nodes.append(node)

            # Test all properties
            self.__testAllSDProperties(node)

        # Layout Nodes
        self.__layoutNodes(nodes)

    def __testSDGraph_newNode(self, aSDPackage):
        if self.mDebugTestSBS:
            # SDSBSCompGraph
            sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
            sdSBSCompGraph.setIdentifier('test_sdgraph_new_node_sdsbscompgraph')
            self.__testGraphNodeCreation(sdSBSCompGraph)

            # SDSBSFxMapGraph
            fxMapNode = sdSBSCompGraph.newNode('sbs::compositing::fxmaps')
            self.assertTrue(fxMapNode, 'Fail to create new node')
            fxMapGraph = fxMapNode.getReferencedResource()
            self.assertTrue(fxMapGraph, 'Fail to create new node')
            self.__testGraphNodeCreation(fxMapGraph)

            # SDSBSFunctionGraph
            sdSBSFunctionGraph = SDSBSFunctionGraph.sNew(aSDPackage)
            sdSBSFunctionGraph.setIdentifier('test_sdgraph_new_node_sdsbsfucntiongraph')
            self.__testGraphNodeCreation(sdSBSFunctionGraph)

        # MDLGraph
        if self.mDebugTestMDL:
            sdMDLGraph = SDMDLGraph.sNew(aSDPackage)
            sdMDLGraph.setIdentifier('test_mdl_node_creation')
            self.__testGraphNodeCreation(sdMDLGraph)

    def __testSDGraph_deleteNode_AllGraph(self, aSDGraph):
        # Delete all graph nodes nodes
        graphNodes0 = aSDGraph.getNodes()
        self.assertGreater(len(graphNodes0), 0, 'The graph should contains some nodes')
        for node in graphNodes0:
            aSDGraph.deleteNode(node)

        graphNodes1 = aSDGraph.getNodes()
        self.assertEqual(len(graphNodes1), 0, 'The graph should be empty')

    def __testSDGraph_deleteNode_SDSBSCompGraph(self, aSDPackage):
        sdGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdGraph.setIdentifier('test_sbs_comp_node_deletion')

        # Create Node
        sdGraph.newNode('sbs::compositing::uniform')
        self.__testSDGraph_deleteNode_AllGraph(sdGraph)

    def __testSDGraph_deleteNode_SDSBSFuncGraph(self, aSDPackage):
        sdGraph = SDSBSFunctionGraph.sNew(aSDPackage)
        sdGraph.setIdentifier('test_sbs_function_node_deletion')

        # Create Node
        sdGraph.newNode('sbs::function::add')
        self.__testSDGraph_deleteNode_AllGraph(sdGraph)

    def __testSDGraph_deleteNode_SDSBSFxMapGraph(self, aSDPackage):
        sdGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdGraph.setIdentifier('test_sbs_fxmap_node_deletion')

        # Create Node
        sdNodeFxMap = sdGraph.newNode('sbs::compositing::fxmaps')

        sdFxMapGraph = sdNodeFxMap.getReferencedResource()
        sdFxMapGraph.newNode('sbs::fxmap::paramset')
        self.__testSDGraph_deleteNode_AllGraph(sdFxMapGraph)

    def __testSDGraph_deleteNode_SDMDLGraph(self, aSDPackage):
        sdGraph = SDMDLGraph.sNew(aSDPackage)
        sdGraph.setIdentifier('test_mdl_node_deletion')

        # Create Node
        sdGraph.newNode('mdl::math::abs(float)')
        self.__testSDGraph_deleteNode_AllGraph(sdGraph)

    def __testSDGraph_deleteNode(self, aSDPackage):
        if self.mDebugTestSBS:
            self.__testSDGraph_deleteNode_SDSBSCompGraph(aSDPackage)
            self.__testSDGraph_deleteNode_SDSBSFuncGraph(aSDPackage)
            self.__testSDGraph_deleteNode_SDSBSFxMapGraph(aSDPackage)
        if self.mDebugTestMDL:
            self.__testSDGraph_deleteNode_SDMDLGraph(aSDPackage)

    def __testSDSBSCompGraph_setPropertyInheritanceMethod(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_sbs_comp_graph_SetPropertyInheritanceMethod')
        outputSizeProperty = sdSBSCompGraph.getPropertyFromId('$outputsize', SDPropertyCategory.Input)
        self.assertTrue(outputSizeProperty)

        # Set the inheritance mode of the "$outputsize" property of the graph
        graphInheritanceModes = [
            # SDPropertyInheritanceMethod.RelativeToInput, # Not available for a SDSBSCompGraph
            SDPropertyInheritanceMethod.RelativeToParent,
            SDPropertyInheritanceMethod.Absolute]
        for inheritanceMode in graphInheritanceModes:
            sdSBSCompGraph.setPropertyInheritanceMethod(outputSizeProperty, inheritanceMode)
            outputSizeInheritanceMode = sdSBSCompGraph.getPropertyInheritanceMethod(outputSizeProperty)
            self.assertEqual(outputSizeInheritanceMode, inheritanceMode, 'Inheritance Mode not Set Property')

        # Set the inheritance mode of the "$tiling" property of the blend node
        sdSBSCompNodeUniform = sdSBSCompGraph.newNode('sbs::compositing::blend')
        tilingProperty = sdSBSCompNodeUniform.getPropertyFromId('$tiling', SDPropertyCategory.Input)
        self.assertTrue(outputSizeProperty)
        nodeInheritanceModes = [
            SDPropertyInheritanceMethod.RelativeToInput,
            SDPropertyInheritanceMethod.RelativeToParent,
            SDPropertyInheritanceMethod.Absolute]
        for inheritanceMode in nodeInheritanceModes:
            sdSBSCompNodeUniform.setPropertyInheritanceMethod(tilingProperty, inheritanceMode)
            tilingInheritanceMode = sdSBSCompNodeUniform.getPropertyInheritanceMethod(tilingProperty)
            self.assertEqual(tilingInheritanceMode, inheritanceMode, 'Inheritance Mode not Set Property')

    def __testSDNode_newPropertyConnection_SDSBSCompNode(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_connection_creation')

        nodeSize = graphgrid.GraphGrid.sGetFirstLevelSize()

        # Create Uniform Color Node
        uniformColorNode = sdSBSCompGraph.newNode('sbs::compositing::uniform')
        uniformColorNodeOutputProperty = uniformColorNode.getPropertyFromId('unique_filter_output', SDPropertyCategory.Output)
        self.assertTrue(uniformColorNodeOutputProperty)

        # Create Output node
        outputNode = sdSBSCompGraph.newNode('sbs::compositing::output')
        outputNode.setPosition(float2(2*nodeSize, 0))
        outputNodeInputProperty = outputNode.getPropertyFromId('inputNodeOutput', SDPropertyCategory.Input)
        self.assertTrue(outputNodeInputProperty)

        # Create connection between uniform color's output and input connector of Output node
        connection0 = uniformColorNode.newPropertyConnection(uniformColorNodeOutputProperty, outputNode, outputNodeInputProperty)
        self.assertTrue(connection0)

        #   - Check connection0
        connection0OutputPropertyNode = connection0.getOutputPropertyNode()
        self.assertTrue(connection0OutputPropertyNode)
        self.assertEqual(connection0OutputPropertyNode.getDefinition().getId(), uniformColorNode.getDefinition().getId())

        connection0OutputProperty = connection0.getOutputProperty()
        self.assertTrue(connection0OutputProperty)
        self.assertEqual(connection0OutputProperty.getId(), uniformColorNodeOutputProperty.getId())
        self.assertEqual(connection0OutputProperty.getCategory(), uniformColorNodeOutputProperty.getCategory())

        connection0InputPropertyNode = connection0.getInputPropertyNode()
        self.assertTrue(connection0InputPropertyNode)
        self.assertEqual(connection0InputPropertyNode.getDefinition().getId(), outputNode.getDefinition().getId())

        connection0InputProperty = connection0.getInputProperty()
        self.assertTrue(connection0InputProperty)
        self.assertEqual(connection0InputProperty.getId(), outputNodeInputProperty.getId())
        self.assertEqual(connection0InputProperty.getCategory(), outputNodeInputProperty.getCategory())

        # Create Blend node
        blendNode = sdSBSCompGraph.newNode('sbs::compositing::blend')
        blendNode.setPosition(float2(outputNode.getPosition().x, 2*nodeSize))
        # blendNodeInputProperty = blendNode.getPropertyFromId('destination', SDPropertyCategory.Input)
        # self.assertTrue(blendNodeInputProperty)

        # Create connection between uniform color's output and 'background' connector of Blend node
        connection1 = uniformColorNode.newPropertyConnectionFromId('unique_filter_output', blendNode, 'destination')
        self.assertTrue(connection1)

        # Check Connections count
        self.assertEqual(len(uniformColorNode.getPropertyConnections(uniformColorNodeOutputProperty)), 2, 'Invalid connections count')

    def __testSDNode_newPropertyConnection_SDMDLNode(self, aSDPackage):
        sdMDLGraph = SDMDLGraph.sNew(aSDPackage)
        sdMDLGraph.setIdentifier('test_mdl_node_connection_creation')

        boolNode = sdMDLGraph.newNode('mdl::color')
        self.assertTrue(boolNode, 'Fail to create node ' + 'mdl::color')
        tintNode = sdMDLGraph.newNode('mdl::df::tint(color,bsdf)')
        self.assertTrue(tintNode, 'Fail to create node ' + 'mdl::df::tint(color,bsdf)')

        boolNodeOutputProperties = boolNode.getProperties(SDPropertyCategory.Output)
        self.assertGreater(len(boolNodeOutputProperties), 0, 'Wrong property number')
        tintNodeInputProperties = tintNode.getProperties(SDPropertyCategory.Input)
        self.assertGreater(len(tintNodeInputProperties), 0, 'Wrong property number')

        newConnection = boolNode.newPropertyConnection(boolNodeOutputProperties[0], tintNode, tintNodeInputProperties[0])
        self.assertTrue(newConnection, 'Fail to create connection')

        sdMDLGraph.setOutputNode(tintNode, True)
        outputNodes = sdMDLGraph.getOutputNodes()
        self.assertEqual(len(outputNodes), 1, 'No output node found')
        outputNode = outputNodes[0]
        self.assertEqual(outputNode.getDefinition().getId(), tintNode.getDefinition().getId(), 'Fail to create connection')

    def __testSDNode_newPropertyConnection(self, aSDPackage):
        if self.mDebugTestSBS:
            self.__testSDNode_newPropertyConnection_SDSBSCompNode(aSDPackage)
        if self.mDebugTestMDL:
            self.__testSDNode_newPropertyConnection_SDMDLNode(aSDPackage)

    def __testSDNode_deletePropertyConnection_SDSBSCompNode(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_connection_deletion')

        nodeSize = graphgrid.GraphGrid.sGetFirstLevelSize()

        # Create Uniform Color Node
        uniformColorNode = sdSBSCompGraph.newNode('sbs::compositing::uniform')

        # Create Output node
        outputNode = sdSBSCompGraph.newNode('sbs::compositing::output')
        outputNode.setPosition(float2(2*nodeSize, 0))

        # Create Blend node
        blendNode = sdSBSCompGraph.newNode('sbs::compositing::blend')
        blendNode.setPosition(float2(outputNode.getPosition().x, 2*nodeSize))

        # Create connection between uniform color's output and 'background' connector of Blend node
        connection0 = uniformColorNode.newPropertyConnectionFromId('unique_filter_output', outputNode, 'inputNodeOutput')
        self.assertTrue(connection0)
        connection1 = uniformColorNode.newPropertyConnectionFromId('unique_filter_output', blendNode, 'source')
        self.assertTrue(connection1)
        connection2 = uniformColorNode.newPropertyConnectionFromId('unique_filter_output', blendNode, 'destination')
        self.assertTrue(connection2)

        uniformColorNodeOutputProperty = uniformColorNode.getPropertyFromId('unique_filter_output', SDPropertyCategory.Output)
        self.assertEqual(len(uniformColorNode.getPropertyConnections(uniformColorNodeOutputProperty)), 3, 'Invalid connections count')

        # Disconnect the link that is connected to the 'destination' of the blend node
        blendNodeDestinationProperty = blendNode.getPropertyFromId('destination', SDPropertyCategory.Input)
        self.assertEqual(len(blendNode.getPropertyConnections(blendNodeDestinationProperty)), 1, 'Invalid connections count')
        blendNode.deletePropertyConnections(blendNodeDestinationProperty)
        self.assertEqual(len(blendNode.getPropertyConnections(blendNodeDestinationProperty)), 0, 'Invalid connections count')

        # Disconnect all output connection of the uniform node connections
        self.assertEqual(len(uniformColorNode.getPropertyConnections(uniformColorNodeOutputProperty)), 2, 'Invalid connections count')
        uniformColorNode.deletePropertyConnections(uniformColorNodeOutputProperty)
        self.assertEqual(len(uniformColorNode.getPropertyConnections(uniformColorNodeOutputProperty)), 0, 'Invalid connections count')

    def __testSDNode_deletePropertyConnection(self, aSDPackage):
        self.__testSDNode_deletePropertyConnection_SDSBSCompNode(aSDPackage)

    def __testSDConnection_disconnect_SDSBSCompNode(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_connection_remove')

        nodeSize = graphgrid.GraphGrid.sGetFirstLevelSize()

        # Create Uniform Color Node
        uniformColorNode = sdSBSCompGraph.newNode('sbs::compositing::uniform')

        # Create Output node
        outputNode = sdSBSCompGraph.newNode('sbs::compositing::output')
        outputNode.setPosition(float2(2*nodeSize, 0))

        # Create Blend node
        blendNode = sdSBSCompGraph.newNode('sbs::compositing::blend')
        blendNode.setPosition(float2(outputNode.getPosition().x, 2*nodeSize))

        # Create connection between uniform color's output and 'background' connector of Blend node
        connection0 = uniformColorNode.newPropertyConnectionFromId('unique_filter_output', outputNode, 'inputNodeOutput')
        self.assertTrue(connection0)
        connection1 = uniformColorNode.newPropertyConnectionFromId('unique_filter_output', blendNode, 'source')
        self.assertTrue(connection1)
        connection2 = uniformColorNode.newPropertyConnectionFromId('unique_filter_output', blendNode, 'destination')
        self.assertTrue(connection2)

        # Disconnect the first connection
        uniformColorNodeOutputProperty = uniformColorNode.getPropertyFromId('unique_filter_output', SDPropertyCategory.Output)
        self.assertEqual(len(uniformColorNode.getPropertyConnections(uniformColorNodeOutputProperty)), 3, 'Invalid connections count')
        connection0.disconnect()
        self.assertEqual(len(uniformColorNode.getPropertyConnections(uniformColorNodeOutputProperty)), 2, 'Invalid connections count')
        connection1.disconnect()
        self.assertEqual(len(uniformColorNode.getPropertyConnections(uniformColorNodeOutputProperty)), 1, 'Invalid connections count')
        connection2.disconnect()
        self.assertEqual(len(uniformColorNode.getPropertyConnections(uniformColorNodeOutputProperty)), 0, 'Invalid connections count')

    def __testSDConnection_disconnect(self, aSDPackage):
        self.__testSDConnection_disconnect_SDSBSCompNode(aSDPackage)

    def __testSDGraph_newInstanceNode_SDSBSCompGraph(self, aContext, aResourceFolder, aAssetsPackage):
        refSDSBSCompGraph = aAssetsPackage.findResourceFromUrl('pbr_graph')
        self.assertTrue(refSDSBSCompGraph)

        sdSBSCompGraph = SDSBSCompGraph.sNew(aResourceFolder)
        sdSBSCompGraph.setIdentifier('sdsbscompgraph')

        # Create SBSCompGraph Instance Node
        node = sdSBSCompGraph.newInstanceNode(refSDSBSCompGraph)
        self.assertTrue(node, 'Fail to create new node')

        # Create instance Node from SDResourceBitmap
        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'substance-128x128.png')
        linkedSDResourceBitmap = SDResourceBitmap.sNewFromFile(aResourceFolder, textureFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceBitmap, 'Fail to create new Resource')
        linkedSDResourceBitmap.setIdentifier('linked_bitmap_resource')
        node = sdSBSCompGraph.newInstanceNode(linkedSDResourceBitmap)
        self.assertTrue(node, 'Fail to create new node')

        # Create instance Node from SDResourceSVG
        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'sbs.svg')
        linkedSDResourceSVG = SDResourceSVG.sNewFromFile(aResourceFolder, textureFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceSVG, 'Fail to create new Resource')
        linkedSDResourceSVG.setIdentifier('linked_svg_resource')
        node = sdSBSCompGraph.newInstanceNode(linkedSDResourceSVG)
        self.assertTrue(node, 'Fail to create new node')

        # Layout nodes
        self.__layoutNodes(sdSBSCompGraph.getNodes())

    def __testSDGraph_newInstanceNode_SDSBSFunctionGraph(self, aContext, aResourceFolder, aAssetsPackage):
        # Load test_write_content.sbs file
        refFunction = aAssetsPackage.findResourceFromUrl('ref_function')
        self.assertTrue(refFunction)

        sdSBSFunctionGraph = SDSBSFunctionGraph.sNew(aResourceFolder)
        sdSBSFunctionGraph.setIdentifier('test_sbs_function_instance_node_creation')

        # Create Instance Node
        node = sdSBSFunctionGraph.newInstanceNode(refFunction)
        self.assertTrue(node, 'Fail to create new node')

    def __testSDGraph_newInstanceNode_SDMDLGraph(self, aContext, aResourceFolder, aAssetsPackage):
        refSBSCompGraph = aAssetsPackage.findResourceFromUrl('pbr_graph')
        self.assertTrue(refSBSCompGraph)
        refMDLGraph = aAssetsPackage.findResourceFromUrl('mdl_dielectric_ior')
        self.assertTrue(refMDLGraph)
        refResourceBitmap = aAssetsPackage.findResourceFromUrl('Resources/substance-128x128')
        self.assertTrue(refResourceBitmap)
        refResourceBSDFMeasurement = aAssetsPackage.findResourceFromUrl('Resources/carpaint_blue')
        self.assertTrue(refResourceBSDFMeasurement)
        refResourceLightProfile = aAssetsPackage.findResourceFromUrl('Resources/example_modules')
        self.assertTrue(refResourceLightProfile)

        sdMDLGraph = SDMDLGraph.sNew(aResourceFolder)
        sdMDLGraph.setIdentifier('test_mdl_instance_node_creation')

        # Create Instance Node
        instanceNode0 = sdMDLGraph.newInstanceNode(refSBSCompGraph)
        self.assertTrue(instanceNode0, 'Fail to create new node')

        instanceNode1 = sdMDLGraph.newInstanceNode(refMDLGraph)
        self.assertTrue(instanceNode1, 'Fail to create new node')

        instanceNode2 = sdMDLGraph.newInstanceNode(refResourceBitmap)
        self.assertTrue(instanceNode2, 'Fail to create new node')

        instanceNode3 = sdMDLGraph.newInstanceNode(refResourceBSDFMeasurement)
        self.assertTrue(instanceNode3, 'Fail to create new node')

        instanceNode4 = sdMDLGraph.newInstanceNode(refResourceLightProfile)
        self.assertTrue(instanceNode4, 'Fail to create new node')

        # Layout nodes
        self.__layoutNodes(sdMDLGraph.getNodes())

    def __testSDGraph_newInstanceNode(self, aContext, aSDPackage):
        # Load test_write_content.sbs file
        assetsPackage = tools.loadSDPackage(aContext, 'test_write_content.sbs')
        self.assertTrue(assetsPackage)

        resourceFolder = SDResourceFolder.sNew(aSDPackage)
        resourceFolder.setIdentifier('test_sdgraph_new_instance_node')

        if self.mDebugTestSBS:
            self.__testSDGraph_newInstanceNode_SDSBSCompGraph(aContext, resourceFolder, assetsPackage)
            self.__testSDGraph_newInstanceNode_SDSBSFunctionGraph(aContext, resourceFolder, assetsPackage)
        if self.mDebugTestMDL:
            self.__testSDGraph_newInstanceNode_SDMDLGraph(aContext, resourceFolder, assetsPackage)

    def __testSDNode_newPropertyGraph(self, aSDPackage, aManageDeletion = False):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        if aManageDeletion:
            sdSBSCompGraph.setIdentifier('test_sbs_comp_node_prop_graph_deletion')
        else:
            sdSBSCompGraph.setIdentifier('test_sbs_comp_node_prop_graph_creation')

        # Set function Graph on a Uniform color
        uniformNode = sdSBSCompGraph.newNode('sbs::compositing::uniform')
        self.assertTrue(uniformNode, 'Fail to create new node')

        uniformNodePropertyOutputColor = uniformNode.getPropertyFromId('outputcolor', SDPropertyCategory.Input)
        self.assertTrue(uniformNodePropertyOutputColor, 'Fail to get outputcolor property')
        propFunctionGraph = uniformNode.newPropertyGraph(uniformNodePropertyOutputColor, 'SDSBSFunctionGraph')
        self.assertTrue(propFunctionGraph, 'Fail to create SDSBSFunctionGraph on property')
        fctNode0 = propFunctionGraph.newNode('sbs::function::const_float4')
        self.assertTrue(fctNode0, 'Fail to create Function Node')

        if aManageDeletion:
            uniformNode.deletePropertyGraph(uniformNodePropertyOutputColor)
            graph = uniformNode.getPropertyGraph(uniformNodePropertyOutputColor)
            self.assertEqual(graph, None, 'The PropertyGraph should have been removed')

        # Set FxMap Graph on a FxMap
        fxMapNode = sdSBSCompGraph.newNode('sbs::compositing::fxmaps')
        self.assertTrue(fxMapNode, 'Fail to create new node')
        fxMapGraph = fxMapNode.getReferencedResource()
        self.assertTrue(fxMapGraph, 'Fail to get the referenced FxMap graph')
        fxMapGraphNodes = fxMapGraph.getNodes()
        self.assertEqual(len(fxMapGraphNodes), 1, 'The FxMap graph should contains at least one node')
        paramsetNode = fxMapGraphNodes[0]
        self.assertEqual(paramsetNode.getDefinition().getId(), 'sbs::fxmap::paramset', 'The FxMap node type should be \'sbs::fxmap::paramset\'')
        paramsetNodePropertyOpacity = paramsetNode.getPropertyFromId('opacity', SDPropertyCategory.Input)
        self.assertTrue(paramsetNodePropertyOpacity, 'Fail to get the \'opacity\' property')
        paramsetNodePropertyOpacityFunctionGraph = paramsetNode.newPropertyGraph(paramsetNodePropertyOpacity, 'SDSBSFunctionGraph')
        self.assertTrue(paramsetNodePropertyOpacityFunctionGraph, 'Fail to create SDSBSFunctionGraph on property')
        fctNode1 = paramsetNodePropertyOpacityFunctionGraph.newNode('sbs::function::const_float4')
        self.assertTrue(fctNode1, 'Fail to create Function Node')

        if aManageDeletion:
            paramsetNode.deletePropertyGraph(paramsetNodePropertyOpacity)
            graph = paramsetNode.getPropertyGraph(paramsetNodePropertyOpacity)
            self.assertEqual(graph, None, 'The PropertyGraph should have been removed')

    def __testSDNode_deletePropertyGraph(self, aSDPackage, aManageDeletion = False):
        self.__testSDNode_newPropertyGraph(aSDPackage, aManageDeletion=True)

    def __testSetOutputNode(self, aGraph, aNode0, aNode1):
        nodeSize = graphgrid.GraphGrid.sGetFirstLevelSize()
        aNode0.setPosition(float2(nodeSize, nodeSize))
        aNode1.setPosition(float2(2*nodeSize, nodeSize))

        aGraph.setOutputNode(aNode0, True)
        outputNodes = aGraph.getOutputNodes()
        self.assertEqual(len(outputNodes), 1, 'The graph should have a root node')
        self.assertEqual(outputNodes[0].getDefinition().getId(), aNode0.getDefinition().getId(), 'The graph should have the \'const_float2\' node as root node')

        aGraph.setOutputNode(aNode1, True)
        outputNodes = aGraph.getOutputNodes()
        self.assertEqual(len(outputNodes), 1, 'The graph should have a root node')
        self.assertEqual(outputNodes[0].getDefinition().getId(), aNode1.getDefinition().getId(), 'The graph should have the \'const_float4\' node as root node')

        aGraph.setOutputNode(aNode1, False)
        self.assertEqual(len(aGraph.getOutputNodes()), 0, 'The graph should not have a root node')

    def __testSDGraph_setOutputNode_SDSBSFunctionGraph(self, aSDPackage):
        # Function
        sdSBSFunctionGraph = SDSBSFunctionGraph.sNew(aSDPackage)
        sdSBSFunctionGraph.setIdentifier('test_sbs_function_set_output_node')

        # Create Nodes
        n0 = sdSBSFunctionGraph.newNode('sbs::function::const_float2')
        n1 = sdSBSFunctionGraph.newNode('sbs::function::const_float4')

        self.assertEqual(len(sdSBSFunctionGraph.getOutputNodes()), 0, 'The graph should not have a root node by default')
        self.__testSetOutputNode(sdSBSFunctionGraph, n0, n1)

    def __testSDGraph_setOutputNode_SDSBSFxMapGraph(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_sbs_fxmap_set_output_node')

        # Create FxMap Node
        fxMapNode = sdSBSCompGraph.newNode('sbs::compositing::fxmaps')
        self.assertTrue(fxMapNode, 'Fail to create new node')
        fxMapGraph = fxMapNode.getReferencedResource()
        self.assertTrue(fxMapGraph, 'Fail to get the referenced FxMap graph')

        # Create Nodes
        n0 = fxMapGraph.newNode('sbs::fxmap::paramset')
        n1 = fxMapGraph.newNode('sbs::fxmap::markov2')

        self.__testSetOutputNode(fxMapGraph, n0, n1)

    def __testSDGraph_setOutputNode_SDMDLGraph(self, aSDPackage):
        sdMDLGraph = SDMDLGraph.sNew(aSDPackage)
        sdMDLGraph.setIdentifier('test_mdl_set_output')

        blinnNode = sdMDLGraph.newNode('mdl::alg::materials::designer::blinn::blinn')
        self.assertTrue(blinnNode, 'Fail to create MDL node ' + 'mdl::alg::materials::designer::blinn::blinn')
        lambertNode = sdMDLGraph.newNode('mdl::alg::materials::designer::lambert::lambert')
        self.assertTrue(lambertNode, 'Fail to create node ' + 'mdl::alg::materials::designer::lambert::lambert')

        self.__testSetOutputNode(sdMDLGraph, blinnNode, lambertNode)

    def __testSDGraph_setOutputNode(self, aSDPackage):
        if self.mDebugTestSBS:
            self.__testSDGraph_setOutputNode_SDSBSFunctionGraph(aSDPackage)
            self.__testSDGraph_setOutputNode_SDSBSFxMapGraph(aSDPackage)
        if self.mDebugTestMDL:
            self.__testSDGraph_setOutputNode_SDMDLGraph(aSDPackage)

    def __testSBSCompInputOutputSetPropertyValueBaseParameters(self, aSDGraphOrSDNode):
        # Set the output Size
        aSDGraphOrSDNode.setInputPropertyValueFromId('$outputsize', SDValueInt2.sNew(int2(2,3)))
        vInt2 = aSDGraphOrSDNode.getPropertyValueFromId('$outputsize', SDPropertyCategory.Input).get()
        self.assertEqual(vInt2.x, 2, 'The value has not been set properly')
        self.assertEqual(vInt2.y, 3, 'The value has not been set properly')

        aSDGraphOrSDNode.setInputPropertyValueFromId('$format', SDValueInt.sNew(2))
        vInt = aSDGraphOrSDNode.getPropertyValueFromId('$format', SDPropertyCategory.Input).get()
        self.assertEqual(vInt, 2, 'The value has not been set properly')

        aSDGraphOrSDNode.setInputPropertyValueFromId('$pixelsize', SDValueFloat2.sNew(float2(0.3,0.5)))
        vFloat2 = aSDGraphOrSDNode.getPropertyValueFromId('$pixelsize', SDPropertyCategory.Input).get()
        self.assertAlmostEqual(vFloat2.x, 0.3, 7, 'The value has not been set properly')
        self.assertAlmostEqual(vFloat2.y, 0.5, 7, 'The value has not been set properly')

        aSDGraphOrSDNode.setInputPropertyValueFromId('$pixelratio', SDValueInt.sNew(0))
        vInt = aSDGraphOrSDNode.getPropertyValueFromId('$pixelratio', SDPropertyCategory.Input).get()
        self.assertEqual(vInt, 0, 'The value has not been set properly')

        aSDGraphOrSDNode.setInputPropertyValueFromId('$tiling', SDValueInt.sNew(0))
        vInt = aSDGraphOrSDNode.getPropertyValueFromId('$tiling', SDPropertyCategory.Input).get()
        self.assertEqual(vInt, 0, 'The value has not been set properly')

        aSDGraphOrSDNode.setInputPropertyValueFromId('$randomseed', SDValueInt.sNew(1234567))
        vInt = aSDGraphOrSDNode.getPropertyValueFromId('$randomseed', SDPropertyCategory.Input).get()
        self.assertEqual(vInt, 1234567, 'The value has not been set properly')

    def __testSDNode_setPropertyValue_SDSBSCompNode(self, aSDPackage):

        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_node_set_property_sbs_comp_node')

        # Uniform Color
        uniforNode = sdSBSCompGraph.newNode('sbs::compositing::uniform')

        # Set the value of the 'colorswitch' property as bool
        uniforNode.setPropertyValue(
            uniforNode.getPropertyFromId('colorswitch', SDPropertyCategory.Input),
            SDValueBool.sNew(False))

        # Set the value of the 'colorswitch' property as ColorRGBA
        uniforNode.setPropertyValue(
            uniforNode.getPropertyFromId('outputcolor', SDPropertyCategory.Input),
            SDValueColorRGBA.sNew(ColorRGBA(0.2, 0.8, 0.5, 0.5)))

        # Set the value of the 'colorswitch' property as float4
        inputProperty = uniforNode.getPropertyFromId('outputcolor', SDPropertyCategory.Input)
        inputPropertyConcreteValue = float4(0.1, 0.2, 0.3, 0.8)
        uniforNode.setPropertyValue(inputProperty, SDValueFloat4.sNew(inputPropertyConcreteValue))
        newInputPropertyValue = uniforNode.getPropertyValue(inputProperty)
        self.assertTrue(newInputPropertyValue, 'Fail to retrieve the propertyvalue')
        self.assertEqual(newInputPropertyValue.getType().getId(), 'ColorRGBA', 'Wrong value type')
        concreteValue = newInputPropertyValue.get()
        self.assertEqual(concreteValue.r, inputPropertyConcreteValue.x, 'Wrong x value')
        self.assertEqual(concreteValue.g, inputPropertyConcreteValue.y, 'Wrong y value')
        self.assertEqual(concreteValue.b, inputPropertyConcreteValue.z, 'Wrong z value')
        self.assertEqual(concreteValue.a, inputPropertyConcreteValue.w, 'Wrong w value')

        # Set the value of the 'colorswitch' property as float, this should trigger an exception
        try:
            uniforNode.setPropertyValue(
                uniforNode.getPropertyFromId('outputcolor', SDPropertyCategory.Input),
                SDValueFloat.sNew(0.5))
            self.assertEqual(False, 'This call should trigger an InvalidType exception')
        except sd.api.APIException:
            pass

        # Base Parameters
        self.__testSBSCompInputOutputSetPropertyValueBaseParameters(uniforNode)

        # Text (string property value)
        textNode = sdSBSCompGraph.newNode('sbs::compositing::text')
        textNode.setInputPropertyValueFromId('text', SDValueString.sNew('Test String'))
        txt = textNode.getPropertyValueFromId('text', SDPropertyCategory.Input).get()
        self.assertEqual(textNode.getPropertyValueFromId('text', SDPropertyCategory.Input).get(), 'Test String', 'The value has not been set properly')

        # Blend (enums (int) property value)
        blendNode = sdSBSCompGraph.newNode('sbs::compositing::blend')
        blendNode.setInputPropertyValueFromId('blendingmode', SDValueInt.sNew(3))
        self.assertEqual(blendNode.getPropertyValueFromId('blendingmode', SDPropertyCategory.Input).get(), 3, 'The value has not been set properly')

        # Input node (attributes edition)
        intputNode = sdSBSCompGraph.newNode('sbs::compositing::input_color')
        self.__testAllSDProperties(intputNode)

        # Output node (attributes edition)
        outputNode = sdSBSCompGraph.newNode('sbs::compositing::output')
        self.__testAllSDProperties(outputNode)

        # Layout nodes
        self.__layoutNodes(sdSBSCompGraph.getNodes())

    def __testSDNode_setPropertyValue_SDSBSFunctionNode(self, aSDPackage):
        sdGraph = SDSBSFunctionGraph.sNew(aSDPackage)
        sdGraph.setIdentifier('test_node_set_property_sbs_function_node')

        node = sdGraph.newNode('sbs::function::const_float4')
        inputPropertyConcreteValue = float4(0.1, 0.2, 0.3, 0.4)
        node.setInputPropertyValueFromId('__constant__', SDValueFloat4.sNew(inputPropertyConcreteValue))

        newInputPropertyValue = node.getPropertyValueFromId('__constant__', SDPropertyCategory.Input)
        self.assertTrue(newInputPropertyValue, 'Fail to retrieve the property value')
        self.assertEqual(newInputPropertyValue.getType().getId(), 'float4', 'Wrong value type')
        concreteValue = newInputPropertyValue.get()
        self.assertEqual(concreteValue.x, inputPropertyConcreteValue.x, 'Wrong x value')
        self.assertEqual(concreteValue.y, inputPropertyConcreteValue.y, 'Wrong y value')
        self.assertEqual(concreteValue.z, inputPropertyConcreteValue.z, 'Wrong z value')
        self.assertEqual(concreteValue.w, inputPropertyConcreteValue.w, 'Wrong w value')

        # Layout nodes
        self.__layoutNodes(sdGraph.getNodes())

    def __testSDNode_setPropertyValue_SDSBSFxMapNode(self, aSDPackage):
        sdGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdGraph.setIdentifier('test_node_set_property_sbs_fxmap_node')

        fxMapNode = sdGraph.newNode('sbs::compositing::fxmaps')
        fxMapGraph = fxMapNode.getReferencedResource()

        node = fxMapGraph.newNode('sbs::fxmap::paramset')
        inputPropertyConcreteValue = float4(0.1, 0.2, 0.3, 0.4)
        node.setInputPropertyValueFromId('opacity', SDValueFloat4.sNew(inputPropertyConcreteValue))

        newInputPropertyValue = node.getPropertyValueFromId('opacity', SDPropertyCategory.Input)
        self.assertTrue(newInputPropertyValue, 'Fail to retrieve the property value')
        self.assertEqual(newInputPropertyValue.getType().getId(), 'float4', 'Wrong value type')
        concreteValue = newInputPropertyValue.get()
        self.assertEqual(concreteValue.x, inputPropertyConcreteValue.x, 'Wrong x value')
        self.assertEqual(concreteValue.y, inputPropertyConcreteValue.y, 'Wrong y value')
        self.assertEqual(concreteValue.z, inputPropertyConcreteValue.z, 'Wrong z value')
        self.assertEqual(concreteValue.w, inputPropertyConcreteValue.w, 'Wrong w value')

        # Layout nodes
        self.__layoutNodes(fxMapGraph.getNodes())

    def __testMDLInputPropertyValue(self, aMDLObject, aPropertyName, aValueTypeName, aValueStr):
        newInputPropertyValue = aMDLObject.getPropertyValueFromId(aPropertyName, SDPropertyCategory.Input)
        self.assertTrue(newInputPropertyValue, 'Fail to retrieve the property value')
        self.assertEqual(newInputPropertyValue.getType().getId(), aValueTypeName, 'Wrong value type')
        concreteValue = SDValueSerializer.sToString(newInputPropertyValue)
        self.assertEqual(concreteValue, aValueStr, 'Wrong value')

    def __testSDNode_setPropertyValue_SDMDLNode(self, aSDPackage):
        sdGraph = SDMDLGraph.sNew(aSDPackage)
        sdGraph.setIdentifier('test_node_set_property_mdl_node')

        # Bool, Color
        node = sdGraph.newNode('mdl::material(bool,material_surface,material_surface,color,material_volume,material_geometry,hair_bsdf)')
        self.assertTrue(node)

        node.setInputPropertyValueFromId('thin_walled', SDValueBool.sNew(False))
        self.assertEqual(node.getPropertyValueFromId('thin_walled', SDPropertyCategory.Input).get(), False)

        node.setInputPropertyValueFromId('thin_walled', SDValueBool.sNew(True))
        self.assertEqual(node.getPropertyValueFromId('thin_walled', SDPropertyCategory.Input).get(), True)

        node.setInputPropertyValueFromId('ior', SDValueColorRGB.sNew(ColorRGB(0.2, 0.3, 0.4)))
        newValue = node.getPropertyValueFromId('ior', SDPropertyCategory.Input).get()
        self.assertAlmostEqual(newValue.r, 0.2, 7)
        self.assertAlmostEqual(newValue.g, 0.3, 7)
        self.assertAlmostEqual(newValue.b, 0.4, 7)

        # Float
        node = sdGraph.newNode('mdl::float2(float,float)')
        self.assertTrue(node)
        node.setInputPropertyValueFromId('x', SDValueFloat.sNew(1.2))
        self.assertAlmostEqual(node.getPropertyValueFromId('x', SDPropertyCategory.Input).get(), 1.2, 7)

        # Bool
        node = sdGraph.newNode('mdl::bool')
        self.assertTrue(node)
        node.setInputPropertyValueFromId('bool', SDValueBool.sNew(True))

        # Layout nodes
        self.__layoutNodes(sdGraph.getNodes())

    def __testSDNode_setPropertyValue(self, aSDPackage):
        if self.mDebugTestSBS:
            self.__testSDNode_setPropertyValue_SDSBSCompNode(aSDPackage)
            self.__testSDNode_setPropertyValue_SDSBSFunctionNode(aSDPackage)
            self.__testSDNode_setPropertyValue_SDSBSFxMapNode(aSDPackage)
        if self.mDebugTestMDL:
            self.__testSDNode_setPropertyValue_SDMDLNode(aSDPackage)

    def __testSDResource_setPropertyValue_SDSBSCompGraph(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_SDResource_SetPropertyValue_SBSCompGraph')

        self.__testSBSCompInputOutputSetPropertyValueBaseParameters(sdSBSCompGraph)
        self.__testAllSDProperties(sdSBSCompGraph)

        # Layout nodes
        self.__layoutNodes(sdSBSCompGraph.getNodes())

    def __testSDResource_setPropertyValue_SDSBSFunctionGraph(self, aSDPackage):
        sdSBSFunctionGraph = SDSBSFunctionGraph.sNew(aSDPackage)
        sdSBSFunctionGraph.setIdentifier('test_SDResource_SetPropertyValue_SBSFunctionGraph')

        self.__testAllSDProperties(sdSBSFunctionGraph)

        # Layout nodes
        self.__layoutNodes(sdSBSFunctionGraph.getNodes())

    def __testSDResource_setPropertyValue_SDMDLGraph(self, aSDPackage):
        sdMDLGraph = SDMDLGraph.sNew(aSDPackage)
        sdMDLGraph.setIdentifier('test_SDResource_SetPropertyValue_MDLGraph')

        self.__testAllSDProperties(sdMDLGraph)

        # Layout nodes
        self.__layoutNodes(sdMDLGraph.getNodes())

    def __testSDResource_setPropertyValue(self, aSDPackage):
        if self.mDebugTestSBS:
            self.__testSDResource_setPropertyValue_SDSBSCompGraph(aSDPackage)
            self.__testSDResource_setPropertyValue_SDSBSFunctionGraph(aSDPackage)
        if self.mDebugTestMDL:
            self.__testSDResource_setPropertyValue_SDMDLGraph(aSDPackage)

    def __testSDResource_newProperty_SDSBSGraph(self, aSDSBSGraph, aTestDelete = False):
        # Create New Input Property
        sdPropertyInputId = 'myInputF3'
        sdPropertyInput = aSDSBSGraph.newProperty(
            sdPropertyInputId,
            SDTypeFloat3.sNew(),
            SDPropertyCategory.Input)
        self.assertTrue(sdPropertyInput)
        self.assertEqual(sdPropertyInput.getId(), sdPropertyInputId)
        self.assertTrue(sdPropertyInput.getType())
        self.assertEqual(sdPropertyInput.getType().getId(), 'float3')
        self.assertEqual(sdPropertyInput.getCategory(), SDPropertyCategory.Input)

        # Check sdPropertyInput can be retrieve from his identifier
        sdProp = aSDSBSGraph.getPropertyFromId(sdPropertyInputId, SDPropertyCategory.Input)
        self.assertTrue(sdProp)

        # Check Delete
        if aTestDelete:
            aSDSBSGraph.deleteProperty(sdPropertyInput)
            deletedSDProp = aSDSBSGraph.getPropertyFromId(sdPropertyInputId, SDPropertyCategory.Input)
            self.assertFalse(deletedSDProp)

    def __testSDResource_newProperty_SDSBSCompGraph(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_SDResource_newProperty_SDSBSCompGraph')
        self.__testSDResource_newProperty_SDSBSGraph(sdSBSCompGraph, aTestDelete=False)

    def __testSDResource_newProperty_SDSBSFunctionGraph(self, aSDPackage):
        sdSBSFunctionGraph = SDSBSFunctionGraph.sNew(aSDPackage)
        sdSBSFunctionGraph.setIdentifier('test_SDResource_newProperty_SDSBSFunctionGraph')
        self.__testSDResource_newProperty_SDSBSGraph(sdSBSFunctionGraph, aTestDelete=False)

    def __testSDResource_newProperty(self, aSDPackage):
        self.__testSDResource_newProperty_SDSBSCompGraph(aSDPackage)
        self.__testSDResource_newProperty_SDSBSFunctionGraph(aSDPackage)

    def __testSDResource_deleteProperty_SDSBSCompGraph(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_SDResource_deleteProperty_SDSBSCompGraph')
        self.__testSDResource_newProperty_SDSBSGraph(sdSBSCompGraph, True)

    def __testSDResource_deleteProperty_SDSBSFunctionGraph(self, aSDPackage):
        sdSBSFunctionGraph = SDSBSFunctionGraph.sNew(aSDPackage)
        sdSBSFunctionGraph.setIdentifier('test_SDResource_deleteProperty_SDSBSFunctionGraph')
        self.__testSDResource_newProperty_SDSBSGraph(sdSBSFunctionGraph, True)

    def __testSDResource_deleteProperty(self, aSDPackage):
        self.__testSDResource_deleteProperty_SDSBSCompGraph(aSDPackage)
        self.__testSDResource_deleteProperty_SDSBSFunctionGraph(aSDPackage)

    def __testSDResource_setPropertyAnnotationValueFromId_testValue(self, aSDSBSGraph, aInputProperty, aInputPropertyAnnotation):
        aInputPropertyAnnotationId = aInputPropertyAnnotation.getId()
        aInputPropertyAnnotationType = aInputPropertyAnnotation.getType()
        aInputPropertyAnnotationTypeName = aInputPropertyAnnotationType.getId()

        logger.debug('  %s %s' % (aInputPropertyAnnotationTypeName, aInputPropertyAnnotation.getId()))

        if aInputPropertyAnnotationId == 'identifier':
            # Avoid changing the identifier in this test
            return

        if aInputPropertyAnnotationId == 'type':
            # Avoid changing the identifier in this test
            return

        newSDValues = []
        if aInputPropertyAnnotationTypeName == 'string':
            if aInputPropertyAnnotationId == 'editor':
                for editorId in ['angle',
                                 'buttons',
                                 'color',
                                 'dropdownlist',
                                 'sizepow2',
                                 'slider',
                                 'text',
                                 'transformation',
                                 'straighttransform',
                                 'reverseposition',
                                 'position',
                                 'functionbutton']:
                    newSDValues.append(SDValueString.sNew(editorId))
            else:
                newSDValues.append(SDValueString.sNew('%s_%s' % (aInputProperty.getId(), aInputPropertyAnnotationId)))
        else:
            newSDValues = self.__getTestSDValues(aInputPropertyAnnotationType)

        if not newSDValues:
            return

        # Test all the values
        for newSDValue in newSDValues:
            self.assertTrue(newSDValue.getType())

            aSDSBSGraph.setPropertyAnnotationValueFromId(
                aInputProperty,
                aInputPropertyAnnotationId,
                newSDValue)

            # Test result
            sdValue = aSDSBSGraph.getPropertyAnnotationValueFromId(
                aInputProperty,
                aInputPropertyAnnotationId)
            self.assertTrue(sdValue)
            self.assertTrue(sdValue.getType())
            self.assertEqual(sdValue.getType().getId(), newSDValue.getType().getId())
            sdValueStr = SDValueSerializer.sToString(sdValue)
            newSDValueStr = SDValueSerializer.sToString(newSDValue)
            self.assertEqual(sdValueStr, newSDValueStr)

    def __testSDResource_createInputProperties(self, aSDSBSGraph):
        # Create input properties
        sdTypes = [
            SDTypeBool.sNew(),
            SDTypeInt.sNew(),
            SDTypeInt2.sNew(),
            SDTypeInt3.sNew(),
            SDTypeInt4.sNew(),
            SDTypeFloat.sNew(),
            SDTypeFloat2.sNew(),
            SDTypeFloat3.sNew(),
            SDTypeFloat4.sNew(),
            SDTypeString.sNew()]
        for sdType in sdTypes:
            inputPropertyId = 'my_input_' + sdType.getId()
            inputProperty = aSDSBSGraph.newProperty(inputPropertyId, sdType, SDPropertyCategory.Input)
            self.assertTrue(inputProperty)

    def __testSDResource_setPropertyAnnotationValueFromId_SDSBSGraph(self, aSDSBSGraph, aTestInputValues = True):
        self.__testSDResource_createInputProperties(aSDSBSGraph)

        # Set the input properties annotations
        for sdInputProperty in aSDSBSGraph.getProperties(SDPropertyCategory.Input):
            logger.debug('Input: \'%s\'' % (sdInputProperty.getId()))

            # Test values
            if aTestInputValues:
                sdInputPropertyType = sdInputProperty.getType()
                sdTestValues = self.__getTestSDValues(sdInputPropertyType)
                for sdValue in sdTestValues:
                    self.assertTrue(sdValue)
                    self.__setSDObjectPropertyValue(aSDSBSGraph, sdInputProperty, sdValue)

            for sdInputPropertyAnnotation in aSDSBSGraph.getPropertyAnnotations(sdInputProperty):
                self.__testSDResource_setPropertyAnnotationValueFromId_testValue(aSDSBSGraph, sdInputProperty, sdInputPropertyAnnotation)

    def __testSDResource_setPropertyAnnotationValueFromId_SDSBSCompGraph(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('test_SDResource_setPropertyAnnotationValueFromId_SBSCompGraph')
        self.__testSDResource_setPropertyAnnotationValueFromId_SDSBSGraph(sdSBSCompGraph, aTestInputValues = True)

    def __testSDResource_setPropertyAnnotationValueFromId_SDSBSFunctionGraph(self, aSDPackage):
        sdSBSFunctionGraph = SDSBSFunctionGraph.sNew(aSDPackage)
        sdSBSFunctionGraph.setIdentifier('test_SDResource_setPropertyAnnotationValueFromId_SBSFunctionGraph')
        self.__testSDResource_setPropertyAnnotationValueFromId_SDSBSGraph(sdSBSFunctionGraph, aTestInputValues = False)

    def __testSDResource_setPropertyAnnotationValueFromId(self, aSDPackage):
        self.__testSDResource_setPropertyAnnotationValueFromId_SDSBSCompGraph(aSDPackage)
        self.__testSDResource_setPropertyAnnotationValueFromId_SDSBSFunctionGraph(aSDPackage)

    def __testSDNode_newProperty_SDSBSCompNode_createInputValues(self, aSDSBSCompNode, aDeleteValues):
        newSDProperties = []
        for sdType in [SDTypeBool.sNew(),
                       SDTypeInt.sNew(),
                       SDTypeInt2.sNew(),
                       SDTypeInt3.sNew(),
                       SDTypeInt4.sNew(),
                       SDTypeFloat.sNew(),
                       SDTypeFloat2.sNew(),
                       SDTypeFloat3.sNew(),
                       SDTypeFloat4.sNew()]:
            newSDProperty = aSDSBSCompNode.newProperty('myValue_'+sdType.__class__.__name__, sdType, SDPropertyCategory.Input)
            self.assertTrue(newSDProperty)

            # Check property has been added
            p = aSDSBSCompNode.getPropertyFromId(newSDProperty.getId(), SDPropertyCategory.Input)
            self.assertTrue(p)

            # Store the property
            newSDProperties.append(newSDProperty)

        if aDeleteValues:
            for sdProperty in newSDProperties:
                aSDSBSCompNode.deleteProperty(sdProperty)

                # Check property has been removed
                p = aSDSBSCompNode.getPropertyFromId(sdProperty.getId(), SDPropertyCategory.Input)
                self.assertTrue(p == None)

    def __testSDNode_newProperty_SDSBSCompNode(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('testSDNode_newProperty_SDSBSCompNode')

        sdNode = sdSBSCompGraph.newNode('sbs::compositing::uniform')
        self.__testSDNode_newProperty_SDSBSCompNode_createInputValues(sdNode, False)

    def __testSDNode_newProperty(self, aSDPackage):
        self.__testSDNode_newProperty_SDSBSCompNode(aSDPackage)

    def __testSDNode_deleteProperty_SDSBSCompNode(self, aSDPackage):
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        sdSBSCompGraph.setIdentifier('testSDNode_deleteProperty_SDSBSCompNode')

        sdNode = sdSBSCompGraph.newNode('sbs::compositing::uniform')
        self.__testSDNode_newProperty_SDSBSCompNode_createInputValues(sdNode, True)

    def __testSDNode_deleteProperty(self, aSDPackage):
        self.__testSDNode_deleteProperty_SDSBSCompNode(aSDPackage)

    def __testMDLConstantNode_exposition(self, aSDPackage):
        cGridSize = graphgrid.GraphGrid.sGetFirstLevelSize()
        colSize = 2 * cGridSize
        rowSize = 2 * cGridSize

        sdMDLGraph = SDMDLGraph.sNew(aSDPackage)
        sdMDLGraph.setIdentifier('test_mdl_constant_node_exposition')

        sdModule = sd.getContext().getSDApplication().getModuleMgr().getModuleFromId('mdl::<builtins>')
        self.assertTrue(sdModule)

        rowIndex = 0
        for sdType in sdModule.getTypes():
            if isinstance(sdType, SDTypeArray):
                # Not supported yet
                continue

            logger.debug('Testing: %s' % sdType.getId())
            nodeId = sdType.getId()
            if not nodeId.startswith('mdl::'):
                nodeId = 'mdl::' + nodeId
            sdMDLNode = sdMDLGraph.newNode(nodeId)
            if not sdMDLNode:
                continue
            if isinstance(sdMDLNode, SDMDLConstantNode):
                rowIndex += 1
                sdMDLNode.setPosition(float2(-colSize, rowIndex*rowSize))
                sdMDLNode.setExposed(True)
                self.__testSDProperties(sdMDLNode, SDPropertyCategory.Annotation)
                continue
            sdMDLGraph.deleteNode(sdMDLNode)

        # Layout nodes
        self.__layoutNodes(sdMDLGraph.getNodes())

if __name__ == '__main__':
    unittest.main()

