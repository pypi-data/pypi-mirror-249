"""Module for the file system utilities."""
import os
import sys

WINDOWS_KEY = 'windows'
DARWIN_KEY = 'darwin'
LINUX_KEY = 'linux'

# pylint: disable=invalid-name


def toCleanPath(path, platform=None):
    """Convert the path to a clean path that we can use safely.

    Args:
        path (str): Full path to clean.
        platform (str, optional): The platform to target the clean. Defaults to current platform.

    Returns:
        str: The clean path.
    """
    if platform is None:
        platform = currentOs()
    safe_path = os.path.normpath(path)
    if platform == WINDOWS_KEY:
        safe_path = safe_path.replace('/', '\\')
    else:
        safe_path = safe_path.replace('\\', '/')

    return safe_path


def toLucidityPath(path):
    """Converts the path to what lucidity expects (forward bars).

    Args:
        path (str): Full path to convert.

    Returns:
        str: The converted path.
    """
    return path.replace('\\', '/')


def toComparePath(path, platform=None):
    """Convert a path to a comparable version of the same path.

    Args:
        path (str): Full path to the path to convert.
        platform (str, optional): The platform to target. Defaults to current platform.

    Returns:
        str: A path that points to the same place but can be string compared.
    """
    if platform is None:
        platform = currentOs()
    safe_path = toCleanPath(path)
    if platform == WINDOWS_KEY:
        safe_path = safe_path.lower()

    return safe_path


def toAbsolutePath(path, base, platform=None):
    """Expand a relative path to a full path.

    Args:
        path (str): Relative path to convert.
        base (str): Full path to base path to resolve the relative path from.
        platform (str, optional): The platform to target. Defaults to current platform.

    Returns:
        str: The full path.
    """
    clean_path = toCleanPath(path, platform=platform)
    clean_base = toCleanPath(base, platform=platform)

    relative = clean_path[len(clean_base) :]

    for _ in range(5):  # @UnusedVariable
        if relative and relative[0] in ['/', '\\']:
            relative = relative[1:]
        else:
            break
    abs_path = os.path.normpath(os.path.join(clean_base, clean_path))
    return abs_path


def currentOs():
    """Returns the name of the current os.

    Returns:
        str: The name of the current os.
    """
    platform_map = {
        'linux': LINUX_KEY,
        'linux2': LINUX_KEY,
        'darwin': DARWIN_KEY,
        'win32': WINDOWS_KEY,
        'win64': WINDOWS_KEY,
    }

    return platform_map.get(sys.platform)


def isSamePath(path_a, path_b, platform=None):
    """Returns whether or not a 2 paths are the same.

    Args:
        path_a (str): A full path to compare.
        path_b (str): The other full path to compare.
        platform (str, optional): The platform to target. Defaults to current platform.

    Returns:
        bool: Whether or not the paths are the same.
    """
    c_path_a = toComparePath(path_a, platform=platform)
    c_path_b = toComparePath(path_b, platform=platform)
    return c_path_a == c_path_b
