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

class GraphGrid:
    @staticmethod
    def sGetFirstLevelSize() -> float:
        return 9.0 * GraphGrid.sGetUnitSize()

    @staticmethod
    def sGetSecondLevelSize() -> float:
        return GraphGrid.sGetFirstLevelSize() / 3.0

    @staticmethod
    def sGetUnitSize() -> float:
        return 96.0 / 9.0
