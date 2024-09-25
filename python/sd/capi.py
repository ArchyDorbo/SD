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
import sys
import ctypes
import sd
from sd import logger
from sd.api import sdapiobject, apiexception
import configparser # For config file

import logging
from logging import StreamHandler

logging.basicConfig(level=logging.WARNING)
_gLogger = logging.getLogger(__name__)


# =======================================================================================
class OSBackend:
    def __init__(self,
                 aDynamicLibraryFileExtension,
                 aDynamicLibraryFilePrefix):
        self.mDynamicLibraryFileExtension = aDynamicLibraryFileExtension
        self.mDynamicLibraryFilePrefix = aDynamicLibraryFilePrefix

    def loadCTypesBinary(self, aBinaryFile):
        cTypesBinary = None

        try:
            _gLogger.info('Loading CTypes binary from %s ...' % str(aBinaryFile))
            cTypesBinary = self._loadCTypesBinary(aBinaryFile)
            _gLogger.info('CTypes binary successfully Loaded from %s' % str(aBinaryFile))
            return cTypesBinary
        except:
            _gLogger.error('Could not load CTypes binary from %s' % str(aBinaryFile))
            raise

    def _loadCTypesBinary(self, aBinaryFile):
        return ctypes.CDLL(aBinaryFile)

class __OSBackendWindows(OSBackend):
    def __init__(self):
        OSBackend.__init__(self,
                           aDynamicLibraryFileExtension = '.dll',
                           aDynamicLibraryFilePrefix = '')

    def _loadCTypesBinary(self, aBinaryFile):
        return ctypes.WinDLL(aBinaryFile)

    def getSubstanceEngineBaseName(self):
        return 'substance_d3d11_blend'

class __OSBackendMacOS(OSBackend):
    def __init__(self):
        OSBackend.__init__(self,
                           aDynamicLibraryFileExtension = '.dylib',
                           aDynamicLibraryFilePrefix='lib')

    def getSubstanceEngineBaseName(self):
        return 'libsubstance_ogl3_blend'

class __OSBackendLinux(OSBackend):
    def __init__(self):
        OSBackend.__init__(self,
                           aDynamicLibraryFileExtension = '.so',
                           aDynamicLibraryFilePrefix='lib')

    def getSubstanceEngineBaseName(self):
        return 'libsubstance_ogl3_blend'

def getOSBackend():
    if sys.platform == 'win32':
        return __OSBackendWindows()
    elif sys.platform == 'darwin':
        return __OSBackendMacOS()
    elif sys.platform == 'linux':
        return __OSBackendLinux()
    raise Exception('Unsupported platform')

# =======================================================================================

class _ConfigFile:
    def __init__(self, aCfgFile):
        configFileSectionNameDefault = 'paths'

        self.mDevSDApiBinaryDir = None
        self.mDevSDPythonSDKDir = None
        self.mDevSDRootDir = None
        self.mDevSubstanceEngineDir = None
        self.mDevSD3DViewIRayDir = None

        configFile = configparser.ConfigParser()
        try:
            configFile.read(aCfgFile)
        except:
            pass

        try:
            self.mDevSDApiBinaryDir = os.path.abspath(configFile[configFileSectionNameDefault]['SDApiBinaryDir'])
        except:
            pass

        try:
            self.mDevSDPythonSDKDir = os.path.abspath(configFile[configFileSectionNameDefault]['SDPythonSDKDir'])
        except:
            pass

        try:
            self.mDevSDRootDir = os.path.abspath(configFile[configFileSectionNameDefault]['SDRootDir'])
        except:
            pass

        try:
            self.mDevSubstanceEngineDir = os.path.abspath(configFile[configFileSectionNameDefault]['SubstanceEngineDir'])
        except:
            pass

        try:
            self.mDevSD3DViewIRayDir = os.path.abspath(configFile[configFileSectionNameDefault]['SD3DViewIRayDir'])
        except:
            pass

