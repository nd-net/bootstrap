from .action import *
from . import tools

@default
@action(
    xcode=argument(help="The path to Xcode", metavar="path")
)
def xcode(xcode="/Applications/Xcode.app"):
    """
    Selects the current Xcode from /Applications and accepts the Xcode license.
    """
    print("Selecting Xcode {}".format(xcode))
    tools.run("sudo", "xcode-select", "-switch", xcode)
    tools.run("sudo", "xcodebuild", "-license", "accept")

@default
@action(
    devices="The devices to delete. Use 'unavailable' to specify all devices that are not available in Xcode anymore."
)
def delete_ios_simulators(devices=["unavailable"]):
    """
    Deletes the given devices from the Xcode simulators.
    """
    print("Deleting Xcode iOS simulators for {}".format(devices))
    tools.run("xcrun", "simctl", "delete", *devices)
    