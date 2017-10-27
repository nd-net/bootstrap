from . import action, tools
@action.action(
    xcode=dict(help="The path to Xcode", metavar="path")
)
def xcode(xcode="/Applications/Xcode.app"):
    """
    Selects the current Xcode from /Applications and accepts the Xcode license.
    """
    print("Selecting Xcode {}".format(xcode))
    tools.run("sudo", "xcode-select", "-switch", xcode)
    tools.run("sudo", "xcodebuild", "-license", "accept")
