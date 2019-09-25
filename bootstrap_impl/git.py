from .action import *
from . import path, tools

target = "~/.config/git/ignore"

def git_config(args, global_setting=True):
    return ["/usr/bin/env", "git", "config", "--global" if global_setting else ""] + args

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
    tools.run(*git_config(["core.excludesfile", etarget]))

@default
@action
def gitignore(target=target, force=False, global_setting=True):
    """
    Updates gitignore.
    """
    import subprocess
    location = subprocess.check_output(git_config(["core.excludesfile"], global_setting=global_setting)).strip()
    
    ensure_path(location, target, force)

@default
@action
def git_prune_tags_on_fetch(value=True, global_setting=True):
    """
    Configures git to prune the tags when fetching from remote
    """
    # from https://stackoverflow.com/a/54297675/112964
    tools.run(*git_config(["fetch.pruneTags", "true" if value else "false"], global_setting=global_setting))
