import argparse
import json
import os
from pathlib import Path
import sys

class NoMapException(Exception):
    pass

def make_ddoc(source_dir, ddoc_name, view_name):
    p = Path(source_dir) / ddoc_name / view_name
    map_path = p / "map.js"

    if not map_path.exists():
        print(f"No such file: {map_path}")
        raise NoMapException

    with open(map_path, mode="r") as f:
        map_src = f.read()

    reduce_path = p / "reduce.js"
    reduce_src = ""
    if reduce_path.exists():
        with open(reduce_path, mode="r") as f:
            reduce_src = f.read()

    preamble = f"""{{
    "views": {{
        "{view_name}": {{"""

    actions = f"""
            "map": {json.dumps(map_src)}"""

    if reduce_src != "":
        actions += f""",
            "reduce": {json.dumps(reduce_src)}"""

    postamble = f"""
        }}
    }},
    "language": "javascript"
}}
"""

    return preamble + actions + postamble


def generate_ddocs(ssrc, sdst):
    src = Path(ssrc).resolve()
    if not src.exists() or not src.is_dir():
        print(f"Source dir '{src.name}' doesn't exist.")
        exit(1)

    dst = Path(sdst).resolve()
    if dst.exists():
        print(f"Build dir '{dst.name}' already present; won't overwrite.")
        exit(1)

    os.makedirs(dst)

    ddocs = {}
    for ddoc in src.iterdir():
        if ddoc.is_dir():
            if "-" in ddoc.name:
                print(f"No '-' allowed in ddoc names")
                exit(1)
            for view in ddoc.iterdir():
                if "-" in view.name:
                    print(f"No '-' allowed in view names")
                    exit(1)
                ddocs[f"{ddoc.name}-{view.name}"] = make_ddoc(src, ddoc.name, view.name)

    for name, data in ddocs.items():
        with open(f"{dst}/{name}.json", mode="w") as f:
            f.write(data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} src dest")
        exit(1)

    src, dst = sys.argv[1:]

    generate_ddocs(src, dst)
