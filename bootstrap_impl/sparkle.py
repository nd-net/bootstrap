from .action import *
from . import path, tools
import os, plistlib

def find_sparkle_apps(directory):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if ("sparkle.framework" == d.lower()):
                yield os.path.join(root, '../..')


@action(
    directories=argument(
        help="The directories that get searched for applications with Sparkle.framework",
        metavar="dir"
    )
)
def sparkle(directories=["/Applications"]):
    for directory in directories:
        for app in find_sparkle_apps(directory):
            info_plist = os.path.join(app, 'Contents/Info.plist')
            print(info_plist)
            plist = plistlib.readPlist(info_plist)
            print("%s: %s" % (app, plist[SUFeedURL]))