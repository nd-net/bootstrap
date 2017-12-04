from .action import *
from . import path, tools

assh_config = path.configfiles("assh.yml")
ssh_registration_urls = ["https://uberspace.de/dashboard/authentication"]

@default
@action(
    includes="The files that should be included in the assh configuration",
    target="The target file for the assh configuration",
    force="Use all specified includes, even those that don't exist"
)
def assh(target="~/.ssh/assh.yml", includes=assh_config, force=False):
    """
    Includes files in the ASSH configuration.
    """
    if not force:
        toInclude = path.existing(path.expandusers(includes))
    else:
        toInclude = includes
    toInclude = [path.compactuser(path.abspath(include)) for include in toInclude]
    
    if not includes:
        print("There are no exising include files at {}".includes)
        return
    
    print("Including {} into {}".format(toInclude, target))
    path.ensure_path_exists(target)
    tools.run(
        path.join(path.scriptdir, "bin", "include-assh"),
        "-t", path.expanduser(target),
        *toInclude
    )

@default
@action(
    type=dict(
        help="specifies the type of key to create",
        choices=["dsa", "ecdsa", "ed25519", "rsa", "rsa1"]
    ),
    keysize=dict(
        help="specifies the number of bits in the key to create",
        metavar="bits"
    ),
    idfile="the name of the SSH key file. If not specified, then this will be retrieved from the type",
    urls=dict(
        help="when creating a new SSH key pair, the public key gets copied into the clipboard and these websites are opened",
        metavar="url"
    ),
    open_urls_for_existing_file="opens the URLs even if the idfile already exists"
)
def ssh_keygen(type="rsa", keysize=4096, idfile=None, urls=ssh_registration_urls, open_urls_for_existing_file=False):
    """
    Copies ssh_config into your .ssh directory.
    If no public key is present, then this creates a
    new SSH public key pair. After key creation,
    this opens webpages where you can add SSH websites and
    copies the public key into the clipboard unless you
    did not specify --open-urls
    """
    if not idfile:
        idfile = path.expanduser("~/.ssh/id_{}.pub".format(type))
    if path.exists(idfile):
        print("SSH key file {} already exists".format(idfile))
        if not open_urls_for_existing_file:
            return
    else:
        print("SSH key file {} does not exist, creating new one with {} and size {}".format(idfile, type, keysize))
        tools.run("ssh-keygen", "-t", type, "-b", str(keysize), "-f", idfile)
    if not open_urls_for_existing_file:
        print("Skipping SSH key registration")
        return
    print("Copying SSH key into clipboard")
    import subprocess
    subprocess.call("/usr/bin/pbcopy", stdin=open(idfile))
    for url in open_urls:
        print("Opening {}".format(url))
        tools.run("open", "https://uberspace.de/dashboard/authentication")

