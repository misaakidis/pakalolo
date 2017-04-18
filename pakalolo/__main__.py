import click
import os
import sys
import gnupg
import pickle
from pakalolo import claimchain, __version__


@click.group(invoke_without_command=True)
@click.option('--homedir', default=None, envvar='PAKALOLOHOME', type=click.Path(exists=False),
              help="set the keyring directory (default is ~/.pakalolo/)")
def cli(homedir):
    """pakalolo key management tool"""
    chain_updated = False
    storedir, gpg = open_keying(homedir)
    chain = load_chain(storedir)
    if chain is None:
        if click.confirm("No claimchain was found in directory " + storedir +
                                 ", would you like to create one?", abort=True):
            chain, chain_updated = first_run(gpg)
    if len(chain.store) == 0:
        if click.confirm("Your claimchain contains no keys, would you like to create one?", abort=True):
            chain, chain_updated = first_run(gpg)
    if chain_updated and click.confirm('Do you want to save your changes?', abort=True):
        store_chain(chain, storedir)


@cli.command()
def version():
    """print program version"""
    sys.exit('pakalolo ' + __version__)


def first_run(gpg):
    print("Welcome to pakalolo")
    print("generating your first key...")
    alice_key = gen_key(gpg)
    chain = claimchain.Chain()
    chain.multi_add([alice_key.fingerprint])
    chain_updated = True
    return chain, chain_updated


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
    gpg = gnupg.GPG(homedir=homedir)
    return homedir, gpg


def gen_key(gpg):
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


def store_chain(chain, storedir, filename='pakalolo'):
    """Save the claimchaine store in the homedir"""
    save_pickle(chain.store, storedir, filename)


def load_chain(storedir, filename='pakalolo'):
    """
    Restore a claimchain from a saved store

    :return: A claimchain instance with the items from the saved store, or None if the store does
            not exist or cannot be loaded.
    """
    try:
        store = load_pickle(storedir, filename)
        chain = claimchain.Chain(store)
    except:
        return None
    return chain


def save_pickle(obj, dir, filename):
    path = os.path.join(dir + filename + '.pkl')
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_pickle(dir, filename):
    path = os.path.join(dir + filename + '.pkl')
    with open(path, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    cli()