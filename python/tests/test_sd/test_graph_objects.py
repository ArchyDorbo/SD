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
from sd.api.sdbasetypes import *
from sd.api.sdgraphobjectcomment import *
from sd.api.sdgraphobjectframe import *
from sd.api.sdgraphobjectpin import *
from sd.api.sdpackage import SDPackage
from sd.api.sdpackagemgr import SDPackageMgr

from sd.api.sbs.sdsbscompgraph import *
from sd.api.sbs.sdsbsfunctiongraph import *
from sd.api.sbs.sdsbsfxmapgraph import *

from sd.api.mdl.sdmdlgraph import *

from tests import tools

import typing

class TestGraphObjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        context = sd.getContext()

        # Create new SDPackage
        cls.pkgMgr = typing.cast(SDPackageMgr, context.getSDApplication().getPackageMgr())
        cls.sdPackage = cls.pkgMgr.newUserPackage()

    @classmethod
    def tearDownClass(cls):
        # Save File
        dstFileAbsPath = os.path.join(tools.getTestOutputDir(__file__), 'test_graph_objects.sbs')
        cls.pkgMgr.savePackageAs(cls.sdPackage, dstFileAbsPath)

    def testCreateNewPackage(self):
        self.assertTrue(self.sdPackage, 'Fail to create new package')

    def testSDSBSCompGraph(self):
        sdSBSCompGraph = SDSBSCompGraph.sNew(self.sdPackage)
        self.__test_SDGraphObjectForSDGraph(sdSBSCompGraph)

    def testSDSBSFxMapGraph(self):
        sdSBSCompGraph = SDSBSCompGraph.sNew(self.sdPackage)
        sdSBSCompNodeFxMap = sdSBSCompGraph.newNode('sbs::compositing::fxmaps')
        sdSBSFxMapGraph = sdSBSCompNodeFxMap.getReferencedResource()
        self.__test_SDGraphObjectForSDGraph(sdSBSFxMapGraph)

    def testSDSBSFunctionGraph(self):
        sdSBSFunctionGraph = SDSBSFunctionGraph.sNew(self.sdPackage)
        self.__test_SDGraphObjectForSDGraph(sdSBSFunctionGraph)

    def testSDMDLGraph(self):
        sdMDLGraph = SDMDLGraph.sNew(self.sdPackage)
        self.__test_SDGraphObjectForSDGraph(sdMDLGraph)

    def __test_SDGraphObjectMethods(self, aGraphObject):
        self.mPosition = float2(self.mPosition.x + 100, self.mPosition.y)

        # Test Position
        aGraphObject.setPosition(self.mPosition)
        v = aGraphObject.getPosition()
        self.assertEqual(v.x, self.mPosition.x)
        self.assertEqual(v.y, self.mPosition.y)

        # Test Description
        desc = '%s Description' % type(aGraphObject).__name__
        aGraphObject.setDescription(desc)
        v = aGraphObject.getDescription()
        self.assertEqual(v, desc)

        if issubclass(type(aGraphObject), SDGraphObjectFrame):
            # Test Color
            c = ColorRGBA(0.2, 0.5, 0.7, 0.8)
            aGraphObject.setColor(c)
            v = aGraphObject.getColor()
            self.assertAlmostEqual(v.r, c.r, 4)
            self.assertAlmostEqual(v.g, c.g, 4)
            self.assertAlmostEqual(v.b, c.b, 4)
            self.assertAlmostEqual(v.a, c.a, 4)

            # Test Size
            size = float2(300, 150)
            aGraphObject.setSize(size)
            v = aGraphObject.getSize()
            self.assertEqual(v.x, size.x)
            self.assertEqual(v.y, size.y)

    def __test_SDGraphObjectForSDGraph(self, aSDGraph):
        self.mPosition = float2(0, 100)

        # Pin
        sdGraphObjectPin = SDGraphObjectPin.sNew(aSDGraph)
        self.assertTrue(sdGraphObjectPin)
        self.__test_SDGraphObjectMethods(sdGraphObjectPin)

        # Comment
        sdGraphObjectComment = SDGraphObjectComment.sNew(aSDGraph)
        self.assertTrue(sdGraphObjectComment)
        self.__test_SDGraphObjectMethods(sdGraphObjectComment)


        nodeDefinitions = aSDGraph.getNodeDefinitions()
        self.assertTrue(nodeDefinitions)
        self.assertTrue(len(nodeDefinitions)>0)
        sdNode = aSDGraph.newNode(nodeDefinitions[0].getId())
        sdNode.setPosition(float2(100, 0))
        self.assertTrue(sdNode)
        sdGraphObjectCommentOfNode = SDGraphObjectComment.sNewAsChild(sdNode)
        self.assertTrue(sdGraphObjectCommentOfNode)
        parentNode = sdGraphObjectCommentOfNode.getParent()
        self.assertTrue(parentNode)
        self.assertEqual(parentNode.getIdentifier(), sdNode.getIdentifier())

        # Frame
        sdGraphObjectFrame = SDGraphObjectFrame.sNew(aSDGraph)
        self.assertTrue(sdGraphObjectFrame)
        self.__test_SDGraphObjectMethods(sdGraphObjectFrame)

        # Check GraphObjects in SBSCompGraph
        array = aSDGraph.getGraphObjects()
        self.assertEqual(len(array), 4)

        # Test deleting all graph objects.
        for obj in aSDGraph.getGraphObjects():
            aSDGraph.deleteGraphObject(obj)
        self.assertEqual(len(aSDGraph.getGraphObjects()), 0)


if __name__ == '__main__':
    unittest.main()

