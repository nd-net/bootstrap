__all__ = [
    'main'
]

from . import action
# order here is important: the order in which these imports are made is the order in which they are shown and executed
from . import icloud, brew, dropbox, pip, karabiner, ssh, xcode, xonsh, launch, terminal, defaults

def main():
    action.add_all_configuration()
    
    import sys
    if not action.execute_actions(sys.argv[1:]):
        action.print_help()
