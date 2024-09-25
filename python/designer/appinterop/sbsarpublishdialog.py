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

from .appinterop import AppInterop

from ..widgets import InfoIcon

from sd.api.sdproperty import SDPropertyCategory, SDPropertyInheritanceMethod
from sd.api.qtforpythonuimgrwrapper import QtForPythonUIMgrWrapper
from sd.api.sbs.sdsbsarexporter import SDCompressionMode
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph
from sd.api.sbs.sdsbsarexporter import SDCompressionMode
from sd.api.sbs.sdsbsgraphthumbnailgenerator import SDSBSGraphThumbnailGenerator

from PySide6 import QtCore, QtGui, QtWidgets

import logging
import os
import sys


logger = logging.getLogger("AppInterop")


def _createWarningIcon(icons, parent):
    warningIcon = QtWidgets.QToolButton(parent)
    warningIcon.setCheckable(False)
    warningIcon.setDisabled(True)
    warningIcon.setIcon(icons['warning'])
    return warningIcon


class WarningsWidget(QtWidgets.QWidget):
    """
    Displays warnings in SBSAR publish dialog
    """

    def __init__(self, warnings, icons, parent=None):
        super(WarningsWidget, self).__init__(parent=parent)

        self.setObjectName("sbsarpublishdialog.graph_warnings_widget")

        gridLayout = QtWidgets.QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        row = 0
        for warning in warnings:
            warningIcon = _createWarningIcon(icons, parent=self)
            gridLayout.addWidget(warningIcon, row, 0, 1, 1)

            warningLabel = QtWidgets.QLabel(self)
            warningLabel.setText("<font color='#FAFA6E'>%s" % warning)
            gridLayout.addWidget(warningLabel, row, 1, 1, 1)
            row += 1


