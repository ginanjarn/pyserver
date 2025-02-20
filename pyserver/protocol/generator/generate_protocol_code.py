import json
from itertools import chain
from pathlib import Path


try:
    from models import (
        Enumeration,
        Structure,
        TypeAlias,
        Request,
        Notification,
    )
    from python_code_generator import Generator
    from dependency_manager import Manager
except ImportError:
    from .models import (
        Enumeration,
        Structure,
        TypeAlias,
        Request,
        Notification,
    )
    from .python_code_generator import Generator
    from .dependency_manager import Manager


def get_schemes(meta_path: str) -> dict:
    """"""
    return json.loads(Path(meta_path).read_text("utf-8"))


def main():
    file_directory = Path(__file__).parent

    scheme = get_schemes(file_directory.joinpath("metaModel.json"))

    enumerations = [Enumeration(**e) for e in scheme["enumerations"]]
    structures = [Structure(**s) for s in scheme["structures"]]
    type_aliases = [TypeAlias(**t) for t in scheme["typeAliases"]]
    requests = [Request(**r) for r in scheme["requests"]]
    notifications = [Notification(**r) for r in scheme["notifications"]]

    elements = chain(enumerations, structures, type_aliases)
    dep_manager = Manager(list(elements))
    ordered_elements = dep_manager.get_ordered_elements()
    gen = Generator(list(chain(ordered_elements, requests, notifications)))
    code = gen.generate()

    output_path = Path(file_directory.parent, "lsp_protocol.py")
    output_path.write_text(code, encoding="utf8")
    print(f"code generated at {output_path!s}")


if __name__ == "__main__":
    main()
