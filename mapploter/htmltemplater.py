import pdfkit
import base64
import os


class HTMLTemplater:
    """A class used to change dynamically HTML code

     Attributes
    ----------
    filepath : str
        path to html file

    Methods
    -------
    replace(fillMap)
        Replacing HTML commented code intro values in parametr

    replaceImage(key, filepath)
        Replacing HTML commented code intro image path

    save(outpath)
        Saving HTML code
    """

    def __init__(self, filepath):
        """
        Parameters
        ----------
        filepath : str
            path to file

        """
        
        self.template = None
        with open(filepath, 'r') as file:
            self.template = file.read()
        
    
    def replace(self, fillMap):
        """Replacing HTML commented code intro values in parametr

        Parameters
        ----------
        fillMap : array
            array with values to replace

        """

        for (key, value) in fillMap.items():
            self.template = self.template.replace(f'<!-- model-replace: {key} -->', str(value))

    def replaceImage(self, key, filepath):
        """Replacing HTML commented code intro image path

        Parameters
        ----------
        key : str
            string with identification which comment to change
        filepath : str
            path to image
        """

        with open(filepath, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = 'data:image/jpeg;base64,' + encoded_string.decode('utf-8')

            self.template = self.template.replace(f'<!-- model-replace: {key} -->', encoded_string)
    
    def save(self, outpath):
        """Saving HTML code
        
        Parameters
        ----------
        outpath : str
            string with output patch
        """

        options={
             'page-size': 'Letter',
            'margin-top': '0.0in',
            'margin-right': '0.0in',
            'margin-bottom': '0.0in',
            'margin-left': '0.0in',
            'no-outline': None
        }
        pdfkit.from_string(self.template, outpath, css=os.path.join(os.path.dirname(os.path.abspath(__file__)),'style.css'), options=options)


