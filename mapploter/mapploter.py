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
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    r = math.floor(colorTable[0])
    g = math.floor(colorTable[1])
    b = math.floor(colorTable[2])
    img = Image.new('RGB', (30, 30), color = (r, g, b))
    image_path = os.path.join(THIS_FOLDER, f'colors/{id}.png')
    img.save(image_path)
    return image_path

def Translate(word):
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
    json_file = os.path.join(this_dir_path, json_path)

    with open(json_file) as json_data:
        dataset  = json.loads(json_data.read())
        json_data.close()
    Figures = pd.json_normalize(dataset['Figures'])
    return Figures


def SplitDF(dataFrame):
    DFarray = []
    objectsOnSite = 3
    for x in range(math.ceil(dataFrame.shape[0] / objectsOnSite)):
        tmp_df = dataFrame.iloc[(x*  objectsOnSite):(x * objectsOnSite + objectsOnSite) , :]
        DFarray.append(tmp_df)

    return DFarray

def plotCoords(dataFrame, image):    
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
    out_dir = os.path.join(this_dir_path, out_dir)
    html_file = os.path.join(this_dir_path, 'template.html')
    
    templater = HTMLTemplater(html_file)
    Idex = 0
    plotchild = plotbase
    for item in FiguresDF.iloc:
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
        plotchild.scatter(item['Coords'][1], item['Coords'][0], color = 'r', s=100)
        Idex += 1

    if out_format == 'pdf':
            out_path = os.path.join(out_dir, f'out{number}.pdf')
            output_file_path = out_path
            templater.save(out_path)
    
    
    return output_file_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', action='store', dest='final',
                        help='Store file name', default='final_figures/log_ksztalty.json')
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    results = parser.parse_args()

    DF = GetDFFromJson(THIS_FOLDER, results.final)
    DFarray = SplitDF(DF)
    img = os.path.join(THIS_FOLDER, 'pictures/map.png')
    plot = plotCoords(DF, img)
  
    pdfarray = []
    i = 0
    for DF in DFarray:
        pdf = generatePDF(THIS_FOLDER, DF, 'pdf', i, plot,'pdf')
        pdfarray.append(pdf)
        i += 1

    merger = PdfFileMerger()
    
    for pdf in pdfarray:
        merger.append(pdf)

    merger.write(os.path.join(THIS_FOLDER, 'pdf/result1.pdf'))
    merger.close()

if __name__ == "__main__":
    main()







