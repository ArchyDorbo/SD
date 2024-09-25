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
from sd.api import sdproperty, sdgraph
from sd.api.sdbasetypes import float2
from tests import tools
import unittest

import logging
logger = logging.getLogger(__name__)


class TestLoadSavePackage(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()
        srcPackageFileName = '2_sbs_graphs.sbs'
        sdPackage = tools.loadSDPackage(context, srcPackageFileName)
        self.assertTrue(sdPackage, 'Fail to load package')

        filePath = sdPackage.getFilePath()
        self.assertEqual(os.path.split(filePath)[1], srcPackageFileName, 'Fail to load package')

        sdResourceArray = sdPackage.getChildrenResources(True)
        self.assertTrue(sdResourceArray)

        # self.assertTrue(len(sbsGraphArray) == 2)
        sdGraphIndex = -1
        tab = '\t'
        for sdResource in sdResourceArray:
            sdResourceIdentifier = sdResource.getIdentifier()
            # Check if the resource is a SDGraph
            if not issubclass(type(sdResource), sdgraph.SDGraph):
                continue
            sdGraphIndex = sdGraphIndex + 1
            sdNodeArray = sdResource.getNodes()
            self.assertTrue(sdNodeArray, 'Fail to get Nodes from SD Graph')
            sdNodeArraySize = len(sdNodeArray)

            if sdGraphIndex == 0:
                self.assertEqual(sdResourceIdentifier, 'myGraph1', 'Graph identifier comparison failed')
                self.assertEqual(sdNodeArraySize, 7, 'Invalid Node count')
            elif sdGraphIndex == 1:
                self.assertEqual(sdResourceIdentifier, 'mySubGraph2', 'Graph identifier comparison failed')
                self.assertEqual(sdNodeArraySize, 5, 'Invalid Node count')
            # put nodes horizontally
            for sdNode in sdNodeArray:
                pos = sdNode.getPosition()
                self.assertTrue(pos, 'Fail to get node Position')

                # Check node position modification
                newPosX = 1234
                newPosY = -654
                sdNode.setPosition(float2(newPosX, newPosY))

                pos = sdNode.getPosition()
                self.assertTrue(pos, 'Fail to get node Position')
                self.assertEqual(pos.x, newPosX, 'Node Position X has not been set correctly')
                self.assertEqual(pos.y, newPosY, 'Node Position Y has not been set correctly')

                nodeDefinition = sdNode.getDefinition()
                inputProperties = nodeDefinition.getProperties(sdproperty.SDPropertyCategory.Input)
                logging.debug(tab + 'Node: ')
                for sdProperty in inputProperties:
                    name = sdProperty.getId()
                    sdType = sdProperty.getType()
                    category = sdProperty.getCategory()
                    logging.debug(tab*2 + '"%s" : "%s" (%s)' % (name, sdType.getId(), str(category)))
                    self.assertTrue(name, 'Empty property name')
                    # self.assertTrue(sdType, 'Empty property sdType for "' + name +'"')
                outputProperties = nodeDefinition.getProperties(sdproperty.SDPropertyCategory.Output)
                logging.debug(tab + 'Node: ')
                for sdProperty in outputProperties:
                    name = sdProperty.getId()
                    sdType = sdProperty.getType()
                    category = sdProperty.getCategory()
                    logging.debug(tab*2 + '"%s" : "%s" (%s)' % (name, sdType.getId(), str(category)))
                    self.assertTrue(name, 'Empty property name')
                    # self.assertTrue(sdType, 'Empty property sdType for "' + name +'"')

            # Save package to new file
            dstFileAbsPath = os.path.join(tools.getTestOutputDir(__file__), 'output.sbs')
            context.getSDApplication().getPackageMgr().savePackageAs(sdPackage, dstFileAbsPath)

if __name__ == '__main__':
    unittest.main()
