import json
from collections import OrderedDict


def remove_comments(data):
    sequence = "//"

    clean_data = ''
    data_buffer = data.partition(sequence)
    clean_data += data_buffer[0]
    while data_buffer[2] != "":
        data_with_comment: str = data_buffer[2]
        data_buffer = data_with_comment.partition("\n")[2]
        data_buffer = data_buffer.partition(sequence)
        clean_data += data_buffer[0]
    
    return clean_data


def data_save(filename: str, data: json):

    file = open(filename, "w", encoding="utf8")

    text = json.dumps(
        obj=data,
        indent=2,
        ensure_ascii=False
    )
    
    file.write(text)
    file.close()


def data_load(filename: str) -> json:
    f = open(filename, "r", encoding="utf8")

    if f.closed:
        print("File not opened")
        return None

    data = f.read()
    f.close()

    clean_data = remove_comments(data)

    return json.loads(clean_data, object_pairs_hook=OrderedDict)


def data_type(data: json) -> str:
    return data ['type']
