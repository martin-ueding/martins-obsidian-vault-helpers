import pathlib
import shutil


def report_orphan_attachments(vault: pathlib.Path, link_graph: dict[pathlib.Path, list[pathlib.Path]]) -> None:
    attachments = (vault / 'Attachments').glob('*.*')
    targets = {target for targets in link_graph.values() for target in targets}
    for attachment in attachments:
        if attachment not in targets:
            shutil.move(attachment, vault / 'Inbox')


def report_notes_not_in_structure(vault: pathlib.Path, link_graph: dict[pathlib.Path, list[pathlib.Path]]) -> None:
    targets_of_structure_notes = {target for source, targets in link_graph.items() if (vault / "Structure Notes") in source.parents for target in targets}
    for source in link_graph.keys():
        if source.parent not in [vault / "Pages", vault / "Structure Notes"]:
            continue
        if source not in targets_of_structure_notes:
            shutil.move(source, vault / 'Inbox')
