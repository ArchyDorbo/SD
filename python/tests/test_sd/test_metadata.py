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
from sd.api.sbs.sdsbsarexporter import *
from tests.sdvaluetools import *
from sd.api.sbs.sdsbscompgraph import *
from sd.api.sdvaluestring import *
from sd.api.sdresourcefolder import *
from sd.api.sdresourcebitmap import *
from sd.api.sdresourcesvg import *
from sd.api.sdresourcefont import *
from sd.api.sdresourcescene import *
from sd.api.sdresourcelightprofile import *
from sd.api.sdresourcebsdfmeasurement import *
from tests import tools
from sd.api.sdmetadatadict import *
from sd.api.mdl.sdmdlconstantnode import *

import logging
logger = logging.getLogger(__name__)


class TestMetadata(unittest.TestCase):

    def runTest(self):

        context = sd.getContext()

        pkgMgr = context.getSDApplication().getPackageMgr()
        sdPackage = pkgMgr.newUserPackage()
        self.assertTrue(sdPackage, 'Fail to create new package')

        newResources = self.__addCustomResources(sdPackage)

        customFileAbsPath = os.path.join(tools.getAssetsDir(), "TEXT.txt")
        linkedSDResourceCustom = SDResource.sNewFromFile(sdPackage, customFileAbsPath, EmbedMethod.Linked)
        self.assertTrue(linkedSDResourceCustom, "Fail to create new Resource")
        linkedSDResourceCustom.setIdentifier('myResourceForMetadataTests')

        self.__addMetadata(sdPackage.getMetadataDict(), newResources, linkedSDResourceCustom)

        sdSBSCompGraph = SDSBSCompGraph.sNew(sdPackage)
        self.__addMetadata(sdSBSCompGraph.getMetadataDict(), newResources, linkedSDResourceCustom)

        sdInputNode = sdSBSCompGraph.newNode('sbs::compositing::input_color')
        sdInputIdentifier = sdInputNode.getPropertyValueFromId('identifier', SDPropertyCategory.Annotation).get()
        self.__addMetadata(sdSBSCompGraph.getPropertyMetadataDictFromId(sdInputIdentifier, SDPropertyCategory.Input), newResources, linkedSDResourceCustom)

        sdOutputNode = sdSBSCompGraph.newNode('sbs::compositing::output')
        sdOutputIdentifier = sdOutputNode.getPropertyValueFromId('identifier', SDPropertyCategory.Annotation).get()
        self.__addMetadata(sdSBSCompGraph.getPropertyMetadataDictFromId(sdOutputIdentifier, SDPropertyCategory.Output), newResources, linkedSDResourceCustom)

        # Folder
        sdFolder = SDResourceFolder.sNew(sdPackage)
        sdFolder.setIdentifier('myFolder')
        self.__addMetadata(sdFolder.getMetadataDict(), newResources, linkedSDResourceCustom)

        # Custom Resource
        self.__addMetadata(linkedSDResourceCustom.getMetadataDict(), newResources, linkedSDResourceCustom)

        # Bitmap
        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'substance-128x128.png')
        sdBitmap = SDResourceBitmap.sNewFromFile(sdPackage, textureFileAbsPath, EmbedMethod.Linked)
        self.__addMetadata(sdBitmap.getMetadataDict(), newResources, linkedSDResourceCustom)

        # SVG
        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'sbs.svg')
        sdSVG = SDResourceSVG.sNewFromFile(sdPackage, textureFileAbsPath, EmbedMethod.Linked)
        self.__addMetadata(sdSVG.getMetadataDict(), newResources, linkedSDResourceCustom)

        # Font
        fontFileAbsPath = os.path.join(tools.getAssetsDir(), 'AdobeClean-Regular.ttf')
        sdFont = SDResourceFont.sNewFromFile(sdPackage, fontFileAbsPath, EmbedMethod.Linked)
        self.__addMetadata(sdFont.getMetadataDict(), newResources, linkedSDResourceCustom)

        # Scene
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'Rounded Cylinder.fbx')
        sdScene = SDResourceScene.sNewFromFile(sdPackage, sceneFileAbsPath, EmbedMethod.Linked)
        self.__addMetadata(sdScene.getMetadataDict(), newResources, linkedSDResourceCustom)

        # Light Profile from file
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'example_modules.ies')
        sdLightProfile = SDResourceLightProfile.sNewFromFile(sdPackage, sceneFileAbsPath, EmbedMethod.Linked)
        self.__addMetadata(sdLightProfile.getMetadataDict(), newResources, linkedSDResourceCustom)

        # BSDF Measurement
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'carpaint_blue.mbsdf')
        sdBSDF = SDResourceBSDFMeasurement.sNewFromFile(sdPackage, sceneFileAbsPath, EmbedMethod.Linked)
        self.__addMetadata(sdBSDF.getMetadataDict(), newResources, linkedSDResourceCustom)

        dstFileAbsPath = os.path.join(tools.getTestOutputDir(__file__), 'test_package_metadata.sbs')
        logger.debug('Save output file to ' + dstFileAbsPath)
        pkgMgr.savePackageAs(sdPackage, dstFileAbsPath)

        # Export Package to .sbsar
        sbsarFilePath = os.path.join(tools.getTestOutputDir(__file__), 'test_package_metadata.sbsar')
        self.__exportToSBSAR(sdPackage, sbsarFilePath)

        # Check .sbsar file
        self.__testSBSAR(sbsarFilePath, newResources)


    def __addCustomResources(self, aSDPackage):
        # SDSBSCompGraph
        sdResourceFolder = SDResourceFolder.sNew(aSDPackage)
        self.assertTrue(sdResourceFolder, 'Fail to create new Resource')
        sdResourceFolder.setIdentifier('test_custom_resources_folder')

        # Custom Resource
        assetsDirs = tools.getAssetsDir()
        newResources = []
        for fileName in os.listdir(assetsDirs):
            customFileAbsPath = os.path.join(assetsDirs, fileName)
            if os.path.isfile(customFileAbsPath):
                linkedSDResourceCustom = SDResource.sNewFromFile(sdResourceFolder, customFileAbsPath, EmbedMethod.Linked)
                self.assertTrue(linkedSDResourceCustom, 'Fail to create new Resource')
                linkedSDResourceCustom.setIdentifier(fileName)
                newResources.append(linkedSDResourceCustom)
        return newResources

    def __addMetadata(self, aSDMetadata, aSDResources, aSDResourceCustom):
        with self.assertRaises(APIException) as error:
            aSDMetadata.getPropertyFromId("ghost")
            self.assertEqual(error.exception.mErrorCode, SDApiError.ItemNotFound, "Item shouldn't exist")

        with self.assertRaises(APIException) as error:
            aSDMetadata.getPropertyValueFromId("ghost")
            self.assertEqual(error.exception.mErrorCode, SDApiError.ItemNotFound, "Item shouldn't exist")

        newPropValue = SDValueString.sNew("newPropValue")
        newPropValue2 = SDValueString.sNew("newPropValue2")
        newPropValue3 = SDValueString.sNew("newPropValue3")
        toDeleteValue = SDValueString.sNew("will be deleted later")

        with self.assertRaises(APIException) as error:
            aSDMetadata.setPropertyValueFromId("1", newPropValue)
            self.assertEqual(error.exception.mErrorCode, SDApiError.InvalidValue, "key is not valid XML")

        with self.assertRaises(APIException) as error:
            aSDMetadata.setPropertyValueFromId("a a", newPropValue)
            self.assertEqual(error.exception.mErrorCode, SDApiError.InvalidValue, "key is not valid XML")

        aSDMetadata.setPropertyValueFromId("newProp", newPropValue)
        newProp = aSDMetadata.getPropertyFromId("newProp")

        aSDMetadata.setPropertyValueFromId("toDelete", toDeleteValue)
        toDelete = aSDMetadata.getPropertyFromId("toDelete")

        assertSDValueEqual(self, aSDMetadata.getPropertyValue(newProp), newPropValue)
        aSDMetadata.setPropertyValueFromId("newProp", newPropValue2)
        assertSDValueEqual(self, aSDMetadata.getPropertyValueFromId("newProp"), newPropValue2)
        aSDMetadata.setPropertyValue(newProp, newPropValue3)
        assertSDValueEqual(self, aSDMetadata.getPropertyValue(newProp), newPropValue3)

        aSDMetadata.setPropertyURLFromResource("myResource", aSDResourceCustom)
        myResourceProp = aSDMetadata.getPropertyFromId("myResource")
        myResourceUrlExpected = aSDResourceCustom.getUrl()
        myResourceUrlAsSDValue = SDValueString.sNew(myResourceUrlExpected)
        assertSDValueEqual(self, aSDMetadata.getPropertyValue(myResourceProp), myResourceUrlAsSDValue)
        assertSDValueEqual(self, aSDMetadata.getPropertyValueFromId("myResource"), myResourceUrlAsSDValue)

        with self.assertRaises(APIException) as error:
            aSDMetadata.setPropertyValue(myResourceProp, newPropValue)
            self.assertEqual(error.exception.mErrorCode, SDApiError.NotSupported, "Shouldn't be able to replace url by string")

        with self.assertRaises(APIException) as error:
            aSDMetadata.setPropertyValueFromId("myResource", newPropValue)
            self.assertEqual(error.exception.mErrorCode, SDApiError.NotSupported, "Shouldn't be able to replace url by string")

        allProps = aSDMetadata.getProperties()
        self.assertEqual(allProps.getSize(), 3)
        self.assertEqual(allProps.getItem(0).getId(), newProp.getId())
        self.assertEqual(allProps.getItem(1).getId(), toDelete.getId())
        self.assertEqual(allProps.getItem(2).getId(), myResourceProp.getId())

        aSDMetadata.deleteProperty(toDelete)
        with self.assertRaises(APIException) as error:
            aSDMetadata.getPropertyFromId("toDelete")
            self.assertEqual(error.exception.mErrorCode, SDApiError.ItemNotFound, "Item shouldn't exist")

        with self.assertRaises(APIException) as error:
            aSDMetadata.deleteProperty(toDelete)
            self.assertEqual(error.exception.mErrorCode, SDApiError.ItemNotFound, "Item shouldn't exist")

        # Remove the test property
        aSDMetadata.deleteProperty(myResourceProp)

        # Create Metadata for all specified resources
        for sdResource in aSDResources:
            aSDMetadata.setPropertyURLFromResource('myResource_'+sdResource.getIdentifier(), sdResource)

    def __exportToSBSAR(self, aSDPackage, aSBSARFilePath):

        # SDSBSCompGraph
        sdSBSCompGraph = SDSBSCompGraph.sNew(aSDPackage)
        self.assertTrue(sdSBSCompGraph, 'Fail to create new Resource')
        sdSBSCompGraph.setIdentifier('dummy')
        # Create Output node
        sdSBSCompGraph.newNode('sbs::compositing::output')

        sdSBSARExporter = SDSBSARExporter.sNew()
        sdSBSARExporter.setExposeRandomSeed(False)
        sdSBSARExporter.exportPackageToSBSAR(aSDPackage, aSBSARFilePath)

    def __testSBSAR(self, aSDSBSARFilePath, aSDRefResources):
        sdSBSARPkg = sd.getContext().getSDApplication().getPackageMgr().loadUserPackage(aSDSBSARFilePath)
        self.assertTrue(sdSBSARPkg)

        resourcesFolder = sdSBSARPkg.findResourceFromUrl('Resources')
        self.assertTrue(resourcesFolder)
        self.assertTrue(isinstance(resourcesFolder, SDResourceFolder))
        resources = resourcesFolder.getChildren(False)
        self.assertEqual(len(resources), len(aSDRefResources))
        for sdResource in resources:
            sdResourceIdentifier = sdResource.getIdentifier()
            sdResourceIdentifier = sdResourceIdentifier.replace('.', '_').replace(' ', '_')

            # Look for the Reference SDResource
            refSDResource = None
            for res in aSDRefResources:
                resIdentifier = res.getIdentifier()
                if resIdentifier == sdResourceIdentifier:
                    refSDResource = res
                    break

            self.assertTrue(refSDResource)

            # Compare the file content between the original file on disk AND the fileContent retrieved from the
            refFilePath = refSDResource.getFilePath()
            refFileContent = None
            with open(refFilePath, "rb") as f:
                refFileContent = f.read()

            sdResourceContent = sdResource.getFileContent()
            self.assertEqual(len(sdResourceContent), len(refFileContent))
            self.assertEqual(sdResourceContent, refFileContent)

if __name__ == '__main__':
    unittest.main()

