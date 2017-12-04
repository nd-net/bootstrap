from .action import *
from . import path, tools

sources = path.configfiles("xonshrc.d")

def expandSources(sources, force):
    if not force:
        sources = [source for source in sources if path.exists(path.expanduser(source))]
    sourceWithDirs = [path.join(source, '*') if path.isdir(source) else source for source in sources]
    relativeToHome = [path.compactuser(path.abspath(source)) for source in sourceWithDirs]
    return relativeToHome

def applySourceLines(rcfile, sourceLines):
    expandedTarget = path.expanduser(rcfile)
    path.ensure_path_exists(expandedTarget)
    
    try:
        with open(expandedTarget, 'rt') as rc:
            xonshrc = rc.readlines()
    except:
        xonshrc = []
    for line in sourceLines:
        while True:
            try:
                xonshrc.remove(line)
            except ValueError:
                break
    xonshrc = sourceLines + ["\n"] + xonshrc
    
    with open(expandedTarget, 'w+t') as rc:
        rc.write("".join(xonshrc))

@default
@action(
    sources="The source files or directories to use",
    target="The target file where the configurations should be integrated",
    force="If enabled, then sources are not checked if they exist"
)
def xonshrc(sources=sources, target="~/.xonshrc", force=False):
    """
    Sources the given configurations into a target file.
    """
    sources = expandSources(sources, force)
    
    print("Sourcing {} into {}".format(sources, target))
    sourceLines = ["""source g`{}`\n""".format(source) for source in sources]
    applySourceLines(target, sourceLines)

@default
@action(
    shell="The path to the target shell",
    force="Force chsh even if the shell's executable does not exist"
)
def chsh(shell="/usr/local/bin/xonsh", force=False):
    """
    Changes the shell of the current user to the given target shell.
    """
    import os
    if os.environ.get('SHELL') == shell:
        print("Not changing the shell since is already in use".format(shell))
        return
    
    if not path.exists(shell) and not Force:
        print("Not changing the shell since it does not exist at {}".format(shell))
        return
        
    config = '/etc/shells'
    with open(config, 'rt') as shellconfig:
        shells = [line.strip() for line in shellconfig.readlines()]
    
    if shell not in shells:
        print('Adding {} to {}'.format(shell, config))
        tools.run('sudo', 'sh', '-c', 'echo {} >> {}'.format(shell, config))
    tools.run('chsh', '-s', shell)    
    