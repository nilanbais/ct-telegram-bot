
import os
import json


def read_json_file(json_file: str, path_to_file: str = "") -> dict:
    """Function to read the content of a json file.
        Optional: you can insert filpath as the file or split the file name and the path to file
    """
    _path = os.path.join(path_to_file, json_file)
    with open(_path, 'r') as json_file:
        data = json.load(json_file)
    return data


test = "C:\\Users\\Gebruiker\\OneDrive - DUX Data\\Documenten\\GitHub\\ct-telegram-bot\\bot\messages\\today.txt"

def read_txt_file(txt_file: str, path_to_file: str = "") -> str:
    _path = os.path.join(path_to_file, txt_file)
    with open(_path, 'r') as _file:
        lines = _file.readlines()
    
    text = " ".join(lines)
    return text