from os.path import *
import sys, os

# use sys.argv[0] to get the calling script's path
scriptdir = dirname(sys.argv[0])

def configfiles(basename):
    """
    Returns a list of files that can be used as config files
    """
    dirs = ("config", "config-" + os.uname()[1].rsplit(".")[0])
    dirpaths = (join(d, basename) for d in dirs)
    realpaths = (join(scriptdir, d) for d in dirpaths)
    return [relpath(d) for d in realpaths]

def expandusers(filename):
    """
    Expands all user directories in the parameters.
    
    >>> expandusers(None) is None
    True
    >>> expandusers('~/foo/bar') == expanduser('~/foo/bar')
    True
    >>> expandusers(['~/foo/bar', '~/foo/baz']) == [expanduser('~/foo/bar'), expanduser('~/foo/baz')]
    True
    """
    if not filename:
        return filename
    try:
        return expanduser(filename)
    except (TypeError, AttributeError):
        return [expanduser(name) for name in filename]

def existing(paths):
    """
    Returns only the existing paths.
    """
    return [path for path in paths if exists(path)]

def ensure_path_exists(filename):
    """
    Ensures that the given filename can be written to
    """
    targetdir = dirname(expanduser(filename))
    if exists(targetdir):
        return
    os.makedirs(abspath(targetdir))
    