import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os   
import math
import pdfkit

from PyPDF2 import PdfFileMerger
from htmltemplater import HTMLTemplater

class Figure:
    def __init__(self, ID, Name, Area, Coords, image_path, templater):
        self.id = ID
        self.name = Name
        self.area = Area
        self.coords = Coords
        self.image_path = image_path
        self.templater = templater
#<img alt="picture" src="<!-- model-replace: picture_src_{self.id} -->">
    def fillSheet(self):
        self.templater.replace ({
            f'figure_{self.id}': f'''
                <article class="figure">
                    <div class="DataPictures">
                        <div class="picture" alt="Real estate picture" "></div>
                    </div>
                    <div class="details">
                        <p><span>Name:</span> <strong>{self.name}</strong></p>
                        <p><span>Area:</span> <strong>{self.area}</strong> </p>
                        <p><span>Cords:</span> <strong>{self.coords}</strong> </p>
                    </div> 
                </article>
                <!-- model-replace: figure_{self.id + 1} -->
            ''',
        })

        #self.templater.replaceImage(f'picture_src_{self.id}', self.image_path)

def GetFromJson(this_dir_path, json_path):
    json_file = os.path.join(this_dir_path, json_path)

    with open(json_file) as json_data:
        dataset  = json.loads(json_data.read())
        json_data.close()

    Figures = pd.json_normalize(dataset['Figures'])
    DFarray = []
    for x in range(math.ceil(Figures.shape[0] / 5)):
        tmp_df = Figures.iloc[(x*5):(x*5+5) , :]
        DFarray.append(tmp_df)

    return DFarray

def generatePDF(this_dir_path, FiguresDF, out_dir, numer, out_format = 'pdf'):
    #config = pdfkit.configuration(wkhtmltopdf=path_to_lib)
    #output_file_path = '' 
    out_dir = os.path.join(this_dir_path, out_dir)
    html_file = os.path.join(this_dir_path, 'template.html')
    #templater = HTMLTemplater(html_file)

    #template picture
    picture_file = os.path.join(this_dir_path, 'pictures/map.jpg')
    templater = HTMLTemplater(html_file)
    Idex = 0
    for item in FiguresDF.iloc:
        figure = Figure(Idex, item['Name'], item['Area'], item['Coords'], picture_file, templater)
        print(item['Name'])
        figure.fillSheet()
        Idex += 1

    if out_format == 'pdf':
            out_path = os.path.join(out_dir, f'out{numer}.pdf')
            output_file_path = out_path
            templater.save(out_path)
    
    
    return output_file_path


def main():

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    print(THIS_FOLDER)
    #json_file = os.path.join(THIS_FOLDER, 'log_ksztalty.json')
    DFarray = GetFromJson(THIS_FOLDER, 'log_ksztalty.json')

    pdfarray = []
    i = 0
    for DF in DFarray:
        pdf = generatePDF(THIS_FOLDER, DF, 'pdf', i,'pdf')
        pdfarray.append(pdf)
        i += 1

    merger = PdfFileMerger()
    
    for pdf in pdfarray:
        merger.append(pdf)

    merger.write(os.path.join(THIS_FOLDER, 'pdf/result.pdf'))
    merger.close()


if __name__ == "__main__":
    main()








#print(coords['Coords'])
"""csvdf = pd.read_csv(csv_file)
print(csvdf)
df = pd.DataFrame([[5.1, 3.5, 0], [4.9, 3.0, 0], [7.0, 3.2, 1],
                   [6.4, 3.2, 1], [5.9, 3.0, 2]],
                  columns=['length', 'width', 'species'])

#ruh_m = plt.imread(mapfile)
for data in csvdf:
    print(data)
    
#    ax2 = data.plot.scatter(x='length',
 #                       y='width',
#                        c='DarkBlue')
    plt.show()
ax1 = df.plot.scatter(x='length',
                      y='width',
                      c='DarkBlue')

BBox = ((51.9662,   52.0127,      
         18.9351, 19.0189))


#ax2.set_xlim(BBox[0], BBox[1])
#ax2.set_ylim(BBox[2], BBox[3])
#ax2.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')


coords = pd.json_normalize(dataset['Figures'])
print(coords['Coords'])
print('as')
BBox = ((18.9351,   19.0189,      
         51.9662, 52.0127))
#df = pd.read_csv('coords.csv')         
df = pd.DataFrame([[52.0001, 18.9995, 0]],
                  columns=['length', 'width', 'species'])
ruh_m = plt.imread('map.png')
fig, ax = plt.subplots(figsize = (8, 7))
ax = df.plot.scatter(df['lenght'], df['width'], c='DarkBlue', s=10)
ax.set_title('plottong')
ax.set_xlim(BBox[0], BBox[1])
ax.set_ylim(BBox[2], BBox[3])
print('as')
ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
plt.show()
print('as')
"""