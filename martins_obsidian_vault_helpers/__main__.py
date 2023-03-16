import argparse
import pathlib

from .orphans import report_orphan_attachments, report_notes_not_in_structure
from .link_graph import build_link_graph


def main():
    options = parse_args()

    vault = options.vault

    link_graph = build_link_graph(vault)
    report_orphan_attachments(vault, link_graph)
    report_notes_not_in_structure(vault, link_graph)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=pathlib.Path)

    return parser.parse_args()


if __name__ == '__main__':
    main()