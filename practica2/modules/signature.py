import modules.utils as utils

from hashlib import sha256
from Crypto.PublicKey import RSA


def sign_file(in_file):
    key_pair = RSA.generate(bits=1024)
    # print(f"Public key:  (n={hex(key_pair.n)}, e={hex(key_pair.e)})")
    # print(f"Private key: (n={hex(key_pair.n)}, d={hex(key_pair.d)})")

    file_to_bytearray = utils.file_to_byte_array(in_file)
    # RSA sign the file
    hash_ = int.from_bytes(sha256(file_to_bytearray).digest(), byteorder='big')
    signature_ = pow(hash_, key_pair.d, key_pair.n)
    # print("Signature:", hex(signature_))
    return key_pair, signature_


def verify_signature(in_file, signature_, keyPair):
    # RSA verify signature
    file_to_bytearray = utils.file_to_byte_array(in_file)
    hash = int.from_bytes(sha256(file_to_bytearray).digest(), byteorder='big')
    hashFromSignature = pow(signature_, keyPair.e, keyPair.n)
    print("Signature valid:", hash == hashFromSignature)
