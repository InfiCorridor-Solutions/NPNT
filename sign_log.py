import json
import os
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import decimal
import base64
import sys

MOCK_LOG =  os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "unsigned_Flight_Log.json")
print(MOCK_LOG)


def sign_log(log_path, private_key_path, out_path=None):
    """
    Function to sign a flight log.
    :param log_path: path to log file to be signed
    :param private_key_path: path to the private key to be used for signing.
    :param out_path: path to save the signed log file -
            defaults to '-signed' added to it's name if no path is specified
    :return: None
    """
    with open(log_path, "rb") as log_obj, open(private_key_path) as key_ob:
        jd = json.loads(log_obj.read(), parse_float = decimal.Decimal())
        rsa_key = RSA.import_key(key_ob.read())
        # print("__signdata to sha256 = __" + json.dumps((jd['FlightLog'])) + "__")
        hashed_logdata = SHA256.new(json.dumps((jd['FlightLog']), separators=(',',':')).encode())
        log_signature = pkcs1_15.new(rsa_key).sign(hashed_logdata)
        # the signature is encoded in base64 for transport
        enc = base64.b64encode(log_signature)
        # dealing with python's byte string expression
        jd['Signature'] = enc.decode('ascii')
    if out_path:
        save_path = out_path
    else:
        save_path = log_path[:-5] + "-signed.json"
    with open(save_path, 'w') as outfile:
        json.dump(jd, outfile, indent=4)
    return save_path

if __name__ == "__main__":
    sign_log(MOCK_LOG, sys.argv[1])