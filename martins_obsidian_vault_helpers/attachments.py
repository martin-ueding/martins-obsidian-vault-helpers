import pathlib
import re
import shutil
import subprocess
import tempfile
import urllib.parse
import multiprocessing.pool

from .command import print_context


@print_context("Moving attachments")
def rename_images_with_hash(vault: pathlib.Path, dry_run: bool) -> None:
    image_pattern = re.compile(r"!\[\[(.+)]]")

    moves = {}
    for file in vault.rglob("*.md"):
        with open(file) as f:
            markdown_contents = f.read()
        new_markdown_contents = markdown_contents
        for source in image_pattern.findall(new_markdown_contents):
            image_path = (
                vault / "Attachments" / pathlib.Path(urllib.parse.unquote(source)).name
            )
            if not image_path.exists():
                continue
            image_hash = get_hash(image_path)
            new_image_path = image_path.with_stem(image_hash)
            target = f"![[{new_image_path.name}]]"
            if source != new_image_path.name:
                new_markdown_contents = new_markdown_contents.replace(
                    f"![[{source}]]", target
                )
                moves[image_path] = new_image_path
        if new_markdown_contents != markdown_contents and not dry_run:
            with open(file, "w") as f:
                f.write(new_markdown_contents)

    move_images(moves, dry_run)


def move_images(moves: dict[str, str], dry_run: bool):
    for old, new in moves.items():
        print(f"- {old} → {new}")
        assert old.exists()
        if not dry_run:
            old.rename(new)


def get_hash(file: pathlib.Path) -> str:
    output = subprocess.run(["sha1sum", str(file)], capture_output=True, check=True)
    return output.stdout.decode().split()[0]


@print_context("Trimming PNG images")
def trim_images(vault: pathlib.Path, dry_run: bool) -> None:
    with multiprocessing.pool.ThreadPool() as pool:
        for image in vault.rglob("*.png"):
            pool.apply(trim_single_image, (image, dry_run))


def trim_single_image(image: pathlib.Path, dry_run: bool) -> None:
    temp = pathlib.Path("/tmp") / image.name
    old_hash = get_hash(image)
    try:
        subprocess.run(
            ["convert", str(image), "-trim", "+repage", str(temp)], check=True
        )
    except subprocess.CalledProcessError:
        pass
    else:
        new_hash = get_hash(temp)
        if old_hash != new_hash:
            print(f"- {image}")
            if not dry_run:
                shutil.copy(temp, image)
