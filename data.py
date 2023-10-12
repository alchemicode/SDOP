from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
import json
import imageio as iio

class DataParser:
    def __init__(self):
        print("Data Parser Loaded")

    def convert_data_to_bytes(self, name, desc, data):
        dict = {"name": name, "desc": desc, "data": data}
        encode = json.dumps(dict).encode('utf-8')
        return encode