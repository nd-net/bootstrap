from .action import action
from . import path, tools

requirements = path.configfiles("requirements.txt")

@action(
    requirements="The files used for the requirements"
)
def pip(requirements=requirements):
    """
    Installs Python 3 modules via pip3 as defined in the requirements file.
    This requires Python 3 on your system and installs it via homebrew if necessary. 
    """
    existingRequirements = path.existing(path.expandusers(requirements))
    args = ["pip3", "install"]
    for requirement in existingRequirements:
        args.append("--requirement")
        args.append(requirement)
    try:
        tools.run(*args)
    except NameError:
        print("Installing Python3")
        tools.run("brew", "install", "python3")
        tools.run(*args)

@action
def pipdate():
    """
    Update existing Python packages. Requires the python egg pipdate.
    """
    tools.run("pipdate3")
