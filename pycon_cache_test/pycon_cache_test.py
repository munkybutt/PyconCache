import site
import sys
import pathlib

from Qt import QtWidgets


def __setup__():
    current_path = pathlib.Path(__file__)
    package_path = current_path.parent.parent
    site.addsitedir(str(package_path))


if __name__ == "__main__":

    __setup__()

    import pycon_cache.pycon_cache as pycon_cache

    app = QtWidgets.QApplication(sys.argv)
    current_path = pathlib.Path(__file__)
    ic = pycon_cache.IconCache(current_path.parent / "icons")
    print(f"ic = {ic}")
    print(f"ic.fancy = {ic.fancy}")
    print(f"ic.folder = {ic.folder}")
    print(f"ic.folder.fancy = {ic.folder.fancy}")
    # sys.exit(app.exec_())
