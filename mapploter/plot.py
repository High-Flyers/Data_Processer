import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os   
import math
import pdfkit

from PyPDF2 import PdfFileMerger
from htmltemplater import HTMLTemplater

csvdf = pd.read_csv(csv_file)
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