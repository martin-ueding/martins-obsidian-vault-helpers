#!/usr/bin/env python3

import argparse
import re
import urllib.parse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="+")
    options = parser.parse_args()

    link_pattern = re.compile(r"\[[^]]+]\((?:\.\./)?202[012]/(.+?).md\)")

    for file in options.filename:
        print(file)
        with open(file) as f:
            lines = list(f)
        new_lines = []
        for line in lines:
            while match := link_pattern.search(line):
                source = match.group(0)
                print(source)
                title = urllib.parse.unquote(match.group(1))
                target = f"[[{title}]]"
                line = line.replace(source, target)
            new_lines.append(line)
        new_markdown_contents = "".join(new_lines)
        markdown_contents = "".join(lines)
        if new_markdown_contents != markdown_contents:
            with open(file, "w") as f:
                f.write(new_markdown_contents)


if __name__ == "__main__":
    main()
