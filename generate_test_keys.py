import sys  
import cryptography
from Cryptodome.PublicKey import RSA
import os

def create_keys(folder, keyname):

    """
    create a RSA 2048 keypair
    :param folder: path to save the keypair
    :param str keyname: name of the key pair to save as keyname_private.pem,and keyname_public.pem
    :return:
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    with open(os.path.join(folder, keyname + "_private.pem"), "wb") as file_out:
        file_out.write(private_key)

    public_key = key.publickey().export_key()
    with open(os.path.join(folder, keyname + "_public.pem"), "wb") as file_out:
        file_out.write(public_key)


if __name__ == "__main__":
    create_keys(sys.argv[1], sys.argv[2])
    