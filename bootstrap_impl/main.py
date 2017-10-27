__all__ = [
    'main'
]

from . import action, brew

def main():
    import sys
    if not action.execute_actions(sys.argv[1:]):
        action.print_help()
