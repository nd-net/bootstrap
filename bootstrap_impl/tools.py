import subprocess, plistlib, getpass

username = getpass.getuser()

def run(command, *args):
    returncode = subprocess.call(["/usr/bin/env", command] + list(args))
    if returncode in (126, 127):
        raise NameError("{} does not exist.".format(command))
    return returncode

def get_appleid(user=None):
    if not user:
        user = username
    try:
        dscl = subprocess.check_output(["/usr/bin/env", "dscl", ".", "readpl", "/Users/{}".format(user), "dsAttrTypeNative:LinkedIdentity", "appleid.apple.com:linked identities"])
        plist = dscl.split("\n", 1)[1]
        appleid = plistlib.readPlistFromString(plist)
        return appleid[0]["full name"]
    except:
        return None
        