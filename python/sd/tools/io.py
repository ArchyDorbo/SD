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

def getAbsFile(aPyFile = None):
    if aPyFile:
        return os.path.abspath(aPyFile)
    return os.path.abspath(__file__)

def getFileBaseName(aPyFile = None):
    """
    :rtype: string
    """

    return os.path.split(getAbsFile(aPyFile))[1].split('.')[0]

def getFileDir(aPyFile = None):
    """
    :rtype: string
    """
    return os.path.abspath(os.path.split(os.path.abspath(getAbsFile(aPyFile)))[0])


def getAPIRootDir():
    return os.path.abspath(os.path.join(getFileDir(), '..', '..'))


def getAssetsDir(aPyFile = None):
    """
    :rtype: string
    """
    return os.path.join(getFileDir(aPyFile), 'assets')


def getUserDocumentDir():
    """
    Return the user document directory path

    :rtype: string
    """
    return os.path.expanduser('~'+os.sep+'Documents')


def getUserDocumentOutputDir(aReferenceFile):
    """
    Get the path of the output dir related to the specified aReferenceFile file path

    :param aReferenceFile: A reference file path that will be used to generate the output subdirectory. Usually __file__
    :type aReferenceFile: string
    :rtype: string
    """
    outputDirFileName = os.path.split(aReferenceFile)[1]
    outputDirBaseName = outputDirFileName.split('.')[0]
    userDocumentDir = os.path.expanduser('~' + os.sep + 'Documents')
    outputDir = os.path.join(userDocumentDir, 'Allegorithmic', 'Substance Designer SDK', outputDirBaseName)
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)
    return outputDir

