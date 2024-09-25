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
from sd.tools import io
from tests import tools


def __getMainFunctions(aPyFile):
    def __getMainFunctionList(aPyModule):
        functionList = []
        for functionDesc in tools.getFunctionsFromPyModule(aPyModule):
            if functionDesc.__name__ == 'main':
                functionList.append(functionDesc)
        return functionList

    # Import module
    pyModule = tools.importPyModuleFromPyFile(aPyFile)

    # Collect Unit test classes
    return __getMainFunctionList(pyModule)

def __runSample(aSDContext, aPyFile):
    functions = __getMainFunctions(aPyFile)
    for function in functions:
        function(aSDContext)


def main():
    samplesPyFiles = tools.getPyFiles(io.getFileDir(__file__), 'sample_')
    sdContext = sd.getContext()
    index = 0
    for samplePyFile in samplesPyFiles:
        index += 1
        tools.printSeparator()
        print('[%d/%d] Running sample: %s' % (index, len(samplesPyFiles), samplePyFile))
        __runSample(sdContext, samplePyFile)
    tools.printSeparator()

if __name__ == '__main__':
    main()
