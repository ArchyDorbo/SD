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
from sd.api import sdproperty, sdgraph, sdresource, sdvalue, sdtypestruct, sdtypeenum, sdusage, sdnode, sdtypematrix
from sd.api.sdproperty import *
from sd.api import sdvaluearray
from sd.api.mdl import sdmdltypetexturereference
from sd.api.sdvalueserializer import SDValueSerializer
from sd.api.sddefinition import *
from sd.api.sdtypestruct import *
from sd.api.sdtypearray import *
from tests.tools import *

class _Logger:
    def __init__(self):
        self.mDepth = 0
        self.mLines = []
    def incDepth(self):
        self.mDepth = self.mDepth + 1
    def decDepth(self):
        self.mDepth = self.mDepth - 1
    def getLines(self):
        return self.mLines
    def log(self, aStr):
        self.write('\t' * self.mDepth + aStr)
    def write(self, aStr):
        self.mLines.append(aStr)

def fixDescription(aText):
    return aText.replace('\n', ' ')

class DataSerializer:
    def __init__(self):
        self.mLogger = _Logger()
        self.mIsCalling_serializeSDProperty = False
        # self.mLogTypes = True
        self.mLogTypes = False
        self.mTypes = {}

    def __addSDType(self, aSDType):
        if not self.mLogTypes:
            return
        sdTypeKey = '%s(\'%s\')' % (type(aSDType).__name__, aSDType.getId())
        if sdTypeKey in self.mTypes:
            return
        self.mTypes[sdTypeKey] = aSDType

        if issubclass(type(aSDType), sdtypestruct.SDTypeStruct):
            for sdTypeProperty in aSDType.getMembers():
                self.__addSDType(sdTypeProperty.getType())

    def __getSDTypeDesc(self, aSDType):

        typeName = aSDType.getId()
        if isinstance(aSDType, SDDefinition):
            sdTypeModifierStr = ''
        else:
            sdTypeModifier = aSDType.getModifier()
            if sdTypeModifier != SDTypeModifier.Auto:
                sdTypeModifierStr = ' [%s]' % sdTypeModifier.name
            else:
                sdTypeModifierStr = ''

        return '\'%s\' (%s)%s' % (typeName, type(aSDType).__name__, sdTypeModifierStr)

    def __serializeProperty(self, aSDProperty):
        sdPropertyId = aSDProperty.getId()
        sdPropertyType = aSDProperty.getType()
        sdPropertyTypeName = ''
        if sdPropertyType:
            sdPropertyTypeName = sdPropertyType.getId()

        line = '%s %s' % (sdPropertyTypeName, sdPropertyId)
        defaultValue = aSDProperty.getDefaultValue()
        if defaultValue:
            line += ' = ' + SDValueSerializer.sToString(defaultValue)
        self.mLogger.log(line)

        self.mLogger.incDepth()
        sdPropertyLabel = aSDProperty.getLabel()
        if sdPropertyLabel:
            self.mLogger.log('Label: \'%s\'' % sdPropertyLabel)
        sdPropertyDescription = aSDProperty.getLabel()
        if sdPropertyDescription:
            self.mLogger.log('Description: \'%s\'' % sdPropertyDescription)
        self.mLogger.decDepth()


    def __serializePropertyArray(self, aSDPropertyArray, aLabel):
        # self.mLogger.log('%s (%d):' % (aLabel, len(aSDPropertyArray)))
        # self.mLogger.incDepth()
        for sdProperty in aSDPropertyArray:
            self.__serializeProperty(sdProperty)
        # self.mLogger.decDepth()

    def __serializeSDType(self, aSDType):
        self.mLogger.log(self.__getSDTypeDesc(aSDType))
        self.mLogger.incDepth()
        if issubclass(type(aSDType), sdtypeenum.SDTypeEnum):
            self.__serializePropertyArray(aSDType.getEnumerators(), 'Enumerators')
        elif issubclass(type(aSDType), sdtypestruct.SDTypeStruct):
            self.__serializePropertyArray(aSDType.getMembers(), 'Properties')
        elif issubclass(type(aSDType), SDTypeArray):
            self.mLogger.log('Item Type:')
            self.mLogger.incDepth()
            self.__serializeSDType(aSDType.getItemType())
            self.mLogger.decDepth()
        elif issubclass(type(aSDType), sdtypematrix.SDTypeMatrix):
            self.mLogger.log('Item Type: %s' % self.__getSDTypeDesc(aSDType.getItemType()))
            self.mLogger.log('Columns: %d' % aSDType.getColumnCount())
            self.mLogger.log('Rows : %d' % aSDType.getRowCount())
        elif issubclass(type(aSDType), sdmdltypetexturereference.SDMDLTypeTextureReference):
            self.mLogger.log('TextureShape: %s' % str(aSDType.getTextureShape()))
        self.mLogger.decDepth()


    def __serializeTypes(self):
        sdTypeKeys = sorted(self.mTypes.keys())
        for sdTypeKey in sdTypeKeys:
            self.__serializeSDType(self.mTypes[sdTypeKey])

    def serializeSDPackage(self, aSDPackage):
        # Serialize Dependencies
        pkgDeps = aSDPackage.getDependencies()
        if pkgDeps:
            self.mLogger.log('Dependencies')
            self.mLogger.incDepth()
            pkgDepIndex = -1
            for pkgDep in pkgDeps:
                pkgDepIndex += 1
                self.mLogger.log('Dependency[%d]' % pkgDepIndex)
                self.mLogger.incDepth()
                self.mLogger.log('FilePath: %s' % pkgDep.getFilePath())
                if pkgDep.getPackage():
                    self.mLogger.log('Package: DEFINED')
                self.mLogger.decDepth()
            self.mLogger.decDepth()


        # Serialize Metadata
        sbsPackageMetadata = aSDPackage.getMetadataDict()
        sbsMetadatas = sbsPackageMetadata.getProperties()
        self.serializeSDPropertyArray(sbsPackageMetadata, sbsMetadatas, "Package Metadata")

        # Serialize Resources
        sdResourceArray = aSDPackage.getChildrenResources(True)
        resourceIndex = -1
        for sdResource in sdResourceArray:
            resourceIndex = resourceIndex + 1
            self.mLogger.log('Resource[%d]' % resourceIndex)
            self.mLogger.incDepth()
            self.serializeSDResource(sdResource)
            self.mLogger.decDepth()

        # Log Types
        if self.mTypes:
            self.mLogger.log('==================================================================')
            self.mLogger.log('Types')
            self.mLogger.log('==================================================================')
            self.mLogger.incDepth()
            self.__serializeTypes()
            self.mLogger.decDepth()

        return self.mLogger.getLines()

    def serializeSDConnectionArray(self, aSDConnectionArray):
        if not aSDConnectionArray:
            return
        self.mLogger.log('Connections:')
        self.mLogger.incDepth()
        index = -1
        for sdConnection in aSDConnectionArray:
            index = index+1
            connectionInputProperty = sdConnection.getInputProperty()
            connectionInputPropertyNode = sdConnection.getInputPropertyNode()

            connectionInputPropertyNodeDefinition = connectionInputPropertyNode.getDefinition()
            connectionInputPropertyNodeDefinitionStr = ''
            if connectionInputPropertyNodeDefinition:
                connectionInputPropertyNodeDefinitionStr = connectionInputPropertyNodeDefinition.getId()
            self.mLogger.log('[%d] : inputPropertyNode=\'%s\'   inputProperty=\'%s\'' %
                             (index, connectionInputPropertyNodeDefinitionStr, connectionInputProperty.getId()))

        self.mLogger.decDepth()

    def serializeSDType(self, aSDType, aLabel, aPropertySDValue = None, aRecursive = False):
        if not aSDType:
            return

        if aLabel:
            self.mLogger.log('%s: %s' % (aLabel, self.__getSDTypeDesc(aSDType)))

    def serializeSDDefinition(self, aSDDefinition, aLabel, aPropertySDValue = None, aRecursive = False):
        if not aSDDefinition:
            return

        if aLabel:
            self.mLogger.log('%s: %s' % (aLabel, aSDDefinition.getId()))

    def serializeSDProperty(self, aSDObject, aSDProperty, aParentProperty = None):
        propertyValueStr = ''
        propertySDValue = None
        if aParentProperty:
            propertySDValue = aSDObject.getPropertyAnnotationValueFromId(aParentProperty, aSDProperty.getId())
        else:
            if not aSDProperty.isFunctionOnly():
                propertySDValue = aSDObject.getPropertyValue(aSDProperty)
        if propertySDValue:
            propertyValueStr = '\'%s\'' % SDValueSerializer.sToString(propertySDValue)
            propertyValueStr = toPlatformIndenpendantAPIRelativePath(propertyValueStr)

        tags = []
        if aSDProperty.isConnectable():
            tags.append('Connectable')
        if aSDProperty.isReadOnly():
            tags.append('ReadOnly')
        if aSDProperty.isVariadic():
            tags.append('Variadic')
        if aSDProperty.isPrimary():
            tags.append('Primary')
        if aSDProperty.isFunctionOnly():
            tags.append('FunctionOnly')

        tagsStr = ''
        for t in tags:
            if tagsStr:
                tagsStr += ', '
            tagsStr += t
        if tagsStr:
            tagsStr = ' (%s)' % tagsStr

        if propertyValueStr != '':
            self.mLogger.log('\'%s\'%s = %s' % (aSDProperty.getId(), tagsStr, propertyValueStr))
        else:
            self.mLogger.log('\'%s\'%s =' % (aSDProperty.getId(), tagsStr))

        self.mLogger.incDepth()

        sdTypes = aSDProperty.getTypes()
        if sdTypes:
            for propertyType in sdTypes:
                if propertyType:
                    self.__addSDType(propertyType)
                    self.serializeSDType(propertyType, 'Property Type')

        if propertySDValue:
            propertyValueType = propertySDValue.getType()
            if propertyValueType:
                self.__addSDType(propertyValueType)
                self.serializeSDType(
                    aSDType = propertyValueType,
                    aLabel = 'Value Type',
                    aPropertySDValue = propertySDValue,
                    aRecursive = True)

        if propertySDValue:
            if issubclass(type(propertySDValue), sdvaluearray.SDValueArray):
                sdArrayOfSDValue = propertySDValue.get()
                self.mLogger.log('Array Values:')
                self.mLogger.incDepth()
                index = -1
                for itemValue in sdArrayOfSDValue:
                    index = index + 1
                    itemValueStr = SDValueSerializer.sToString(itemValue)
                    self.mLogger.log('[%d] \'%s\'' % (index, itemValueStr))
                self.mLogger.decDepth()

        # Dump wether the Label is defined:
        label = aSDProperty.getLabel()
        if label:
            self.mLogger.log('Has label')

        # Property Annotations
        if issubclass(type(aSDObject), sdresource.SDResource):
            # reentrance check
            if not self.mIsCalling_serializeSDProperty:
                self.mIsCalling_serializeSDProperty = True

                sdPropertyAnnotations = aSDObject.getPropertyAnnotations(aSDProperty)
                if sdPropertyAnnotations:
                    self.mLogger.log('Property Annotations:')
                    self.mLogger.incDepth()

                    for sdProperty in sdPropertyAnnotations:
                        self.serializeSDProperty(aSDObject, sdProperty, aSDProperty)
                    self.mLogger.decDepth()

                #input/output metadata:
                propertyMetadata = aSDObject.getPropertyMetadataDictFromId(aSDProperty.getId(), aSDProperty.getCategory())
                if propertyMetadata:
                    self.mLogger.incDepth()
                    sbsMetadatas = propertyMetadata.getProperties()
                    self.serializeSDPropertyArray(propertyMetadata, sbsMetadatas, "Property Metadata")
                    self.mLogger.decDepth()

                self.mIsCalling_serializeSDProperty = False

        # Property Graph
        if issubclass(type(aSDObject), sdnode.SDNode):
            sdGraph = aSDObject.getPropertyGraph(aSDProperty)
            if sdGraph:
                sdResourceUrl = sdGraph.getUrl()
                self.mLogger.log('Graph = %s (%s)' % (str(type(sdGraph)), sdResourceUrl))
                sdResourceIdentifier = sdGraph.getIdentifier()

                if not sdResourceIdentifier:
                    self.mLogger.incDepth()
                    self.serializeSDResource(sdGraph)
                    self.mLogger.decDepth()

            # Property Connections
            self.serializeSDConnectionArray(aSDObject.getPropertyConnections(aSDProperty))


        self.mLogger.decDepth()

    def serializeSDPropertyArray(self, aSDObject, aSDPropertyArray, aCategoryLabel = ''):
        if not aSDPropertyArray:
            return
        self.mLogger.log('Category = %s' % aCategoryLabel)
        self.mLogger.incDepth()
        for sdProperty in aSDPropertyArray:
            self.serializeSDProperty(aSDObject, sdProperty)
        self.mLogger.decDepth()

    def serializeSDProperties(self, aSDObject, aSDPropertyCategory):
        sdPropertyArray = aSDObject.getProperties(aSDPropertyCategory)
        self.serializeSDPropertyArray(aSDObject, sdPropertyArray, aSDPropertyCategory.name)

    def serializeSDNode(self, aSDNode):
        nodeDefinition = aSDNode.getDefinition()
        self.serializeSDType(nodeDefinition, 'Node Type')

        self.mLogger.log('Identifier = \'%s\'' % aSDNode.getIdentifier())

        sdPosition = aSDNode.getPosition()
        self.mLogger.log('Position = (%f, %f)' % (sdPosition.x, sdPosition.y))

        sdRefResource = aSDNode.getReferencedResource()
        if sdRefResource:
            sdRefGraphResourceUrl = sdRefResource.getUrl()
            sdRefGraphResourceIdentifier = sdRefResource.getIdentifier()
            self.mLogger.log('Ref Resource = %s (%s)' % (str(type(sdRefResource)), sdRefGraphResourceUrl))
            if not sdRefGraphResourceIdentifier:
                self.mLogger.incDepth()
                self.serializeSDResource(sdRefResource)
                self.mLogger.decDepth()

        self.serializeAllSDProperties(aSDNode)

    def serializeSDNodeArray(self, aSDNodeArray):
        self.mLogger.incDepth()

        nodeIndex = -1
        for sdNode in aSDNodeArray:
            nodeIndex = nodeIndex + 1
            self.mLogger.log('Node[%d]:' % nodeIndex)
            self.mLogger.incDepth()
            self.serializeSDNode(sdNode)
            self.mLogger.decDepth()
        self.mLogger.decDepth()

    def serializeSDResource(self, aSDResource):
        if not aSDResource:
            return

        if aSDResource.getUrl():
            self.serializeSDType(aSDResource.getType(), 'Resource Type')
            self.mLogger.log('Resource Url = \'%s\'' % aSDResource.getUrl())
            self.mLogger.log('Resource Identifier = \'%s\'' % aSDResource.getIdentifier())

            absFilePath = aSDResource.getFilePath()
            self.mLogger.log('Resource File Path = \'%s\'' % toPlatformIndenpendantAPIRelativePath(absFilePath))
            self.mLogger.log('Resource Embed Method = \'%s\'' % aSDResource.getEmbedMethod().name)

        self.serializeAllSDProperties(aSDResource)

        resourceMetadata = aSDResource.getMetadataDict()
        if resourceMetadata:
            sbsMetadatas = resourceMetadata.getProperties()
            self.serializeSDPropertyArray(resourceMetadata, sbsMetadatas, "Resource Metadata")

        # Check if the resource is a SDGraph
        if issubclass(type(aSDResource), sdgraph.SDGraph):
            # Dump nodes
            self.mLogger.log('Nodes:')
            self.serializeSDNodeArray(aSDResource.getNodes())

            # Dump output nodes
            self.mLogger.log('Output Nodes:')
            self.serializeSDNodeArray(aSDResource.getOutputNodes())


    def serializeAllSDProperties(self, aSDResourceOrSDNode):
        self.mLogger.log('Properties:')
        self.mLogger.incDepth()
        self.serializeSDProperties(aSDResourceOrSDNode, SDPropertyCategory.Annotation)
        self.serializeSDProperties(aSDResourceOrSDNode, SDPropertyCategory.Input)
        self.serializeSDProperties(aSDResourceOrSDNode, SDPropertyCategory.Output)
        self.mLogger.decDepth()


    def serializeSDPropertyDefinition(self, aSDProperty):
        defaultValue = aSDProperty.getDefaultValue()
        defaultValueStr = ''
        if defaultValue:
            defaultValueStr = SDValueSerializer.sToString(defaultValue)

        flags = []
        if aSDProperty.isConnectable():
            flags.append('CONNECTABLE')
        if aSDProperty.isReadOnly():
            flags.append('READ_ONLY')
        if aSDProperty.isVariadic():
            flags.append('VARIADIC')
        if aSDProperty.isPrimary():
            flags.append('PRIMARY')
        if aSDProperty.isFunctionOnly():
            flags.append('FUNCTION_ONLY')
        if flags:
            flagsStr = '[%s]' % ', '.join(flags)
        else:
            flagsStr = ''

        if defaultValue:
            msg = '\'%s\' = %s %s' % (aSDProperty.getId(), defaultValueStr, flagsStr)
        else:
            msg = '\'%s\' %s' % (aSDProperty.getId(), flagsStr)
        self.mLogger.log(msg)
        self.mLogger.incDepth()

        label = aSDProperty.getLabel()
        if label:
            self.mLogger.log('Label: \'%s\'' % aSDProperty.getLabel())

        description = aSDProperty.getDescription()
        if description:
            self.mLogger.log('Description: \'%s\'' % fixDescription(aSDProperty.getDescription()))

        self.mLogger.log('Types:')
        self.mLogger.incDepth()
        for sdType in aSDProperty.getTypes():
            # self.__serializeSDType(sdType)
            self.mLogger.log(self.__getSDTypeDesc(sdType))

        self.mLogger.decDepth()
        self.mLogger.decDepth()


    def serializeSDPropertyDefinitionArray(self, aFunctionDefinition, aSDPropertyCategory):
        sdProperties = aFunctionDefinition.getProperties(aSDPropertyCategory)
        if not sdProperties:
            return
        self.mLogger.log('SDPropertyCategory = \'%s\'' % aSDPropertyCategory.name)
        self.mLogger.incDepth()
        for sdProperty in sdProperties:
            self.serializeSDPropertyDefinition(sdProperty)
        self.mLogger.log('')
        self.mLogger.decDepth()


    def serializeSDDefinition(self, aSDDefinition):
        label = aSDDefinition.getLabel()
        if label:
            self.mLogger.log('Label: \'%s\'' % label)

        description = aSDDefinition.getDescription()
        if description:
            self.mLogger.log('Description: \'%s\'' % fixDescription(description))

        # self.mLogger.log('Properties:')
        # self.mLogger.incDepth()
        self.serializeSDPropertyDefinitionArray(aSDDefinition, SDPropertyCategory.Input)
        self.serializeSDPropertyDefinitionArray(aSDDefinition, SDPropertyCategory.Output)
        self.serializeSDPropertyDefinitionArray(aSDDefinition, SDPropertyCategory.Annotation)
        # self.mLogger.decDepth()

    def serializeSDModuleDefinitions(self, aSDModule):
        definitions = aSDModule.getDefinitions()
        if not definitions:
            return
        count = len(definitions)
        index = 0
        self.mLogger.log('Definitions:')
        self.mLogger.incDepth()
        for definition in definitions:
            index += 1
            self.mLogger.log('[%d/%d] \'%s\'' % (index, count, definition.getId()))
            self.mLogger.incDepth()
            self.serializeSDDefinition(definition)
            self.mLogger.decDepth()
        self.mLogger.decDepth()

    def serializeSDModuleTypes(self, aSDModule):
        sdTypes = aSDModule.getTypes()
        if not sdTypes:
            return
        count = len(sdTypes)
        index = 0
        self.mLogger.log('Types:')
        self.mLogger.incDepth()
        for sdType in sdTypes:
            index += 1
            self.mLogger.log('[%d/%d] \'%s\'' % (index, count, sdType.getId()))
            self.mLogger.incDepth()
            self.__serializeSDType(sdType)
            self.mLogger.decDepth()
        self.mLogger.decDepth()

    def serializeSDModule(self, aSDModule):
        self.serializeSDModuleDefinitions(aSDModule)
        self.serializeSDModuleTypes(aSDModule)


    def serializeSDModules(self, aSDModuleMgr):
        sdModules = aSDModuleMgr.getModules()
        count = len(sdModules)
        index = -1
        for sdModule in sdModules:
            index += 1
            self.mLogger.log('[%d/%d] \'%s\' (%s)' % (index, count, sdModule.getId(), type(sdModule).__name__))
            self.mLogger.incDepth()
            self.serializeSDModule(sdModule)
            self.mLogger.decDepth()

        return self.mLogger.getLines()
