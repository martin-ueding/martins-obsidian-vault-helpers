import argparse
import pathlib

from .attachments import rename_images_with_hash, trim_images
from .orphans import report_orphan_attachments, report_notes_not_in_structure


def main():
    options = parse_args()

    vault = options.vault

    # trim_images(vault, options.dry_run)
    rename_images_with_hash(vault, options.dry_run)
    report_orphan_attachments(vault, options.dry_run)
    report_notes_not_in_structure(vault, options.dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("vault", type=pathlib.Path)
    parser.add_argument("--dry-run", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    main()
