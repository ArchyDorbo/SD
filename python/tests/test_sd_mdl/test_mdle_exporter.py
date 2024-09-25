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

from __future__ import absolute_import, print_function

import os
import shutil
import unittest

from pathlib import Path

import sd

from sd.api.mdl.sdmdleexporter import *
from sd.api.mdl.sdmdlgraph import *
from tests import tools

import logging
logger = logging.getLogger(__name__)


class MDLEExporterTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctx = sd.getContext()

        pathPackages = [
            Path('test_mdl_bsdf.sbs'),
            Path('test_mdl_exporter.sbs'),
            Path('test_mdl_texture2d.sbs'),
            Path('test_mdl_lightprofile.sbs'),
        ]

        for pathPackage in pathPackages:
            def testLambda(self):
                sdPackage = tools.loadSDPackage(self.context, str(pathPackage))
                self.assertTrue(sdPackage, f'Fail to load package from {pathPackage}')

                sdMDLGraph = next((
                    sdResource
                    for sdResource in sdPackage.getChildrenResources(False)
                    if isinstance(sdResource, SDMDLGraph)
                ), None)
                self.assertTrue(sdMDLGraph, 'Could not find a MDL Graph in the package at depth 1')

                pathMDLE = Path(tools.getTestOutputDir(__file__)) / f'{pathPackage.stem}_{sdMDLGraph.getIdentifier()}.mdle'

                if pathMDLE.exists():
                    pathMDLE.unlink()

                if pathMDLE.parent.exists():
                    pathMDLE.parent.rmdir()

                SDMDLEExporter.sExportPreset(sdMDLGraph, str(pathMDLE))

                # Check results
                self.assertTrue(pathMDLE.exists(), f'Failed to export {sdMDLGraph.getIdentifier()} to {pathMDLE}')

                logger.debug(f'{sdMDLGraph.getIdentifier()} exported to {pathMDLE}')

if __name__ == '__main__':
    unittest.main()

