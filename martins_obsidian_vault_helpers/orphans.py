import pathlib
import shutil

from .command import print_context

from .link_graph import build_link_graph


@print_context("Orphan attachments")
def report_orphan_attachments(vault: pathlib.Path, dry_run: bool) -> None:
    link_graph = build_link_graph(vault)
    attachments = (vault / "Attachments").glob("*.*")
    targets = {target for targets in link_graph.values() for target in targets}
    for attachment in attachments:
        if attachment not in targets:
            print(f"- {attachment}")
            if not dry_run:
                shutil.move(attachment, vault / "Inbox")


@print_context("Notes not in structure")
def report_notes_not_in_structure(
    vault: pathlib.Path,
    dry_run: bool,
) -> None:
    link_graph = build_link_graph(vault)
    targets_of_structure_notes = {
        target
        for source, targets in link_graph.items()
        if (vault / "Structure Notes") in source.parents
        for target in targets
    }
    for source in link_graph.keys():
        if source.parent not in [vault / "Pages", vault / "Structure Notes"]:
            continue
        if source not in targets_of_structure_notes:
            print(f"- {source}")
            if not dry_run:
                shutil.move(source, vault / "Inbox")
