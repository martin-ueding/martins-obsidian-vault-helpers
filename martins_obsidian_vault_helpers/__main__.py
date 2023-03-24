import argparse
import pathlib

from .attachments import rename_images_with_hash

from .orphans import report_orphan_attachments, report_notes_not_in_structure
from .link_graph import build_link_graph


def main():
    options = parse_args()

    vault = options.vault

    rename_images_with_hash(vault, options.dry_run)
    link_graph = build_link_graph(vault)
    report_orphan_attachments(vault, link_graph, options.dry_run)
    report_notes_not_in_structure(vault, link_graph, options.dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=pathlib.Path)
    parser.add_argument("--dry-run", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    main()
