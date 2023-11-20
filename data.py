from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import json
import os

PNG_SIGNATURE = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])    

DEFAULT_IMAGE : bytearray

EXAMPLE_IMAGE : bytearray

LOGO_IMAGE : bytearray

class Package:
    def __init__(self, name, desc, data, images):
        self.filepath = ""

        self.name = name
        self.desc = desc
        # Data will be the dictionary of data to be converted to JSON
        self.data = data
        # images will be a list of (string, bytearray) tuples, to have index and name
        self.images = images
        if len(self.images) == 0:
            self.images.append(("default", DEFAULT_IMAGE))

    def convert_data_to_bytes(self):
        dict = {"name": self.name, "desc": self.desc, "data": self.data, "images": [i[0] for i in self.images]}
        encode = json.dumps(dict).encode('utf-8')
        return encode
    
    def get_filename(self):
        return os.path.basename(self.filepath)
    def get_file_extension(self):
        return self.get_filename().split(".")[1]
        
    
def read_package(bytes : bytes):
    decode = json.loads(bytes.decode("utf-8"))
    name = decode["name"]
    desc = decode["desc"]
    data = decode["data"]
    img = decode["images"]
    return Package(name,desc,data,img)


def parse_data_type(data_type, val : str):
    try:
        if data_type.__name__ == "bool":
            if val.strip().lower() == "true":
                parsed_val = True
            elif val.strip().lower() == "false":
                parsed_val = False
            else:
                parsed_val = False
            return parsed_val
        elif data_type.__name__ == "list":            
            valid_val = val.replace("\'","\"").strip()
            if valid_val[0] != '[' or valid_val[len(valid_val)-1] != ']':
                valid_val = "[" + valid_val + "]"
            vals = valid_val[1:-1].replace(" ", "").split(",")
            parsed_vals = []
            for i in range(len(vals)):
                try:
                    v = json.loads(vals[i])
                    parsed_vals.append(v)
                except:
                    parsed_vals.append(None)
            return parsed_vals
        else:
            parsed_val = data_type.__call__(val)
            return parsed_val
    except:
        empty_val = data_type.__call__()
        return empty_val
