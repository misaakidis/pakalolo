import click
import os
import sys
import gnupg
import pickle
from pakalolo import claimchain, __version__

gpg = None
storedir = None
chain = None
chain_updated = False


@click.group(invoke_without_command=True)
@click.option('--homedir', default=None, envvar='PAKALOLOHOME', type=click.Path(exists=False),
              help="set the keyring directory (default is ~/.pakalolo/)")
def cli(homedir):
    """pakalolo key management tool"""
    open_keying(homedir)
    global chain
    chain = load_chain('pakalolo')
    if chain is None:
        if click.confirm("No claimchain was found in directory " + storedir +
                                 ", would you like to create one?", abort=True):
            chain = first_run()
    if len(chain.store) == 0:
        if click.confirm("Your claimchain contains no keys, would you like to create one?", abort=True):
            chain = first_run()
    if chain_updated and click.confirm('Do you want to save your changes?', abort=True):
        store_chain('pakalolo')


@cli.command()
def version():
    """print program version"""
    sys.exit('pakalolo ' + __version__)


def first_run():
    print "Welcome to pakalolo"
    print "generating your first key..."
    alice_key = gen_key()
    chain = claimchain.Chain()
    chain.multi_add([alice_key.fingerprint])
    global chain_updated
    chain_updated = True
    return chain


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
    save_pickle(chain.store, '/' + store_file)


def load_chain(store_file):
    """
    Restore a claimchain from a saved store

    :return: A claimchain instance with the items from the saved store, or None if the store does
            not exist or cannot be loaded.
    """
    try:
        store = load_pickle(store_file)
        chain = claimchain.Chain(store)
    except:
        return None
    return chain


def save_pickle(obj, name):
    path = os.path.join(storedir + name + '.pkl')
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_pickle(name):
    path = os.path.join(storedir + name + '.pkl')
    with open(path, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    cli()