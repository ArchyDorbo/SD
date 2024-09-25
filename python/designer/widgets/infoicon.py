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

from PySide6 import QtCore, QtGui, QtWidgets


class InfoIcon(QtWidgets.QToolButton):
    '''Info icon that displays its tooltip immediately.'''

    def __init__(self, parent=None):
        super(InfoIcon, self).__init__(parent)

        icon = QtGui.QIcon()
        icon.addFile(":/alg/gui/icons/info.svg", QtCore.QSize(), QtGui.QIcon.Disabled)
        self.setIcon(icon)

        self.setCheckable(False)
        self.setDisabled(True)

    def event(self, event):
        if event.type() == QtCore.QEvent.ToolTip:
            # Ignore tool tip events, we draw the tooltip ourselves.
            event.accept()
            return True

        if event.type() == QtCore.QEvent.Enter:
            # Draw the tooltip as soon as the mouse enters the widget.
            QtWidgets.QToolTip.showText(
                self.mapToGlobal(QtCore.QPoint(0, 0)), self.toolTip())

        return super(InfoIcon, self).event(event)
