from .action import *
from . import tools

@default
@action(
    dropbox="The path to Dropbox"
)
def dropbox(dropbox="/Applications/Dropbox.app"):
    """
    Starts dropbox so that it can sync.
    """
    tools.run("open", dropbox)
