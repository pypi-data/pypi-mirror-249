"""Classes to represent the Flywheel Hierarchy in a navigable tree."""
import logging
import os
from abc import abstractmethod
from http.client import IncompleteRead
from pathlib import Path, WindowsPath

from requests.exceptions import ChunkedEncodingError

from .adaptive_qt import QtGui

log = logging.getLogger(__name__)

DOWNLOAD_RETRY_LIMIT = 5


def return_long_windows_path(path):
    r"""Return a WindowsPath with the long path prefix, if Windows is the OS.

    "\\\\?\\" is the long path prefix for Windows.

    Args:
        path (Path): Path to convert.

    Returns:
        WindowsPath: Path with the long path prefix.
    """
    if isinstance(path, WindowsPath) and "\\\\?\\" not in str(path):
        path = Path("\\\\?\\" + str(path))
    return path


class ContainerParentModel(QtGui.QStandardItemModel):
    """Model to carry the cache_dir property."""

    cache_dir = None

    def set_cache_dir(self, cache_dir):
        """Set the cache_dir property and cascade to all child items.

        Args:
            cache_dir (Path): The cache_dir to set.
        """
        # Set the cache_dir class property.
        ContainerParentModel.cache_dir = Path(cache_dir)
        # Cascade the cache_dir to all child items.
        if self.item(0):
            # Set the cache_dir property on the root item.
            # This will cascade to all child items using the class variable.
            self.item(0).set_cache_dir(ContainerParentModel.cache_dir)

    @classmethod
    def get_cache_dir(cls):
        """Get the cache_dir property.

        Returns:
            Path: Get the cache_dir property.
        """
        return cls.cache_dir


class HierarchyItem(QtGui.QStandardItem):
    """Base class for all hierarchy items."""

    # Set static class variables.
    cache_dir = None
    icon_dir = None

    def __init__(self, parent_item=None, name=""):
        """Initialize the item.

        Args:
            parent_item (QStandardItem, optional): Possible. Defaults to None.
            name (str): The name of the item.
        """
        super().__init__()
        self.parent_item = parent_item
        self.setText(name)
        if self.parent_item:
            self.set_cache_dir(self.parent_item.get_cache_dir())
            self.parent_item.appendRow(self)
        self._set_icon()

    @classmethod
    def set_icon_dir(cls, icon_dir):
        """Set the directory containing icons for the hierarchy items.

        Args:
            icon_dir (Path): The directory hosting icons.
        """
        if icon_dir:
            cls.icon_dir = Path(icon_dir)
        else:
            cls.icon_dir = None

    def _set_icon(self):
        """Set the icon for the hierarchy item."""
        if self.icon_dir and hasattr(self, "icon_path") and self.icon_path.exists():
            self.setIcon(QtGui.QIcon(str(self.icon_path)))

    def set_cache_dir(self, cache_dir):
        """Set the cache_dir property.

        Args:
            cache_dir (Path): The cache_dir to set.
        """
        # Set the cache_dir class property for all class instances.
        HierarchyItem.cache_dir = Path(cache_dir)
        self.recurse_is_cached(self)

    def get_cache_dir(self):
        """Get the cache_dir property.

        Returns:
            Path: Get the cache_dir property.
        """
        return return_long_windows_path(HierarchyItem.cache_dir)

    def __lt__(self, other):
        """Overload "<" operator to enable case-insensitive tree item sorting.

        Args:
            other (HierarchyItem): Item to compare.

        Returns:
            bool: True if self < other else False
        """
        return str.upper(self.text()) < str.upper(other.text())

    def recurse_is_cached(self, item):
        """Recurse through the hierarchy and update the cached status of all files.

        Args:
            item (HierarchyItem): The item to check.
        """
        if isinstance(item, FileItem):
            item._set_icon()
        for i in range(item.rowCount()):
            if item.child(i):
                self.recurse_is_cached(item.child(i))


class FolderItem(HierarchyItem):
    """Folder Items conveniently collapse long lists into a tree node."""

    def __init__(self, parent_item, folder_name):
        """Initialize Folder Items unpopulated.

        Args:
            parent_item (ContainerItem): Container Item parent for Folder Item.
            folder_name (str): A name for the folder item (e.g. SESSIONS).
        """
        if self.icon_dir and not hasattr(self, "icon_path"):
            self.icon_path = self.icon_dir / "folder.png"
        super().__init__(parent_item, folder_name)
        self.parent_container = parent_item.container
        self.folder_item = QtGui.QStandardItem()


