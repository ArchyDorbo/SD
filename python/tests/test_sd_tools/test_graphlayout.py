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

import sd
from sd.tools import graphlayout
from sd.api import sdgraph
from tests import tools
import unittest

class TestGraphLayout(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()

        # Load Package
        sdPackage = tools.loadSDPackage(context, '2_sbs_graphs.sbs')

        # Process all nodes
        for sdResource in sdPackage.getChildrenResources(True):
            # Check if the resource is a SDGraph
            if not issubclass(type(sdResource), sdgraph.SDGraph):
                continue
            res = graphlayout.alignSDNodes(
                sdResource.getNodes(),
                aAlignDirection=graphlayout.AlignmentDirection.Horizontal)
            self.assertTrue(res, 'Fail to align horizontally SDNodes')

            res = graphlayout.alignSDNodes(
                sdResource.getNodes(),
                aAlignDirection=graphlayout.AlignmentDirection.Vertical)
            self.assertTrue(res, 'Fail to align vertically SDNodes')

            res = graphlayout.snapSDNodes(sdResource.getNodes())
            self.assertTrue(res, 'Fail to snap SDNodes')

if __name__ == '__main__':
    unittest.main()
