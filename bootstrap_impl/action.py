import argparse

parser = argparse.ArgumentParser(
    description="""
        Performs a bootstrap installation of your system.
    """)
subparsers = parser.add_subparsers()

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
        name = arg if arg else fn.__name__.replace("_", "-")
        subparser = subparsers.add_parser(name, help=fn.__doc__, description=fn.__doc__)
        subparser.set_defaults(action=fn)
        
        import inspect
        specs = inspect.getargspec(fn)
        if specs.defaults and len(specs.args) == len(specs.defaults):
            for name, default in zip(specs.args, specs.defaults):
                add_argument(subparser, name, default, kw.get(name))
        
        fn.parser = subparser
        return fn
    return add_parser

def execute_actions(arguments):
    rest = arguments
    args = argparse.Namespace()
    executed = []
    while rest:
        args, rest = parser.parse_known_args(rest, namespace=args)
        kw = dict(vars(args))
        del kw["action"]
        args.action(**kw)
        executed.append(args.action)
    return executed

def print_help():
    parser.print_help()

def add_all_configuration():
    called = list(subparsers.choices.keys())
    try:
        called.remove("edit")
    except ValueError:
        pass
    def execute_all(**kw):
        for name in called:
            parser = subparsers.choices[name]
            parser.get_default("action")(**kw)

    all = subparsers.add_parser("all", parents=[], conflict_handler="resolve", help="Executes all options using default arguments: {}".format(called))
    all.set_defaults(action=execute_all)
    
    help = subparsers.add_parser("help", help="Print help information. Similar to -h")
    help.set_defaults(action=print_help)
