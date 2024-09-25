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
from sd.api.mdl.sdmdlgraph import *
from sd.api.sdvaluecolorrgb import *
from sd.api.sdvaluefloat import *
from sd.api.sdvaluestring import *
from sd.api.sdcolorspace import *
from sd.api.sdvalueint import *
from sd.api.sdvaluebool import *


def main(aSDContext):
    """
    This sample show how to create the "Metallic" MDL material as defined by the template "Metallic" of Substance 3D Designer

    :param aSDContext: The SDContext
    :return: None
    """
    cGridSize = GraphGrid.sGetFirstLevelSize()
    colSize = 2*cGridSize
    rowSize = 2*cGridSize
    sbsPackageName = os.path.split(__file__)[1].split('.')[0] # Get the package name from the current python file base name

    # Create a new Package
    sdPackageMgr = aSDContext.getSDApplication().getPackageMgr()
    sdPackage = sdPackageMgr.newUserPackage()

    # Create a new MDL Graph in this package
    sdMDLGraph = SDMDLGraph.sNew(sdPackage)
    sdMDLGraph.setIdentifier(sbsPackageName)

    # Get the output Node that has been created automatically when the graph has been created
    sdMDLNodeMaterial = sdMDLGraph.getOutputNodes()[0]
    sdMDLNodeMaterial.setPosition(float2(-colSize, 0))

    # Create 'material_surface' node
    sdMDLNodeMaterialSurface = sdMDLGraph.newNode('mdl::material_surface(bsdf,material_emission)')
    sdMDLNodeMaterialSurface.setPosition(float2(-2*colSize, 0))
    sdMDLNodeMaterialSurface.newPropertyConnectionFromId('output', sdMDLNodeMaterial, 'surface')

    # Create 'microfacet_ggx_smith_bsdf' node
    sdMDLNodeMicrofacetGGX = sdMDLGraph.newNode('mdl::df::microfacet_ggx_smith_bsdf(float,float,color,float3,::df::scatter_mode,string)')
    sdMDLNodeMicrofacetGGX.setPosition(float2(-3 * colSize, 0))
    sdMDLNodeMicrofacetGGX.newPropertyConnectionFromId('output', sdMDLNodeMaterialSurface, 'scattering')

    # Create constant 'color' node
    sdMDLNodeConstantColor = sdMDLGraph.newNode('mdl::color')
    sdMDLNodeConstantColor.setPosition(float2(-4 * colSize, rowSize))
    #   - Set the color as a linear value (MDL works in linear)
    sdMDLNodeConstantColor.setInputPropertyValueFromId(
        'color',
        SDValueColorRGB.sNew(SDColorSpace.sConvertColorRGB(ColorRGB(0.5, 0.5, 0.5), 'sRGB', 'Linear')))
    sdMDLNodeConstantColor.setExposed(True)
    sdMDLNodeConstantColor.setAnnotationPropertyValueFromId('identifier', SDValueString.sNew('basecolor'))
    sdMDLNodeConstantColor.setAnnotationPropertyValueFromId('description', SDValueString.sNew('The Base Color of the material'))
    sdMDLNodeConstantColor.setAnnotationPropertyValueFromId('in_group', SDValueString.sNew('Base Color'))
    sdMDLNodeConstantColor.setAnnotationPropertyValueFromId('display_name', SDValueString.sNew('Base Color'))
    sdMDLNodeConstantColor.setAnnotationPropertyValueFromId('gamma_type', SDValueInt.sNew(SDGammaType.SRGB.value))
    sdMDLNodeConstantColor.setAnnotationPropertyValueFromId('visible_by_default', SDValueBool.sNew(True))
    sdMDLNodeConstantColor.setAnnotationPropertyValueFromId('type_modifier', SDValueInt.sNew(SDTypeModifier.Uniform.value))
    sdMDLNodeConstantColor.setAnnotationPropertyValueFromId('sampler_usage', SDValueString.sNew('baseColor'))
    sdMDLNodeConstantColor.newPropertyConnectionFromId('output', sdMDLNodeMicrofacetGGX, 'tint')

    # Create constant 'operator*' node
    sdMDLNodeMultFloat = sdMDLGraph.newNode('mdl::operator*(float,float)')
    sdMDLNodeMultFloat.setPosition(float2(-4 * colSize, -rowSize))
    sdMDLNodeMultFloat.newPropertyConnectionFromId('output', sdMDLNodeMicrofacetGGX, 'roughness_u')
    sdMDLNodeMultFloat.newPropertyConnectionFromId('output', sdMDLNodeMicrofacetGGX, 'roughness_v')

    # Create float constant node
    sdMDLNodeConstantRoughness = sdMDLGraph.newNode('mdl::float')
    sdMDLNodeConstantRoughness.setPosition(float2(-5 * colSize, -rowSize))
    sdMDLNodeConstantRoughness.setInputPropertyValueFromId('float', SDValueFloat.sNew(0.5))
    sdMDLNodeConstantRoughness.setExposed(True)
    sdMDLNodeConstantRoughness.setAnnotationPropertyValueFromId('identifier', SDValueString.sNew('roughness'))
    sdMDLNodeConstantRoughness.setAnnotationPropertyValueFromId('display_name', SDValueString.sNew('Roughness'))
    sdMDLNodeConstantRoughness.setAnnotationPropertyValueFromId('description', SDValueString.sNew('The Roughness of the material'))
    sdMDLNodeConstantRoughness.setAnnotationPropertyValueFromId('in_group', SDValueString.sNew('Roughness'))
    sdMDLNodeConstantRoughness.setAnnotationPropertyValueFromId('gamma_type', SDValueInt.sNew(SDGammaType.Linear.value))
    sdMDLNodeConstantRoughness.setAnnotationPropertyValueFromId('visible_by_default', SDValueBool.sNew(True))
    sdMDLNodeConstantRoughness.setAnnotationPropertyValueFromId('type_modifier', SDValueInt.sNew(SDTypeModifier.Auto.value))
    sdMDLNodeConstantRoughness.setAnnotationPropertyValueFromId('sampler_usage', SDValueString.sNew('roughness'))
    # TODO: Setup the Hard Range to [0; 1]
    sdMDLNodeConstantRoughness.newPropertyConnectionFromId('output', sdMDLNodeMultFloat, 'x')
    sdMDLNodeConstantRoughness.newPropertyConnectionFromId('output', sdMDLNodeMultFloat, 'y')

    # Geometry Part
    sdMDLNodeMaterialGeometry = sdMDLGraph.newNode('mdl::material_geometry(float3,float,float3)')
    sdMDLNodeMaterialGeometry.setPosition(float2(-2*colSize, 2*rowSize))
    sdMDLNodeMaterialGeometry.newPropertyConnectionFromId('output', sdMDLNodeMaterial, 'geometry')

    sdMDLNodeConstantNormal = sdMDLGraph.newNode('mdl::float3')
    sdMDLNodeConstantNormal.setPosition(float2(-3*colSize, 2 * rowSize))
    sdMDLNodeConstantNormal.setExposed(True)
    sdMDLNodeConstantNormal.setAnnotationPropertyValueFromId('identifier', SDValueString.sNew('normal'))
    sdMDLNodeConstantNormal.setAnnotationPropertyValueFromId('display_name', SDValueString.sNew('Normal'))
    sdMDLNodeConstantNormal.setAnnotationPropertyValueFromId('in_group', SDValueString.sNew('Normal'))
    sdMDLNodeConstantNormal.setAnnotationPropertyValueFromId('gamma_type', SDValueInt.sNew(SDGammaType.Linear.value))
    sdMDLNodeConstantNormal.setAnnotationPropertyValueFromId('visible_by_default', SDValueBool.sNew(True))
    sdMDLNodeConstantNormal.setAnnotationPropertyValueFromId('type_modifier', SDValueInt.sNew(SDTypeModifier.Auto.value))
    sdMDLNodeConstantNormal.setAnnotationPropertyValueFromId('sampler_usage', SDValueString.sNew('normal'))
    sdMDLNodeConstantNormal.newPropertyConnectionFromId('output', sdMDLNodeMaterialGeometry, 'normal')

    # Create 'normal' function node
    sdMDLNodeNormal = sdMDLGraph.newNode('mdl::state::normal()')
    sdMDLNodeNormal.setPosition(float2(-4 * colSize, 2 * rowSize))
    sdMDLNodeNormal.newPropertyConnectionFromId('output', sdMDLNodeConstantNormal, 'normal')

    # Save the new package on disk
    dstFileAbsPath = os.path.join(io.getUserDocumentOutputDir(__file__), sbsPackageName+'.sbs')
    sdPackageMgr.savePackageAs(sdPackage, dstFileAbsPath)
    print('Save output file to ' + dstFileAbsPath)


if __name__ == '__main__':
    main(sd.getContext())
