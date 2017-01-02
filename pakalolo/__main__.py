import click
import os
import sys
import gnupg
import hippiehug
import pickle
from pakalolo import __version__

gpg = None
storedir = None
claimchain = None


@click.group(invoke_without_command=True)
@click.option('--homedir', default=None, envvar='PAKALOLOHOME', type=click.Path(exists=False),
              help="set the keyring directory (default is ~/.pakalolo/)")
def cli(homedir):
    """pakalolo key management tool"""
    open_keying(homedir)
    global claimchain
    claimchain = load_chain('pakalolo')
    if claimchain.store.__len__() == 0:
        first_run()
    if click.confirm('Do you want to save your changes?', abort=True):
        store_chain('pakalolo')


@cli.command()
def version():
    """print program version"""
    sys.exit('pakalolo ' + __version__)


def first_run():
    print "Welcome to pakalolo"
    alice_key = gen_key()
    global claimchain
    claimchain.multi_add([alice_key.fingerprint])


def open_keying(homedir=None):
    """Open the pakalolo keyring"""
    if homedir is None:
        homedir = os.path.expanduser("~") + '/.pakalolo/'
    if not os.path.exists(homedir):
        try:
            os.makedirs(homedir)
        except OSError as exception:
            sys.exit("pakalolo cannot create the directory: " + homedir)
    if not os.access(homedir, os.W_OK):
        sys.exit("pakalolo has no write access to the directory: " + homedir)
    global gpg
    global storedir
    storedir = homedir
    gpg = gnupg.GPG(homedir=homedir)


def gen_key():
    alice = {'name_real': 'Alice',
             'name_email': 'alice@inter.net',
             'expire_date': '2017-04-01',
             'key_type': 'RSA',
             'key_length': 1024,
             'key_usage': '',
             'subkey_type': 'RSA',
             'subkey_length': 1024,
             'subkey_usage': 'encrypt,sign,auth',
             'passphrase': 'sekrit'}
    alice_input = gpg.gen_key_input(**alice)
    alice_key = gpg.gen_key(alice_input)
    return alice_key


def store_chain(store_file):
    """Save the claimchaine store in the homedir"""
    save_pickle(claimchain.store, '/' + store_file)

def load_chain(store_file):
    """
    Restore a claimchain from a saved store

    :return: A claimchain instance with the items from the saved store, or an empty claimchain if the store does
            not exist or cannot be read.
    """
    try:
        store = load_pickle(store_file)
        claimchain = hippiehug.Chain(store)
    except:
        claimchain = hippiehug.Chain()
    return claimchain


def save_pickle(obj, name):
    with open(storedir+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_pickle(name):
    with open(storedir + name + '.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    cli()