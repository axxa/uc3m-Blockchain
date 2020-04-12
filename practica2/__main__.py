import sys

import modules.cifrado as cifrado
import modules.signature as signature
import modules.utils as utils

mode_array = ['cs', 'ds', 'h', 'vh', 'ca', 'da', 'cert', 'ts', 'tsv']

def dummy_data():
    in_file = "transaction.xml"
    out_encrypted_file = "transaction.aes"
    out_decrypted_file = "decrypt_out.xml"
    password = "asd"
    return in_file, out_encrypted_file, out_decrypted_file, password

def execute_mode(args):
    mode = args.get('-m')
    password = args.get('-p')
    in_file = args.get('-i')
    out_file = args.get('-o')
    # validar modo
    if mode not in mode_array:
        raise ValueError(f'el modos disponibles:  {mode_array} ')
    if mode == 'cs':  # cifrado simetrico
        if password is not None and out_file is not None and in_file is not None:
            cifrado.encrypt(in_file, out_file, password)
        else:
            raise ValueError(f'Ejecucion en modo cifrado tiene parametros incompletos')
    elif mode == 'ds':  # descifrado simetrico
        if password is not None and in_file is not None and out_file is not None:
            cifrado.decrypt(in_file, out_file, password)
        else:
            raise ValueError(f'Ejecucion en modo descifrado tiene parametros incompletos')


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) == 0:
        in_file, out_encrypted_file, out_decrypted_file, password = dummy_data()
    else:
        args_dict = utils.listToDict(args)
        execute_mode(args_dict)

    '''sha256_infile = cifrado.calculate_sha256(in_file)

    sha256_outfile = cifrado.calculate_sha256(out_decrypted_file)

    key_pair, signature_ = signature.sign_file(in_file)

    signature.verify_signature(in_file, signature_, key_pair)

    print(f'sha256_infile:  {sha256_infile}\nsha256_outfile: {sha256_outfile}')'''

