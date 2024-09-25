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


import logging
__gLogger = logging.getLogger(__name__)


# =======================================================================================
# INTERNAL USE ONLY
# =======================================================================================
# Global variable used to store the CTypes binary from the C++ application
__runtimeCTypesBinary = None


def setRuntimeBinary(aRuntimeCTypesBinary):
    global __runtimeCTypesBinary
    __runtimeCTypesBinary = aRuntimeCTypesBinary


def getRuntimeBinary():
    return __runtimeCTypesBinary


# =======================================================================================
__gContext = None


def getContext():
    from sd import context

    global __gContext
    if not __gContext:
        __gContext = context.Context()
    return __gContext


# =======================================================================================
__deprecatedMessageEmitted = set()


def __logDeprecatedWarning(funcName, className, recommendedAction):
    __gLogger.warning(
        'Deprecated function %s in class %s. %s.' %
        (funcName, className, recommendedAction))


def deprecatedMethod(className, recommendedAction):
    """
    Decorator to attach to class methods that are deprecated and eventually will be removed
    :param func: The function flagged as deprecated
    :type func: function
    :param recommendedAction: String with the recommended action to do to be up to standard
    :type recommendedAction: string
    """
    def deprecatedMsg(func):
        def deprecatedFunction(*args, **kwargs):
            if func not in __deprecatedMessageEmitted:
                __logDeprecatedWarning(
                    func.__name__, className, recommendedAction)
                __deprecatedMessageEmitted.add(func)
            return func(*args, **kwargs)
        return deprecatedFunction
    return deprecatedMsg
