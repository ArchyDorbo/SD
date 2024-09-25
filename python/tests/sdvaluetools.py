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

from sd.api.sdvaluebool import *
from sd.api.sdvaluebool2 import *
from sd.api.sdvaluebool3 import *
from sd.api.sdvaluebool4 import *
from sd.api.sdvalueint import *
from sd.api.sdvalueint2 import *
from sd.api.sdvalueint3 import *
from sd.api.sdvalueint4 import *
from sd.api.sdvaluefloat import *
from sd.api.sdvaluefloat2 import *
from sd.api.sdvaluefloat3 import *
from sd.api.sdvaluefloat4 import *
from sd.api.sdvaluedouble import *
from sd.api.sdvaluedouble2 import *
from sd.api.sdvaluedouble3 import *
from sd.api.sdvaluedouble4 import *
from sd.api.sdvaluestring import *
from sd.api.sdvaluecolorrgb import *
from sd.api.sdvaluecolorrgba import *
from sd.api.sdvaluetexture import *
from sd.api.sdvaluearray import *
from sd.api.sdvaluestruct import *
from sd.api.sdvaluematrix import *
from sd.api.sdvalueenum import *
from sd.api.sdvalueusage import *
from sd.api.mdl.sdmdlvalue import *


def assertSDValueEqual(aTestInstance, aSDValue0, aSDValue1):
    if (isinstance(aSDValue0, SDValueInt) and isinstance(aSDValue1, SDValueEnum)) or (isinstance(aSDValue1, SDValueInt) and isinstance(aSDValue0, SDValueEnum)):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertEqual(aSDValue1BaseValue, aSDValue0BaseValue, 'The value has not been set properly')
        return

    aTestInstance.assertEqual(type(aSDValue0), type(aSDValue1))

    if isinstance(aSDValue0, SDValueBool) or isinstance(aSDValue0, SDValueInt) or isinstance(aSDValue0, SDValueString):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertEqual(aSDValue1BaseValue, aSDValue0BaseValue, 'The value has not been set properly')
    elif isinstance(aSDValue0, SDValueBool2) or isinstance(aSDValue0, SDValueInt2):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertEqual(aSDValue1BaseValue.x, aSDValue0BaseValue.x, 'The value has not been set properly')
        aTestInstance.assertEqual(aSDValue1BaseValue.y, aSDValue0BaseValue.y, 'The value has not been set properly')
    elif isinstance(aSDValue0, SDValueBool3) or isinstance(aSDValue0, SDValueInt3):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertEqual(aSDValue1BaseValue.x, aSDValue0BaseValue.x, 'The value has not been set properly')
        aTestInstance.assertEqual(aSDValue1BaseValue.y, aSDValue0BaseValue.y, 'The value has not been set properly')
        aTestInstance.assertEqual(aSDValue1BaseValue.z, aSDValue0BaseValue.z, 'The value has not been set properly')
    elif isinstance(aSDValue0, SDValueBool4) or isinstance(aSDValue0, SDValueInt4):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertEqual(aSDValue1BaseValue.x, aSDValue0BaseValue.x, 'The value has not been set properly')
        aTestInstance.assertEqual(aSDValue1BaseValue.y, aSDValue0BaseValue.y, 'The value has not been set properly')
        aTestInstance.assertEqual(aSDValue1BaseValue.z, aSDValue0BaseValue.z, 'The value has not been set properly')
        aTestInstance.assertEqual(aSDValue1BaseValue.w, aSDValue0BaseValue.w, 'The value has not been set properly')

    elif isinstance(aSDValue0, SDValueFloat) or isinstance(aSDValue0, SDValueDouble):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue, aSDValue0BaseValue, 7, 'The value has not been set properly')
    elif isinstance(aSDValue0, SDValueFloat2) or isinstance(aSDValue0, SDValueDouble2):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.x, aSDValue0BaseValue.x, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.y, aSDValue0BaseValue.y, 7, 'The value has not been set properly')
    elif isinstance(aSDValue0, SDValueFloat3) or isinstance(aSDValue0, SDValueDouble3):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.x, aSDValue0BaseValue.x, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.y, aSDValue0BaseValue.y, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.z, aSDValue0BaseValue.z, 7, 'The value has not been set properly')
    elif isinstance(aSDValue0, SDValueFloat4) or isinstance(aSDValue0, SDValueDouble4):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.x, aSDValue0BaseValue.x, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.y, aSDValue0BaseValue.y, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.z, aSDValue0BaseValue.z, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.w, aSDValue0BaseValue.w, 7, 'The value has not been set properly')

    elif isinstance(aSDValue0, SDValueColorRGB):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.r, aSDValue0BaseValue.r, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.g, aSDValue0BaseValue.g, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.b, aSDValue0BaseValue.b, 7, 'The value has not been set properly')

    elif isinstance(aSDValue0, SDValueColorRGBA):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.r, aSDValue0BaseValue.r, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.g, aSDValue0BaseValue.g, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.b, aSDValue0BaseValue.b, 7, 'The value has not been set properly')
        aTestInstance.assertAlmostEqual(aSDValue1BaseValue.a, aSDValue0BaseValue.a, 7, 'The value has not been set properly')

    elif isinstance(aSDValue0, SDValueArray):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()

        aTestInstance.assertEqual(len(aSDValue0BaseValue), aSDValue0.getSize(), 'The value has not been set properly')
        v = aSDValue0.get()
        aTestInstance.assertEqual(len(aSDValue0BaseValue), len(v), 'The value has not been set properly')

    elif isinstance(aSDValue0, SDValueTexture):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertTrue(aSDValue0BaseValue, 'The texture is invalid')
        aTestInstance.assertTrue(aSDValue1BaseValue, 'The texture is invalid')
        texture0Size = aSDValue0BaseValue.getSize()
        texture1Size = aSDValue1BaseValue.getSize()
        aTestInstance.assertEqual(texture0Size.x, texture1Size.x, 'The Size X is different')
        aTestInstance.assertEqual(texture0Size.y, texture1Size.y, 'The Size Y is different')

        # Don't test the pixel format because, the color management system may have change,
        # the SDK may have change the pixel format in between
        # texture0PixelFormat = aSDValue0BaseValue.getPixelFormat()
        # texture1PixelFormat = aSDValue1BaseValue.getPixelFormat()
        # aTestInstance.assertEqual(texture0PixelFormat, texture1PixelFormat, 'The Pixel format is different')

    elif isinstance(aSDValue0, SDValueEnum):
        aSDValue0BaseValue = aSDValue1.get()
        aSDValue1BaseValue = aSDValue0.get()
        aTestInstance.assertEqual(aSDValue0BaseValue, aSDValue1BaseValue, 'The enum int value is different')

        aSDValue0ValueId = aSDValue1.getValueId()
        aSDValue1ValueId = aSDValue0.getValueId()
        aTestInstance.assertEqual(aSDValue0ValueId, aSDValue1ValueId, 'The enum identifier value is different')

    elif isinstance(aSDValue0, SDValueMatrix):
        # Compare value
        aSDValue0ColCount = aSDValue0.getColumnCount()
        aSDValue0RowCount = aSDValue0.getRowCount()
        aSDValue1ColCount = aSDValue1.getColumnCount()
        aSDValue1RowCount = aSDValue1.getRowCount()
        aTestInstance.assertEqual(aSDValue0RowCount, aSDValue1RowCount, 'The matrix row count is different')
        aTestInstance.assertEqual(aSDValue0ColCount, aSDValue1ColCount, 'The matrix column count is different')

        for c in range(aSDValue0ColCount):
            for r in range(aSDValue0RowCount):
                aSDValue0Item = aSDValue0.getItem(c, r)
                aTestInstance.assertTrue(aSDValue0Item, 'The value has not been set properly')
                aSDValue1Item = aSDValue1.getItem(c, r)
                aTestInstance.assertTrue(aSDValue1Item, 'The value has not been set properly')
                assertSDValueEqual(aTestInstance, aSDValue0Item, aSDValue1Item)

    elif isinstance(aSDValue0, SDValueStruct):
        aSDValue0Type = aSDValue0.getType()
        aSDValue1Type = aSDValue1.getType()
        aTestInstance.assertTrue(aSDValue0Type)
        aTestInstance.assertTrue(aSDValue1Type)
        aTestInstance.assertEqual(aSDValue0Type.getId(), aSDValue1Type.getId())

        aSDValue0Properties = aSDValue0Type.getMembers()
        aSDValue1Properties = aSDValue1Type.getMembers()
        aTestInstance.assertEqual(len(aSDValue0Properties), len(aSDValue1Properties))
        for sdProperty0 in aSDValue0Properties:
            aSDValue0ItemValue = aSDValue0.getPropertyValue(sdProperty0)
            aSDValue1ItemValue = aSDValue1.getPropertyValue(sdProperty0)
            assertSDValueEqual(aTestInstance, aSDValue0ItemValue, aSDValue1ItemValue)

    elif isinstance(aSDValue0, SDMDLValue):
        # TODO
        return
    else:
        raise Exception('Unable to compare the two SDValues')
