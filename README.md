# bootstrap

Bootstrap prepares a new Mac to a working state with the following features:

* *brew*: Installs [homebrew](http://brew.sh) and uses ``brew bundle`` to install standard programs using a Brewfile from the config-directory
* *dropbox*: Starts [Dropbox](http://dropbox.com) so that it can sync data such as 1password vaults
* *pip*: Installs Python 3 packages from a given ``requirements.txt``
* *pipdate*: Updates all existing Python 3 packages

# Installation

Install the tool via ``curl -fsSL https://raw.githubusercontent.com/nd-net/bootstrap/master/bootstrap|/usr/bin/python -``
