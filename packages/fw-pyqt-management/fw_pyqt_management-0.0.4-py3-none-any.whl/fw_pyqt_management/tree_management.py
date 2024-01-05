"""Tree Management."""
import functools
import logging
import os
import platform
import shutil
import subprocess
import threading
import webbrowser
from pathlib import Path, WindowsPath

import xmltodict

from .adaptive_qt import (
    CustomContextMenu,
    NoEditTriggers,
    QApplication,
    QMenu,
    QMessageBox,
    WaitCursor,
)
from .fw_container_items import (
    AcquisitionItem,
    AnalysisFolderItem,
    AnalysisItem,
    CollectionItem,
    ContainerItem,
    ContainerParentModel,
    FileItem,
    GroupItem,
    HierarchyItem,
    ProjectItem,
    SessionItem,
    SubjectItem,
)

log = logging.getLogger(__name__)


def run_in_other_thread(function):
    """Run a function in a separate thread.

    webbrowser.open and os.startfile cause 3D Slicer to crash in Windows if called
    from the main thread. This function runs the function in a separate thread,
    preventing the crash.

    source: https://maprantala.com/2014/12/31/calling-os.startfile-and-webbrowser.open-from-arcgis/

    Args:
        function (function): Function to run in a separate thread.

    Returns:
        function: Function handler.
    """

    @functools.wraps(function)
    def fn_(*args, **kwargs):
        thread = threading.Thread(target=function, args=args, kwargs=kwargs)

        thread.start()

        thread.join()

    return fn_


def no_op():
    """This function does nothing."""
    pass


# Windows allow reduires the following to open a folder in another thread.
if platform.system() == "Windows":
    startfile = run_in_other_thread(os.startfile)
# Define it as a no-op (no operations) for testing with other OSs.
else:
    startfile = no_op
# All OS require the following to open a browser in another thread.
open_browser = run_in_other_thread(webbrowser.open)


