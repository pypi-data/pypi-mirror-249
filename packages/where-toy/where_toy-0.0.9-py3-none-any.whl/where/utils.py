""" Utility to locate python modules """

import importlib.util
import importlib.resources

from .dirtree import print_tree


def where_module(name, recurse=False):
    """Locate and display module location/contents"""

    name = name.replace("-", "_")

    if recurse:
        path = importlib.resources.files(name)

        if not path:
            print(f"Package/module {name!r} not found!")
            return None

        print_tree(path)
        return

    spec = importlib.util.find_spec(name)

    if not spec:
        print(f"Package/module {name!r} not found!")
        return None

    if spec.origin:
        print(spec.origin)

    if spec.submodule_search_locations:
        for path in spec.submodule_search_locations:
            print(path)

    return spec
