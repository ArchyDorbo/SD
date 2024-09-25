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
from sd.api.apiexception import APIException
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph
from sd.api.sbs.sdsbscompgraphpreset import SDSBSCompGraphPreset
from sd.api.sdapiobject import SDApiError
from sd.api.sdbasetypes import *
from sd.api.sdvalue import SDValue
from sd.api.sdvaluebool import SDValueBool
from sd.api.sdvaluecolorrgb import SDValueColorRGB
from sd.api.sdvaluecolorrgba import SDValueColorRGBA
from sd.api.sdvaluefloat import SDValueFloat
from sd.api.sdvaluefloat2 import SDValueFloat2
from sd.api.sdvaluefloat3 import SDValueFloat3
from sd.api.sdvaluefloat4 import SDValueFloat4
from sd.api.sdvalueint import SDValueInt
from sd.api.sdvalueint2 import SDValueInt2
from sd.api.sdvalueint3 import SDValueInt3
from sd.api.sdvalueint4 import SDValueInt4
from sd.api.sdvalueserializer import SDValueSerializer
from sd.api.sdvaluespotcolor import SDValueSpotColor
from sd.api.sdvaluestring import SDValueString

from tests import tools

import typing

import logging
logger = logging.getLogger(__name__)


def spotColorsNotAvailable():
    import sd
    ctx = sd.getContext()
    app = ctx.getSDApplication()
    return app.getSpotColorLibrary() == None


class TestSDSBSGraphPresets(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.context = sd.getContext()
        cls.package = tools.loadSDPackage(cls.context, 'presets_test.sbs')
        cls.graph = typing.cast(
            SDSBSCompGraph, cls.package.findResourceFromUrl('all_input_types'))
        assert(cls.graph)

        cls.existingPreset = {
            'label': 'Existing preset',
            'tags': 'Sample tag here',
            'inputs': [
                {
                    'name': 'bool',
                    'value': SDValueBool.sNew(True)
                },
                {
                    'name': 'int1',
                    'value': SDValueInt.sNew(0)
                },
                {
                    'name': 'int2',
                    'value': SDValueInt2.sNew(int2(1, 2))
                },
                {
                    'name': 'int3',
                    'value': SDValueInt3.sNew(int3(3, 4, 5))
                },
                {
                    'name': 'int4',
                    'value': SDValueInt4.sNew(int4(6, 7, 8, 9))
                },
                {
                    'name': 'float1',
                    'value': SDValueFloat.sNew(0.100000001)
                },
                {
                    'name': 'float2',
                    'value': SDValueFloat2.sNew(float2(0.200000003, 0.300000012))
                },
                {
                    'name': 'float3',
                    'value': SDValueFloat3.sNew(float3(0.400000006, 0.5, 0.600000024))
                },
                {
                    'name': 'float4',
                    'value': SDValueFloat4.sNew(float4(0.699999988, 0.800000012, 0.899999976, 1)),
                },
                {
                    'name': 'string',
                    'value': SDValueString.sNew('Sample string')
                }
            ]
        }

    @classmethod
    def tearDownClass(cls):
        cls.context.getSDApplication().getPackageMgr().unloadUserPackage(cls.package)

    def testExistingPreset(self):
        presets = self.graph.getPresets()
        self.assertEqual(len(presets), 1)

        self.assertEqual(presets[0].getLabel(), self.existingPreset['label'])
        self.assertEqual(presets[0].getUserTags(), self.existingPreset['tags'])

        preset = typing.cast(SDSBSCompGraphPreset, self.graph.getPreset(
            self.existingPreset['label']))
        self.assertTrue(preset)

        inputs = preset.getInputs()
        self.assertEqual(len(inputs), len(self.existingPreset['inputs']))

        for i, input in enumerate(inputs):
            inputData = self.existingPreset['inputs'][i]
            self.assertEqual(input.getIdentifier(), inputData['name'])
            self.assertEqual(SDValueSerializer.sToString(
                input.getValue()), SDValueSerializer.sToString(inputData['value']))

    def testCreatePreset(self):
        self.assertEqual(len(self.graph.getPresets()), 1)

        preset = self.graph.newPreset('Test preset')
        self.assertEqual(len(self.graph.getPresets()), 2)

        #
        # Create preset inputs.
        #

        for input in self.existingPreset['inputs']:
            preset.addInput(input['name'], input['value'])

        #
        # Check input values match values in dictionary.
        #

        inputs = preset.getInputs()
        self.assertEqual(len(inputs), len(self.existingPreset['inputs']))

        for i, input in enumerate(inputs):
            inputData = self.existingPreset['inputs'][i]
            self.assertEqual(input.getIdentifier(), inputData['name'])
            self.assertEqual(SDValueSerializer.sToString(
                input.getValue()), SDValueSerializer.sToString(inputData['value']))

        self.graph.deletePreset(preset.getLabel())
        self.assertEqual(len(self.graph.getPresets()), 1)

    def testColorInputValues(self):
        preset = self.graph.newPreset('Test preset')

        col3 = SDValueColorRGB.sNew(ColorRGB(1.0, 0.5, 0.0))
        preset.addInput('float3', col3)

        col4 = SDValueColorRGBA.sNew(ColorRGBA(1.0, 0.6, 0.3, 0.0))
        preset.addInput('float4', col4)

        inputs = preset.getInputs()
        self.assertEqual(len(inputs), 2)

        self.assertEqual(
            SDValueSerializer.sToString(inputs[0].getValue()),
            SDValueSerializer.sToString(SDValueFloat3.sNew(float3(1.0, 0.5, 0.0))))

        self.assertEqual(
            SDValueSerializer.sToString(inputs[1].getValue()),
            SDValueSerializer.sToString(SDValueFloat4.sNew(float4(1.0, 0.6, 0.3, 0.0))))

        self.graph.deletePreset(preset.getLabel())

    @unittest.skipIf(spotColorsNotAvailable(), "No spot color support")
    def testSpotColorInputValues(self):
        spotColorLib = self.context.getSDApplication().getSpotColorLibrary()
        assert(spotColorLib)

        spotCol = spotColorLib.findSpotColorByName(
            "PANTONE+ Solid Coated", "PANTONE 7690 C")
        self.assertTrue(spotCol)

        preset = self.graph.newPreset('Test preset')
        preset.addInput('float3', spotCol)
        preset.addInput('float4', spotCol)

        inputs = preset.getInputs()
        self.assertEqual(len(inputs), 2)

        self.assertEqual(
            SDValueSerializer.sToString(inputs[0].getValue()),
            SDValueSerializer.sToString(spotCol))

        self.assertEqual(
            SDValueSerializer.sToString(inputs[1].getValue()),
            SDValueSerializer.sToString(spotCol))

        self.graph.deletePreset(preset.getLabel())

'''
# Uncomment to run the test in Designer's Python editor.
if __name__ == '__main__':

    import sys

    def dontQuit(code):
        pass
    sys.exit = dontQuit

    unittest.main()
'''