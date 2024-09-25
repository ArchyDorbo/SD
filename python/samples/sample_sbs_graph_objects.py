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
from sd.api.sdgraphobjectpin import *
from sd.api.sdgraphobjectframe import *
from sd.api.sdgraphobjectcomment import *

def main(aSDContext):
    """
    This sample show how to create graph object such as: Pins, Comments, Frames

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
    # Create new Pin
    sdGraphObjectPin = SDGraphObjectPin.sNew(sdSBSCompGraph)
    sdGraphObjectPin.setPosition(float2(2*cGridSize, 0))
    sdGraphObjectPin.setDescription('The Pin')

    # =========================================================================
    # Create a uniform color node
    sdSBSCompNodeUniform = sdSBSCompGraph.newNode('sbs::compositing::uniform')

    # =========================================================================
    # Create New Comment attached on a Node
    sdGraphObjectComment = SDGraphObjectComment.sNewAsChild(sdSBSCompNodeUniform)
    sdGraphObjectComment.setPosition(float2(-cGridSize*0.5, cGridSize*0.5))
    sdGraphObjectComment.setDescription('The Uniform node\'s comment')

    # =========================================================================
    # Create new Frame
    sdGraphObjectFrame = SDGraphObjectFrame.sNew(sdSBSCompGraph)
    sdGraphObjectFrame.setPosition(float2(-cGridSize, -cGridSize))
    sdGraphObjectFrame.setTitle('The Frame Title')
    sdGraphObjectFrame.setDescription('The frame description')
    sdGraphObjectFrame.setColor(ColorRGBA(0.2, 0.5, 0.7, 0.8))
    sdGraphObjectFrame.setSize(float2(2*cGridSize, 2*cGridSize))

    # =========================================================================
    # Save the new package on disk
    dstFileAbsPath = os.path.join(io.getUserDocumentOutputDir(__file__), sbsPackageName + '.sbs')
    sdPackageMgr.savePackageAs(sdPackage, dstFileAbsPath)
    print('Save output file to ' + dstFileAbsPath)


if __name__ == '__main__':
    main(sd.getContext())
