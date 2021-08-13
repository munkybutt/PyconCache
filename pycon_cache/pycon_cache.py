from __future__ import annotations

import pathlib
import imghdr

from Qt import QtGui
from typing import Any
from typing import Union

path_types = Union[str, pathlib.Path]

class IconCache:
    """This object is an icon cache based on a folder structure.

    All valid image files in the given icon cache folder will be
    converted to an icon upon access via dot notation and the
    resultant icon will be cached for efficient reuse later.

    All folders within the given icon cache folder will be be
    converted to an IconCache object and cached to provide access
    to the icons and folders within in a recursive manner.

    Usage examples:

        IconFolder/Icon.png will be accessed like so:

            icon_cache = IconCache(IconFolder)
            icon_cache.Icon

        IconFolder/SubIconFolder/Icon.png will be accessed like so:

            icon_cache = IconCache(IconFolder)
            icon_cache.SubIconFolder.Icon

    Note that the dot notation access is case sensitive.
    """

    def __init__(self, in_cache_path: path_types) -> None:

        super().__init__()

        self.__icons__: dict = {}

        self._cache_path: path_types = ""

        self.cache_path = in_cache_path

    @property
    def cache_path(self) -> path_types:
        return self._cache_path

    @cache_path.setter
    def cache_path(self, in_path: path_types) -> None:
        if not self._is_valid_directory(in_path):
            raise ValueError(f"{in_path} is not a valid directory")

        self._cache_path: path_types = in_path

    @staticmethod
    def _is_valid_directory(in_path: path_types) -> bool:
        path_object: pathlib.Path = in_path if isinstance(in_path, pathlib.Path) else pathlib.Path(in_path)
        return path_object.is_dir()

    @classmethod
    def _get_icon(cls, in_path: path_types, in_name: str) -> Union[QtGui.QIcon, IconCache, None]:
        path_object: pathlib.Path = in_path if isinstance(in_path, pathlib.Path) else pathlib.Path(in_path)
        if path_object.is_dir():
            for sub_path_object in path_object.iterdir():
                if sub_path_object.stem != in_name:
                    continue

                if sub_path_object.is_dir():
                    return IconCache(sub_path_object)

                return cls._get_icon(sub_path_object, in_name)

        elif path_object.stem == in_name and imghdr.what(str(path_object)):
            return QtGui.QIcon(str(path_object))

    def __getattr__(self, in_attribute_name: str) -> Any:
        if in_attribute_name in self.__icons__:
            return self.__icons__[in_attribute_name]

        icon = self._get_icon(self.cache_path, in_attribute_name)
        if icon:
            self.__icons__[in_attribute_name] = icon
            return icon

        raise AttributeError(f"{self} has no attribute named '{in_attribute_name}'")


if __name__ == "__main__":

    iD = IconCache(r"D:\Code\Git\PyconCache\pycon_cache_test\icons")
    # iD.fancy
    # iD.folder
    # p = pathlib.Path(r"D:\Code\Git\PyconCache\pycon_cache_test\icons")
    # print(str(p))
    # print(imghdr.what(r"D:\Code\Git\PyconCache\pycon_cache_test\icons\fancy.png"))
