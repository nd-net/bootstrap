from .action import *
from . import path, tools

@action()
def edit():
    """
    Edits the bootstrap directory.
    """
    tools.run("mate", path.scriptdir)

@action()
def update():
    """
    Updates bootstrap via git pull.
    """
    import os
    os.chdir(path.scriptdir)
    tools.run("git", "pull")
    