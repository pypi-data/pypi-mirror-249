"""
linky
Copyright (C) 2021 LoveIsGrief

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from pathlib import Path
from typing import List

from linky.config import Config
from linky.utils.path_utils import get_paths_in_root


def get_tags(config: Config, *paths: Path, relative: bool = False) -> List[Path]:
    """
    Get all tags of a the given paths

    @param config: The repository's config
    @param paths: These must be within the linked root, otherwise an exception will be thrown
    @param relative: Whether the paths should be printed relative to the linked root
    @return: string (not natural!) sorted list of absolute or linked-root relative paths
    """
    tag_paths = []
    for path in paths:
        tag_paths.extend(in_root for in_root in get_paths_in_root(path, config))
    if relative:
        tag_paths = [tag_path.relative_to(config.base_path.parent) for tag_path in tag_paths]
    return sorted(tag_paths, key=str)