# =======================================================================================
class SDAppInfo:
    def __init__(self):

        currentScriptDirAbsPath = os.path.split(__file__)[0]
        configFileDirAbsPath = os.path.abspath(os.path.join(currentScriptDirAbsPath, '..'))
        configFile = _ConfigFile(os.path.join(configFileDirAbsPath, 'designersdk_dev.cfg'))

        self.mDevSDApiBinaryDir = configFile.mDevSDApiBinaryDir
        self.mDevSDPythonSDKDir = configFile.mDevSDPythonSDKDir
        self.mDevSDRootDir = configFile.mDevSDRootDir
        self.mDevSubstanceEngineDir = configFile.mDevSubstanceEngineDir
        self.mDevSD3DViewIRayDir = configFile.mDevSD3DViewIRayDir

        if sys.platform.startswith('darwin'):
            self.mAppResourcesDirName = 'Resources'
        else:
            self.mAppResourcesDirName = 'resources'

        _gLogger.info('SDApiBinaryFile: ' + str(self.getSDApiBinaryFile()))
        _gLogger.info('SDApiBinaryDir: ' + str(self.getSDApiBinaryDir()))
        _gLogger.info('SDRootDir: ' + str(self.getSDRootDir()))
        _gLogger.info('SDResourcesDir: ' + str(self.getSDResourcesDir()))
        _gLogger.info('SDPackagesDir: ' + str(self.getSDPackagesDir()))
        _gLogger.info('SDTemplatesDir: ' + str(self.getSDTemplatesDir()))
        _gLogger.info('SDPluginsDir: ' + str(self.getPluginsDir()))
        _gLogger.info('SDPythonSDKDir: ' + str(self.getSDPythonSDKDir()))
        _gLogger.info('SDSubstanceEngineFileHint: ' + str(self.getSubstanceEngineFileHint()))
        _gLogger.info('SD3DViewDir: ' + str(self.getSD3DViewDir()))
        _gLogger.info('SD3DViewIRayDir: ' + str(self.getSD3DViewIRayDir()))

    def registerPaths(self):

        # Do some checks
        sdApiBinaryDir = self.getSDApiBinaryDir()
        sdPythonSDKDir = self.getSDPythonSDKDir()

        self.__addToPath(sdApiBinaryDir)
        self.__addToPath(sdPythonSDKDir)

    def getSDRootDir(self):
        """
        :return: The SD installation root dir from the current file location: %INSTALLDIR%/resources/python/sd/CURRENT_FILE.py
        """
        if self.mDevSDRootDir:
            return self.mDevSDRootDir

        currentScriptDirAbsPath = os.path.split(__file__)[0]
        path = os.path.abspath(os.path.join(currentScriptDirAbsPath, '..', '..', '..'))
        if not os.path.isdir(path):
            raise Exception('SD Application not installed correctly')
        return path

    def getSDResourcesDir(self):
        """
        :return: the resources directory of SD or '' if not found
        """
        pythonScriptRootDir = self.getSDRootDir()
        path = os.path.join(pythonScriptRootDir, self.mAppResourcesDirName)
        if not os.path.isdir(path):
            _gLogger.warning('SD Resources application not found')
            return ''
        return path

    def getSDPackagesDir(self):
        return os.path.join(self.getSDResourcesDir(), 'packages')

    def getSDTemplatesDir(self):
        return os.path.join(self.getSDResourcesDir(), 'templates')

    def getSD3DViewDir(self):
        return os.path.join(self.getSDResourcesDir(), 'view3d')

    def getSD3DViewIRayDir(self):
        if self.mDevSD3DViewIRayDir:
            return self.mDevSD3DViewIRayDir
        return os.path.join(self.getSD3DViewDir(), 'iray')

    def getSDApiBinaryFile(self):
        binaryDir = ''
        if self.mDevSDApiBinaryDir:
            binaryDir = self.mDevSDApiBinaryDir
        else:
            binaryDir = self.getSDRootDir()

        osBackend = getOSBackend()
        binary = os.path.join(binaryDir, osBackend.mDynamicLibraryFilePrefix + 'designersdk' + osBackend.mDynamicLibraryFileExtension)
        if not os.path.isfile(binary):
            raise Exception('SD API library not found: ' + str(binary))
        return binary

    def getSDApiBinaryDir(self):
        return os.path.split(self.getSDApiBinaryFile())[0]

    def getPluginsDir(self):
        return os.path.join(self.getSDRootDir(), 'plugins')

    def getSDPythonSDKDir(self):
        if self.mDevSDPythonSDKDir:
            return self.mDevSDPythonSDKDir
        path = os.path.join(self.getPluginsDir(), 'pythonsdk')
        if not os.path.isdir(path):
            raise Exception('SD PythonSDK dir not found: ' + str(path))
        return path

    def getSubstanceEngineFileHint(self):
        if self.mDevSubstanceEngineDir:
            substanceEngineDir = self.mDevSubstanceEngineDir
        else:
            substanceEngineDir = os.path.join(self.getPluginsDir(), 'engines')

        osBackend = getOSBackend()
        fileHint = os.path.join(substanceEngineDir, osBackend.getSubstanceEngineBaseName())
        return fileHint

    def __addToPath(self, aPath):
        if not aPath:
            return
        if not aPath in sys.path:
            sys.path = [aPath] + sys.path

        found = False
        for p in os.environ['PATH'].split(os.pathsep):
            if p == aPath:
                found = True
                break

        if not found:
            os.environ['PATH'] = aPath + os.pathsep + os.environ['PATH']