class AnalysisFolderItem(FolderItem):
    """Folder Item specifically for analyses."""

    def __init__(self, parent_item):
        """Initialize AnalysisFolderItem unpopulated.

        Args:
            parent_item (ContainerItem): Container that hosts analyses
                (projects, subjects, sessions, acquisitions)
        """
        folder_name = "ANALYSES"
        if self.icon_dir:
            self.icon_path = self.icon_dir / "dwnld-folder.png"
        super().__init__(parent_item, folder_name)

        self.setToolTip("Double-Click to list Analyses.")

    def _dblclicked(self):
        if hasattr(self.parent_container, "analyses"):
            self.parent_container = self.parent_container.reload()
            if self.icon_dir:
                self.icon_path = self.icon_dir / "folder.png"
            self._set_icon()
            if not self.hasChildren() and self.parent_container.analyses:
                for analysis in self.parent_container.analyses:
                    AnalysisItem(self, analysis)


class ContainerItem(HierarchyItem):
    """TreeView node to host all common functionality for Flywheel containers."""

    files_folder_name = "FILES"

    def __init__(self, parent_item, container):
        """Initialize new container item with its parent and flywheel container object.

        Args:
            parent_item (QtGui.QStandardItem): Parent of this item to instantiate.
            container (flywheel.Container): Flywheel container (e.g. group, project,...)
        """
        container_name = container.label
        super().__init__(parent_item, container_name)
        self.analyses_folder_item = None
        self.child_container_folder_item = None
        self.files_folder_item = None

        if not hasattr(self, "has_analyses"):
            self.has_analyses = False
        self.container = container
        # List only the files folder before expanding.
        # This is required to have something to Expand to.
        # This allows a sort of container items not to affect the child folders.
        self._files_folder()
        self.setData(container.id)
        log.debug("Found %s %s", container.container_type, container.label)

    def _get_info(self):
        """Get the info of the container."""
        self.container = self.container.reload()
        return self.container.info

    def _files_folder(self):
        """Create a "FILES" folder if self.container has one."""
        folder_name = self.files_folder_name
        if hasattr(self.container, "files"):
            self.files_folder_item = FolderItem(self, folder_name)

    def _list_files(self):
        """List all file items of a container object under the "FILES" folder.

        TODO: Make this a part of a filesFolderItem???
        """
        if hasattr(self.container, "files"):
            if not self.files_folder_item.hasChildren() and self.container.files:
                for fl in self.container.files:
                    FileItem(self.files_folder_item, fl)
                self.files_folder_item.sortChildren(0)

    def _analyses_folder(self):
        """Create "ANALYSES" folder, if container has analyses object."""
        if hasattr(self.container, "analyses") and self.has_analyses:
            self.analyses_folder_item = AnalysisFolderItem(self)

    def _child_container_folder(self):
        """Create a folder with the name of the child containers (e.g. SESSIONS)."""
        if hasattr(self, "child_container_name"):
            self.child_container_folder_item = FolderItem(
                self, self.child_container_name
            )

    @abstractmethod
    def _list_child_containers(self):
        """Abstract method to list child containers."""

    def _on_expand(self):
        """On expansion of container tree node, list all files."""
        child_folder_names = [self.child(i).text() for i in range(self.rowCount())]

        if self.has_analyses and "ANALYSES" not in child_folder_names:
            self._analyses_folder()
        if (
            hasattr(self, "child_container_name")
            and self.child_container_name not in child_folder_names
        ):
            self._child_container_folder()
        self._list_files()

    def refresh_all(self):
        """Refresh the files, analyses, and child_containers of the given container."""
        # Reload the container
        self.container = self.container.reload()  # Remove all children files
        self.removeRows(0, self.rowCount())
        # Repopulate the top-level folders
        self._files_folder()
        self._analyses_folder()
        self._child_container_folder()

        # Repopulate the child folders
        self._list_files()
        self._list_child_containers()
        if hasattr(self.container, "analyses") and self.has_analyses:
            self.analyses_folder_item._dblclicked()

    def refresh_files(self):
        """Refresh the files of the given container."""
        # Reload the container
        self.container = self.container.reload()
        # Remove all children files
        self.files_folder_item.removeRows(0, self.files_folder_item.rowCount())
        # Repopulate the list of files
        self._list_files()

    def refresh_analyses(self):
        """Refresh the analyses of the given container."""
        if hasattr(self.container, "analyses") and self.has_analyses:
            # Reload the container
            self.container = self.container.reload()
            # Remove all children analyses
            self.analyses_folder_item.removeRows(
                0, self.analyses_folder_item.rowCount()
            )
            # Repopulate the list of analyses
            self.analyses_folder_item._dblclicked()

    def refresh_child_container_folder(self):
        """Refresh the sub-containers of the given container."""
        if hasattr(self, "child_container_name"):
            # Reload the container
            self.container = self.container.reload()
            # Remove all children files
            self.child_container_folder_item.removeRows(
                0, self.child_container_folder_item.rowCount()
            )
            # This could be an abstract function:
            self._list_child_containers()

    def _get_cache_path(self):
        """Construct cache path of container (e.g. cache_root/group/.../container_id/).

        Returns:
            pathlib.Path: Cache Path to container indicated.
        """
        container_path = self.get_cache_dir()

        for par in [
            "group",
            "project",
            "subject",
            "session",
            "acquisition",
            "analysis",
        ]:
            if (
                hasattr(self.container, "parents")
                and self.container.parents
                and self.container.parents.get(par)
            ):
                container_path /= self.container.parents[par]
        # If this container does not have parents it is a
        # Group, Collection, or Collection file.
        # If it has the "parents" attribute, it is a Collection FileItem
        if hasattr(self.container, "parents") and not self.container.parents:
            # If this is a Collection FileItem, the container is the file itself.
            # the below line reflects the need to have the collection id as the parent
            # of the file in the cache.
            # e.g self.{FolderItem}.{CollectionItem}.container.id
            container_path /= self.parent_item.parent_item.container.id
        container_path /= self.container.id
        return container_path


