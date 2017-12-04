from .action import *
from . import path, tools

default_paths = path.configfiles("defaults/*")

def get_file_arguments(plist_buddy, files):
    import shlex
    for file in files:
        with open(file, "rt") as buddy_file:
            first_line = buddy_file.readline()
        if not first_line.startswith("#!"):
            continue
        first_line = first_line[2:]
        parts = shlex.split(first_line)
        while parts and "plist-buddy" not in parts[0]:
            del parts[0]
        if not parts:
            continue
        # parts[0] is now the plist-buddy call. Replace it with the given path
        parts[0] = plist_buddy
        parts.append(file)
        yield parts

def get_default_files(default_paths):
    from glob import glob
    
    files = []
    for default_path in path.expandusers(default_paths):
        files += glob(default_path)
    
    files.sort(key=path.basename)
    return files

@default
@action(
    default_paths=dict(
        help="the paths used for default files, with possible glob characters",
        metavar="file"
    )
)
def apply_defaults(default_paths=default_paths):
    """
    Applies defaults using plist-buddy. The defaults files are sorted alphabetically for the filename if necessary.
    """
    plist_buddy = path.join(path.scriptdir, 'bin', 'plist-buddy')
    files = get_default_files(default_paths)
    for command in get_file_arguments(path.join(path.scriptdir, 'bin', 'plist-buddy'), files):
        print("Applying defaults from {}".format(command[-1]))
        tools.run(*command)
