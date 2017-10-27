from . import action, path, tools

assh_config = path.configfiles("assh.yml")

@action.action(
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
        path.join(path.scriptdir, 'bin', 'include-assh'),
        '-t', path.expanduser(target),
        *toInclude
    )