class GroupItem(ContainerItem):
    """TreeView Node for the functionality of group containers."""

    def __init__(self, parent_item, group):
        """Initialize Group Item with parent and group container.

        Args:
            parent_item (QtGui.QStandardItemModel): Top-level tree item or model.
            group (flywheel.Group): Flywheel group container to attach as tree node.
        """
        if self.icon_dir:
            self.icon_path = self.icon_dir / "group.png"
        self.child_container_name = "PROJECTS"
        self.group = group
        super().__init__(parent_item, group)

    def _list_projects(self):
        """Populate with flywheel projects."""
        if not self.child_container_folder_item.hasChildren():
            for project in self.group.projects():
                ProjectItem(self.child_container_folder_item, project)

    def _list_child_containers(self):
        """Override for abstract method."""
        self._list_projects()

    def _on_expand(self):
        """On expansion of group tree node, list all projects."""
        super()._on_expand()
        self._list_projects()


class CollectionItem(ContainerItem):
    """TreeView Node for the functionality of Collection containers."""

    def __init__(self, parent_item, collection):
        """Initialize Collection Item with parent and collection container.

        Args:
            parent_item (FolderItem): The folder item tree node that is the parent.
            collection (flywheel.Collection): Flywheel collection container to attach as
                tree node.
        """
        if self.icon_dir:
            self.icon_path = self.icon_dir / "collection.png"
        self.child_container_name = "SESSIONS"
        # Collections do not have accessible Analyses
        self.has_analyses = False
        super().__init__(parent_item, collection)
        self.collection = self.container

    def _list_sessions(self):
        """Populate with flywheel sessions."""
        if not self.child_container_folder_item.hasChildren():
            for session in self.collection.sessions():
                SessionItem(self.child_container_folder_item, session)
            self.child_container_folder_item.sortChildren(0)

    def _list_child_containers(self):
        """Override for abstract method."""
        self._list_sessions()

    def _on_expand(self):
        """On expansion of project tree node, list all sessions."""
        super()._on_expand()
        self._list_sessions()


class ProjectItem(ContainerItem):
    """TreeView Node for the functionality of Project containers."""

    def __init__(self, parent_item, project):
        """Initialize Project Item with parent and project container.

        Args:
            parent_item (FolderItem): The folder item tree node that is the parent.
            project (flywheel.Project): Flywheel project container to attach as tree
                node.
        """
        if self.icon_dir:
            self.icon_path = self.icon_dir / "project.png"
        self.child_container_name = "SUBJECTS"
        self.has_analyses = True
        super().__init__(parent_item, project)
        self.project = self.container

    def _list_subjects(self):
        """Populate with flywheel subjects."""
        if not self.child_container_folder_item.hasChildren():
            for subject in self.project.subjects():
                SubjectItem(self.child_container_folder_item, subject)
            self.child_container_folder_item.sortChildren(0)

    def _list_child_containers(self):
        """Override for abstract method."""
        self._list_subjects()

    def _on_expand(self):
        """On expansion of project tree node, list all subjects."""
        super()._on_expand()
        self._list_subjects()


