import json
from collections import OrderedDict
import glob


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


def insert_language_comment(text) -> str:
    splited_text = text.split('"translations": [', 1)
    text_with_comment = splited_text[0]
    text_with_comment += '"translations": [\n\n'
    text_with_comment += '// Error codes (Do not edit this section, including the comment)\n'
    text_with_comment += '// BEGIN STATUS MANAGED SECTION'
    text_with_comment += splited_text[1]
    return text_with_comment


def data_save(filename: str, data: json):

    file = open(filename, "w", encoding="utf8")

    text = json.dumps(
        obj=data,
        indent=2,
        ensure_ascii=False
    )

    if data_type(data) == 'languageDefinition':
        text = insert_language_comment(text)

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


def dir_load(dir_path, type: set = '.json') -> list:
    format = '/*.json'
    files = glob.glob(dir_path + format)

    data = []
    for file in files:
        new_data = data_load(file)
        if new_data is not None:
            print('File loaded: ', file)
            data.append((file, new_data))
        else:
            print('File cannot by loaded: ', file)

    return data
