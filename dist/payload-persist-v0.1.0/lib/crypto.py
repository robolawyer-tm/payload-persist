import gnupg
from . import config

def get_gpg():
    return gnupg.GPG(gnupghome=config.GNUPG_HOME)

def encrypt_secret(secret_text, passphrase):
    gpg = get_gpg()
    return gpg.encrypt(
        secret_text,
        recipients=None,
        symmetric=True,
        passphrase=passphrase
    )

def decrypt_secret(encrypted_text, passphrase):
    gpg = get_gpg()
    return gpg.decrypt(encrypted_text, passphrase=passphrase)
