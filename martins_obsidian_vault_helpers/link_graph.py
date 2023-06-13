import pathlib
import re


def build_link_graph(vault: pathlib.Path) -> dict[pathlib.Path, list[pathlib.Path]]:
    markdown_paths = list(vault.rglob("*.md"))
    attachment_paths = list((vault / "Attachments").glob("*.*"))
    names = {path.stem: path for path in markdown_paths} | {
        path.name: path for path in attachment_paths
    }
    link_graph = {
        path: filter_references(gather_references(path), names)
        for path in markdown_paths
    }
    return link_graph


def gather_references(path: pathlib.Path) -> list[str]:
    matches = []
    with open(path) as f:
        for line in f:
            matches += re.findall(r"\[\[([^]/]+)]]", line)
    return matches


def filter_references(
    references: list[str], names: dict[str, pathlib.Path]
) -> list[pathlib.Path]:
    return [names[reference] for reference in references if reference in names]
