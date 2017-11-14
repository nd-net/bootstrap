from . import action, tools, path

@action.action()
def edit():
    """
    Edits the bootstrap directory.
    """
    tools.run("mate", path.scriptdir)