# =======================================================================================
class CTypesFunctions:
    def __init__(self, aCTypesBinary):

        tError = ctypes.c_int
        tVoidPtr = ctypes.c_void_p
        tVoidPtrByRef = ctypes.POINTER(tVoidPtr)
        tSizeT = ctypes.c_size_t
        tConstCharPtr = ctypes.c_char_p
        tInt = ctypes.c_int
        tFloat = ctypes.c_float

        self.mFunctions = {
            # defined in capi.h
            'CApi_init'         : [tError, [tConstCharPtr, tConstCharPtr, tConstCharPtr, tConstCharPtr, tConstCharPtr, tConstCharPtr, tConstCharPtr] ],
            'CApi_uninit'       : [tError, []],
            'CApi_getVersion'   : [tConstCharPtr, []],
            'CApi_getSDApplication' : [tError, [tVoidPtrByRef]],
            'CApi_getAPIObjectCount': [tSizeT, []],
            'CApi_log': [tError, [tConstCharPtr, tInt, tConstCharPtr]],
        }

        self.mCTypesBinary = aCTypesBinary
        self.mCTypesFunctions = {}
        for fctName in self.mFunctions:
            # retrieve CTypes function

            fct = self.mCTypesBinary.__getattr__(fctName)
            if not fct:
                raise Exception('CType function "'+fct+'" not found in binary: ')

            # Set return type and arguments types
            fctTuple = self.mFunctions[fctName]
            fctReturnType = fctTuple[0]
            fctArgsTypes = fctTuple[1]

            fct.restype = fctReturnType
            fct.argtypes = fctArgsTypes

            # Store the CTypes function
            self.mCTypesFunctions[fctName] = fct

        _gLogger.info(str(len(self.mFunctions)) + ' CTypes functions registered')

    def getFunction(self, aFunctionName):
        if aFunctionName not in self.mCTypesFunctions:
            raise Exception('CTypes function not found: "' + str(aFunctionName) + '"')
        return self.mCTypesFunctions[aFunctionName]

