import logging
import shutil
from pathlib import Path

from linky.config import read_conf
from linky.utils import path_utils


def remove(path: Path, _all: bool = False):
    """
    Permanently removes either files or directories from linky management

    @param path: What to delete
    @param _all: Only impacts directories: whether to select items that have the current tag
                  or all items regardless of tag.
                 This is essentially the difference between walking through the current directory
                  or walking through the directory in the base.
    """
    if _all:
        remove_all(path)
    else:
        remove_files(path)


def remove_all(path: Path):
    """
    Permanently removes a file or directory from linky management

    @param path: What we're trying to delete
    """
    logger = logging.getLogger("actions.remove")
    logger.debug("Removing: %s", path)
    config = read_conf(path)
    base_path = config.base_path
    logger.debug("Base path: %s", base_path)

    path_in_base = path_utils.get_path_in_base(base_path, path, config.categories.keys())
    other_paths = path_utils.get_paths_in_root(path_in_base, config)

    for other_path in other_paths + [path_in_base]:
        if other_path.is_symlink() or other_path.is_file():
            other_path.unlink()
        elif other_path.is_dir():
            shutil.rmtree(other_path)
        logger.info("Removed %s", other_path)

        # Make sure to remove empty parent directories
        path_utils.del_empty_parents(other_path)


def remove_files(path: Path):
    """
    Only removes files within the path from linky management

    Folders will be recursed into to remove the files they contain.
    Using this approach, it isn't possible to delete folders across tags or tag groups.

    For example
    .
    └── Tags
        ├── Document
        │   └── folder
        │       ├── document.odt
        │       └── useful_document.odt
        ├── Movie
        │   └── folder
        │       └── movie.mp4
        ├── Music
        │   └── folder
        │       └── music.m4a
        └── Useful
            └── folder
                ├── useful
                └── useful_document.odt
    Targeting Tags/Document/folder will only remove:
      - Tags/Document/folder/useful_document.odt
      - Tags/Document/folder/document.odt
      - Tags/Document/folder
      - Tags/Useful/folder/useful_document.odt (it's a file and has other tags)
    Nothing else.

    @param path: What we're trying to delete
    """
    logger = logging.getLogger("actions.remove_files")
    logger.debug("Removing file/files in: %s", path)
    config = read_conf(path)
    base_path = config.base_path
    logger.debug("Base path: %s", base_path)

    path_in_base = path_utils.get_path_in_base(base_path, path, config.categories.keys())

    if path_in_base == path:
        # Deleting it in base is the equivalent of wanting to remove it everywhere
        remove_all(path)

    elif path.is_file():
        # Files can be deleted everywhere
        other_paths = path_utils.get_paths_in_root(path_in_base, config)

        for other_path in other_paths + [path_in_base]:
            other_path.unlink()
            logger.info("Removed %s", other_path)
            # Make sure to remove empty parent directories
            path_utils.del_empty_parents(other_path)

    elif path.is_dir():
        for abs_child, _ in path_utils.walk(path, include_dirs=False):
            remove_files(abs_child)

    else:
        raise ValueError("Path is neither file nor directory")
