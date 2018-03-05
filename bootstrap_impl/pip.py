from .action import *
from . import path, tools

requirements = path.configfiles("requirements.txt")
xonsh_requirements = path.configfiles("xonsh-requirements.txt")


@default
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

@default
@action(
    xonsh_requirements="The files used for the requirements"
)
def xpip(xonsh_requirements=xonsh_requirements):
    """
    Installs Xonsh Python 3 modules via xpip as defined in the requirements file.
    """
    existingRequirements = path.existing(path.expandusers(xonsh_requirements))
    args = ["xpip", "install"]
    for requirement in existingRequirements:
        args.append("--requirement")
        args.append("'{}'".format(requirement))
    tools.run("xonsh", "-c", " ".join(args))

@default
@action
def pipdate():
    """
    Update existing Python packages. Requires the python egg pipdate.
    """
    tools.run("pipdate3")

@default
@action
def xpipdate():
    """
    Update existing Xonsh Python packages. Requires the python egg pipdate.
    """
    import subprocess, re
    
    versions = subprocess.check_output(['/usr/bin/env', 'xonsh', '-c', 'xpip freeze --local'])
    entries = re.findall("^(.*?)=", versions, re.MULTILINE)
    for entry in entries:
        tools.run("xonsh", "-c", "xpip install -U {}".format(entry))
