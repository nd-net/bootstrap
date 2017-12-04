from .action import *
from . import path, tools, brew
import subprocess

def parse_brewfiles(brewfiles):
    import re
    from collections import defaultdict
    matches = defaultdict(set)
    
    for brewfile in path.expandusers(brewfiles):
        if not path.exists(brewfile):
            continue
        with open(brewfile) as file:
            brewfile = file.read()
        launches = re.finditer(r'''
            (?x)
            (?<!\#)
            (?P<type>cask|mas)
            \s.*?
            (?P<namedelimiter>[''])(?P<name>.*)(?P=namedelimiter)
            .*
            \#.*\blaunch\b
            (?:
                \:(?P<appdelimiter>['']?)
                (?P<app>.*)
                (?P=appdelimiter)
            )?
        ''', brewfile)
        for launch in launches:
            app = launch.group('app')
            if app:
                matches['app'].add(app)
            else:
                matches[launch.group('type')].add(launch.group('name'))
    return matches

def find_cask_locations(casks):
    if not casks:
        return
    try:
        args = ['/usr/bin/env', 'brew', 'cask', 'list']
        args += casks
        info = subprocess.check_output(args)
    except subprocess.CalledProcessError as e:
        info = e.output
    import re
    apps = re.finditer(r'''
        (?x)
        ==>\ Apps
        \s+
        (?P<app>.*)\s+\(
    ''', info)
    for app in apps:
        yield app.group('app')
    
def find_app_locations(appNames):
    for name in appNames:
        if '/' in name:
            yield name
        else:
            yield '/Applications/{}.app'.format(name)

def find_apps_to_launch(brewfiles):
    matches = parse_brewfiles(brewfiles)

    appNames = list(find_cask_locations(matches['cask']))
    for key in ('app', 'mas'):
        appNames += find_app_locations(matches[key])
    return appNames

def launch_apps(appNames):
    running = subprocess.check_output(['/usr/bin/env', 'ps', 'aux'])
    for name in appNames:
        if name in running:
            print('Already started: {}'.format(name))
            continue
        print('Starting {}'.format(name))
        tools.run('open', name)

@default
@action(
    brewfiles="The files to be used for homebrew"
)
def launch(brewfiles=brew.brewfiles):
    """
    Launches all items selected in the Brewfile that have a # launch comment
    """
    appNames = find_apps_to_launch(brewfiles)
    if appNames:
        launch_apps(appNames)
    else:
        print("Did not find any launch apps")        
