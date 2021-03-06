import argparse

_parser = argparse.ArgumentParser(
    description="""
        Performs a bootstrap installation of your system.
    """)
_subparsers = _parser.add_subparsers()

_default_parsers = []
_upgrade_parsers = []

def argument(help=None, metavar=None, choices=None, nargs=None, required=None, type=None):
    return dict(kv for kv in vars().items() if kv[1])

def default(fn):
    _default_parsers.append(fn.parser_name)
    return fn

def upgrade(fn):
    _upgrade_parsers.append(fn.parser_name)
    return fn

def action(_=None, **kw):
    # if action is used like this @action, then it is called with the function as its own argument,
    # yet when it is used like @action(), then the result of the action is called with the function
    # unify this
    if callable(_):
        return action(None, **kw)(_)
    def add_argument(parser, name, default, help):
        with_dashes = name.replace("_", "-")
        names = ["-{}".format(name[0]), "--{}".format(with_dashes)]
        args = dict(help=help, default=default, type=type(default), action="store")
        defaultstr = str(default)
        if type(help) is dict:
            args.update(help)
        if default == False:
            args["action"] = "store_true"
            defaultstr = None
            del args["type"]
        elif default == True:
            help = args.get("help")
            if help:
                args["help"] = "disable " + help
            args["action"] = "store_false"
            defaultstr = None
            del args["type"]
        elif type(default) is list:
            args.setdefault("nargs", "*")
            try:
                args["type"] = type(default[0])
            except:
                del args["type"]
            defaultstr = "[{}]".format(", ".join(default))
        if defaultstr and default is not None:
            args["help"] = "{help}\n(default: {defaultstr})".format(defaultstr=defaultstr, **args)
        parser.add_argument(*names, **args)
        return parser

    def add_parser(fn):
        action_name = fn.__name__.replace("_", "-")
        subparser = _subparsers.add_parser(action_name, help=fn.__doc__, description=fn.__doc__)
        subparser.set_defaults(action=fn)
        
        import inspect
        specs = inspect.getargspec(fn)
        # only add arguments if all of them have defaults
        if specs.defaults and len(specs.args) == len(specs.defaults):
            for name, default in zip(specs.args, specs.defaults):
                add_argument(subparser, name, default, kw.get(name))
        
        fn.parser = subparser
        fn.parser_name = action_name
        return fn
    return add_parser

def execute_actions(arguments):
    rest = arguments
    args = argparse.Namespace()
    executed = []
    while rest:
        args, rest = _parser.parse_known_args(rest, namespace=args)
        kw = dict(vars(args))
        del kw["action"]
        args.action(**kw)
        executed.append(args.action)
    return executed

def print_help():
    _parser.print_help()

def add_all_configuration(*except_configuration):
    def add_configuration(name, parsers):
        for config in except_configuration:
            try:
                parsers.remove(config)
            except ValueError:
                pass
        def execute_all(**kw):
            for name in parsers:
                parser = _subparsers.choices[name]
                parser.get_default("action")(**kw)

        all = _subparsers.add_parser(name, parents=[], conflict_handler="resolve", help="Executes {} options using default arguments: {}".format(name, parsers))
        all.set_defaults(action=execute_all)
    
    add_configuration("all", _default_parsers)
    add_configuration("upgrade", _upgrade_parsers)
    
    help = _subparsers.add_parser("help", help="Print help information. Similar to -h")
    help.set_defaults(action=print_help)