class GraphInfoWidget(QtWidgets.QWidget):
    """
    Graph entry in the graph list widget
    """

    ICON_SIZE = 64
    HEIGHT_PAD = 24
    __defaultIcon = None

    def __init__(self, graph, icons, parent=None):
        super(GraphInfoWidget, self).__init__(parent=parent)

        self.__graph = graph

        self.warnings = []
        self.__selfWarnings = []
        self.__checkGraphForWarnings(self.__graph)

        self.setObjectName("sbsarpublishdialog.graph_info_widget")
        self.setFixedHeight(self.ICON_SIZE + self.HEIGHT_PAD)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setSpacing(20)

        if not self.__defaultIcon:
            thisDir = os.path.abspath(os.path.dirname(__file__))
            iconsDir = os.path.join(thisDir, '..', 'icons')
            self.__defaultIcon = QtGui.QIcon(os.path.join(
                iconsDir, 'graph.svg')).pixmap(self.ICON_SIZE, self.ICON_SIZE)

        #
        # Graph icon.
        #

        self.__graphIcon = QtWidgets.QLabel(self)
        self.__graphIcon.setObjectName(
            "sbsarpublishdialog.graph_info_widget.graph_icon")
        self.__graphIcon.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.__graphIcon.setMinimumSize(
            QtCore.QSize(self.ICON_SIZE, self.ICON_SIZE))
        self.__graphIcon.setMaximumSize(
            QtCore.QSize(self.ICON_SIZE, self.ICON_SIZE))
        self.__graphIcon.setScaledContents(True)
        layout.addWidget(self.__graphIcon)

        self.updateGraphThumbnail()

        # Graph icon tooltip.
        graphDesc = graph.getPropertyValueFromId(
            "description", SDPropertyCategory.Annotation).get()
        graphCat = graph.getPropertyValueFromId(
            "category", SDPropertyCategory.Annotation).get()
        graphAuthor = graph.getPropertyValueFromId(
            "author", SDPropertyCategory.Annotation).get()
        graphAuthorURL = graph.getPropertyValueFromId(
            "author_url", SDPropertyCategory.Annotation).get()
        graphTags = graph.getPropertyValueFromId(
            "tags", SDPropertyCategory.Annotation).get()

        tooltip = "<p style='white-space:pre'>"
        tooltip += '<b>%s</b>\n' % QtWidgets.QApplication.translate(
            "SBSARPublishDialog", 'Name:')
        tooltip += '%s\n' % graph.getIdentifier()
        tooltip += '\n'

        tooltip += '<b>%s</b>\n' % QtWidgets.QApplication.translate(
            "SBSARPublishDialog", 'Description:')
        tooltip += '%s\n' % (graphDesc if graphDesc else '-')
        tooltip += '\n'

        tooltip += '<b>%s</b>\n' % QtWidgets.QApplication.translate(
            "SBSARPublishDialog", 'Category:')
        tooltip += '%s\n' % (graphCat if graphCat else '-')
        tooltip += '\n'

        tooltip += '<b>%s</b>\n' % QtWidgets.QApplication.translate(
            "SBSARPublishDialog", 'Author:')
        tooltip += '%s\n' % (graphAuthor if graphAuthor else '-')
        tooltip += '\n'

        tooltip += '<b>%s</b>\n' % QtWidgets.QApplication.translate(
            "SBSARPublishDialog", 'Author URL:')
        tooltip += '%s\n' % (graphAuthorURL if graphAuthorURL else '-')
        tooltip += '\n'

        tooltip += '<b>%s</b>\n' % QtWidgets.QApplication.translate(
            "SBSARPublishDialog", 'Tags:')
        tooltip += '%s\n' % (graphTags if graphTags else '-')
        tooltip += '</p>'
        self.__graphIcon.setToolTip(tooltip)

        widget = QtWidgets.QWidget()
        verticalLayout = QtWidgets.QVBoxLayout(widget)

        #
        # Graph identifier.
        #

        horizontalLayout = QtWidgets.QHBoxLayout()
        graphNameLabel = QtWidgets.QLabel(self)
        graphNameLabel.setText('<b>%s</b>' % graph.getIdentifier())
        graphNameLabel.setObjectName(
            "sbsarpublishdialog.graph_info_widget.graph_name_label")
        horizontalLayout.addWidget(graphNameLabel)

        if self.__selfWarnings:
            warningIcon = _createWarningIcon(icons, parent=self)
            warningIcon.setToolTip('\n'.join(self.__selfWarnings))
            horizontalLayout.addWidget(warningIcon)

        verticalLayout.addLayout(horizontalLayout)

        #
        # Graph type.
        #

        horizontalLayout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(self)
        label.setText(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "Type:"))
        label.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        horizontalLayout.addWidget(label)

        graphType = graph.getGraphType()
        if graphType == '':
            graphType = QtWidgets.QApplication.translate(
                "SBSARPublishDialog", "Unspecified")

        graphTypeLabel = QtWidgets.QLabel(self)
        graphTypeLabel.setText(graphType)
        graphTypeLabel.setObjectName(
            "sbsarpublishdialog.graph_info_widget.graph_type_label")
        horizontalLayout.addWidget(graphTypeLabel)
        verticalLayout.addLayout(horizontalLayout)

        #
        # Physical size.
        #

        horizontalLayout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(self)
        label.setText(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "Physical size (cm)"))
        label.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))
        horizontalLayout.addWidget(label)

        physicalSizeLabel = QtWidgets.QLabel(self)
        physicalSizeLabel.setObjectName(
            "sbsarpublishdialog.graph_info_widget.physical_size_label")
        physicalSize = graph.getPropertyValueFromId(
            "physical_size", SDPropertyCategory.Annotation)
        physicalSizeLabel.setText(
            "%s - %s - %s" % (physicalSize.get()[0], physicalSize.get()[1], physicalSize.get()[2]))
        horizontalLayout.addWidget(physicalSizeLabel)
        verticalLayout.addLayout(horizontalLayout)
        layout.addWidget(widget)

    @property
    def graphIdentifier(self):
        return self.__graph.getIdentifier()

    def generateGraphThumbnail(self, thumbnailGenerator):
        thumbnailGenerator.generateThumbnail(self.__graph)

    def updateGraphThumbnail(self):
        icon = self.__graph.getIcon()
        if icon:
            self.hasIcon = True
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(
                QtForPythonUIMgrWrapper.convertSDTextureToQImage(icon))
            self.__graphIcon.setPixmap(pixmap)
        else:
            self.hasIcon = False
            self.__graphIcon.setPixmap(self.__defaultIcon)

    @staticmethod
    def __getInputNodes(graph):
        isInputNode = lambda n: \
            n.getDefinition().getId() in {"sbs::compositing::input_color", "sbs::compositing::input_grayscale"}
        return [n for n in graph.getNodes() if isInputNode(n)]

    @staticmethod
    def __hasRelativeToInputParameter(node):
        isRelativeToInput = lambda param: \
            node.getPropertyInheritanceMethod(param) == SDPropertyInheritanceMethod.RelativeToInput
        parameters = node.getProperties(SDPropertyCategory.Input)
        return any(isRelativeToInput(p) for p in parameters)

    def __checkGraphForWarnings(self, graph):
        if len(graph.getOutputNodes()) == 0:
            self.warnings.append(
                QtWidgets.QApplication.translate(
                    "SBSARPublishDialog",
                    "One or more graphs don't have an output"))
            self.__selfWarnings.append(
                QtWidgets.QApplication.translate(
                    "SBSARPublishDialog",
                    "Does not have any output"))

        prop = graph.getPropertyFromId('$outputsize', SDPropertyCategory.Input)
        inheritanceMethod = graph.getPropertyInheritanceMethod(prop)
        propValue = graph.getPropertyValue(prop).get()

        if inheritanceMethod != SDPropertyInheritanceMethod.RelativeToParent or propValue.x != 0 or propValue.y != 0:
            self.warnings.append(
                QtWidgets.QApplication.translate(
                    "SBSARPublishDialog",
                    "One or more graphs have a non-relative to parent output size parameter"))
            self.__selfWarnings.append(
                QtWidgets.QApplication.translate(
                    "SBSARPublishDialog",
                    "Has a non-relative to parent output size parameter"))

        if any(GraphInfoWidget.__hasRelativeToInputParameter(n) for n in GraphInfoWidget.__getInputNodes(graph)):
            self.warnings.append(
                QtWidgets.QApplication.translate(
                    "SBSARPublishDialog",
                    "One or more graphs have input nodes with parameters relative to input"))
            self.__selfWarnings.append(
                QtWidgets.QApplication.translate(
                    "SBSARPublishDialog",
                    "Has one or more input nodes with parameters relative to input"))


