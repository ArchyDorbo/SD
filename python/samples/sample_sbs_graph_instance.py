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
from sd.api.sdapplication import *
from sd.ui.graphgrid import *
from sd.api.sbs.sdsbscompgraph import *
from sd.api.sdvaluecolorrgba import *
from sd.api.sdvalueusage import *
from sd.api.sdvaluearray import *
from sd.api.sdvaluestruct import *
from sd.api.sdvaluefloat import *
from sd.api.sdvalueint import *

from sd.api.sdtypeusage import *
from sd.api.sdresourcebitmap import *
from sd.api.sdtypestruct import *

def main(aSDContext):
    """
    Sample used to show how to instanciate a Substance Compositing graph in another and also how to setup a gradient node

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

    #   - Set the graph identifier
    sdSBSCompGraph.setIdentifier(sbsPackageName)


    # =========================================================================
    # Create output Node BaseColor
    sdSBSCompNodeOutputBaseColor = sdSBSCompGraph.newNode('sbs::compositing::output')
    sdSBSCompNodeOutputBaseColor.setPosition(float2(0, -cGridSize))
    sdValueArray = SDValueArray.sNew(SDTypeUsage.sNew(), 0)
    sdValueArray.pushBack(SDValueUsage.sNew(SDUsage.sNew('baseColor', 'RGBA', 'sRGB')))
    sdSBSCompNodeOutputBaseColor.setAnnotationPropertyValueFromId('usages', sdValueArray)

    # Create output Node Normal
    sdSBSCompNodeOutputNormal = sdSBSCompGraph.newNode('sbs::compositing::output')
    sdSBSCompNodeOutputNormal.setPosition(float2(0, cGridSize))
    sdValueArray = SDValueArray.sNew(SDTypeUsage.sNew(), 0)
    sdValueArray.pushBack(SDValueUsage.sNew(SDUsage.sNew('normal', 'RGBA', 'sRGB')))
    sdSBSCompNodeOutputNormal.setAnnotationPropertyValueFromId('usages', sdValueArray)

    # =========================================================================
    sdSBSCompNodeGradient = sdSBSCompGraph.newNode('sbs::compositing::gradient')
    sdSBSCompNodeGradient.setPosition(float2(-2*cGridSize, -cGridSize))

    sdTypeStructGradientKeyRGBAStructType = SDTypeStruct.sNew('sbs::compositing::gradient_key_rgba')
    # Create key 0 to Red
    sdValueStructKey0 = SDValueStruct.sNew(sdTypeStructGradientKeyRGBAStructType)
    sdValueStructKey0.setPropertyValueFromId('value', SDValueColorRGBA.sNew(ColorRGBA(1, 0, 0, 1)))
    sdValueStructKey0.setPropertyValueFromId('position', SDValueFloat.sNew(0))
    sdValueStructKey0.setPropertyValueFromId('midpoint', SDValueFloat.sNew(0.5))

    # Create key 1 to Green
    sdValueStructKey1 = SDValueStruct.sNew(sdTypeStructGradientKeyRGBAStructType)
    sdValueStructKey1.setPropertyValueFromId('value', SDValueColorRGBA.sNew(ColorRGBA(0, 1, 0, 1)))
    sdValueStructKey1.setPropertyValueFromId('position', SDValueFloat.sNew(0.5))
    sdValueStructKey1.setPropertyValueFromId('midpoint', SDValueFloat.sNew(0.5))

    # Create key 2 to Blue
    sdValueStructKey2 = SDValueStruct.sNew(sdTypeStructGradientKeyRGBAStructType)
    sdValueStructKey2.setPropertyValueFromId('value', SDValueColorRGBA.sNew(ColorRGBA(0, 0, 1, 1)))
    sdValueStructKey2.setPropertyValueFromId('position', SDValueFloat.sNew(1))
    sdValueStructKey2.setPropertyValueFromId('midpoint', SDValueFloat.sNew(0.5))

    # Create array of keys
    sdValueArray = SDValueArray.sNew(sdTypeStructGradientKeyRGBAStructType, 0)
    sdValueArray.pushBack(sdValueStructKey0)
    sdValueArray.pushBack(sdValueStructKey1)
    sdValueArray.pushBack(sdValueStructKey2)

    # Set the key array to the node property
    sdSBSCompNodeGradient.setInputPropertyValueFromId('gradientrgba', sdValueArray)
    sdSBSCompNodeGradient.newPropertyConnectionFromId('unique_filter_output', sdSBSCompNodeOutputBaseColor, 'inputNodeOutput')

    # =========================================================================
    sdSBSCompNodeNormal = sdSBSCompGraph.newNode('sbs::compositing::normal')
    sdSBSCompNodeNormal.setPosition(float2(-2*cGridSize, cGridSize))
    sdSBSCompNodeNormal.newPropertyConnectionFromId('unique_filter_output', sdSBSCompNodeOutputNormal, 'inputNodeOutput')

    # =========================================================================
    resourcePath = sdApplication.getPath(SDApplicationPath.DefaultResourcesDir)
    sdPackageAlveolus = sdPackageMgr.loadUserPackage(os.path.join(resourcePath, 'packages', 'pattern_alveolus.sbs'), True)
    sdSBSCompNodeInstanceAlveolus = sdSBSCompGraph.newInstanceNode(sdPackageAlveolus.findResourceFromUrl('alveolus'))
    sdSBSCompNodeInstanceAlveolus.setPosition(float2(-4*cGridSize, 0))
    sdSBSCompNodeInstanceAlveolus.setInputPropertyValueFromId('Tiling', SDValueInt.sNew(5))
    sdSBSCompNodeInstanceAlveolusFirstOutputProperty = sdSBSCompNodeInstanceAlveolus.getProperties(SDPropertyCategory.Output)[0]
    sdSBSCompNodeInstanceAlveolusFirstOutputPropertyId = sdSBSCompNodeInstanceAlveolusFirstOutputProperty.getId()
    sdSBSCompNodeInstanceAlveolus.newPropertyConnectionFromId(
        sdSBSCompNodeInstanceAlveolusFirstOutputPropertyId,
        sdSBSCompNodeGradient,
        'input1')
    sdSBSCompNodeInstanceAlveolus.newPropertyConnectionFromId(
        sdSBSCompNodeInstanceAlveolusFirstOutputPropertyId,
        sdSBSCompNodeNormal,
        'input1')


    # =========================================================================
    # Save the new package on disk
    dstFileAbsPath = os.path.join(io.getUserDocumentOutputDir(__file__), sbsPackageName + '.sbs')
    sdPackageMgr.savePackageAs(sdPackage, dstFileAbsPath)
    print('Save output file to ' + dstFileAbsPath)


if __name__ == '__main__':
    main(sd.getContext())
