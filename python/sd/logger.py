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

import ctypes
import logging

from enum import Enum

class LogLevel(Enum):
    Info = 0
    Warning = 1
    Error = 2

class SDRuntimeLogHandler(logging.StreamHandler):
    def __init__(self, aCAPI, channelName = None):
        super(SDRuntimeLogHandler, self).__init__()
        self.__CApi_log = aCAPI.getCTypesFct('CApi_log')
        self.__channelName = channelName

    def emit(self, record):
        if self.__channelName:
            channelName = self.__channelName
        else:
            # Use the logger name as the channel.
            channelName = record.name

        res = self.__CApi_log(
            ctypes.create_string_buffer(record.msg.encode('utf-8')),
            ctypes.c_int(self.__convertLogLevel(record.levelno)),
            ctypes.create_string_buffer(channelName.encode('utf-8')))
        if res != 0:
            raise sd.api.apiexception.APIException(sdapiobject.SDApiError(res))

    @staticmethod
    def __convertLogLevel(pyLogLevel):
        if pyLogLevel == logging.INFO:
            return LogLevel.Info.value
        elif pyLogLevel == logging.WARNING:
            return LogLevel.Warning.value
        elif pyLogLevel == logging.ERROR:
            return LogLevel.Error.value
        else:
            # Default to info log level.
            return LogLevel.Info.value
