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
from sd.tools import io
from sd.ui.graphgrid import *
from sd.api.sbs.sdsbscompgraph import *
from sd.api.sdbasetypes import *
from sd.api.sdvaluefloat4 import *

def main(aSDContext):
    """
    This sample show how to setup a parameter that is controled by a function on a uniform node in a Substance Compositing graph.

    :param aSDContext: The SDContext
    :return: None
    """
    cGridSize = GraphGrid.sGetFirstLevelSize()
    sbsPackageName = os.path.split(__file__)[1].split('.')[0]  # Get the package name from the current python file base name

    # =========================================================================
    # Create a new Package
    sdPackageMgr = aSDContext.getSDApplication().getPackageMgr()
    sdPackage = sdPackageMgr.newUserPackage()

    # =========================================================================
    # Create a new Substance Compositing Graph in this package
    sdSBSCompGraph = SDSBSCompGraph.sNew(sdPackage)

    #   - Set the graph identifier
    sdSBSCompGraph.setIdentifier(sbsPackageName)

    # =========================================================================
    # Create a uniform color node
    sdSBSCompNodeUniform = sdSBSCompGraph.newNode('sbs::compositing::uniform')
    sdSBSCompNodeUniform.setPosition(float2(-2*cGridSize, cGridSize))

    #   - Get the input property that controls the output color
    uniformNodePropertyOutputColor = sdSBSCompNodeUniform.getPropertyFromId('outputcolor', SDPropertyCategory.Input)

    #   - Create a new property graph of type SDSBSFunctionGraph
    propertySBSFunctionGraph = sdSBSCompNodeUniform.newPropertyGraph(uniformNodePropertyOutputColor, 'SDSBSFunctionGraph')

    #   - Fill the property function. Here create a simple constant node that will return a green value
    float4ConstantNode = propertySBSFunctionGraph.newNode('sbs::function::const_float4')
    float4ConstantNode.setInputPropertyValueFromId('__constant__', SDValueFloat4.sNew(float4(0, 1, 0, 1)))

    # Set the constant node as output of the property's SBSFunctionGraph
    propertySBSFunctionGraph.setOutputNode(float4ConstantNode, True)

    # =========================================================================
    # Save the new package on disk
    dstFileAbsPath = os.path.join(io.getUserDocumentOutputDir(__file__), sbsPackageName + '.sbs')
    sdPackageMgr.savePackageAs(sdPackage, dstFileAbsPath)
    print('Save output file to ' + dstFileAbsPath)


if __name__ == '__main__':
    main(sd.getContext())
