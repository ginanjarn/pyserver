"""generate"""

import argparse
from pathlib import Path

try:
    import model
    import python_generator
except ImportError:
    from . import model
    from . import python_generator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", help="output path, else output.py in current directory"
    )
    args = parser.parse_args()

    scheme_path = Path(Path(__file__).parent, "metaModel.json")
    loaded = model.load_model(scheme_path)
    source = "\n\n".join(python_generator.generate_code(loaded))

    output_name = args.output
    output = Path(output_name) if output_name else Path("output.py")
    output.write_text(source, encoding="utf-8")


if __name__ == "__main__":
    main()
