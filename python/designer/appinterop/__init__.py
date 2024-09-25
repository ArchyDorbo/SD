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

#
# Initialize logger for the submodule.
#

import logging
import sd

logger = logging.getLogger("AppInterop")
logger.addHandler(sd.getContext().createRuntimeLogHandler())
logger.propagate = False
logger.setLevel(logging.DEBUG)

#
# Local imports
#

from .appinteropui import AppInteropUI
