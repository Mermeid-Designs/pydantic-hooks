from argparse import ArgumentParser
from importlib.util import module_from_spec, spec_from_file_location
from inspect import getmembers, isclass
from json import dump
from os import sep
from pathlib import Path
from sys import version_info, path
from typing import Sequence
from traceback import format_exc

from pydantic import BaseModel
from pydantic import __version__ as pydantic_version


def export_models(path: str | Path, output_dir: str | Path) -> None:
    # Type cast `path` and `output_dir` to Path objects, if applicable
    #   Handles case where input is neither str nor Path (auto-fails check when error is thrown)
    path = Path(path) if not isinstance(path, Path) else path
    output_dir = Path(output_dir) if not isinstance(output_dir,
                                                    Path) else output_dir
    print(f"Exporting {str(path)} model(s) to {output_dir}")

    # Ensure path points to an existing file or directory
    if not path.exists():
        raise FileNotFoundError(
            f"[Errno 2] No such file or directory: '{path}'")
    # Raise warning if object directory contains a suffix
    if output_dir.suffix != "":
        print(
            f"Unexpected file suffix {output_dir.suffix} in output directory path {output_dir}"
        )

    # Enable access to module or package information
    spec = spec_from_file_location(str(path.parent.joinpath(path.stem)).replace(sep, '.'), str(path.absolute()))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    # Export pydantic schema to json file
    for key, obj in getmembers(module):
        if isclass(obj) and issubclass(obj,
                                       BaseModel) and obj is not BaseModel:
            # Create output directory if it doesn't already exist
            output_dir.mkdir(parents=True, exist_ok=True)

            with open(output_dir.joinpath(f"{key}.json"),
                      "w",
                      encoding="utf-8") as file:
                dump(
                    obj.model_json_schema()
                    if pydantic_version >= '2.0' else obj.schema_json(),
                    file,
                    indent=2,
                )
                print(f"Exported {key} model as {key} JSON Schema")
    print("Exported all models!")


def main(argv: Sequence[str] | None = None) -> int:
    path.append(str(Path().absolute()))
    
    parser = ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    parser.add_argument(
        "--input",
        help="Path to python module, submodule, or file containing the schemas",
        metavar="FILE",
        required=False,
    )
    parser.add_argument("--output",
                        help="Output folder path",
                        metavar="FILE",
                        required=True)
    parser.add_argument(
        "--all",
        help="Export all models regardless of if source has changed",
        action="store_true",
        required=False,
    )
    args = parser.parse_args(argv)

    # If `input` is unset, default to current repo directory
    source = Path(args.input or Path()).absolute()
    # Ensure `source` is a valid directory or file
    if not source.exists():
        print(
            f"FileNotFoundError: Errno 2] No such file or directory: '{source}'"
        )
        return 1

    # Iterate through all python files in source directory if `all` is True
    if args.all:
        potential_files = source.glob("**/*.py")
    # Otherwise, only iterate through changed files within `source`
    elif version_info < (3, 9):  # Python version < 3.9
        potential_files = [
            file for file in args.filenames
            if source in Path(file).absolute().parents
        ]
    else:  # Python version >= 3.9
        potential_files = [
            file for file in args.filenames
            if Path(file).absolute().is_relative_to(source)
        ]
      
    retval = 0
    for file in potential_files:
        try:
            export_models(file, args.output)
        except Exception as e:
            print(format_exc())
            retval = 1
    return retval


if __name__ == "__main__":
    raise SystemExit(main())
