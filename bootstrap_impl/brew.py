from .action import *
from . import path, tools

brewfiles = path.configfiles("Brewfile")

def ensure_brew_exists():
    HOMEBREW_URL = 'https://raw.githubusercontent.com/Homebrew/install/master/install'
    try:
        tools.run('brew', '--version')
    except NameError:
        print('Downloading homebrew')
        import urllib2
        response = urllib2.urlopen(HOMEBREW_URL)
        print('Installing homebrew')
        script = response.read()
        tools.run('ruby', '-e', script)

@default
@upgrade
@action(
    brewfiles="The files to be used for homebrew",
    update="update existing homebrew packages",
    cleanup="clean up packages"
)
def brew(brewfiles=brewfiles, update=True, cleanup=True):
    """
    Installs the content of Brewfile via homebrew.
    If homebrew is not present on the system,
    then this also downloads and installs homebrew.
    """
    ensure_brew_exists()
    tools.run("brew", "update")
    for brewfile in path.expandusers(brewfiles):
        if not path.exists(brewfile):
            continue
        print("Installing bundle {}".format(brewfile))
        tools.run("brew", "bundle", "--verbose", "--file={}".format(brewfile))
    if update:
        tools.run("brew", "upgrade")
        tools.run("brew", "cask", "upgrade")
    if cleanup:
        tools.run("brew", "cleanup")
        tools.run("brew", "cask", "cleanup")

@default
@upgrade
@action
def anon(enable=False):
    """
    Executes brew analytics off
    """
    tools.run("brew", "analytics", "on" if enable else "off")
