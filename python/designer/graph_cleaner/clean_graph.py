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

from sd.api import sdproperty, sdnode, sdgraph, qtforpythonuimgrwrapper, sdhistoryutils
from sd.api.mdl import sdmdlgraph, sdmdlconstantnode
from sd.api.sbs import sdsbscompgraph, sdsbsfxmapnode

from PySide6 import QtCore

from functools import partial
import logging

from . import ui_setup

logger = logging.getLogger("GraphCleaner")

INPUT_NODES_COMP = (
    "sbs::compositing::input_color",
    "sbs::compositing::input_grayscale",
    "sbs::compositing::input_value"
)

HISTORY_ENTRY_LABEL = QtCore.QCoreApplication.translate(
    "GraphCleaner::History", "Clean graph(s)")


class GraphCleaner:
    """
    Class for removing unused nodes in a graph.

    :param graph: the SDGraph object that should be cleaned.
    :param graph_id: the identifier of the graph that should be cleaned.
    """

    def __init__(
            self,
            graph: sdgraph.SDGraph,
            graph_id: str
    ):

        self.__ALL_NODES = set()
        self.__USED_NODES = set()
        self.__IGNORED_NODES = set()
        self.__UNUSED_NODES = set()
        self.__GRAPH = graph
        self.__GRAPH_ID = graph_id
        self.unused_nodes_count = 0
        self.can_clean = True

        self.__clean_current_graph()

    def __collect_connected_nodes(self, node: sdnode.SDNode) -> None:
        """
        This function adds all nodes connected to a specified node's input connectors to the __USED_NODES set.

        :param node: The SDNode object which inputs should be collected.
        :return: None
        """

        connected_nodes = []
        identifier = node.getIdentifier()

        if identifier not in self.__USED_NODES:

            self.__USED_NODES.add(node.getIdentifier())
            node_props = node.getProperties(
                sdproperty.SDPropertyCategory.Input)

            for prop in node_props:
                if prop.isConnectable():
                    if node.getPropertyConnections(prop):

                        # Keep the UI alive while waiting for connected nodes to be collected
                        QtCore.QCoreApplication.processEvents(
                            QtCore.QEventLoop.AllEvents | QtCore.QEventLoop.WaitForMoreEvents,
                            200
                        )

                        connected_node = node.getPropertyConnections(
                            prop)[0].getInputPropertyNode()
                        connected_nodes.append(connected_node)
                        self.__collect_connected_nodes(connected_node)

    def __collect_all_nodes(self) -> None:
        """
        This function adds all nodes in the graph targeted by the Graph Cleaner instance to the __ALL_NODES set.

        :return: None
        """

        graph_nodes = self.__GRAPH.getNodes()
        for node in graph_nodes:
            if not bool(node.getDefinition()):
                self.can_clean = False
            self.__ALL_NODES.add(node.getIdentifier())

    def __collect_input_nodes(self) -> None:
        """
        This function adds all Input or exposed nodes in the graph targeted by the Graph Cleaner instance to the __USED_NODES set.

        :return: None
        """

        graph = self.__GRAPH
        node_id_set = self.__ALL_NODES

        for node_id in node_id_set:

            node = graph.getNodeFromId(node_id)

            if isinstance(graph, sdmdlgraph.SDMDLGraph) \
                    and isinstance(node, sdmdlconstantnode.SDMDLConstantNode) \
                    and node.isExposed():
                self.__IGNORED_NODES.add(node.getIdentifier())

            elif isinstance(graph, sdsbscompgraph.SDSBSCompGraph) \
                    and node.getDefinition().getId() in INPUT_NODES_COMP:
                self.__IGNORED_NODES.add(node.getIdentifier())

    def __remove_nodes_in_id_set(self, nodes_id_set: set) -> None:
        """
        This function removes all nodes which identifiers are listed in the provided set from the graph targeted by the Graph Cleaner instance.

        :param nodes_id_set: The set of identifiers for the nodes that should be deleted.
        :return: None
        """

        for node_id in nodes_id_set:
            node = self.__GRAPH.getNodeFromId(node_id)
            if node:
                self.__GRAPH.deleteNode(node)

    def __remove_unused_nodes(self) -> None:
        """
        This function removes all unused nodes from the graph targeted by the Graph Cleaner instance.

        The set of unused nodes is the difference between the set of used nodes (__USED_NODES)
        and the set of all nodes (__ALL_NODES).

        :return: None
        """

        self.__collect_all_nodes()

        if self.can_clean:
            self.__collect_input_nodes()

            output_nodes = self.__GRAPH.getOutputNodes()
            for output_node in output_nodes:
                self.__collect_connected_nodes(output_node)

            self.__UNUSED_NODES = self.__ALL_NODES.difference(
                self.__USED_NODES.union(self.__IGNORED_NODES))
            self.unused_nodes_count = len(self.__UNUSED_NODES)

            if self.__UNUSED_NODES:
                self.__remove_nodes_in_id_set(self.__UNUSED_NODES)

    def __clean_current_graph(self) -> None:
        """
        This function removes unused nodes in the graph targeted by the Graph Cleaner instance.

        :return: None
        """

        self.__remove_unused_nodes()

        if self.can_clean:
            if self.unused_nodes_count:
                logger.info(f"{self.unused_nodes_count} unused nodes removed in {self.__GRAPH_ID} graph."
                            )
        else:
            logger.warning(
                f"{self.__GRAPH_ID} graph was not cleaned: at least one node has no definition.")


