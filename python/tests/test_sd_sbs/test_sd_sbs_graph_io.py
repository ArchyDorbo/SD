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
from sd.api.sdapiobject import SDApiError
from sd.api.sdarray import SDArray
from sd.api.sdvaluestring import SDValueString
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph

from tests import tools

import typing

import logging
logger = logging.getLogger(__name__)


class TestSDSBSGraphIO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.context = sd.getContext()
        cls.package = tools.loadSDPackage(cls.context, 'graph_io_test.sbs')
        cls.graph = typing.cast(
            SDSBSCompGraph, cls.package.findResourceFromUrl('graph_io_test'))
        assert(cls.graph)

    @classmethod
    def tearDownClass(cls):
        cls.context.getSDApplication().getPackageMgr().unloadUserPackage(cls.package)

    @staticmethod
    def __convertSDStringArray(stringArray: SDArray[SDValueString]) -> list[str]:
        result: list[str] = []
        for strVal in stringArray:
            result.append(strVal.get())

        return result

    def testListInputs(self):
        inputList = self.__convertSDStringArray(
            self.graph.getInputIdentifiers())
        self.assertEqual(inputList, ['input0', 'input1', 'input2'])

    def testListOutputs(self):
        outputList = self.__convertSDStringArray(
            self.graph.getOutputIdentifiers())
        self.assertEqual(outputList, [
                         'basecolor', 'normal', 'roughness', 'metallic', 'height', 'ambientocclusion'])

    def testReverseInputs(self):
        inputList = self.__convertSDStringArray(
            self.graph.getInputIdentifiers())

        inputList.sort(reverse=True)

        for i, inputId in enumerate(inputList):
            self.graph.reorderGraphInput(
                inputIdentifier=inputId, newPosition=i)

        sortedInputList = self.__convertSDStringArray(
            self.graph.getInputIdentifiers())
        self.assertEqual(inputList, sortedInputList)

    def testReverseOutputs(self):
        outputList = self.__convertSDStringArray(
            self.graph.getOutputIdentifiers())

        outputList.sort(reverse=True)

        for i, outputId in enumerate(outputList):
            self.graph.reorderGraphOutput(
                outputIdentifier=outputId, newPosition=i)

        sortedOutputList = self.__convertSDStringArray(
            self.graph.getOutputIdentifiers())
        self.assertEqual(outputList, sortedOutputList)

    def testreorderGraphInputExceptions(self):
        #
        # No input with specified id.
        #

        try:
            self.graph.reorderGraphInput(
                inputIdentifier='noInput', newPosition=0)
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.ItemNotFound)
        except:
            self.assertTrue(False)

        #
        # Out of bounds.
        #

        try:
            self.graph.reorderGraphInput(
                inputIdentifier='input1', newPosition=7)
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.IndexOutOfBounds)
        except:
            self.assertTrue(False)

        try:
            self.graph.reorderGraphInput(
                inputIdentifier='input1', newPosition=-4)
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.IndexOutOfBounds)
        except:
            self.assertTrue(False)

    def testreorderGraphOutputExceptions(self):
        #
        # No output with specified id.
        #

        try:
            self.graph.reorderGraphOutput(
                outputIdentifier='noOutput', newPosition=0)
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.ItemNotFound)
        except:
            self.assertTrue(False)

        #
        # Out of bounds.
        #

        try:
            self.graph.reorderGraphOutput(
                outputIdentifier='metallic', newPosition=7)
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.IndexOutOfBounds)
        except:
            self.assertTrue(False)

        try:
            self.graph.reorderGraphOutput(
                outputIdentifier='metallic', newPosition=-4)
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.IndexOutOfBounds)
        except:
            self.assertTrue(False)


# Uncomment to run the test in Designer's Python editor.
if __name__ == '__main__':

    import sys

    def dontQuit(code):
        pass
    sys.exit = dontQuit

    unittest.main()
