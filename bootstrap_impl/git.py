from .action import *
from . import path, tools

target = "~/.config/git/ignore"

def ensure_path(location, target, force):
    etarget = path.expanduser(target)
    clocation = path.compactuser(location)
    if location == etarget:
        print("Global gitignore already at {}".format(clocation))
        return
    path.ensure_path_exists(etarget)
    if path.exists(location):
        if not path.exists(etarget) or force:
            print("Moving global gitignore from {} to {}".format(clocation, target))
            tools.run("mv", location, etarget)
    if not path.exists(etarget):
        # touch
        with open(etarget, "wt"):
            pass
    tools.run("/usr/bin/env", "git", "config", "--global", "core.excludesfile", etarget)

@default
@action
def gitignore(target=target, force=False):
    """
    Updates the global gitignore.
    """
    import subprocess
    location = subprocess.check_output(["/usr/bin/env", "git", "config", "--global", "core.excludesfile"]).strip()
    
    ensure_path(location, target, force)