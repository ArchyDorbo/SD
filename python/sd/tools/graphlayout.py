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

from sd.ui import graphgrid
from sd.api import SDArray, SDNode
from sd.api.sdbasetypes import float2

from typing import Optional


class AlignmentDirection:
    Horizontal = 0
    Vertical = 1


def alignSDNodes(
        aSDNodes: Optional[SDArray[SDNode]],
        aAlignDirection=AlignmentDirection.Horizontal,
        aSDNodeSpace=graphgrid.GraphGrid.sGetFirstLevelSize()):
    """
    Align the specified SDNodes
    :param aSDNodes: A list of SDNode objects
    :param aAlignDirection: The alignment direction
    :param aSDNodeSpace: The space between nodes
    :return: None
    """
    class NodeInfo:
        def __init__(self, aSDNode: SDNode, aPosition: float2):
            self.mSDNode = aSDNode
            self.mPosition = aPosition

    if not aSDNodes or len(aSDNodes) < 2:
        return

    # Collect node info
    # Find top most Node
    nodeInfoList: list[NodeInfo] = []
    for sdNode in aSDNodes:
        nodePos = sdNode.getPosition()
        nodeInfoList.append(NodeInfo(sdNode, nodePos))

    if aAlignDirection == AlignmentDirection.Horizontal:
        dirComponentIndex = 0  # X
    else:
        dirComponentIndex = 1  # Y

    oppositeDirComponentIndex = 1 - dirComponentIndex

    # Sort along the opposite axis
    nodeInfoList = sorted(
        nodeInfoList, key=lambda nodeInfo: nodeInfo.mPosition[oppositeDirComponentIndex])

    # Get the mean value of X
    vMin: float = nodeInfoList[0].mPosition[oppositeDirComponentIndex]
    vMax: float = vMin
    i = 1
    while i < len(nodeInfoList):
        v = nodeInfoList[i].mPosition[oppositeDirComponentIndex]
        if v < vMin:
            vMin = v
        elif v > vMax:
            vMax = v
        i = i + 1
    vPos = (vMin + vMax) / 2.0

    # Change positions
    # Sort along the opposite axis
    nodeInfoList = sorted(
        nodeInfoList, key=lambda nodeInfo: nodeInfo.mPosition[dirComponentIndex])

    reverseIteration = False
    graphDirectionLeftToRight = True  # TODO: expose as argument
    if aAlignDirection == AlignmentDirection.Horizontal:
        if graphDirectionLeftToRight:
            reverseIteration = True

    nodeCount = len(nodeInfoList)
    if reverseIteration:
        nodeInfoStartIndex = nodeCount-1
        nodeInfoLastIndex = 0
        nodeInfoIndexIncrement = -1
        directionFactor = -1
    else:
        nodeInfoStartIndex = 0
        nodeInfoLastIndex = nodeCount-1
        nodeInfoIndexIncrement = 1
        directionFactor = 1

    nodeInfoIndex = nodeInfoStartIndex
    while nodeInfoIndex != (nodeInfoLastIndex+nodeInfoIndexIncrement):
        if aAlignDirection == AlignmentDirection.Horizontal:
            newPosition = [nodeInfoList[nodeInfoIndex].mPosition[0], vPos]
        else:
            newPosition = [vPos, nodeInfoList[nodeInfoIndex].mPosition[1]]

        nodeInfoList[nodeInfoIndex].mSDNode.setPosition(
            float2(newPosition[0], newPosition[1]))

        nodeInfoIndex = nodeInfoIndex + nodeInfoIndexIncrement

    return True


def snapSDNodes(
        aSDNodes: Optional[SDArray[SDNode]],
        aSnapSize=graphgrid.GraphGrid.sGetSecondLevelSize()):
    """
    Align the specified SDNodes
    :param aSDNodes: A list of SDNode objects
    :param aSnapSize: The snap size
    :return: None
    """
    def __snapPosition(aPosition: float2, aNodeWidth: float, aNodeHeight: float, aSnapSize: float) -> float2:
        def __alignvalue(aValue, aSnapSize):
            hSnapCellCountf = aValue / aSnapSize
            hSnapCellCounti = int(hSnapCellCountf)
            hSnapCellCountFrac = hSnapCellCountf - hSnapCellCounti
            newValue = aSnapSize * hSnapCellCounti
            if hSnapCellCountFrac > 0 and hSnapCellCountFrac > 0.5:
                newValue += aSnapSize
            elif hSnapCellCountFrac < 0 and abs(hSnapCellCountFrac) > 0.5:
                newValue -= aSnapSize
            return newValue

        newPosition = float2(aPosition.x, aPosition.y)

        # Apply offset
        offset = float2(aNodeWidth / 2.0, aNodeHeight / 2.0)
        newPosition.x -= offset.x
        newPosition.y -= offset.y

        # Align horizontally
        newPosition.x = __alignvalue(newPosition.x, aSnapSize)

        # Align vertically
        newPosition.y = __alignvalue(newPosition.y, aSnapSize)

        # undo offset
        newPosition.x += offset.x
        newPosition.y += offset.y
        return newPosition

    if not aSDNodes:
        return False

    for sdNode in aSDNodes:
        nodePos = sdNode.getPosition()
        nodeWidth = graphgrid.GraphGrid.sGetFirstLevelSize()  # Same as the the grid size
        nodeHeight = nodeWidth  # Supposed to be square

        snapedPos = __snapPosition(nodePos, nodeWidth, nodeHeight, aSnapSize)

        sdNode.setPosition(snapedPos)

    return True