class SubjectItem(ContainerItem):
    """TreeView Node for the functionality of Subject containers."""

    def __init__(self, parent_item, subject):
        """Initialize Subject Item with parent and project container.

        Args:
            parent_item (FolderItem): The folder item tree node that is the parent.
            subject (flywheel.Subject): Flywheel subject container to attach as tree
                node.
        """
        if self.icon_dir:
            self.icon_path = self.icon_dir / "subject.png"
        self.child_container_name = "SESSIONS"
        self.has_analyses = True
        super().__init__(parent_item, subject)
        self.subject = self.container

    def _list_sessions(self):
        """Populate with flywheel sessions."""
        if not self.child_container_folder_item.hasChildren():
            for session in self.subject.sessions():
                SessionItem(self.child_container_folder_item, session)
            self.child_container_folder_item.sortChildren(0)

    def _list_child_containers(self):
        """Override for abstract method."""
        self._list_sessions()

    def _on_expand(self):
        """On expansion of subject tree node, list all sessions."""
        super()._on_expand()
        self._list_sessions()


class SessionItem(ContainerItem):
    """TreeView Node for the functionality of Session containers."""

    def __init__(self, parent_item, session):
        """Initialize Session Item with parent and subject container.

        Args:
            parent_item (FolderItem): The folder item tree node that is the parent.
            session (flywheel.Session): Flywheel session container to attach as tree
                node.
        """
        if self.icon_dir:
            self.icon_path = self.icon_dir / "session.png"
        self.child_container_name = "ACQUISITIONS"
        self.has_analyses = True
        super().__init__(parent_item, session)
        self.session = self.container

    def _list_acquisitions(self):
        """Populate with flywheel acquisitions."""
        if not self.child_container_folder_item.hasChildren():
            for acquisition in self.session.acquisitions():
                AcquisitionItem(self.child_container_folder_item, acquisition)
            self.child_container_folder_item.sortChildren(0)

    def _list_child_containers(self):
        """Override for abstract method."""
        self._list_acquisitions()

    def _on_expand(self):
        """On expansion of session tree node, list all acquisitions."""
        super()._on_expand()
        self._list_acquisitions()


class AcquisitionItem(ContainerItem):
    """TreeView Node for the functionality of Acquisition containers."""

    def __init__(self, parent_item, acquisition):
        """Initialize Acquisition Item with parent and Acquisition container.

        Args:
            parent_item (FolderItem): The folder item tree node that is the parent.
            acquisition (flywheel.Acquisition): Flywheel acquisition container to attach
                as tree node.
        """
        if self.icon_dir:
            self.icon_path = self.icon_dir / "acquisition.png"
        self.has_analyses = True
        super().__init__(parent_item, acquisition)
        self.acquisition = self.container

    def _list_child_containers(self):
        """Override for abstract method."""
        return


class AnalysisItem(ContainerItem):
    """TreeView Node for the functionality of Analysis objects."""

    def __init__(self, parent_item, analysis):
        """Initialize Subject Item with parent and analysis object.

        Args:
            parent_item (FolderItem): The folder item tree node that is the parent.
            analysis (flywheel.Analysis): Flywheel analysis object to attach as tree
                node.
        """
        self.files_folder_name = "OUTPUT FILES"
        if self.icon_dir:
            self.icon_path = self.icon_dir / "analysis.png"
        super().__init__(parent_item, analysis)
        self._input_files_folder()
        self.sortChildren(0)

    def _list_child_containers(self):
        """Override for abstract method."""
        return

    def _input_files_folder(self):
        """Create an "INPUT FILES" folder if self.container has one."""
        folder_name = "INPUT FILES"
        if hasattr(self.container, "inputs"):
            self.input_files_folder_item = FolderItem(self, folder_name)

    def _list_input_files(self):
        """List all input files used by an Analysis.

        TODO: Make this a part of a filesFolderItem???
        """
        if hasattr(self.container, "inputs"):
            if not self.input_files_folder_item.hasChildren() and self.container.inputs:
                for fl in self.container.inputs:
                    FileItem(self.input_files_folder_item, fl)
                self.input_files_folder_item.sortChildren(0)

    def _on_expand(self):
        """On expansion of container tree node, list all files."""
        # If input and output folder exists, list all child folders.
        if self.rowCount() <= 2:
            self._list_files()
            self._list_input_files()

    def _add_input_to_cache(self, input_file_name):
        """Add input file to cache.

        Args:
            input_file_name (str): Name of input file to add to cache.

        Returns:
            fileItem: Returns the fileItem that was added to the cache or None.
        """
        if hasattr(self.container, "_inputs"):
            for i in range(self.input_files_folder_item.rowCount()):
                file_item = self.input_files_folder_item.child(i)
                if file_item.file.name == input_file_name:
                    file_item._add_to_cache()
                    return file_item

        return None


