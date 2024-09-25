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
import unittest
import sd
from sd.tools import io
from sd.api.sdresourcebitmap import *
from sd.api.sdresourcesvg import *
from sd.api.sdresourcefont import *
from sd.api.sdresourcescene import *
from sd.api.sdresourcelightprofile import *
from sd.api.sdresourcebsdfmeasurement import *

from sd.api.sbs.sdsbscompgraph import *
from sd.api.sbs.sdsbsfunctiongraph import *
from sd.api.mdl.sdmdlgraph import *

from tests import tools
from tests import data_serializer


class TestResourceDefinitions(unittest.TestCase):

    def runTest(self):
        context = sd.getContext()
        sdPackage = context.getSDApplication().getPackageMgr().newUserPackage()

        # Create resources in Package
        self.__createResources(sdPackage)

        # Generate lines to serialize
        lines = data_serializer.DataSerializer().serializeSDPackage(sdPackage)

        # Write data file
        logFileDir = tools.getAssetsDir()
        currentFileBaseName = io.getFileBaseName(__file__)
        srcDumpFile = os.path.join(logFileDir, currentFileBaseName + '.txt')
        with open(srcDumpFile, 'wt') as f:
            for line in lines:
                f.write(line + '\n')
            f.close()


    def __createResources(self, aSDPackage):
        # Substance Compositing Graph
        SDSBSCompGraph.sNew(aSDPackage)

        # Substance Fucntion Graph
        SDSBSFunctionGraph.sNew(aSDPackage)

        # MDL Graph
        SDMDLGraph.sNew(aSDPackage)

        # Bitmap
        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'substance-128x128.png')
        SDResourceBitmap.sNewFromFile(aSDPackage, textureFileAbsPath, EmbedMethod.Linked)

        # SVG
        textureFileAbsPath = os.path.join(tools.getAssetsDir(), 'sbs.svg')
        SDResourceSVG.sNewFromFile(aSDPackage, textureFileAbsPath, EmbedMethod.Linked)

        # Font
        fontFileAbsPath = os.path.join(tools.getAssetsDir(), 'AdobeClean-Regular.ttf')
        SDResourceFont.sNewFromFile(aSDPackage, fontFileAbsPath, EmbedMethod.Linked)

        # Scene
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'Rounded Cylinder.fbx')
        SDResourceScene.sNewFromFile(aSDPackage, sceneFileAbsPath, EmbedMethod.Linked)

        # Light Profile from file
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'example_modules.ies')
        SDResourceLightProfile.sNewFromFile(aSDPackage, sceneFileAbsPath, EmbedMethod.Linked)

        # BSDF Measurement
        sceneFileAbsPath = os.path.join(tools.getAssetsDir(), 'carpaint_blue.mbsdf')
        SDResourceBSDFMeasurement.sNewFromFile(aSDPackage, sceneFileAbsPath, EmbedMethod.Linked)

if __name__ == '__main__':
    unittest.main()