class GraphInfoList(QtWidgets.QWidget):
    """
    List of graphs to publish widget
    """

    def __init__(self, icons, parent=None):
        super(GraphInfoList, self).__init__(parent=parent)
        self.setObjectName("sbsarpublishdialog.graph_info_list")

        self.setStyleSheet("background-color: #262626;")
        self.setAutoFillBackground(True)

        self.__icons = icons
        self.__layout = QtWidgets.QVBoxLayout(self)
        self.__entries = []

    def addGraphEntry(self, graph):
        entry = GraphInfoWidget(graph, self.__icons, parent=self)
        self.__entries.append(entry)
        self.__layout.addWidget(entry)

    def finishGraphList(self):
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.__layout.addItem(spacerItem)

    def anyGraphThumbnailMissing(self):
        for entry in self.__entries:
            if not entry.hasIcon:
                return True

        return False

    def generateMissingThumbnails(self):
        if not self.anyGraphThumbnailMissing():
            return

        thumbnailGenerator = SDSBSGraphThumbnailGenerator.sNew()

        progressDialog = QtWidgets.QProgressDialog(
            labelText=QtWidgets.QApplication.translate(
                "SBSARPublishDialog", "Generating thumbnails"),
            cancelButtonText=QtWidgets.QApplication.translate(
                "SBSARPublishDialog", "Cancel"),
            minimum=0.0,
            maximum=0.0,
            parent=self
        )
        progressDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        progressDialog.setValue(0)

        for entry in self.__entries:
            if not entry.hasIcon:
                entry.generateGraphThumbnail(thumbnailGenerator)

                while not thumbnailGenerator.isFinished():
                    # Keep the UI alive while generating the thumbnail.
                    QtCore.QCoreApplication.processEvents(
                        QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents,
                        200
                    )

                    if progressDialog.wasCanceled():
                        thumbnailGenerator.cancel()
                        progressDialog.close()
                        return

                thumbnailGenError = thumbnailGenerator.getLastError()
                if thumbnailGenError:
                    logger.warning(
                        'Could not generate icon for graph %s' % entry.graphIdentifier)

                entry.updateGraphThumbnail()

        progressDialog.close()

    def getWarnings(self):
        warnings = []
        for entry in self.__entries:
            warnings += entry.warnings

        return list(set(warnings))


