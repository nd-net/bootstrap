from .action import *
from . import path, tools
import subprocess

setting = path.configfiles("The Terminal.terminal")[0]

def read_plist(plist):
    """Read plist, even binary on Python 2.x"""
    import plistlib, subprocess
    args = ["/usr/bin/plutil", "-convert", "xml1", "-o", "-", path.expanduser(plist)]
    xml = subprocess.check_output(args)
    return plistlib.readPlistFromString(xml)

@default
@action(
    setting="the setting used as default setting"
)
def terminal_settings(setting=setting):
    """
    Configures the default setting of terminal to be a given setting
    """
    plist = path.expanduser("~/Library/Preferences/com.apple.Terminal.plist")
    expandedSetting = path.expanduser(setting)
    
    sleeptime = 1
    if not path.exists(expandedSetting):
        print("The terminal setting {} does not exist".format(setting))
        return
    settingName = subprocess.check_output(["/usr/libexec/PlistBuddy", expandedSetting, "-c", "print :name"]).strip()
    
    commands = [
        'add ":Window Settings:{}" dict',
        'merge "{1}" ":Window Settings:{0}"',
        'set ":Default Window Settings" "{}"',
        'set ":Startup Window Settings" "{}"'
    ]
    
    args = []
    for command in commands:
        args.append("-c")
        args.append(command.format(settingName, expandedSetting))
    
    print("Merging in setting {} from {}".format(settingName, setting))
    tools.run("/usr/libexec/PlistBuddy", plist, *args)
    
