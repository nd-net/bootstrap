from .action import action
from . import path, tools
    
@action(
    username="The OS's user name to check"
)
def icloud(username=tools.username):
    """
    Opens the iCloud preference pane for the user and tabs to the first entry if the user isn't signed in into iCloud.
    """
    try:
        print("Signed in {} with Apple ID {}.".format(username, tools.get_appleid(username)))
    except:
        print("Could not get Apple ID for {}. Opening System Preferences".format(username))
        tools.run("osascript", "-e", """
        tell application "System Preferences"
            activate
            reveal pane "iCloud"
        end tell
        tell application "System Events" to keystroke tab
        """)
