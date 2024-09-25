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
from sd.api import sdgraph
import unittest
from tests import tools

import logging
logger = logging.getLogger(__name__)

class TestApiObject(unittest.TestCase):
    def __mainScoped(self, aContext):
        with tools.loadSDPackage(aContext, '2_sbs_graphs.sbs') as sdPackage:
            with sdPackage.getChildrenResources(True) as sdResources:
                for sdResource in sdResources:
                    # Check if the resource is a SDGraph
                    if issubclass(type(sdResource), sdgraph.SDGraph):
                        with sdResource.getNodes() as sdNodes:
                            for sdNode in sdNodes:
                                pos = sdNode.getPosition()

    def __mainFlat(self, aContext):
        sdPackage = tools.loadSDPackage(aContext, '2_sbs_graphs.sbs')
        sdResources = sdPackage.getChildrenResources(True)
        for sdResource in sdResources:
            # Check if the resource is a SDGraph
            if issubclass(type(sdResource), sdgraph.SDGraph):
                sdNodes = sdResource.getNodes()
                for sdNode in sdNodes:
                    pos = sdNode.getPosition()

    def __mainNested(self, aContext):
        """
        This test is crafted to make sure objects are taken out of array and that they still
        are valid after the array goes out of scope
        """
        def __getResourceCount(package):
            return len(package.getChildrenResources(True))

        def __getResourceByIndex(package, index):
            return package.getChildrenResources(True)[index]

        sdPackage = tools.loadSDPackage(aContext, '2_sbs_graphs.sbs')
        for i in range(__getResourceCount(sdPackage)):
            # Check if the resource is a SDGraph
            sdResource = __getResourceByIndex(sdPackage, i)
            if issubclass(type(sdResource), sdgraph.SDGraph):
                sdNodes = sdResource.getNodes()
                for sdNode in sdNodes:
                    pos = sdNode.getPosition()

    def __mainArrays(self, aContext):
        sdPackage = tools.loadSDPackage(aContext, '2_sbs_graphs.sbs')
        firstResource = None
        for resource in sdPackage.getChildrenResources(True):
            firstResource = resource
            break
        logger.debug(firstResource.getIdentifier())
        logger.debug(firstResource.getType().getId())

        firstNode = None
        for node in firstResource.getNodes():
            firstNode = node
            break
        logger.debug('Pos: %dx%d' % (firstNode.getPosition().x, firstNode.getPosition().y))

    def runTest(self):
        context = sd.getContext()

        self.__mainScoped(context)
        apiObjectsScoped = context.getCTypesFct('CApi_getAPIObjectCount')()

        self.__mainFlat(context)
        apiObjectsFlat = context.getCTypesFct('CApi_getAPIObjectCount')()

        self.__mainNested(context)
        apiObjectsNested = context.getCTypesFct('CApi_getAPIObjectCount')()
        logger.debug('Living api objects after scoped run: %d' % apiObjectsScoped)
        logger.debug('Living api objects after nested run: %d' % apiObjectsNested)

        self.assertEqual(apiObjectsScoped, apiObjectsFlat, 'Ref Count is different')
        self.assertEqual(apiObjectsScoped, apiObjectsNested, 'Ref Count is different')

        self.__mainArrays(context)
        apiObjectsArrays = context.getCTypesFct('CApi_getAPIObjectCount')()
        self.assertEqual(apiObjectsArrays , apiObjectsFlat, 'Ref Count is different')
        self.assertEqual(apiObjectsArrays , apiObjectsNested, 'Ref Count is different')
        self.assertEqual(apiObjectsArrays , apiObjectsScoped, 'Ref Count is different')

if __name__ == '__main__':
    unittest.main()
