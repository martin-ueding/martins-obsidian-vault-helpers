import os
import re
import pprint
import shutil
import urllib.parse


def main():
  usages = {}
  for dirpath, dirnames, filenames in os.walk(os.path.expanduser('~/Dokumente/Notizen')):
    dirnames.sort()
    filenames.sort()
    dirnames[:] = [dirname for dirname in dirnames if not dirname.startswith('.')]
    filenames[:] = [filename for filename in filenames if filename.endswith('.md')]
    for filename in filenames:
      filepath = os.path.relpath(os.path.join(dirpath, filename))
      u = get_usages(filepath)
      if len(u) > 0:
        usages[filepath] = u
  pprint.pprint(usages, compact=True, width=80)

  for md_path, img_paths in usages.items():
    for img_path in img_paths:
      move_to_correct_location(md_path, img_path)


def get_usages(path):
  filenames = []
  new_contents = []
  with open(path) as f:
    for line in f:
      m = re.match(r'^!\[\]\((.*)\)$', line)
      if m:
        relpath = find_file(os.path.basename(urllib.parse.unquote(m.group(1))))
        if relpath is None:
          raise RuntimeError(f'File does not exist: {path}, {m.group(1)}')
        filenames.append(relpath)
        new_contents.append(f'![](img/{os.path.basename(m.group(1))})\n')
      else:
        new_contents.append(line)
  with open(path, 'w') as f:
    for line in new_contents:
      f.write(line)
  return filenames


def find_file(basename):
  for dirpath, dirnames, filenames in os.walk(os.path.expanduser('~/Dokumente/Notizen')):
    dirnames[:] = [dirname for dirname in dirnames if not dirname.startswith('.')]
    if basename in filenames:
      return os.path.relpath(os.path.join(dirpath, basename))


def move_to_correct_location(md_path, img_path):
  target_dir = os.path.join(os.path.dirname(md_path), 'img')
  if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
  target_img = os.path.join(target_dir, os.path.basename(img_path))
  if img_path != target_img:
    print(img_path, '→', target_img)
    shutil.move(img_path, target_img)


if __name__ == '__main__':
  main()
