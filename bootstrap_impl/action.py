import argparse

_parser = argparse.ArgumentParser(
    description="""
        Performs a bootstrap installation of your system.
    """)
_subparsers = _parser.add_subparsers()

_default_parsers = []

def default(fn):
    _default_parsers.append(fn.parser_name)
    return fn

def action(arg=None, **kw):
    if callable(arg):
        return action(None, **kw)(arg)
    def add_argument(parser, name, default, help):
        with_dashes = name.replace("_", "-")
        names = ["-{}".format(name[0]), "--{}".format(with_dashes)]
        args = dict(help=help, default=default, type=type(default), action="store")
        defaultstr = str(default)
        if type(help) is dict:
            args.update(help)
        if default == False:
            args["action"] = "store_true"
            del args["type"]
        elif default == True:
            help = args.get("help")
            if help:
                args["help"] = "disable " + help
            args["action"] = "store_false"
            defaultstr = str(False)
            del args["type"]
        elif type(default) is list:
            args["nargs"] = "*"
            try:
                args["type"] = type(default[0])
            except:
                del args["type"]
            defaultstr = "[{}]".format(", ".join(default))
        args["help"] = "{help}\n(default: {defaultstr})".format(defaultstr=defaultstr, **args)
        parser.add_argument(*names, **args)
        return parser

    def add_parser(fn):
        action_name = arg if arg else fn.__name__.replace("_", "-")
        subparser = _subparsers.add_parser(action_name, help=fn.__doc__, description=fn.__doc__)
        subparser.set_defaults(action=fn)
        
        import inspect
        specs = inspect.getargspec(fn)
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
    for config in except_configuration:
        try:
            _default_parsers.remove(config)
        except ValueError:
            pass
    def execute_all(**kw):
        for name in _default_parsers:
            parser = _subparsers.choices[name]
            parser.get_default("action")(**kw)

    all = _subparsers.add_parser("all", parents=[], conflict_handler="resolve", help="Executes all options using default arguments: {}".format(_default_parsers))
    all.set_defaults(action=execute_all)
    
    help = _subparsers.add_parser("help", help="Print help information. Similar to -h")
    help.set_defaults(action=print_help)
