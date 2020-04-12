
def file_to_byte_array(in_file):
    with open(in_file, 'rb') as file_t:
        blob_data = bytearray(file_t.read())
        return blob_data

def listToDict(lst):
    op = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return op

def display_help():
    print('ej: CriptoFinanciera -m [cs | ds | h | vh | ca | da | cert | ts | tsv] [-p contraseña]'
          '-i fichero.xml [-ad adicionales.txt] [-o salida.cpt]')
    print(' -m indica el modo:')
    print(' cs/ds: cifrado/descifrado simétrico. La contraseña se establecerá con -p')
    print(' h/vh: función resumen y su verificación')
    print(' ca/da: cifrado/descifrado asimétrico. Las claves pública/privada deberán guardarse en '
          ' un fichero en la misma carpeta')
    print(' cert: Creación de un certificado X.509, cuyo nombre se especificará con -o')
    print(' ts/tsv: Sellado de tiempo y su verificación. La autoridad de sellado de tiempo podrá establecerse '
          'directamente en el código fuente.')