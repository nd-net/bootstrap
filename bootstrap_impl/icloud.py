from .action import action
from . import path, tools
import getpass

username = getpass.getuser()
    
@action(
    username="The OS's user name to check"
)
def icloud(username=username):
    """
    Opens the iCloud preference pane for the user and tabs to the first entry if the user isn't signed in into iCloud.
    """
    try:
        import subprocess
        dscl = subprocess.check_output(["/usr/bin/env", "dscl", ".", "readpl", "/Users/{}".format(username), "dsAttrTypeNative:LinkedIdentity", "appleid.apple.com:linked identities"])
        plist = dscl.split("\n", 1)[1]
        import plistlib
        appleid = plistlib.readPlistFromString(plist)
        print("Signed in {} with Apple ID {}.".format(username, appleid[0]["full name"]))
    except:
        print("Could not get Apple ID for {}. Opening System Preferences".format(username))
        tools.run("osascript", "-e", """
        tell application "System Preferences"
            activate
            reveal pane "iCloud"
        end tell
        tell application "System Events" to keystroke tab
        """)