class SBSARPublishDialog(QtWidgets.QDialog):
    """
    SBSAR publish dialog
    """

    __icons = {}

    __sbsarCompressionMethods = [
        SDCompressionMode.Auto,
        SDCompressionMode.Best,
        SDCompressionMode.NoCompression
    ]

    def __init__(self, package, publishParams, parent=None):
        super(SBSARPublishDialog, self).__init__(parent=parent)

        self.__loadIcons()

        self.setWindowTitle(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "Substance 3D asset publish options"))
        self.setObjectName("sbsarpublishdialog")

        verticalLayout = QtWidgets.QVBoxLayout(self)
        verticalLayout.setSpacing(10)

        widget = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(widget)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        label = QtWidgets.QLabel(self)
        label.setText(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "File path"))
        gridLayout.addWidget(label, 0, 0, 1, 1)

        self.__filePathTextEntry = QtWidgets.QLineEdit(self)
        self.__filePathTextEntry.setAcceptDrops(False)
        self.__filePathTextEntry.setReadOnly(True)
        self.__filePathTextEntry.setObjectName(
            "sbsarpublishdialog.filepath_entry")
        self.__filePathTextEntry.setText(
            package.getFilePath().replace('.sbs', '.sbsar'))

        gridLayout.addWidget(self.__filePathTextEntry, 0, 1, 1, 2)

        self.__fileDialogAccepted = False

        self.__selectPath = QtWidgets.QToolButton(self)
        self.__selectPath.setText("...")
        self.__selectPath.setObjectName(
            "sbsarpublishdialog.select_filepath_button")
        self.__selectPath.pressed.connect(self.__onSelectPath)
        gridLayout.addWidget(self.__selectPath, 0, 3, 1, 1)

        label = QtWidgets.QLabel(self)
        label.setText(
            QtWidgets.QApplication.translate("SBSARPublishDialog", "Archive compression"))
        gridLayout.addWidget(label, 1, 0, 1, 1)

        self.__archiveCompressionCombo = QtWidgets.QComboBox(self)
        if sys.platform == 'darwin':
            # Avoid issues with styled combo boxed on OSX.
            # Reference: https://bugreports.qt.io/browse/QTBUG-30282
            self.__archiveCompressionCombo.setStyle(
                QtWidgets.QStyleFactory.create("Windows"))

        self.__archiveCompressionCombo.setObjectName(
            "sbsarpublishdialog.archive_compression_combo")
        self.__archiveCompressionCombo.addItem(
            QtWidgets.QApplication.translate("SBSARPublishDialog", "Auto"))
        self.__archiveCompressionCombo.addItem(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "Best (Slow encode/decode)"))
        self.__archiveCompressionCombo.addItem(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "None (Fast encode/decode)"))
        gridLayout.addWidget(self.__archiveCompressionCombo, 1, 1, 1, 2)

        self.__archiveCompressionInfo = InfoIcon(self)
        self.__archiveCompressionInfo.setToolTip(
            QtWidgets.QApplication.translate(
                "SBSARPublishDialog",
                "Compression mode used for embedded bitmap resources")
        )
        gridLayout.addWidget(self.__archiveCompressionInfo, 1, 3, 1, 1)
        verticalLayout.addWidget(widget)

        widget = QtWidgets.QWidget()
        horizontalLayout = QtWidgets.QHBoxLayout(widget)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(widget)
        label.setText(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "<b>Exposed graphs</b>"))
        horizontalLayout.addWidget(label)

        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem1)

        self.__generateMissingIconsButton = QtWidgets.QPushButton(widget)
        self.__generateMissingIconsButton.setText(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "Generate missing icons"))
        self.__generateMissingIconsButton.setObjectName(
            "sbsarpublishdialog.generate_missing_icons_button")
        self.__generateMissingIconsButton.setToolTip(
            QtWidgets.QApplication.translate(
                "SBSARPublishDialog",
                "Automatically generate an icon for any graph that does not have one")
        )
        self.__generateMissingIconsButton.pressed.connect(
            self.__onGenerateThumbnailsPressed)
        horizontalLayout.addWidget(self.__generateMissingIconsButton)

        self.__genMissingIconsInfo = InfoIcon(widget)
        self.__genMissingIconsInfo.setToolTip('<qt>%s</qt>' %  # <- Needed for Qt to line break properly.
                                              QtWidgets.QApplication.translate(
                                                  "SBSARPublishDialog",
                                                  'Exposed graphs can be accessed when using the .sbsar file in Substance 3D Designer or any other application. Any graph not meant for outside usage, like sub-graphs, can be excluded by setting their attribute "Exposed in SBSAR" to "No".')
                                              )
        horizontalLayout.addWidget(self.__genMissingIconsInfo)
        verticalLayout.addWidget(widget)

        self.__graphListScrollArea = QtWidgets.QScrollArea(self)
        self.__graphListScrollArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAsNeeded)
        self.__graphListScrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.__graphListScrollArea.setWidgetResizable(True)
        self.__graphListScrollArea.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding))

        self.__graphInfoList = GraphInfoList(
            icons=self.__icons, parent=self)
        self.__graphInfoList.setObjectName(
            "sbsarpublishdialog.graph_info_list")
        self.__graphListScrollArea.setWidget(self.__graphInfoList)
        verticalLayout.addWidget(self.__graphListScrollArea)

        #
        # Add all exposed graphs to the list.
        #

        resources = package.getChildrenResources(isRecursive=True)
        for res in resources:
            if isinstance(res, SDSBSCompGraph):
                if res.getExposedInSBSAR():
                    self.__graphInfoList.addGraphEntry(res)

        self.__graphInfoList.finishGraphList()

        #
        # Handle warnings.
        #

        warnings = self.__graphInfoList.getWarnings()

        if AppInterop.isAnyDependencyModified(package):
            warnings.insert(0,
                            QtWidgets.QApplication.translate(
                                "SBSARPublishDialog",
                                "One or more package dependencies are not saved"))

        if len(warnings) != 0:
            self.__warningsWidget = WarningsWidget(
                warnings, self.__icons, parent=self)
            verticalLayout.addWidget(self.__warningsWidget)

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setSpacing(5)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem1)

        self.__publishButton = QtWidgets.QPushButton(self)
        self.__publishButton.setText(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "Publish"))
        self.__publishButton.setAutoDefault(False)
        self.__publishButton.setDefault(True)
        self.__publishButton.setObjectName("sbsarpublishdialog.publish_button")
        self.__publishButton.pressed.connect(self.__onPublishPressed)
        horizontalLayout.addWidget(self.__publishButton)

        self.__cancelButton = QtWidgets.QPushButton(self)
        self.__cancelButton.setText(QtWidgets.QApplication.translate(
            "SBSARPublishDialog", "Cancel"))
        self.__cancelButton.setAutoDefault(False)
        self.__cancelButton.setObjectName("sbsarpublishdialog.cancel_button")
        self.__cancelButton.pressed.connect(self.__onCancelPressed)
        horizontalLayout.addWidget(self.__cancelButton)
        verticalLayout.addLayout(horizontalLayout)

        self.__generateMissingIconsButton.setEnabled(
            self.__graphInfoList.anyGraphThumbnailMissing())

        #
        # Init dialog settings from the last publish done if it exists.
        #

        if publishParams:
            self.__filePathTextEntry.setText(publishParams['sbsar_file_path'])

            self.__archiveCompressionCombo.setCurrentIndex(
                self.__sbsarCompressionMethods.index(
                    publishParams['compression_mode']
                )
            )

        # Update enabled state of widgets.
        self.__validate()

    def exportParameters(self):
        return {
            'sbsar_file_path': self.__filePathTextEntry.text(),
            'compression_mode': self.__sbsarCompressionMethods[self.__archiveCompressionCombo.currentIndex()]
        }

    #
    # Callbacks.
    #

    def __onPublishPressed(self):
        sbsarFilePath = self.__filePathTextEntry.text()

        # Show overwrite message box if the sbsar file exists and
        # we didn't show the file dialog before.
        if QtCore.QFile.exists(sbsarFilePath) and not self.__fileDialogAccepted:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(QtWidgets.QApplication.translate(
                "SBSARPublishDialog", "%s already exists.") % QtCore.QFileInfo(sbsarFilePath).fileName())
            msgBox.setInformativeText(QtWidgets.QApplication.translate(
                "SBSARPublishDialog", "Do you want to replace it?"))
            msgBox.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
            result = msgBox.exec()

            if result == QtWidgets.QMessageBox.No:
                return

        self.__dialogInfo = {}
        self.__dialogInfo['archive_compression'] = self.__archiveCompressionCombo.currentIndex(
        )
        self.__dialogInfo['file_path'] = sbsarFilePath
        self.accept()

    def __onCancelPressed(self):
        self.reject()

    def __onSelectPath(self):
        documentsPath = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation)
        filePath = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            dir=self.__filePathTextEntry.text() if self.__filePathTextEntry.text() else documentsPath,
            caption=QtCore.QCoreApplication.translate(
                "SBSARPublishDialog", "Publish to"),
            filter=QtCore.QCoreApplication.translate(
                "PyAppInterop", "Substance 3D asset files (*.sbsar)"))[0]

        if filePath != '':
            self.__fileDialogAccepted = True
            self.__filePathTextEntry.setText(filePath)

        self.__validate()

    def __onGenerateThumbnailsPressed(self):
        try:
            self.__graphInfoList.generateMissingThumbnails()
            self.__generateMissingIconsButton.setEnabled(
                self.__graphInfoList.anyGraphThumbnailMissing())
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                QtCore.QCoreApplication.translate(
                    "SBSARPublishDialog", "Error generating thumbnails"),
                QtCore.QCoreApplication.translate(
                    "SBSARPublishDialog", "Error generating thumbnails. Check the console for details."),
                QtWidgets.QMessageBox.Ok)

    #
    # Utility methods.
    #

    def __validate(self):
        if self.__filePathTextEntry.text() == '':
            self.__publishButton.setEnabled(False)
        else:
            self.__publishButton.setEnabled(True)

    @classmethod
    def __loadIcons(cls):
        thisDir = os.path.abspath(os.path.dirname(__file__))
        iconsDir = os.path.join(thisDir, '..', 'icons')
        iconList = [
            'warning',
        ]

        for iconName in iconList:
            if not iconName in cls.__icons:
                # Special case for warning icon.
                if iconName == 'warning':
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap(os.path.join(
                        iconsDir, iconName + '.svg')), QtGui.QIcon.Normal)
                    icon.addPixmap(QtGui.QPixmap(os.path.join(
                        iconsDir, iconName + '.svg')), QtGui.QIcon.Disabled)
                    cls.__icons[iconName] = icon
                else:
                    cls.__icons[iconName] = QtGui.QIcon(
                        os.path.join(iconsDir, iconName + '.svg'))
