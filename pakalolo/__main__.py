from os.path import expanduser
import gnupg

def main(args=None):
    print("Pakalolo key manager")

def make_keying():
    # Create a keyring under ~/.pakalolo
    home = expanduser("~")
    gpg = gnupg.GPG(homedir=home + '/.pakalolo')

if __name__ == "__main__":
    main()