from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import json

PNG_SIGNATURE = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])    

DEFAULT_IMAGE : bytearray

EXAMPLE_IMAGE : bytearray

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
