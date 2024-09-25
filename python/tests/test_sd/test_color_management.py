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

def isDesignerSDK():
    import sd
    ctx = sd.getContext()
    app = ctx.getSDApplication()
    return app.getUIMgr() == None


class TestColorManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx = sd.getContext()
        app = ctx.getSDApplication()
        cls.cmEngine = app.getColorManagementEngine()

    @classmethod
    def tearDownClass(cls):
        pass

    @unittest.skipIf(isDesignerSDK(), "No color management in designersdk")
    def testColorManagementEngine(self):
        self.assertTrue(self.cmEngine)

        self.assertTrue(self.cmEngine)

        cmName = self.cmEngine.getName()

        self.assertTrue(cmName)
        self.assertTrue(self.cmEngine.getWorkingColorSpaceName())
        self.assertTrue(self.cmEngine.getRawColorSpaceName())

        self.assertTrue(len(self.cmEngine.getColorSpaces()) != 0)

        if cmName == 'ocio':
            self.assertTrue(self.cmEngine.getOCIOConfigFileName())
        else:
            self.assertFalse(self.cmEngine.getOCIOConfigFileName())

if __name__ == '__main__':
    unittest.main()
