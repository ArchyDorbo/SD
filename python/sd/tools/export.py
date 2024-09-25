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
from sd.api.sbs import sdsbscompgraph
from sd.api import sdproperty
from sd.api.apiexception import APIException

def exportSDGraphOutputs(
        aSDGraph,
        aOutputDir = '',
        aFileExt = 'png'):
    """
    Export the textures of the output node of the specified sSDGraph
    :param aSDGraph: The graph that contains the outputs to export
    :param aOutputDir: The output directory used to save the output's images
    :return: True if succeed else False
    """
    if not aSDGraph:
        return False

    if not issubclass(type(aSDGraph), sdsbscompgraph.SDSBSCompGraph):
        return False

    # Compute the SDSBSCompGraph so that all node's textures are computed
    aSDGraph.compute()

    # Get some information on the graph
    graphIdentifier = aSDGraph.getIdentifier()

    # Iterate on nodes
    nodeIndex = -1
    for sdNode in aSDGraph.getOutputNodes():
        nodeIndex = nodeIndex + 1

        nodeDefinition = sdNode.getDefinition()
        outputProperties = nodeDefinition.getProperties(sdproperty.SDPropertyCategory.Output)
        for outputProperty in outputProperties:
            # Get the property value
            propertyValue = sdNode.getPropertyValue(outputProperty)

            # Get the property value as texture
            propertyTexture = propertyValue.get()
            if not propertyTexture:
                continue

            # Save the texture on disk
            fileExt = aFileExt
            fileName = str(graphIdentifier) + '_output_'+ str(nodeIndex) +'.'+ str(fileExt)
            textureFileName = os.path.abspath(os.path.join(aOutputDir, fileName))

            try:
                propertyTexture.save(textureFileName)
            except APIException:
                print('Fail to save texture %s' % textureFileName)

    return True
