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

from sd.api import qtforpythonuimgrwrapper
from sd.api import SDAPIObject
from sd.api.sbs import sdsbscompgraph, sdsbsfxmapgraph

from PySide6 import QtWidgets, QtGui, QtCore

from functools import partial
import os


class CleanAction(QtWidgets.QWidgetAction):
    """
    Parent class for building the widget holding the graph cleaning tools.

    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    """

    def __init__(
            self,
            ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper
    ):

        super(CleanAction, self).__init__(ui_mgr.getMainWindow())

        self.ui_mgr = ui_mgr
        self.__button = QtWidgets.QToolButton(self.ui_mgr.getMainWindow())
        self.action_clean = QtGui.QAction()
        self.action_clean_recursive = QtGui.QAction()

    def build_action_ui(self) -> None:

        menu = self.setup_menu()
        self.__button.setDefaultAction(menu.menuAction())

        self.__button.defaultAction().setToolTip(
            QtCore.QCoreApplication.translate("GraphCleaner", "Remove unused nodes"))
        self.__button.defaultAction().setIcon(QtGui.QIcon(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            'icons',
            "clean_drop.svg"
        )))
        self.__button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.setDefaultWidget(self.__button)

    def setup_menu(self) -> QtWidgets.QMenu:

        menu = QtWidgets.QMenu(self.ui_mgr.getMainWindow())

        label = QtWidgets.QWidgetAction(menu)
        label.setDefaultWidget(QtWidgets.QLabel(
            QtCore.QCoreApplication.translate("GraphCleaner", "Remove unused nodes")))
        menu.addAction(label)

        menu.addAction(self.action_clean)
        menu.addAction(self.action_clean_recursive)

        return menu


class GraphViewCleanAction(CleanAction):
    """
    Class for building the widget holding the graph cleaning tools in the Graph View toolbar.

    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    """

    def __init__(
            self,
            ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper
    ):

        super(GraphViewCleanAction, self).__init__(ui_mgr=ui_mgr)

        self.action_clean.setText(
            QtCore.QCoreApplication.translate("GraphCleaner", "This graph only"))

        from . import clean_graph

        self.action_clean.triggered.connect(partial(
            clean_graph.on_graph_view_clean_action_triggered,
            ui_mgr=self.ui_mgr,
            is_recursive=False
        ))

        self.action_clean_recursive.setText(
            QtCore.QCoreApplication.translate("GraphCleaner", "This graph and parameter functions"))
        self.action_clean_recursive.triggered.connect(partial(
            clean_graph.on_graph_view_clean_action_triggered,
            ui_mgr=self.ui_mgr,
            is_recursive=True
        ))

        self.current_graph = self.ui_mgr.getCurrentGraph()
        self.recursion_supported = isinstance(self.current_graph, sdsbscompgraph.SDSBSCompGraph) \
            or isinstance(self.current_graph, sdsbsfxmapgraph.SDSBSFxMapGraph)

        if not self.recursion_supported:
            self.action_clean_recursive.setDisabled(True)

        self.build_action_ui()


class ExplorerCleanAction(CleanAction):
    """
    Class for building the widget holding the graph cleaning tools in the Explorer toolbar.

    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    """

    def __init__(
            self,
            ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper
    ):

        super(ExplorerCleanAction, self).__init__(ui_mgr=ui_mgr)

        self.explorer_selection: dict[str, SDAPIObject] = dict()

        self.action_clean.setText(
            QtCore.QCoreApplication.translate("GraphCleaner", "Selected graph(s) only"))

        from . import clean_graph

        self.action_clean.triggered.connect(partial(
            clean_graph.on_explorer_clean_action_triggered,
            ui_mgr=self.ui_mgr,
            explorer_action=self,
            is_recursive=False
        ))

        self.action_clean_recursive.setText(
            QtCore.QCoreApplication.translate("GraphCleaner", "Selected graph(s) and parameter functions"))
        self.action_clean_recursive.triggered.connect(partial(
            clean_graph.on_explorer_clean_action_triggered,
            ui_mgr=self.ui_mgr,
            explorer_action=self,
            is_recursive=True
        ))

        self.build_action_ui()

    def update_menu_actions(self) -> None:

        has_graphs = bool(self.explorer_selection["graphs"])
        has_packages = bool(self.explorer_selection["packages"])
        has_folders = bool(self.explorer_selection["folders"])
        has_graph_children = bool(self.explorer_selection["graphs_children"])

        cleaning_available = (has_graphs and (not has_folders) and (not has_packages)) \
            or (has_folders and (not has_graphs) and (not has_packages) and has_graph_children) \
            or (has_packages and (not has_graphs) and (not has_folders) and has_graph_children)

        if cleaning_available:
            self.setEnabled(True)
            if self.explorer_selection["graphs_comp"]:
                self.action_clean_recursive.setEnabled(True)
            else:
                self.action_clean_recursive.setDisabled(True)
        else:
            self.setDisabled(True)