# =======================================================================================
class CAPI:
    """
    Class used to manage the C API
    It it based on CTypes and retrieve the binary from the runtime C++ application
    or the shared library specified in the SDAppInfo object
    """
    def __init__(self):
        # Init Binary from the runtime binary
        self.mCTypesBinary = None
        self.mCApiInitialized = False
        self.mSDAppInfo = None
        self.mIsRuntime = False

        # We determine if we are using the runtime binary by checking the import of
        # the sdRuntime module that should have been created by the runtime
        try:
            import algRuntime
            self.mIsRuntime = True
            self.getLogger().info('Runtime CTypesBinary detected')
        except:
            self.mIsRuntime = False
            self.getLogger().info('Non Runtime CTypesBinary detected')

        if self.mIsRuntime:
            try:
                # Retrieve the CTypes binary from algRuntime
                self.mCTypesBinary = algRuntime.getCTypesBinary()
                self.getLogger().info('CTypes successfully initialized from runtime binary')
            except:
                self.getLogger().warning('Runtime CTypesBinary not found')

            if self.mCTypesBinary:
                self.mCTypesFunctions = CTypesFunctions(self.mCTypesBinary)
        else:
            # Try loading the binary from SDAppInfo
            sdAppInfo = SDAppInfo()
            sdAppInfo.registerPaths()

            binaryFile = sdAppInfo.getSDApiBinaryFile()

            osBackend = getOSBackend()
            self.mCTypesBinary = osBackend.loadCTypesBinary(binaryFile)

            if self.mCTypesBinary:
                self.mCTypesFunctions = CTypesFunctions(self.mCTypesBinary)

                # Init the API
                # It will instantiate all the C++ Components
                substanceEngineHint = sdAppInfo.getSubstanceEngineFileHint()
                res = self.getCTypesFct('CApi_init')(
                    ctypes.create_string_buffer(binaryFile.encode('utf-8')),
                    ctypes.create_string_buffer(substanceEngineHint.encode('utf-8')),
                    ctypes.create_string_buffer(sdAppInfo.getSDPackagesDir().encode('utf-8')),
                    ctypes.create_string_buffer(sdAppInfo.getSDTemplatesDir().encode('utf-8')),
                    ctypes.create_string_buffer(sdAppInfo.getSD3DViewDir().encode('utf-8')),
                    ctypes.create_string_buffer(sdAppInfo.getSD3DViewIRayDir().encode('utf-8')),
                    ctypes.create_string_buffer(sdAppInfo.getSDApiBinaryDir().encode('utf-8')))
                if res != 0:
                    raise Exception('Fail to initialize CTypes binary (CApi_init): %s' % sd.api.apiexception.APIException(sdapiobject.SDApiError(res)))

                self.mSDAppInfo = sdAppInfo
                self.mCApiInitialized = True

        if not self.mCTypesBinary:
            raise Exception('Fail to initialize CTypes binary')

        if self.isRuntime():
            # Add the runtime log handler to our logger.
            self.getLogger().addHandler(logger.SDRuntimeLogHandler(self, channelName='PythonSDK'))

            # Do not propagate log messages to the root logger
            # to avoid double messages in Designer's console.
            self.getLogger().propagate = False

        self.getLogger().info('CAPI Version: %s' % self.getVersion())

    def __del__(self):
        if self.mCTypesBinary:
            if self.mCApiInitialized:
                self.getCTypesFct('CApi_uninit')()

    def getCTypesBinary(self):
        return self.mCTypesBinary

    def getCTypesFct(self, aFctName):
        """
        :param aFctName: The CTypes function name
        :return: return the CTypes function object that match the
        """
        return self.mCTypesFunctions.getFunction(aFctName)

    def isRuntime(self):
        return self.mIsRuntime

    def getSDAppInfo(self):
        return self.mSDAppInfo

    @staticmethod
    def getLogger():
        global _gLogger
        return _gLogger

    def getVersion(self):
        if self.mCTypesBinary:
            versionStr = self.getCTypesFct('CApi_getVersion')()
            if versionStr:
                return versionStr.decode('utf-8')
        return ''

# =======================================================================================
__gCAPI = None
def getCAPI():
    """
    :rtype: CAPI
    """
    global __gCAPI
    if not __gCAPI:
        __gCAPI = CAPI()
    return __gCAPI
