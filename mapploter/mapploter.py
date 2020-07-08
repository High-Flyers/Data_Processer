import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os   
import math
import pdfkit
import argparse

from PIL import Image
from PyPDF2 import PdfFileMerger
from htmltemplater import HTMLTemplater

def MakeColorSquare(colorTable, id):
    """Making an color image and returning path to it

        Parameters
        ----------
        colorTable : array
            array of rgb color
        id : int
            id of the figure, used to save identify image

    """

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    r = math.floor(colorTable[0])
    g = math.floor(colorTable[1])
    b = math.floor(colorTable[2])
    img = Image.new('RGB', (30, 30), color = (r, g, b))
    image_path = os.path.join(THIS_FOLDER, f'colors/{id}.png')
    img.save(image_path)
    return image_path

def Translate(word):
    """Translating word to polish version

         Parameters
        ----------
        word : str
            word to translate
    """

    if word == 'triangle':
        trasnated = 'trójkąt'
    elif word == 'circle':
        trasnated = 'koło'
    elif word == 'quadrangle':
        trasnated = 'czworokąt'
    elif word == 'square':
        trasnated = 'kwadrat'
    else:
        trasnated = 'nieznany'
    return trasnated

class Figure:
    """A class used to represent Figure object

     Attributes
    ----------
    ID : int
        id of the figure
    name : str
        the name of the figure
    Area : float
        area of the figure
    Coords : array
        coords of the figure
    Disease : str
        detected disease
    Distances : array
        distances of the figure
    Color : array
        array of rgb color
    PlothPath : str
        path to plot image
    Image_path : str
        path to figure image
    templater : HTMLTemplater
        object to generate data in html code

    Methods
    -------
    fillSheet()
        fillig html with own data
    """

    def __init__(self, ID, Name, Area, Coords, Disease, Distances, Color, PlotPath, Image_path, templater):
        self.id = ID
        self.name = Name
        self.area = Area
        self.coords = Coords
        self.disease = Disease
        self.distances = Distances
        self.color = Color
        self.plotPath = PlotPath
        self.image_path  = Image_path
        self.templater = templater
        
    def fillSheet(self):
        """fillig html with own data"""
        self.templater.replace ({
            f'figure_{self.id}': f'''
                <article class="figure">
                    <div class="DataPictures">
                        <img alt="mapofcoords" src="<!-- model-replace: plot_src_{self.id} -->"/>
                    </div>
                    <div class="details">
                        <p><span>Kształt:</span> <strong>{Translate(self.name)}</strong></p>
                        <p><span>Choroba:</span> <strong>{self.disease}</strong> </p>
                        <p><span>Pole:</span> <strong>{self.area}</strong> m<sup>2</sup></p>
                        <p><span>Koordynaty:</span> <strong>{self.coords}</strong> </p>
                        <p class="poglad"><span>Podgląd:</span> <br><img alt="mapofcoords" src="<!-- model-replace: picture_src_{self.id} -->"/></p> 
                        <p class="poglad"><span>Kolor:</span> <br><img alt="mapofcoords" src="<!-- model-replace: color_src_{self.id} -->"/></p> 
                    </div> 
                </article>
                <!-- model-replace: figure_{self.id + 1} -->
            ''',
        })
        self.templater.replaceImage(f'color_src_{self.id}', MakeColorSquare(self.color, self.id))
        self.templater.replaceImage(f'picture_src_{self.id}', self.image_path)
        self.templater.replaceImage(f'plot_src_{self.id}', self.plotPath)


def GetDFFromJson(this_dir_path, json_path):
    """Geting data frame from json file
        Parameters
        ----------
        this_dir_path : str
            path to this dir
        json_path : str
            path to json file
    """

    json_file = os.path.join(this_dir_path, json_path)

    with open(json_file) as json_data:
        dataset  = json.loads(json_data.read())
        json_data.close()
    Figures = pd.json_normalize(dataset['Figures'])
    return Figures


def SplitDF(dataFrame):
    """Spliting data frame to array containing the number of objects per page

        Parameters
        ----------
        dataFrame : array
            data frame from json file
    """

    DFarray = []
    objectsOnSite = 3
    for x in range(math.ceil(dataFrame.shape[0] / objectsOnSite)):
        tmp_df = dataFrame.iloc[(x*  objectsOnSite):(x * objectsOnSite + objectsOnSite) , :]
        DFarray.append(tmp_df)

    return DFarray

def plotCoords(dataFrame, image):    
    """Ploting Cords on the map and returning the plot

        Parameters
        ----------
        dataFrame : array
            data frame from json file
        image : str
            image path to map image
    """

    nparray = dataFrame['Coords'].to_numpy()
    width = []
    lenght = []
    img = plt.imread(image)
    for item in nparray:
        width.append(item[0])
        lenght.append(item[1])

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[19.0255, 19.0315, 50.2351, 50.2401])
    ax.scatter(lenght, width, color='r', s=100)
    ax.set_xlim(19.0255, 19.0315)
    ax.set_ylim( 50.2351, 50.2401)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    return ax



def generatePDF(this_dir_path, FiguresDF, out_dir, number, plotbase, out_format = 'pdf'): 
    """Generating pdf file from dataframe

        Parameters
        ----------
        this_dir_path : str
            path to this dir
        FiguresDF : array
            data frame with object on one page
        out_dir : str
            path to out dir
        number : int
            number of page
        plotbase : plt.subplots()
            base plot of coords
        out_format : str, optional
            out format of the file (default pdf)
    """

    out_dir = os.path.join(this_dir_path, out_dir)
    html_file = os.path.join(this_dir_path, 'template.html')
    
    templater = HTMLTemplater(html_file)
    Idex = 0
    plotchild = plotbase
    for item in FiguresDF.iloc:
        #plot own coords on map with different color
        plotchild.scatter(item['Coords'][1], item['Coords'][0], color = 'b', s=100)
        name = item['ID']
        plt.savefig(os.path.join(this_dir_path, f'plotsimg/plot{name}.jpg'))
        plot_file = os.path.join(this_dir_path, f'plotsimg/plot{name}.jpg')
        
        name_of_file = item['File']
        if(name_of_file == ""):
            image_file = 1
        else:
            image_file = os.path.join(this_dir_path, f'figures_photos/{name_of_file}')
        figure = Figure(Idex, item['Name'], item['Area'], item['Coords'], item['Choroba'], item['Distances'], item['Mean color'], plot_file, image_file, templater)
        figure.fillSheet()
        #plot own coords on map with the same color as the rest
        plotchild.scatter(item['Coords'][1], item['Coords'][0], color = 'r', s=100)
        Idex += 1

    if out_format == 'pdf':
            out_path = os.path.join(out_dir, f'out{number}.pdf')
            output_file_path = out_path
            templater.save(out_path)
    
    
    return output_file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', action='store', dest='final',
                        help='Store file name', default='final_figures/log_ksztalty.json')
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    results = parser.parse_args()

    DF = GetDFFromJson(THIS_FOLDER, results.final)
    DFarray = SplitDF(DF)
    mapFile = os.path.join(THIS_FOLDER, 'pictures/map.png')
    plot = plotCoords(DF, mapFile)
  
    pdfarray = []
    i = 0
    for DF in DFarray:
        pdf = generatePDF(THIS_FOLDER, DF, 'pdf', i, plot,'pdf')
        pdfarray.append(pdf)
        i += 1

    #merging all the pdf to one
    merger = PdfFileMerger()
    
    for pdf in pdfarray:
        merger.append(pdf)

    merger.write(os.path.join(THIS_FOLDER, 'pdf/result1.pdf'))
    merger.close()


