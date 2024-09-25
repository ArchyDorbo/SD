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
from sd.api.sdapiobject import SDApiError
from sd.api.apiexception import APIException
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph

from tests import tools

import logging
logger = logging.getLogger(__name__)


class TestSDSBSGraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.context = sd.getContext()
        cls.package = cls.context.getSDApplication().getPackageMgr().newUserPackage()
        cls.graph = SDSBSCompGraph.sNew(cls.package)

    @classmethod
    def tearDownClass(cls):
        cls.context.getSDApplication().getPackageMgr().unloadUserPackage(cls.package)

    #
    # Default parent size.
    #

    def testDefaultParentSizeBasic(self):
        from sd.api.sdbasetypes import int2

        self.assertTrue(self.graph, 'Failed to create new graph')

        self.graph.setDefaultParentSize(int2(1024, 1024))
        size = self.graph.getDefaultParentSize()
        self.assertEqual(size.x, 1024)
        self.assertEqual(size.y, 1024)

    def testDefaultParentSizeNonPow2Rounding(self):
        from sd.api.sdbasetypes import int2

        self.assertTrue(self.graph, 'Failed to create new graph')

        self.graph.setDefaultParentSize(int2(1027, 1027))
        size = self.graph.getDefaultParentSize()
        self.assertEqual(size.x, 2048)
        self.assertEqual(size.y, 2048)

        self.graph.setDefaultParentSize(int2(3211, 785))
        size = self.graph.getDefaultParentSize()
        self.assertEqual(size.x, 4096)
        self.assertEqual(size.y, 1024)

    def testDefaultParentSizeInvalidRaisesException(self):
        from sd.api.sdbasetypes import int2

        self.assertTrue(self.graph, 'Failed to create new graph')

        try:
            self.graph.setDefaultParentSize(int2(0, -1024))
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.InvalidArgument)
        except:
            self.assertTrue(False)

        try:
            self.graph.setDefaultParentSize(int2(-200, 0))
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.InvalidArgument)
        except:
            self.assertTrue(False)

    #
    # Graph Type
    #
    def testGetSetValidGraphType(self):
        self.assertTrue(self.graph, 'Failed to create new graph')

        self.graph.setGraphType("atlas_material")

        graphType = self.graph.getGraphType()
        self.assertEqual(graphType, "atlas_material")

    def testGetSetInvalidGraphType(self):
        self.assertTrue(self.graph, 'Failed to create new graph')

        try:
            self.graph.setGraphType("my_graph_type")
            self.assertTrue(False)
        except APIException as e:
            self.assertEqual(e.mErrorCode, SDApiError.InvalidArgument)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
