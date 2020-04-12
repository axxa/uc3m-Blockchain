
def file_to_byte_array(in_file):
    with open(in_file, 'rb') as file_t:
        blob_data = bytearray(file_t.read())
        return blob_data

def listToDict(lst):
    op = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return op