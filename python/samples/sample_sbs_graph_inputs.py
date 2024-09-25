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
from sd.api.sdvalueint import *
from sd.api.sdvaluestring import *
from sd.api.sdvaluefloat import *
from sd.api.sdvaluebool import *
from sd.api.sdtypefloat2 import *

def main(aSDContext):
    """
    This sample show how to create a Substance Compositing Graph inputs

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

    #   - Create new input property
    sdGraphInputProperty = sdSBSCompGraph.newProperty('myInput', SDTypeFloat2.sNew(), SDPropertyCategory.Input)

    #   - Display the annotations of the properties
    print('Available annotations:')
    for annotationProperty in sdSBSCompGraph.getPropertyAnnotations(sdGraphInputProperty):
        print('   %s: %s' % (annotationProperty.getId(), annotationProperty.getType().getId()))

    #   - Set the min value
    sdSBSCompGraph.setPropertyAnnotationValueFromId(sdGraphInputProperty, 'min', SDValueFloat.sNew(0.25))

    #   - Set the max value
    sdSBSCompGraph.setPropertyAnnotationValueFromId(sdGraphInputProperty, 'max', SDValueFloat.sNew(0.75))

    #   - Set the step value
    sdSBSCompGraph.setPropertyAnnotationValueFromId(sdGraphInputProperty, 'step', SDValueFloat.sNew(0.05))

    #   - Set the clamp value
    sdSBSCompGraph.setPropertyAnnotationValueFromId(sdGraphInputProperty, 'clamp', SDValueBool.sNew(True))

    #   - Set editor as 'Position'
    sdSBSCompGraph.setPropertyAnnotationValueFromId(sdGraphInputProperty, 'editor', SDValueString.sNew('position'))

    # =========================================================================
    # Save the new package on disk
    dstFileAbsPath = os.path.join(io.getUserDocumentOutputDir(__file__), sbsPackageName + '.sbs')
    sdPackageMgr.savePackageAs(sdPackage, dstFileAbsPath)
    print('Save output file to ' + dstFileAbsPath)


if __name__ == '__main__':
    main(sd.getContext())