class TreeManagement:
    """Class that coordinates all tree-related functionality."""

    def __init__(  # noqa: PLR0913
        self,
        fw_client,
        tree_view,
        cache_dir,
        icon_dir=None,
        paired_file_types=None,
        selection_mode=None,
    ):
        """Initialize the TreeManagement class.

        NOTE: Each of these parameters needs to be explicity changed after initialization
              E.g. TreeManagement.set_fw_client(fw_client)

        Args:
            fw_client (object): The Flywheel client object.
            tree_view (object): The PyQt tree view object.
            cache_dir (str): The directory path for caching files.
            icon_dir (str, optional): The directory path for icons. Defaults to None.
            paired_file_types (dict, optional): The dictionary of paired file types. Defaults to None.
            selection_mode (int, optional): The selection mode for the tree view. Defaults to None.
        """
        log.debug("Init TreeManagement")
        self.set_fw_client(fw_client)
        self.tree_view = tree_view
        self.current_item = None
        self.cache_files = {}
        self.cache_dir = cache_dir

        if paired_file_types:
            self.paired_file_types = paired_file_types
        else:
            self.paired_file_types = {}

        if icon_dir is None:
            self.icon_dir = Path(__file__).parent / "resources" / "icons"
        else:
            self.icon_dir = icon_dir

        if selection_mode is not None:
            self.tree_view.selectionMode = selection_mode

        self.tree_view.setEditTriggers(NoEditTriggers)
        self.tree_view.clicked.connect(self.tree_clicked)
        self.tree_view.doubleClicked.connect(self.tree_dblclicked)
        self.tree_view.expanded.connect(self.on_expanded)

        self.tree_view.setContextMenuPolicy(CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.open_menu)
        self.source_model = ContainerParentModel()
        # The cache directory is cascaded to the individual item objects.
        self.set_cache_dir(cache_dir)
        self.tree_view.setModel(self.source_model)

        HierarchyItem.set_icon_dir(self.icon_dir)

    def set_fw_client(self, fw_client):
        """Set the fw_client property and cascade to the tree source model.

        Args:
            fw_client (flywheel.Client): The fw_client to set.
        """
        self.fw_client = fw_client
        self.set_instance()

    def set_instance(self, instance=None):
        """Set the instance property and cascade to the tree source model.

        Args:
            instance (str, optional): The instance to set. Defaults to None.
        """
        if instance is None:
            if self.fw_client:
                config = self.fw_client.get_config()
                # with config["site"]["api_url"] having form
                # https://instance.flywheel.io/api
                self.instance = config["site"]["api_url"].split("/")[2]
            else:
                self.instance = None
        else:
            self.instance = instance

    def set_cache_dir(self, cache_dir):
        """Set the cache_dir property and cascade to the tree source model.

        Args:
            cache_dir (Path): The cache_dir to set.
        """
        self.cache_dir = Path(cache_dir)
        if isinstance(self.cache_dir, WindowsPath) and "\\\\?\\" not in str(
            self.cache_dir
        ):
            self.cache_dir = Path("\\\\?\\" + str(self.cache_dir))
        self.source_model.set_cache_dir(self.cache_dir)

    def get_cache_dir(self):
        """Get the cache_dir property.

        Returns:
            Path: Get the cache_dir property.
        """
        return self.cache_dir

    def tree_clicked(self, index):
        """Cascade the tree clicked event to relevant tree node items.

        Args:
            index (QtCore.QModelIndex): Index of tree item clicked.
        """
        item = self.get_id(index)
        if isinstance(item, ContainerItem):
            self.current_item = item

    def tree_dblclicked(self, index):
        """Cascade the double clicked signal to the tree node double clicked.

        Args:
            index (QtCore.QModelIndex): Index of tree node double clicked.
        """
        item = self.get_id(index)
        if isinstance(item, AnalysisFolderItem):
            item._dblclicked()

    def populate_tree(self):
        """Populate the tree starting with groups.

        NOTE: This is never used in the current implementation.
        """
        groups = self.fw_client.groups()
        for group in groups:
            _ = GroupItem(self.source_model, group)
        self.tree_view.setEnabled(True)
        self.expand_all_visible_items()

    def expand_all_visible_items(self):
        """Expand all visible items in the tree."""
        proxy = self.source_model
        for row in range(proxy.rowCount()):
            index = proxy.index(row, 0)
            self.tree_view.expand(index)

    def populate_tree_from_collection(self, collection):
        """Populate Tree from a single Collection.

        Args:
            collection (flywheel.Collection): Collection to populate tree with.

        Returns:
            CollectionItem: Returns the CollectionItem object.
        """
        collection_item = CollectionItem(self.source_model, collection)
        self.tree_view.setEnabled(True)
        self.expand_all_visible_items()

        return collection_item

    def populate_tree_from_project(self, project):
        """Populate Tree from a single Project.

        Args:
            project (flywheel.Project): Project to populate tree with.

        Returns:
            ProjectItem: Returns the ProjectItem object.
        """
        project_item = ProjectItem(self.source_model, project)
        self.tree_view.setEnabled(True)
        self.expand_all_visible_items()

        return project_item

    def get_id(self, index):
        """Retrieve the tree item from the selected index.

        Args:
            index (QtCore.QModelIndex): Index from selected tree node.

        Returns:
            QtGui.QStandardItem: Returns the item with designated index.
        """
        item = self.source_model.itemFromIndex(index)
        # id = item.data()
        # I will want to move this to "clicked" or "on select"
        # self.ui.txtID.setText(id)
        return item

    def instance_container_url(self, container_item):
        """Provide a complete URL to the new Analysis.

        Returns:
            str: URL to the new Analysis on the instance.
        """
        if isinstance(container_item, ProjectItem):
            project_id = container_item.container.id
            container_url = f"https://{self.instance}/#/projects/{project_id}"
        elif isinstance(container_item, CollectionItem):
            collection_id = container_item.container.id
            container_url = f"https://{self.instance}/#/collections/{collection_id}"
        else:
            project_id = container_item.container.parents["project"]
            container_url = f"https://{self.instance}/#/projects/{project_id}/"
            if isinstance(container_item, SubjectItem):
                subject_id = container_item.container.id
                container_url += f"subjects/{subject_id}"
            elif isinstance(container_item, SessionItem):
                session_id = container_item.container.id
                container_url += f"sessions/{session_id}"
            elif isinstance(container_item, AcquisitionItem):
                session_id = container_item.container.parents["session"]
                container_url += f"sessions/{session_id}"
            elif isinstance(container_item, AnalysisItem):
                session_id = container_item.container.parents["session"]
                container_url += f"sessions/{session_id}?tab=analysis"
            # Else leave it at the default session level
            else:
                session_id = container_item.container.parents["session"]
                container_url += f"sessions/{session_id}"

        return container_url

    def open_menu(self, position):
        """Function to manage context menus.

        Args:
            position (QtCore.QPoint): Position right-clicked and where menu rendered.
        """
        indexes = self.tree_view.selectedIndexes()
        if len(indexes) > 0:
            has_file = False
            is_browsable = False
            is_cached = True
            for index in indexes:
                item = self.source_model.itemFromIndex(index)
                if isinstance(item, FileItem):
                    has_file = True
                    is_cached *= item._is_cached()
                elif isinstance(
                    item, (ProjectItem, SubjectItem, SessionItem, CollectionItem)
                ):
                    is_browsable = True

            menu = QMenu()
            if has_file:
                if is_cached:
                    action = menu.addAction("Open Containing Folder")
                    action.triggered.connect(self._open_containing_folder)
                else:
                    action = menu.addAction("Cache Selected Files")
                    action.triggered.connect(self._cache_selected)
            elif is_browsable:
                action = menu.addAction("View on Instance")
                action.triggered.connect(self._view_on_instance)

            menu.exec(self.tree_view.viewport().mapToGlobal(position))

    def _view_on_instance(self):
        """View the selected items on the instance."""
        # only use the first valid selected item
        if self.tree_view.selectedIndexes():
            index = self.tree_view.selectedIndexes()[0]
            item = self.source_model.itemFromIndex(index)
            view_url = self.instance_container_url(item)
            open_browser(view_url)

    def _cache_selected(self):
        """Cache selected files to local directory."""
        # TODO: Acknowledge this is for files only or change for all files of selected
        #       Acquisitions.
        try:
            QApplication.setOverrideCursor(WaitCursor)

            indexes = self.tree_view.selectedIndexes()
            if len(indexes) > 0:
                for index in indexes:
                    item = self.source_model.itemFromIndex(index)
                    if isinstance(item, FileItem):
                        item._add_to_cache()
                # Cascade cache directory to update cache status of all files in all parents
                self.source_model.set_cache_dir(self.cache_dir)
        except Exception as exc:
            log.exception(exc)
        finally:
            QApplication.restoreOverrideCursor()

    def _open_containing_folder(self):
        """Open containing folder of selected file."""
        indexes = self.tree_view.selectedIndexes()
        if len(indexes) > 0:
            for index in indexes:
                item = self.source_model.itemFromIndex(index)
                if isinstance(item, FileItem) and item._is_cached():
                    self._open_folder(item._get_cache_path().parent)

    def _open_folder(self, path):
        if platform.system() == "Windows":
            startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", path])

    def on_expanded(self, index):
        """Triggered on the expansion of any tree node.

        Used to populate subtree on expanding only.  This significantly speeds up the
        population of the tree.

        Args:
            index (QtCore.QModelIndex): Index of expanded tree node.
        """
        item = self.source_model.itemFromIndex(index)
        if hasattr(item, "_on_expand"):
            item._on_expand()

    def _is_data_file(self, file_item):
        """Check if a file is the data part of a header/data pair.

        Args:
            file_item (FileItem): File Item to check the extension of.

        Returns:
            bool: True or False
        """
        file_ext = file_item.file.name.split(".")[-1]
        data_types_temp = list(self.paired_file_types.values())
        data_types = []
        for x in data_types_temp:
            if isinstance(x, list):
                data_types.extend(x)
            else:
                data_types.append(x)

        if file_ext in data_types:
            return True
        else:
            return False

    def _is_paired_type(self, file_item):
        """Determine if this file is of a paired type.

        Args:
            file_item (FileItem): File item to test if it has a data pair.

        Returns:
            bool: True or False of paired type.
        """
        return file_item.container.name.split(".")[-1] in self.paired_file_types.keys()

    def _get_paired_file_items(self, file_item):
        """Get the pairs of current file, if they exists.

        self.paired_file_types accommodates for multiple specified data formats from a
        single header file (e.g. .mhd can refer to a .raw or .zraw).

        TODO: Resolve the data file directly from the header file.
              Some header types may not open without data (Analyze).

        Args:
            file_item (FileItem): File item to test if it has a data pair.

        Returns:
            list: List of paired FileItems or empty list
        """
        parent_container = file_item.file.parent
        all_file_names = [fl.name for fl in parent_container.files]

        fl_ext = file_item.container.name.split(".")[-1]
        # this can be a single string or a list of strings
        paired_ext = self.paired_file_types[fl_ext]
        paired_file_base_name = file_item.container.name[: -len(fl_ext)]
        # if it is a string, make it a list
        if isinstance(paired_ext, str):
            paired_ext = [paired_ext]

        # for a list of possible paired file names.
        possible_paired_file_names = [paired_file_base_name + ext for ext in paired_ext]

        # cache the first possible match.
        # TODO: We may have to open the header to find the name. There are headers that
        #       This would not work for (e.g. Analyze files)
        intersection_list = list(
            set(possible_paired_file_names).intersection(all_file_names)
        )
        paired_file_items = []
        for paired_file_name in intersection_list:
            paired_file_items.append(
                FileItem(None, parent_container.get_file(paired_file_name))
            )

        if not paired_file_items:
            msg = f"The pairs for {file_item.file.name} cannot be found."
            log.info(msg)

        return paired_file_items

    def _process_mrml_storage_node(self, parent_item, node):  # noqa: PLR0912
        """Cache file item related to mrml storage node, if found in parent item.

        Args:
            parent_item (FolderItem): Folder item containing siblings of node
            node (dict): Dictionary representation of mrml node.

        Returns:
            bool: Success or failure of finding and caching mrml storage node.
        """
        # list all files under the container FolderItem in question
        all_file_names = [
            parent_item.child(i).file.name for i in range(parent_item.rowCount())
        ]
        # Use the file name at the end of the possible path
        dep_file_path = Path(node["@fileName"])
        dep_file_name = dep_file_path.name
        if dep_file_name in all_file_names:
            dep_index = all_file_names.index(dep_file_name)
            dep_item = parent_item.child(dep_index)
            # Cache file without explicitly opening in Slicer
            _, _ = dep_item._add_to_cache()
            if self._is_paired_type(dep_item):
                paired_items = self._get_paired_file_items(dep_item)
                for paired_item in paired_items:
                    _, _ = paired_item._add_to_cache()
        # If the file is not found in the parent item, look for another parent container
        # if the file path has depth greater than 2 (container_id/file_id/file_name)
        elif (
            node.get("@attributes") and "parent_container_id" in node.get("@attributes")
        ) or len(dep_file_path.parts) > 2:
            if node.get("@attributes") and "parent_container_id" in node.get(
                "@attributes"
            ):
                attributes = dict(
                    tuple(x.split(":")) for x in node["@attributes"].split(";")
                )
                parent_container_id = attributes["parent_container_id"]
            else:
                parent_container_id = dep_file_path.parts[-2]
            parent_container = self.fw_client.get(parent_container_id)
            file_obj = parent_container.get_file(dep_file_name)
            if file_obj:
                dep_item = FileItem(None, file_obj)
                _, _ = dep_item._add_to_cache()
                if self._is_paired_type(dep_item):
                    paired_items = self._get_paired_file_items(dep_item)
                    for paired_item in paired_items:
                        _, _ = paired_item._add_to_cache()
            else:
                return False
        # The file may be a part of an Analysis Input
        elif isinstance(parent_item.parent(), AnalysisItem) and dep_file_name in [
            input.name for input in parent_item.parent().container._inputs
        ]:
            analysis_item = parent_item.parent()
            dep_item = analysis_item._add_input_to_cache(dep_file_name)
            if self._is_paired_type(dep_item):
                paired_items = self._get_paired_file_items(dep_item)
                for paired_item in paired_items:
                    _, _ = paired_item._add_to_cache()

        else:
            msg = (
                f"The mrml dependency file, {dep_file_name}, "
                "was not found in sibling files of the container."
            )
            log.info(msg)
            return False
        return True

    def _get_mrml_dependencies(self, file_item: FileItem):
        """Retrieve the MRML storage node dependencies from the sibling files.

        For more information on Medical Reality Modeling Language files see:
        https://slicer.readthedocs.io/en/v4.11/developer_guide/mrml_overview.html


        Args:
            file_item (FileItem): MRML File item to retrieve dependencies for.
        """
        # TODO: allow for cross-container dependencies.
        parent_item = file_item.parent()
        success = True
        with open(file_item._get_cache_path()) as f:
            mrml_data = xmltodict.parse(f.read())

        for key in mrml_data["MRML"].keys():
            # Storage nodes are represented on disk
            if key.endswith("Storage"):
                # The value will be node or a list of nodes
                # If the contents is a node (dict) put it in a list
                if isinstance(mrml_data["MRML"][key], dict):
                    mrml_data["MRML"][key] = [mrml_data["MRML"][key]]
                # Parse the list of storage nodes
                for node in mrml_data["MRML"][key]:
                    # TODO: Warn if the node cannot be retrieved from the parent item
                    # Replace %20 with a space character
                    node["@fileName"] = node["@fileName"].replace("%20", " ")
                    success *= self._process_mrml_storage_node(parent_item, node)
        return success

    def cache_item_dependencies(self, file_item):
        """Cache the dependencies of file_item.

        Dependencies include:
            Paired files
                files with a header-data pair
                - MetaImage header/data(.mhd/.raw)
                - Analyze header/data (.hdr/.img)
            MRML files with dependencies.
                - MRML files are a Slicer-specific XML format that can reference
                  multiple other files.

        Args:
            file_item (FileItem): A file item object to check for dependencies.

        Returns:
            bool: Success or failure of finding and caching item dependencies.
        """
        if self._is_paired_type(file_item):
            paired_file_items = self._get_paired_file_items(file_item)
            for paired_file_item in paired_file_items:
                # Paired file is cached without giving it to slicer to explicity open
                _, _ = paired_file_item._add_to_cache()
        if file_item.file.name.endswith(".mrml"):
            # TODO: If mrml is the output of Analysis, load Analysis inputs into
            #       the analysis folder directory.
            success = self._get_mrml_dependencies(file_item)
            if not success:
                msg = (
                    f"One or more file dependencies for {file_item.file.name} cannot "
                    "be found. Do you wish to continue?"
                )
                log.info(msg)

                result = QMessageBox.question(None, "File Dependency Error", msg)

                return result == QMessageBox.Yes

        return True

    def cache_selected_for_open(self):
        """Cache selected files if necessary for opening in application."""
        self.cache_files.clear()

        for index in self.tree_view.selectedIndexes():
            item = self.source_model.itemFromIndex(index)
            if isinstance(item, FileItem):
                # Ensure file is most recent version
                item._update_file_object()
                file_path, file_type = item._add_to_cache()
                # A file may have dependencies to cache
                # e.g. .mhdr/.raw or .mrml file
                success = self.cache_item_dependencies(item)

                if not success:
                    break

                # Don't add a file if it is a data file referenced by a header file
                if not self._is_data_file(item):
                    self.cache_files[item.container.id] = {
                        "file_path": str(file_path),
                        "file_type": file_type,
                    }

    def cache_uploaded_files(self, parent_container_item, uploaded_files):
        """Retain uploaded files in cache.

        Args:
            parent_container_item (ContainerItem): Parent container item of uploaded
                files
            uploaded_files (list): List of file paths.
        """
        # Parse through uploaded files
        for cache_file in uploaded_files:
            cache_file = Path(cache_file)
            if cache_file.exists():
                # Ensure that the container and the parent item have it
                file_obj = parent_container_item.container.get_file(cache_file.name)
                file_items = [
                    parent_container_item.files_folder_item.child(i)
                    for i in range(parent_container_item.files_folder_item.rowCount())
                    if parent_container_item.files_folder_item.child(i).file.name
                    == cache_file.name
                ]
                if file_obj and file_items:
                    # If container and parent item have the file
                    # create the directory, copy, and cache.
                    file_item = file_items[0]
                    file_path = file_item._get_cache_path()
                    file_path.parents[0].mkdir(parents=True, exist_ok=True)
                    shutil.copy(cache_file, file_path)
                    _, _ = file_item._add_to_cache()
