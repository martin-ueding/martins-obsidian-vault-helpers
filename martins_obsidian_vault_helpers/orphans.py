import pathlib
import shutil


def report_orphan_attachments(
    vault: pathlib.Path,
    link_graph: dict[pathlib.Path, list[pathlib.Path]],
    dry_run: bool,
) -> None:
    attachments = (vault / "Attachments").glob("*.*")
    targets = {target for targets in link_graph.values() for target in targets}
    print("Orphan attachments:")
    for attachment in attachments:
        if attachment not in targets:
            print(f"- {attachment}")
            if not dry_run:
                shutil.move(attachment, vault / "Inbox")
    print()


def report_notes_not_in_structure(
    vault: pathlib.Path,
    link_graph: dict[pathlib.Path, list[pathlib.Path]],
    dry_run: bool,
) -> None:
    targets_of_structure_notes = {
        target
        for source, targets in link_graph.items()
        if (vault / "Structure Notes") in source.parents
        for target in targets
    }
    print("Notes not in structure notes:")
    for source in link_graph.keys():
        if source.parent not in [vault / "Pages", vault / "Structure Notes"]:
            continue
        if source not in targets_of_structure_notes:
            print(f"- {source}")
            if not dry_run:
                shutil.move(source, vault / "Inbox")
    print()
