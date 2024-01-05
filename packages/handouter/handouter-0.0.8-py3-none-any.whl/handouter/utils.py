import os


def read_file(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        contents = f.read()
    return contents


def write_file(filepath, contents):
    with open(filepath, "w", encoding="utf8") as f:
        f.write(contents)


def replace_ext(filepath, new_ext):
    if not new_ext.startswith("."):
        new_ext = "." + new_ext
    dirname = os.path.dirname(filepath)
    basename = os.path.basename(filepath)
    base, _ = os.path.splitext(basename)
    return os.path.join(dirname, base + new_ext)
