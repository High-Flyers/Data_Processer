import pdfkit
import base64
import os


class HTMLTemplater:
    
    def __init__(self, filepath):
        self.template = None
        with open(filepath, 'r') as file:
            self.template = file.read()
        
    
    def replace(self, fillMap):
        for (key, value) in fillMap.items():
            self.template = self.template.replace(f'<!-- model-replace: {key} -->', str(value))

    def replaceImage(self, key, filepath):
        with open(filepath, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = 'data:image/jpeg;base64,' + encoded_string.decode('utf-8')

            self.template - self.template.replace(f'<!-- model-replace: {key} -->', encoded_string)
    
    def save(self, outpath):
        options={
             'page-size': 'Letter',
            'margin-top': '0.0in',
            'margin-right': '0.0in',
            'margin-bottom': '0.0in',
            'margin-left': '0.0in',
            'no-outline': None
        }
        pdfkit.from_string(self.template, outpath, css=os.path.join(os.path.dirname(os.path.abspath(__file__)),'style.css'), options=options)