class CompletionDialog(QtWidgets.QMessageBox):
    """
    Class for building the completion dialog that is  displayed when cleaning is completed.

    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    :param cleaned_nodes_count: The amount of nodes removed in all cleaned graphs.
    :param cleaned_subgraphs_count: The amount of cleaned parameter functions.
    :param cleaned_graphs_count: The amount of cleaned graphs.
    :param not_cleaned_graphs_count: The amount of graphs which could not be cleaned.
    :param from_explorer: Specifies that the cleaning was triggered from the Explorer.
    """

    def __init__(
            self,
            ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper,
            cleaned_nodes_count: int,
            cleaned_subgraphs_count: int,
            cleaned_graphs_count: int,
            not_cleaned_graphs_count: int,
            from_explorer: bool,
    ):

        super(CompletionDialog, self).__init__(ui_mgr.getMainWindow())

        self.__cleaned_nodes_count = cleaned_nodes_count
        self.__cleaned_subgraphs_count = cleaned_subgraphs_count
        self.__cleaned_graphs_count = cleaned_graphs_count
        self.__not_cleaned_graphs_count = not_cleaned_graphs_count
        self.__from_explorer = from_explorer

        self.setWindowTitle(QtCore.QCoreApplication.translate(
            "GraphCleaner::CompletionDialog", "Clean graph(s)"))

        self.__text = self.__build_report()
        self.setText(self.__text)

    def __build_report(self) -> str:

        # Build possible strings for localisation team

        nodes_report = QtCore.QCoreApplication.translate(
            "GraphCleaner",
            "{nodes_count} node(s) removed from this graph."
        ).format(
            nodes_count=str(self.__cleaned_nodes_count)
        )

        nodes_report_functions = QtCore.QCoreApplication.translate(
            "GraphCleaner",
            "{nodes_count} node(s) removed from this graph and {functions_count} parameter function(s)."
        ).format(
            nodes_count=str(self.__cleaned_nodes_count),
            functions_count=str(self.__cleaned_subgraphs_count)
        )

        nodes_report_graphs = QtCore.QCoreApplication.translate(
            "GraphCleaner",
            "{nodes_count} node(s) removed from {graphs_count} graph(s)."
        ).format(
            nodes_count=str(self.__cleaned_nodes_count),
            graphs_count=str(self.__cleaned_graphs_count)
        )

        nodes_report_graphs_functions = QtCore.QCoreApplication.translate(
            "GraphCleaner",
            "{nodes_count} node(s) removed from {graphs_count} graph(s) and {functions_count} parameter function(s)."
        ).format(
            nodes_count=str(self.__cleaned_nodes_count),
            graphs_count=str(self.__cleaned_graphs_count),
            functions_count=str(self.__cleaned_subgraphs_count)
        )

        graphs_not_cleaned_report = QtCore.QCoreApplication.translate(
            "GraphCleaner",
            "{graphs_count} graph(s) could not be cleaned."
        ).format(
            graphs_count=str(self.__not_cleaned_graphs_count)
        )

        see_console = QtCore.QCoreApplication.translate(
            "GraphCleaner", "See Console for details.")
        no_unused_nodes = QtCore.QCoreApplication.translate(
            "GraphCleaner", "No unused nodes found.")

        # Build report depending on context

        if self.__not_cleaned_graphs_count:
            see_console = " ".join([graphs_not_cleaned_report, see_console])

        report = ""

        if self.__cleaned_nodes_count:
            if self.__from_explorer:
                if self.__cleaned_subgraphs_count:
                    report = nodes_report_graphs_functions
                else:
                    report = nodes_report_graphs
            else:
                if self.__cleaned_subgraphs_count:
                    report = nodes_report_functions
                else:
                    report = nodes_report
            return " ".join([report, see_console])
        elif self.__not_cleaned_graphs_count:
            return see_console
        else:
            return no_unused_nodes


class CleanProgressDialog(QtWidgets.QProgressDialog):
    """
    Class for building the progress bar dialog that is displayed when the cleaning process is longer than 2 seconds.

    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    """

    def __init__(
            self,
            ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper
    ):

        super(CleanProgressDialog, self).__init__(
            parent=ui_mgr.getMainWindow(),
            minimum=0,
            maximum=0,
            labelText=QtCore.QCoreApplication.translate(
                "GraphCleaner", "Cleaning graphs...")
        )

        self.can_close = False

        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Do not include close button in title bar
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.WindowTitleHint
        )
        self.setCancelButton(None)
        self.setWindowTitle(QtCore.QCoreApplication.translate(
            "GraphCleaner", "Clean graph(s)"))

    # Override methods that can close the dialog

    def reject(self):
        if self.can_close:
            super(CleanProgressDialog, self).reject()

    def accept(self):
        if self.can_close:
            super(CleanProgressDialog, self).accept()

    def done(self):
        if self.can_close:
            super(CleanProgressDialog, self).done()
