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
    type=argument(
        help="specifies the type of key to create",
        choices=["dsa", "ecdsa", "ed25519", "rsa", "rsa1"]
    ),
    keysize=argument(
        help="specifies the number of bits in the key to create",
        metavar="bits",
        type=int
    ),
    id_file="the name of the SSH key file. If not specified, then this will be retrieved from the type",
    pem="save the private keys in PEM format instead of RFC4716 format",
    derivation_rounds=argument(
        help="the number of KDF (key derivation function) rounds used. If nothing is specified and using RFC4716, then a default of 100 will be used",
        type=int
    ),
    comment=argument(
        help="The comment to use for the key",
        type=str
    ),
    urls=argument(
        help="when creating a new SSH key pair, the public key gets copied into the clipboard and these websites are opened",
        metavar="url"
    ),
    force="create a new key even if another already exits",
    open_urls_for_existing_file="opens the URLs even if the idfile already exists"
)
def ssh_keygen(type="ed25519", keysize=None, id_file=None, pem=False, derivation_rounds=None, comment=None, force=False, urls=ssh_registration_urls, open_urls_for_existing_file=False):
    """
    Copies ssh_config into your .ssh directory.
    If no public key is present, then this creates a
    new SSH public key pair. After key creation,
    this opens webpages where you can add SSH websites and
    copies the public key into the clipboard unless you
    did not specify --open-urls
    """
    if not id_file:
        id_file = path.expanduser("~/.ssh/id_{}".format(type))
    pub_file = id_file + ".pub"
    
    if path.exists(id_file) and path.exists(pub_file) and not force:
        print("SSH key file {} already exists".format(id_file))
        if not open_urls_for_existing_file:
            return
    else:
        params = ["-t", type, "-f", id_file];
        if keysize:
            params += ["-b", str(keysize)]
        if not pem:
            params += ["-o"]
            if derivation_rounds is None:
                derivation_rounds = 100
        if derivation_rounds:
            if not pem:
                params += ["-a", str(derivation_rounds)]
            else:
                print("Using key derivation {} with PEM is not supported".format(derivation_rounds))
        if comment is not None:
            params += ["-C", comment]
        print("SSH key file {} does not exist, creating new one with {}, format {} (with {} derivation rounds) and size {}".format(id_file, type, "PEM" if pem else "RFC4716", derivation_rounds or 0, keysize or "default"))
        tools.run("ssh-keygen", *params)
        
    print("Copying SSH key into clipboard")
    import subprocess
    subprocess.call("/usr/bin/pbcopy", stdin=open(pub_file))
    for url in urls:
        print("Opening {}".format(url))
        tools.run("open", "https://uberspace.de/dashboard/authentication")

