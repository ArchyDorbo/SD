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
import sd
from sd.tools import export
from sd.api import sdproperty, sdgraph
from tests import tools
import unittest

class TestExport(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()

        # Load Package
        sdPackage = tools.loadSDPackage(context, 'test_export.sbs')
        self.assertTrue(sdPackage, 'Fail to load package')

        graphUrl = 'myGraph1'
        sdResource = sdPackage.findResourceFromUrl(graphUrl)
        self.assertTrue(sdResource, 'Graph \'%s\'not found' % graphUrl)
        # Check if the resource is a SDGraph
        if not issubclass(type(sdResource), sdgraph.SDGraph):
            self.assertTrue(sdResource, 'Resource \'%s\' is not a Graph' % graphUrl)
        self.__checkGraph(sdResource)

        outputDir = context.getTempDir(os.path.split(__file__)[1].split('.')[0])
        self.__exportGraph(sdResource, outputDir)

    def __checkGraph(self, aSDGraph):
        if not aSDGraph:
            return False

        # Get some information on the graph
        graphIdentifier = aSDGraph.getIdentifier()

        # Iterate on nodes
        for sdNode in aSDGraph.getNodes():
            nodeDefinition = sdNode.getDefinition()
            outputProperties = nodeDefinition.getProperties(sdproperty.SDPropertyCategory.Output)

            # Check the node type
            sdNodeTypeName = nodeDefinition.getId()
            if sdNodeTypeName == 'sbs::compositing::output':
                self.assertEqual(len(outputProperties), 1, 'Wrong output property number')
            elif sdNodeTypeName == 'sbs::compositing::sbscompgraph_instance':
                self.assertEqual(len(outputProperties), 5, 'Wrong output property number')
            else:
                self.assertEqual(len(outputProperties), 1, 'Wrong output property number')

    def __exportGraph(self, aSDGraph, aOutputDir):
        export.exportSDGraphOutputs(aSDGraph, aOutputDir)

if __name__ == '__main__':
    unittest.main()
