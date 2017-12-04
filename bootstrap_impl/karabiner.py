from .action import *
from . import tools, path

configurations = path.configfiles("karabiner.json")
target = "~/.config/karabiner/karabiner.json"

@default
@action(
    configurations="The configurations to merge",
    target="The target configuration where into which the configurations should be merged"
)
def karabiner(configurations=configurations, target=target):
    """
    Merges the given the Karabiner configurations into your system configuration.
    """
    mergefiles = path.existing(path.expandusers([target] + configurations))
    if not mergefiles:
        print("Karabiner configuration files don't exist")
        return
    print("Installing Karabiner configuration - merging {}".format(mergefiles))
    
    path.ensure_path_exists(target)
    tools.run(
        path.join(path.scriptdir, 'bin', 'json-merge-patch'),
        'merge',
        '-o', path.expanduser(target),
        *mergefiles
    )
