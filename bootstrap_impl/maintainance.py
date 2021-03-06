from __future__ import print_function

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
    
@action()
def location():
    """
    Prints the location of bootstrap so that you can cd there with `cd $(bootstrap location)`
    """
    import sys
    end = "\n" if sys.stdout.isatty() else ""
    print(path.scriptdir, end=end)