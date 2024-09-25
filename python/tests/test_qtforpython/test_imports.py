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

import importlib
import platform
import unittest

def isDesignerSDK():
    import sd
    ctx = sd.getContext()
    app = ctx.getSDApplication()
    return app.getUIMgr() == None

class TestQtForPython(unittest.TestCase):

    @unittest.skipIf(isDesignerSDK(), "Test requires Designer")
    def test_import(self):
        """
        Test that PySide modules load correctly
        """
        components = [
            'Charts',
            'Concurrent',
            'Core',
            #'Core5Compat', # Not available in PySide6
            'Gui',
            'Multimedia',
            'MultimediaWidgets',
            'Network',
            'OpenGL',
            'OpenGLWidgets',
            'PrintSupport',
            'Qml',
            'Quick',
            'QuickWidgets',
            'Sql',
            'Svg',
            'SvgWidgets',
            'UiTools',
            'WebSockets',
            'Widgets',
            'Xml'
        ]

        for component_name in components:
            with self.subTest(component_name=component_name):
                module_name = f"PySide6.Qt{component_name}"
                try:
                    module = importlib.import_module(module_name)
                except Exception as e:
                    self.fail(f'Import of {module_name} failed with exception "{e}".')

if __name__ == '__main__':
    unittest.main()
