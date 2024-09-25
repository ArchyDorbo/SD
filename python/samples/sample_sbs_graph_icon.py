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
from sd.api.sdvaluecolorrgba import *
from sd.api.sdvalueint import *
from sd.api.sdresourcebitmap import *
from sd.api.sdapplication import *

def main(aSDContext):
    """
    This sample show how to create and set an icon of a Substance Compositing Graph.

    :param aSDContext: The SDContext
    :return: None
    """
    cGridSize = GraphGrid.sGetFirstLevelSize()
    sbsPackageName = os.path.split(__file__)[1].split('.')[0]  # Get the package name from the current python file base name

    # =========================================================================
    # Create a new Package
    sdApplication = aSDContext.getSDApplication()
    sdPackageMgr = sdApplication.getPackageMgr()
    sdPackage = sdPackageMgr.newUserPackage()

    # =========================================================================
    # Create a new Substance Compositing Graph in this package
    sdSBSCompGraph = SDSBSCompGraph.sNew(sdPackage)
    sdSBSCompGraph.setIdentifier(sbsPackageName)

    # =========================================================================
    # Create an output node
    sdSBSCompNodeOutput = sdSBSCompGraph.newNode('sbs::compositing::output')

    # =========================================================================
    # Create an instance node
    resourcePath = sdApplication.getPath(SDApplicationPath.DefaultResourcesDir)
    sdPackageAlveolus = sdPackageMgr.loadUserPackage(os.path.join(resourcePath, 'packages', 'pattern_alveolus.sbs'), True)
    sdSBSCompNodeInstanceAlveolus = sdSBSCompGraph.newInstanceNode(sdPackageAlveolus.findResourceFromUrl('alveolus'))
    sdSBSCompNodeInstanceAlveolus.setPosition(float2(-2*cGridSize, 0))
    sdSBSCompNodeInstanceAlveolus.setInputPropertyValueFromId('Tiling', SDValueInt.sNew(5))

    # Retrieve the first output property of the instance node
    sdFirstOutputProperty = sdSBSCompNodeInstanceAlveolus.getProperties(SDPropertyCategory.Output)[0]

    # Connect this output property to the input property of the output node
    sdSBSCompNodeInstanceAlveolus.newPropertyConnectionFromId(sdFirstOutputProperty.getId(), sdSBSCompNodeOutput, 'inputNodeOutput')

    # =========================================================================
    # Compute the SBS Compositing graph
    sdSBSCompGraph.compute()

    # =========================================================================
    # Get the value of the first output property of the instance node.
    # This property's type is a SDTypeTexture so the returned SDValue is a SDValueTexture
    sdFirstOutputPropertyValueTexture = sdSBSCompNodeInstanceAlveolus.getPropertyValue(sdFirstOutputProperty)

    # Get the SDTexture of the SDValueTexture
    sdTexture = sdFirstOutputPropertyValueTexture.get()

    # =========================================================================
    # Set the icon of the graph
    sdSBSCompGraph.setIcon(sdTexture)

    # =========================================================================
    # Save the new package on disk
    dstFileAbsPath = os.path.join(io.getUserDocumentOutputDir(__file__), sbsPackageName + '.sbs')
    sdPackageMgr.savePackageAs(sdPackage, dstFileAbsPath)
    print('Save output file to ' + dstFileAbsPath)


if __name__ == '__main__':
    main(sd.getContext())
