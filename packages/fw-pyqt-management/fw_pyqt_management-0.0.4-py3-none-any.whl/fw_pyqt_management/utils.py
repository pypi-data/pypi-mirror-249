"""Utility functions for SlicerFlywheelConnect."""
import importlib
import logging
import platform
from importlib.util import find_spec
from pathlib import Path
from tempfile import TemporaryDirectory

import pip

from .adaptive_qt import Ok_btn, QMessageBox

# fmt: off
if not find_spec("importlib_metadata"):
    pip.main(["install", "importlib_metadata"])

from importlib_metadata import version

# fmt: on

log = logging.getLogger(__name__)


def pip_install(package, pkg_version=None, upgrade=False):
    """Install package using pip.

    pkg_version and upgrade are mutually exclusive.

    Args:
        package (str): Name of package to install.
        pkg_version (str, optional): Version of package to install. Defaults to None.
        upgrade (bool, optional): Upgrade package if already installed. Defaults to False.
    """
    command = ["install"]

    if pkg_version and not upgrade:
        package = f"{package}=={pkg_version}"
        command.append(package)

    if upgrade and not pkg_version:
        command.extend(["--upgrade", package])

    if upgrade and pkg_version:
        msg = (
            "pkg_version and upgrade are mutually exclusive. "
            "Qualifiers will be ignored."
        )
        log.warning(msg)

    log.debug("Installing %s", package)
    pip.main(command)


def is_developer_mode_enabled():
    """Check if Developer Mode is enabled in Windows.

    Returns:
        bool: Indicates if Developer Mode is enabled.
    """
    try:
        with TemporaryDirectory() as temp_dir:
            # Create a temporary symlink
            temp_dir = Path(temp_dir) / "symlink_test"
            target_file = temp_dir / "target_file"
            symlink = temp_dir / "symlink"

            temp_dir.mkdir(exist_ok=True)
            target_file.write_text("This is a test file.")

            symlink.symlink_to(target_file)

            # Clean up
            symlink.unlink()
            target_file.unlink()
            temp_dir.rmdir()

        return True

    except (OSError, NotImplementedError):
        return False


def check_requirements(required_modules):
    """Ensures all requirements for the application are installed and up-to-date.

    Args:
        required_modules (dict): A dictionary of required modules.

    NOTE: This function is necessary in the Slicer Python environment to ensure that
    packages are installed and updated to the required version. For non-Slicer
    Python environments, it is recommended to use Poetry or requirements.txt.

    TODO: This functionality will be eliminated by using a SuperBuild artifact for
    Slicer extensions. see
    <https://discourse.slicer.org/t/install-python-library-with-extension/10110/6>
    """
    for module, package_dict in required_modules.items():
        package, pkg_version, upgrade = package_dict.values()

        if not importlib.util.find_spec(module, package=package):
            pip_install(f"{package}", pkg_version=pkg_version)
        elif upgrade:
            pip_install(f"{package}", upgrade=True)
        elif pkg_version:
            installed_version = version(package)
            if installed_version != pkg_version:
                pip_install(f"{package}", pkg_version=pkg_version)


def check_developer_mode():
    """Check for "Developer Mode" in Windows."""
    if platform.system() == "Windows":
        if not is_developer_mode_enabled():
            msg = (
                "<a href='https://gitlab.com/flywheel-io/scientific-solutions/app/"
                "Slicerflywheelcaseiterator#windows-requirements'>Developer Mode</a> "
                "is required. "
                "Please enable it and restart or Run as Administrator. "
            )
            log.debug(msg)
            _ = QMessageBox.warning(None, "Developer Mode", msg, Ok_btn)
