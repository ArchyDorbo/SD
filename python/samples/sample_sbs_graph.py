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
from sd.api.sdvalueusage import *
from sd.api.sdvaluearray import *
from sd.api.sdvalueenum import *
from sd.api.sdtypeusage import *
from sd.api.sdresourcebitmap import *

def main(aSDContext):
    """
    This sample show how to create a simple Substance Compositing Graph that uses:
        - a Bitmap Node
        - a Uniform Color
        - a Blend Node
        - an Output Node
        - Bitmap Resource that links a bitmap file

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

    #   - Set the position of the uniform node
    sdSBSCompNodeUniform.setPosition(float2(-2*cGridSize, cGridSize))

    #   - Set the inheritance mode of the '$format' property to absolute
    sdSBSCompNodeUniform.setInputPropertyInheritanceMethodFromId('$format', SDPropertyInheritanceMethod.Absolute)

    #   - Change the Output format of the '$format' property to 'hdr_high_precision'
    sdSBSCompNodeUniform.setInputPropertyValueFromId('$format', SDValueEnum.sFromValueId('sbs::compositing::format', 'hdr_high_precision'))

    #   - Change the color property of this node
    #       - Create the value color. The SDValueColorRGBA embeds the base type value of type ColorRGBA
    sdValueColorRGBA = SDValueColorRGBA.sNew(ColorRGBA(0.2, 0.5, 0.8, 1.0))
    #       - Set the color value to the 'outputcolor' input property of the node
    sdSBSCompNodeUniform.setInputPropertyValueFromId('outputcolor', sdValueColorRGBA)

    # =========================================================================
    # Create a bitmap node
    #   - Import bitmap resource
    #       - Get the bitmap file path from the 'assets' directory
    bitmapFileAbsPath = os.path.join(io.getAssetsDir(__file__), 'substance-128x128.png')
    #       - Create a new resource in the package that link the specified bitmap
    linkedSDResourceBitmap = SDResourceBitmap.sNewFromFile(sdPackage, bitmapFileAbsPath, EmbedMethod.Linked)
    #       - Change the resource identifier
    linkedSDResourceBitmap.setIdentifier('linked_bitmap_resource')

    #   - Instantiate the bitmap resource to the graph to have a node that will refers the created bitmap resource
    sdSBSCompNodeBitmap = sdSBSCompGraph.newInstanceNode(linkedSDResourceBitmap)
    #       - Set the position of the bitmap node
    sdSBSCompNodeBitmap.setPosition(float2(-2*cGridSize, -cGridSize))

    # =========================================================================
    # Create a blend Node
    sdSBSCompNodeBlend = sdSBSCompGraph.newNode('sbs::compositing::blend')
    #   - Set the position of the output node
    sdSBSCompNodeBlend.setPosition(float2(0, 0))

    # =========================================================================
    # Create an output Node
    sdSBSCompNodeOutput = sdSBSCompGraph.newNode('sbs::compositing::output')

    #   - Set the position of the output node
    sdSBSCompNodeOutput.setPosition(float2(2*cGridSize, 0))

    #   - Add one usage 'baseColor' to the output node
    #       The usages of an output (or input node) are define from/to an array.
    #       - Create an array value of usages (of undefined size)
    sdValueArray = SDValueArray.sNew(SDTypeUsage.sNew(), 0)
    #       - Create an usage value that embed the usage to add to the node
    sdValueUsage = SDValueUsage.sNew(SDUsage.sNew('baseColor', 'RGBA', 'sRGB'))
    #       - Add the usage value to the array
    sdValueArray.pushBack(sdValueUsage)
    #       - Set the value array to the 'usages' annotation of the output node
    sdSBSCompNodeOutput.setAnnotationPropertyValueFromId('usages', sdValueArray)

    # =========================================================================
    # Create connections
    #   - Connect the Bitmap node to the Blend node
    #       - 'unique_filter_output': The identifier of the output property of the Uniform Node.
    #           This property is Connectable (i.e. SDProperty.isConnectable() is True), it means that a Connector is displayed for this property in the graph,
    #           and a connection can be defined from/to this property.
    #       - 'sdSBSCompNodeOutput': This is the other Node to connect
    #       - 'source': This is the input property of the other Node
    sdSBSCompNodeBitmap.newPropertyConnectionFromId('unique_filter_output', sdSBSCompNodeBlend, 'source')

    #   - Connect the Uniform node to the Blend node
    #       - 'unique_filter_output': The identifier of the output property of the Uniform Node.
    #           This property is Connectable (i.e. SDProperty.isConnectable() is True), it means that a Connector is displayed for this property in the graph,
    #           and a connection can be defined from/to this property.
    #       - 'sdSBSCompNodeOutput': This is the other Node to connect
    #       - 'destination': This is the input property of the other Node
    sdSBSCompNodeUniform.newPropertyConnectionFromId('unique_filter_output', sdSBSCompNodeBlend, 'destination')

    #   - Connect the Blend node to the output node
    #       - 'unique_filter_output': The identifier of the output property of the Uniform Node.
    #           This property is Connectable (i.e. SDProperty.isConnectable() is True), it means that a Connector is displayed for this property in the graph,
    #           and a connection can be defined from/to this property.
    #       - 'sdSBSCompNodeOutput': This is the other Node to connect
    #       - 'inputNodeOutput': This is the input property of the other Node
    sdSBSCompNodeBlend.newPropertyConnectionFromId('unique_filter_output', sdSBSCompNodeOutput, 'inputNodeOutput')

    # =========================================================================
    # Save the new package on disk
    dstFileAbsPath = os.path.join(io.getUserDocumentOutputDir(__file__), sbsPackageName + '.sbs')
    sdPackageMgr.savePackageAs(sdPackage, dstFileAbsPath)
    print('Save output file to ' + dstFileAbsPath)


if __name__ == '__main__':
    main(sd.getContext())