def get_node_property_graphs(
    node: sdnode.SDNode,
    graph_id: str
) -> dict:
    """
    This function returns a dictionary of property graphs found in an SDNode object, using these key/value pairs:
      - key: Node label - Property label
      - value: SDGraph object for the property's property graph

    :param node: The SDNode object for the node from which property graphs should be retrieved.
    :param graph_id: The identifier of the graph containing the node being processed.
    :return: The dictionary containing the property graphs.
    """

    property_graphs: dict[str, sdgraph.SDGraph] = dict()
    node_props = node.getProperties(sdproperty.SDPropertyCategory.Input)
    for prop in node_props:
        prop_graph = node.getPropertyGraph(prop)
        if prop_graph:
            prop_graph_location = "({}) {} {} - {}".format(
                graph_id,
                node.getIdentifier(),
                node.getDefinition().getLabel(),
                prop.getLabel()
            )
            property_graphs[prop_graph_location] = prop_graph
    return property_graphs


def on_graph_view_clean_action_triggered(
        ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper,
        is_recursive: bool
) -> None:
    """
    This function is called when a cleaning action is triggered in the Graph View.

    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    :param is_recursive: Specifies whether cleaning should recurse into property graphs.
    :return: None
    """

    nodes_removed_total = 0
    subgraphs_cleaned_total = 0
    graphs_not_cleaned_total = 0
    cleaners = set()
    graph = ui_mgr.getCurrentGraph()
    graph_id = graph.getIdentifier()

    progress_dialog = ui_setup.CleanProgressDialog(ui_mgr=ui_mgr)

    with sdhistoryutils.SDHistoryUtils.UndoGroup(HISTORY_ENTRY_LABEL):
        graph_cleaner = GraphCleaner(graph=graph, graph_id=graph_id)
        cleaners.add(graph_cleaner)

        if not graph_cleaner.can_clean:
            graphs_not_cleaned_total += 1

        if is_recursive:
            for node in graph.getNodes():
                prop_graphs = get_node_property_graphs(
                    node=node, graph_id=graph_id)
                for key, value in prop_graphs.items():
                    prop_graph_cleaner = GraphCleaner(
                        graph=value, graph_id=key)
                    cleaners.add(prop_graph_cleaner)
                    if prop_graph_cleaner.can_clean:
                        if prop_graph_cleaner.unused_nodes_count:
                            subgraphs_cleaned_total += 1
                    else:
                        graphs_not_cleaned_total += 1

                if node.getDefinition().getId() == "sbs::compositing::fxmaps":
                    fx_map_graph = node.getReferencedResource()
                    fx_map_cleaner = GraphCleaner(
                        graph=fx_map_graph, graph_id=f"{node.getIdentifier()} FX-Map")
                    cleaners.add(fx_map_cleaner)
                    if fx_map_cleaner.can_clean:
                        if fx_map_cleaner.unused_nodes_count:
                            subgraphs_cleaned_total += 1
                    else:
                        graphs_not_cleaned_total += 1

                    for fx_map_node in fx_map_graph.getNodes():
                        prop_graphs = get_node_property_graphs(
                            node=fx_map_node, graph_id="FX-Map")
                        for key, value in prop_graphs.items():
                            fx_map_prop_graph_cleaner = GraphCleaner(
                                graph=value, graph_id=key)
                            cleaners.add(fx_map_prop_graph_cleaner)
                            if fx_map_prop_graph_cleaner.can_clean:
                                if fx_map_prop_graph_cleaner.unused_nodes_count:
                                    subgraphs_cleaned_total += 1
                            else:
                                graphs_not_cleaned_total += 1

    for cleaner in cleaners:
        if cleaner:
            nodes_removed_total += cleaner.unused_nodes_count

    progress_dialog.can_close = True
    progress_dialog.reset()
    del progress_dialog

    completion_dialog = ui_setup.CompletionDialog(
        ui_mgr=ui_mgr,
        cleaned_nodes_count=nodes_removed_total,
        cleaned_subgraphs_count=subgraphs_cleaned_total,
        cleaned_graphs_count=1,
        not_cleaned_graphs_count=graphs_not_cleaned_total,
        from_explorer=False
    )
    completion_dialog.exec()


