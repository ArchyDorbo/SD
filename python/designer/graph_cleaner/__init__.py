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


##########################################################################
# CLEAN GRAPH PLUGIN FOR ADOBE SUBSTANCE 3D DESIGNER
# ___________________
# This plugin adds a tool in the Explorer and Graph View toolbars
# to remove unused nodes in graphs, regardless of graph type.
# A node is detected as unused if it is not a part of a stream which
# ends in an output node.
# Nodes that contribute to the graph's interface are ignored:
#   - Input nodes in compositing graphs
#   - Exposed nodes in MDL and model graphs
##########################################################################

import sd
from sd.api import qtforpythonuimgrwrapper, sdgraph, sdpackage, sdresourcefolder
from sd.api.sbs import sdsbscompgraph

from functools import partial
import logging

from . import ui_setup

#
# Initialize logger for the submodule.
#

logger = logging.getLogger("GraphCleaner")
logger.addHandler(sd.getContext().createRuntimeLogHandler())
logger.propagate = False
logger.setLevel(logging.DEBUG)


#
# Globals.
#

APP = sd.getContext().getSDApplication()
UI_MGR = APP.getQtForPythonUIMgr()
PKG_MGR = APP.getPackageMgr()
GRAPH_CREATED_CALLBACK_ID_SET = set()
EXPLORER_CREATED_CALLBACK_ID_SET = set()
EXPLORER_SELECTION_CHANGED_CALLBACK_ID_SET = set()


#
# Callbacks.
#

def on_new_graph_view_created(
        graph_view_id: int,
        ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper
) -> None:
    """
    Function called when a new Graph View is created.

    :param graph_view_id: The identifier of the graph loaded in the new Graph View.
    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    :return: None
    """

    graph_cleaner_action = ui_setup.GraphViewCleanAction(ui_mgr=ui_mgr)
    ui_mgr.addActionToGraphViewToolbar(graph_view_id, graph_cleaner_action)


def on_explorer_created(
        explorer_id: int,
        ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper
) -> None:
    """
    Function called when a new Explorer view is created.

    :param explorer_id: The identifier of the new Explorer view
    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    :return: None
    """

    graph_cleaner_action = ui_setup.ExplorerCleanAction(ui_mgr=ui_mgr)
    ui_mgr.addActionToExplorerToolbar(explorer_id, graph_cleaner_action)

    EXPLORER_SELECTION_CHANGED_CALLBACK_ID_SET.add(ui_mgr.registerExplorerSelectionChangedCallback(partial(
        explorer_selection_changed,
        ui_mgr=ui_mgr,
        action=graph_cleaner_action,
        og_explorer_id=explorer_id
    )))

    explorer_selection_changed(
        explorer_id=explorer_id,
        ui_mgr=ui_mgr,
        action=graph_cleaner_action,
        og_explorer_id=explorer_id
    )


def explorer_selection_changed(
        explorer_id: int,
        ui_mgr: qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper,
        action: ui_setup.ExplorerCleanAction,
        og_explorer_id: int
) -> None:
    """
    Function called when the user selection changes in a specified Explorer view.

    :param explorer_id: The identifier of the target Explorer view.
    :param ui_mgr: The QtForPython UI manager wrapper object for the current context.
    :param action: The action that should react to the user selection change.
    :param og_explorer_id: The identifier of the original Explorer view, if one existed beforehand.
    :return: None.
    """

    graphs = set()
    graphs_children = set()
    graphs_comp = False
    packages = set()
    folders = set()

    if explorer_id != og_explorer_id:
        return None
    selection = ui_mgr.getExplorerSelection(explorer_id)

    if selection:
        for item in selection:
            if isinstance(item, sdgraph.SDGraph):
                graphs.add(item)
                if isinstance(item, sdsbscompgraph.SDSBSCompGraph):
                    graphs_comp = True
            if isinstance(item, sdpackage.SDPackage):
                packages.add(item)
                for content in item.getChildrenResources(isRecursive=True):
                    if isinstance(content, sdgraph.SDGraph):
                        graphs_children.add(content)
                        if isinstance(content, sdsbscompgraph.SDSBSCompGraph):
                            graphs_comp = True
            elif isinstance(item, sdresourcefolder.SDResourceFolder):
                folders.add(item)
                for content in item.getChildren(isRecursive=True):
                    if isinstance(content, sdgraph.SDGraph):
                        graphs_children.add(content)
                        if isinstance(content, sdsbscompgraph.SDSBSCompGraph):
                            graphs_comp = True

    action.explorer_selection = {
        "graphs": graphs,
        "graphs_comp": graphs_comp,
        "graphs_children": graphs_children,
        "packages": packages,
        "folders": folders
    }

    action.update_menu_actions()


#
# Initialize / uninitialize module.
#

def initializeGraphCleaner():
    # Do nothing if we don't have an UI.
    if not UI_MGR:
        return

    GRAPH_CREATED_CALLBACK_ID_SET.add(UI_MGR.registerGraphViewCreatedCallback(
        partial(on_new_graph_view_created, ui_mgr=UI_MGR)
    ))

    EXPLORER_CREATED_CALLBACK_ID_SET.add(UI_MGR.registerExplorerCreatedCallback(
        partial(on_explorer_created, ui_mgr=UI_MGR)
    ))

    logger.debug("Registered clean graph actions")


def uninitializeGraphCleaner():
    # Do nothing if we don't have an UI.
    if not UI_MGR:
        return

    for callback_id in GRAPH_CREATED_CALLBACK_ID_SET:
        UI_MGR.unregisterCallback(callback_id)

    for callback_id in EXPLORER_CREATED_CALLBACK_ID_SET:
        UI_MGR.unregisterCallback(callback_id)

    for callback_id in EXPLORER_SELECTION_CHANGED_CALLBACK_ID_SET:
        UI_MGR.unregisterCallback(callback_id)

    logger.debug("Unregistered clean graph actions")
