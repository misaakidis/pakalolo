import click
import os
import sys
import gnupg
from pakalolo import __version__

gpg = None

@click.group()
@click.option('--homedir', default=None, envvar='PAKALOLOHOME', type=click.Path(exists=False),
              help="set the directory to store the pakalolo keyring(default is ~/.pakalolo/)")
def cli(homedir):
    """pakalolo key management tool"""
    open_keying(homedir)


@cli.command()
def version():
    """print program version"""
    sys.exit('pakalolo ' + __version__)


def open_keying(homedir=None):
    """Open the pakalolo keyring"""
    if homedir is None:
        homedir = os.path.expanduser("~") + '/.pakalolo'
    if not os.path.exists(homedir):
        try:
            os.makedirs(homedir)
        except OSError as exception:
            sys.exit("pakalolo cannot create the directory: " + homedir)
    if not os.access(homedir, os.W_OK):
        sys.exit("pakalolo has no write access to the directory: " + homedir)
    global gpg
    gpg = gnupg.GPG(homedir=homedir)


if __name__ == "__main__":
    cli()