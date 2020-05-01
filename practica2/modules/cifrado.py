import pyAesCrypt
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


bufferSize = 64 * 1024
public_key_path = 'public_key.pem'
private_key_path = 'private_key.pem'
cert_path = 'certX509.crt'

# Cifrado Simetrico-------------------------------------------------------------------------------
def encrypt_simetrico(in_file, out_encrypted_file, password):
    print(f'Resultado de encripcion en {out_encrypted_file}')
    pyAesCrypt.encryptFile(in_file, out_encrypted_file, password, bufferSize)


def decrypt_simetrico(out_encrypted_file, out_decrypted_file, password):
    print(f'Resultado de desencriptado en {out_decrypted_file}')
    pyAesCrypt.decryptFile(out_encrypted_file, out_decrypted_file, password, bufferSize)
# ------------------------------------------------------------------------------------------------


# Cifrado Asimetrico-------------------------------------------------------------------------------
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048*2,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def store_keys(private_key, public_key):
    # private key
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(private_key_path, 'wb') as f:
        f.write(pem)

    # public key
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(public_key_path, 'wb') as f:
        f.write(pem)


def create_keys():
    private_key, public_key = generate_keys()
    store_keys(private_key, public_key)
    # create_self_signed_cert(cert_path, private_key)


def read_public_key():

    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def read_private_key():
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    return private_key


def encrypt_asimetrico(in_file, out_file):
    # message = b'encrypt me!'
    with open(in_file, "rb") as f:
        bytes_ = f.read()  # read entire file as bytes

    public_key = read_public_key()

    encrypted = public_key.encrypt(
        bytes_,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA1(),
            # algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(out_file, 'wb') as f:
        f.write(encrypted)


def decrypt_asimetrico(in_file, out_file):
    private_key = read_private_key()
    with open(in_file, "rb") as f:
        encrypted = f.read()  # read entire file as bytes

    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )

    with open(out_file, 'wb') as f:
        f.write(original_message)

# ------------------------------------------------------------------------------------------------


def calculate_sha256(in_file):
    with open(in_file, "rb") as f:
        bytes_ = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes_).hexdigest();
        return readable_hash
