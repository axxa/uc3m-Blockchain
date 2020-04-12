import sys

import modules.cifrado as cifrado
import modules.signature as signature
import modules.utils as utils

'''
ej: CriptoFinanciera -m [cs | ds | h | vh | ca | da | cert | ts | tsv] [-p contraseña] 
                     -i fichero.xml [-ad adicionales.txt] [-o salida.cpt]
-m indica el modo:
    cs/ds: cifrado/descifrado simétrico. La contraseña se establecerá con -p
    h/vh: función resumen y su verificación
    ca/da: cifrado/descifrado asimétrico. Las claves pública/privada deberán guardarse en un fichero en la misma carpeta
    cert: Creación de un certificado X.509, cuyo nombre se especificará con -o
    ts/tsv: Sellado de tiempo y su verificación. La autoridad de sellado de tiempo podrá establecerse directamente en el 
            código fuente.
'''
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
    # en caso de verificacion resumen, se toma el string de sha256 despues del comando -ad
    sha256_infile = args.get('-ad')
    sha256_outfile = ''
    # validar modo
    if mode not in mode_array:
        raise ValueError(f'el modos disponibles:  {mode_array} ')
    if mode == 'cs':  # cifrado simetrico
        if password is not None and out_file is not None and in_file is not None:
            cifrado.encrypt_simetrico(in_file, out_file, password)
        else:
            raise ValueError(f'Ejecucion en modo cifrado tiene parametros incompletos')
    elif mode == 'ds':  # descifrado simetrico
        if password is not None and in_file is not None and out_file is not None:
            cifrado.decrypt_simetrico(in_file, out_file, password)
        else:
            #python3 __main__.py -m ds -p asd -i transaction.aes -o transaction_descifrada.xml
            raise ValueError(f'Ejecucion en modo descifrado tiene parametros incompletos')
    elif mode == 'h':  # funcion resumen (calculo sha256)
        if in_file is not None:
            sha256_infile = cifrado.calculate_sha256(in_file)
            print(f'sha256 para fichero {in_file}: {sha256_infile}')
    elif mode == 'vh':
        if in_file is not None:
            sha256_outfile = cifrado.calculate_sha256(in_file)
            if sha256_outfile is not None and sha256_infile is not None:
                print(f'sha256 para fichero {in_file}: {sha256_outfile}')
                print(f'Verificacion valida: {sha256_infile == sha256_outfile}')
            else:
                raise ValueError(f'Ejecucion en modo verificacion resumen tiene un sha256 vacio')

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        in_file, out_encrypted_file, out_decrypted_file, password = dummy_data()
        cifrado.encrypt_simetrico(in_file, out_encrypted_file, password)
        cifrado.decrypt_simetrico(out_encrypted_file, out_decrypted_file, password)
        sha256_infile = cifrado.calculate_sha256(in_file)
        sha256_outfile = cifrado.calculate_sha256(out_decrypted_file)
        key_pair, signature_ = signature.sign_file(in_file)
        signature.verify_signature(in_file, signature_, key_pair)
        print(f'sha256_infile:  {sha256_infile}\nsha256_outfile: {sha256_outfile}')
    else:
        if '--help' in args:
            utils.display_help()
        else:
            args_dict = utils.listToDict(args)
            execute_mode(args_dict)


