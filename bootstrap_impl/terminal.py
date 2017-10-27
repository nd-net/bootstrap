from .action import action
from . import path, tools

setting = path.configfiles("The Terminal.terminal")[0]

def read_plist(plist):
    """Read plist, even binary on Python 2.x"""
    import plistlib, subprocess
    args = ["/usr/bin/plutil", "-convert", "xml1", "-o", "-", path.expanduser(plist)]
    xml = subprocess.check_output(args)
    return plistlib.readPlistFromString(xml)

@action(
    setting="the setting used as default setting"
)
def termsettings(setting=setting):
    """
    Configures the default setting of terminal to be a given setting
    """
    plist = "~/Library/Preferences/com.apple.Terminal.plist"
    sleeptime = 1
    if not path.exists(setting):
        print("The terminal setting {} does not exist".format(setting))
        return
    settingName = path.splitext(path.basename(setting))[0]
    
    xml = read_plist(plist)
    if settingName in xml.get("Window Settings", {}):
        print("{} is already a known terminal setting".format(settingName))
    else:
        import time
        print("Importing {} and waiting until {} is present".format(setting, settingName))
        tools.run("open", path.expanduser(setting))
        while settingName not in xml.get("Window Settings", {}):
            time.sleep(sleeptime)
            xml = read_plist(plist)
        print("{} is now present".format(settingName))
    
    print("Applying default terminal settings")
    tools.run(
        "osascript", 
        "-e",
        'tell application "Terminal" to set default settings to settings set "{}"'.format(settingName))