def on_explorer_clean_action_triggered(
        ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper,
        explorer_action: ui_setup.ExplorerCleanAction,
        is_recursive: bool
) -> None:
    """
    This function is called when a cleaning action is triggered in the Explorer.

    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    :param explorer_action: The ExplorerCleanAction object holding the cleaning tools in the Explorer toolbar.
    :param is_recursive: Specifies whether cleaning should recurse into property graphs.
    :return: None
    """

    nodes_removed_total = 0
    graphs_cleaned_total = 0
    subgraphs_cleaned_total = 0
    graphs_not_cleaned_total = 0
    cleaners: set[GraphCleaner] = set()

    progress_dialog = ui_setup.CleanProgressDialog(ui_mgr=ui_mgr)

    selected_graphs = explorer_action.explorer_selection["graphs"].union(
        explorer_action.explorer_selection["graphs_children"]
    )

    with sdhistoryutils.SDHistoryUtils.UndoGroup(HISTORY_ENTRY_LABEL):
        for graph in selected_graphs:

            graph_id = graph.getIdentifier()
            graph_cleaner = GraphCleaner(graph, graph.getIdentifier())
            cleaners.add(graph_cleaner)

            if graph_cleaner.can_clean:
                if graph_cleaner.unused_nodes_count:
                    graphs_cleaned_total += 1
            else:
                graphs_not_cleaned_total += 1

            if is_recursive:
                for node in graph.getNodes():
                    prop_graphs = get_node_property_graphs(
                        node=node, graph_id=graph_id)
                    for key, value in prop_graphs.items():
                        prop_graph_cleaner = GraphCleaner(value, key)
                        cleaners.add(prop_graph_cleaner)
                        if prop_graph_cleaner.can_clean:
                            if prop_graph_cleaner.unused_nodes_count:
                                subgraphs_cleaned_total += 1
                        else:
                            graphs_not_cleaned_total += 1

                    if bool(node.getDefinition()) and node.getDefinition().getId() == "sbs::compositing::fxmaps":
                        fx_map_graph = node.getReferencedResource()
                        fx_map_cleaner = GraphCleaner(
                            graph=fx_map_graph, graph_id=f"({graph_id}) FX-Map")
                        cleaners.add(fx_map_cleaner)
                        if fx_map_cleaner.can_clean:
                            if fx_map_cleaner.unused_nodes_count:
                                subgraphs_cleaned_total += 1
                        else:
                            graphs_not_cleaned_total += 1

                        for fx_map_node in fx_map_graph.getNodes():
                            prop_graphs = get_node_property_graphs(
                                node=fx_map_node, graph_id=f"{graph_id} - FX-Map")
                            for key, value in prop_graphs.items():
                                fx_map_prop_graph_cleaner = GraphCleaner(
                                    graph=value, graph_id=key)
                                cleaners.add(fx_map_prop_graph_cleaner)
                                if fx_map_prop_graph_cleaner.can_clean:
                                    if fx_map_prop_graph_cleaner.unused_nodes_count:
                                        subgraphs_cleaned_total += 1
                                else:
                                    graphs_not_cleaned_total += 1

    for cleaner in cleaners:
        if cleaner:
            nodes_removed_total += cleaner.unused_nodes_count

    progress_dialog.can_close = True
    progress_dialog.reset()
    del progress_dialog

    completion_dialog = ui_setup.CompletionDialog(
        ui_mgr=ui_mgr,
        cleaned_nodes_count=nodes_removed_total,
        cleaned_subgraphs_count=subgraphs_cleaned_total,
        cleaned_graphs_count=graphs_cleaned_total,
        not_cleaned_graphs_count=graphs_not_cleaned_total,
        from_explorer=True
    )
    completion_dialog.exec()
