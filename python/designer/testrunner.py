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

import sd
import os
import sys

from PySide6 import QtGui, QtWidgets


class TestRunner(object):
    __runAllTestsAction = None

    @classmethod
    def initialize(cls):
        app = sd.getContext().getSDApplication()
        uiMgr = app.getQtForPythonUIMgr()

        if uiMgr:
            debugMenu = uiMgr.findMenuFromObjectName("Pfx.Editor.Menu.Debug")

            if debugMenu:
                thisDir = os.path.abspath(os.path.dirname(__file__))
                testsDir = os.path.abspath(os.path.join(thisDir, ".."))

                if not testsDir in sys.path:
                    sys.path.append(testsDir)

                iconPath = os.path.join(thisDir, "icons", "icon_run_tests.svg")
                icon = QtGui.QIcon(iconPath)

                cls.__runAllTestsAction = QtGui.QAction(icon, "Run All Tests", debugMenu)
                cls.__runAllTestsAction.triggered.connect(cls.runAllTests)
                debugMenu.addAction(cls.__runAllTestsAction)

    @classmethod
    def uninitialize(cls):
        if cls.__runAllTestsAction:
            app = sd.getContext().getSDApplication()
            uiMgr = app.getQtForPythonUIMgr()
            debugMenu = uiMgr.findMenuFromObjectName("Pfx.Editor.Menu.Debug")
            debugMenu.removeAction(cls.__runAllTestsAction)

    @classmethod
    def runAllTests(cls):
        from tests.run_tests import runTests

        try:
            result = runTests()
            print(result)
        except SystemExit:
            # Ignore unittest calls to sys.exit()
            pass
