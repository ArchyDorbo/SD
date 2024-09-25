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

from .appinterop import AppInteropUI
from .pluginmanager import PluginManagerUI
from .testrunner import TestRunner
from .graph_cleaner import initializeGraphCleaner, uninitializeGraphCleaner


def initialize():
    AppInteropUI.initialize()
    PluginManagerUI.initialize()
    TestRunner.initialize()
    initializeGraphCleaner()


def uninitialize():
    uninitializeGraphCleaner()
    TestRunner.uninitialize()
    PluginManagerUI.uninitialize()
    AppInteropUI.uninitialize()
