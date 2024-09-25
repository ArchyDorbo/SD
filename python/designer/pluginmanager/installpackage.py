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
import sys
import json
import zipfile

from sd.api.sdplugin import SDPlugin
from sd.api.sdpluginmgr import SDPluginMgr

from PySide6 import QtCore


def installPackage(packagePath, pluginMgr, model):
    packageDir = os.path.dirname(packagePath)
    packageFilename = os.path.basename(packagePath)
    packageName, _ = os.path.splitext(packageFilename)

    # Open the package.
    try:
        archive = zipfile.ZipFile(packagePath, 'r')
    except:
        raise RuntimeError(
            QtCore.QCoreApplication.translate("PluginManagerUI", "Couldn't open package {}").format(packagePath))

    # Read the metadata.
    try:
        # Don't use os.path.join. Zip archives always use / as the path separator.
        metadata = archive.read(packageName + '/pluginInfo.json')
        metadata = metadata.decode("utf-8")
    except:
        archive.close()
        raise RuntimeError(
            QtCore.QCoreApplication.translate("PluginManagerUI", "Couldn't read pluginInfo.json file inside package {}").format(packagePath))

    # Check that the plugin is compatible.
    err = pluginMgr.checkPluginCompatibility(metadata)
    if err:
        archive.close()
        raise RuntimeError(err)

    # Install the plugin package.
    userPluginDir = pluginMgr.getUserPluginsDir()

    if os.path.exists(os.path.join(userPluginDir, packageName)):
        archive.close()
        raise RuntimeError(
            QtCore.QCoreApplication.translate("PluginManagerUI", "A package named {0} is already installed in {1}.").format(packageName, userPluginDir))

    archive.extractall(userPluginDir)
    archive.close()

    # Add the plugin dir to the path, so that it can be imported.
    pluginDir = os.path.join(userPluginDir, packageName)
    if not pluginDir in sys.path:
        sys.path.append(pluginDir)

    plugin = pluginMgr.loadPlugin(packageName, userPluginDir)
    index = model.newPluginLoaded(plugin)
    return index
