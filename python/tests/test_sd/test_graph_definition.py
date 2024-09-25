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

import unittest
from samples.plugins.custom_graph.custom_graph import *


class TestGraphDefinition(unittest.TestCase):

    def runTest(self):
        CustomGraph.init('custom_graph_test')


if __name__ == '__main__':
    TestGraphDefinition().runTest()