class FileItem(ContainerItem):
    """TreeView Node for the functionality of File objects."""

    def __init__(self, parent_item, file_obj):
        """Initialize File Item with parent and file object.

        Args:
            parent_item (FolderItem): The folder item tree node that is the parent.
            file_obj (flywheel.FileEntry): File object of the tree node.
        """
        # TODO: Do we want to put a label on the filename to indicate version?
        #       i.e. (i) for i>1?
        if file_obj.version > 1:
            file_obj.label = file_obj.name + f" ({file_obj.version})"
        else:
            file_obj.label = file_obj.name
        self.parent_item = parent_item
        self.container = file_obj
        self.file = file_obj
        self.file_type = file_obj.type

        if self.icon_dir:
            self.icon_path = self.icon_dir / "file.png"
        super().__init__(parent_item, file_obj)

        self._set_icon()

    def _list_child_containers(self):
        """Override for abstract method."""
        return

    def _set_icon(self):
        if self._is_cached():
            if self.icon_dir:
                self.icon_path = self.icon_dir / "file_cached.png"
            self.setToolTip("File is cached.")
        else:
            if self.icon_dir:
                self.icon_path = self.icon_dir / "file.png"
            self.setToolTip("File is not cached")

        super()._set_icon()

    def _get_cache_path(self):
        """Construct cache path of file (e.g. cache_root/group/.../file_id/file_name).

        Returns:
            pathlib.Path: Cache Path to file indicated.
        """
        file_path = super()._get_cache_path()
        file_path /= self.container.name
        return file_path

    def create_symlink(self, file_path):
        """Create a symbolic link to the file in its parent container directory.

        This provides single-directory access to all files under a particular container.
        The latest version gets the symbolic link.
        Otherwise, each file is cached to a file_id directory that is based on version.

        NOTE: For this to work on Windows Developer Mode must be enabled or
                the application must be run "As Administrator".

        TODO: This can be improved to make a copy if symbolic link fails.
              Make a setting in the ancestor class to control this.

        Args:
            file_path (pathlib.Path): Path to file to link to.
        """
        symlink_path = file_path.parent.parent / file_path.name
        if symlink_path.exists():
            os.remove(symlink_path)
        symlink_path.symlink_to(file_path)
        return symlink_path

    def _is_cached(self):
        """Check if file is cached.

        Returns:
            bool: If file is cached locally on disk.
        """
        return self._get_cache_path().exists()

    def _update_file_object(self):
        """Update file object with latest version from server."""
        file_parent = self.container.parent
        file_parent = file_parent.reload()
        file_obj = [fl for fl in file_parent.files if fl.name == self.file.name]
        if file_obj:
            file_obj = file_obj[0]
        else:
            # TODO: Handle this better. May need to delete the file from the tree.
            file_obj = self.file
        # If the cached file version is different, update our displayed file object
        if file_obj.version != self.file.version:
            file_obj.label = file_obj.name
            if file_obj.version > 1:
                file_obj.label += f" ({file_obj.version})"
            self.file = file_obj
            self.file_type = file_obj.type
            self.container = self.file
            self.setData(self.container.id)
            self.setText(self.file.label)
            self._set_icon()

    def _add_to_cache(self):
        """Add file to cache directory under path.

        Returns:
            pathlib.Path: Path to file in cache.
        """
        self._update_file_object()
        file_parent = self.container.parent
        file_path = self._get_cache_path()

        if not file_path.exists():
            msg = f"Downloading file: {self.file.name}"
            log.info(msg)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # TODO: Incorporate the below into the fw_tree_hierarchy repo
            download_success = False
            download_retries = 0
            while not download_success:
                try:
                    file_parent.download_file(self.file.name, str(file_path))
                    download_success = True
                except (
                    ConnectionResetError,
                    IncompleteRead,
                    ChunkedEncodingError,
                ) as e:
                    log.exception(e)
                    download_retries += 1
                    if download_retries >= DOWNLOAD_RETRY_LIMIT:
                        log.error(
                            "Download failed after %s retries.", DOWNLOAD_RETRY_LIMIT
                        )
                        return None, None
                    log.error("Retrying download.")
        else:
            msg = f"File already downloaded: {self.file.name}"
            log.info(msg)
        # on any caching, ensure icon is set
        if self.icon_dir:
            self.icon_path = self.icon_dir / "file_cached.png"
        self.setToolTip("File is cached.")
        self._set_icon()
        # Always update the symbolic link to the latest version of the file
        symlink_path = self.create_symlink(file_path)
        return symlink_path, self.file_type
