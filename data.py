from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import json
import imageio as iio

def convert_data_to_bytes(pack):
    dict = {"name": pack.name, "desc": pack.desc, "data": pack.data}
    encode = json.dumps(dict).encode('utf-8')
    return encode
    

class Package:
    def __init__(self, name, desc, data, images):
        f = open("default.png", "rb")
        i = f.read()
        DEFAULT_IMAGE = bytearray(i)
        f.close()
        self.name = name
        self.desc = desc
        # Data will be the dictionary of data to be converted to JSON
        self.data = data
        # images will be a list of (string, bytearray) tuples, to have index and name
        self.images = images
        if len(self.images) == 0:
                self.images.append(("default", DEFAULT_IMAGE))
