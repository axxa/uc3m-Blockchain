import pyAesCrypt
import hashlib

bufferSize = 64 * 1024

# Cifrado Simetrico-------------------------------------------------------------------------------
def encrypt(in_file, out_encrypted_file, password):
    print(f'Resultado de encripcion en {out_encrypted_file}')
    pyAesCrypt.encryptFile(in_file, out_encrypted_file, password, bufferSize)


def decrypt(out_encrypted_file, out_decrypted_file, password):
    print(f'Resultado de desencriptado en {out_decrypted_file}')
    pyAesCrypt.decryptFile(out_encrypted_file, out_decrypted_file, password, bufferSize)
#------------------------------------------------------------------------------------------------

def calculate_sha256(in_file):
    with open(in_file, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        return readable_hash