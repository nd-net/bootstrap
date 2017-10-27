import subprocess

def run(command, *args):
    returncode = subprocess.call(["/usr/bin/env", command] + list(args))
    if returncode in (126, 127):
        raise NameError("{} does not exist.".format(command))
    return returncode
