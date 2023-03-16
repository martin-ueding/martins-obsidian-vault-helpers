#!/usr/bin/env python3

import argparse
import re
import pathlib
import urllib.parse
import subprocess


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="+")
    options = parser.parse_args()

    image_pattern = re.compile(r"!\[\[(.+)]]")

    moves = {}
    for file in options.filename:
        print(file)
        with open(file) as f:
            markdown_contents = f.read()
        new_markdown_contents = markdown_contents
        for source in image_pattern.findall(new_markdown_contents):
            print(source)
            image_path = pathlib.Path(file).parent / "img" / pathlib.Path(urllib.parse.unquote(source)).name
            if not image_path.exists():
                continue
            image_hash = get_hash(image_path)
            new_image_path = image_path.with_stem(image_hash)
            target = f"![[{new_image_path.name}]]"
            if source != new_image_path.name:
                new_markdown_contents = new_markdown_contents.replace(f"![[{source}]]", target)
                moves[image_path] = new_image_path
        if new_markdown_contents != markdown_contents:
            with open(file, "w") as f:
                f.write(new_markdown_contents)

    for old, new in moves.items():
        print(old, new)
        if old.exists():
            old.rename(new)


def get_hash(file: pathlib.Path) -> str:
    output = subprocess.run(["sha1sum", str(file)], capture_output=True, check=True)
    return output.stdout.decode().split()[0]


if __name__ == "__main__":
    main()
