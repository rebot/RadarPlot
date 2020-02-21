# In[0]: Imports

import os
from pyx import *
import numpy as np
import pandas as pd
import itertools as it
from pylatexenc.latexencode import unicode_to_latex

# In[0]: Default settings

unit.set(wscale=2)
text.set(text.LatexEngine)
text.preamble(
    r'\usepackage[scaled]{helvet}\renewcommand\familydefault{\sfdefault} ')

if not os.path.exists('export/'):
    os.mkdir('export/')


# In[1]: Make the generateRadarPlot function

class RadarPlot(object):

    s = 0.5  # Scale
    r = 5   # Radius
    g = 5  # Gridlines
    # Define default colors
    colors = ['#9CD5E7', '#E1D2C6', '#03A698']

    def __init__(self):
        # Maak dataBin aan
        self.dataBin = []
        # Generate canvas
        self.c = canvas.canvas()

    def generateCanvas(self):

        # Maak rechte lijnen
        for a in self.t:
            self.c.stroke(path.path(path.moveto(0, 0), path.lineto(self.s * self.r * np.cos(
                a), self.s * self.r * np.sin(a))), [style.linestyle.solid, color.gray(0.9)])

        # Maak de rand aan
        r = np.array(self.g) * self.s
        self.c.stroke(path.path(path.moveto(0, r[0]), *[path.lineto(r_ * np.cos(a), r_ * np.sin(a)) for r_, a in zip(r[1:], self.t[1:])], path.closepath()), [style.linestyle.solid, color.gray(0.9)])

        # Maak het grid aan
        grid = range(1, self.g)
        for r in grid:
            clr = [style.linestyle.solid, color.gray(0.1)]
            if r < 9:
                clr = [style.linestyle(
                    style.linecap.round, style.dash([0, 2])), color.gray(0.3)]
            self.c.stroke(path.path(path.moveto(0, self.s * r), *[path.lineto(self.s * r * np.cos(
                a), self.s * r * np.sin(a)) for a in self.t], path.closepath()), clr)

        # Voeg titels toe
        titels = self.dataBin[0]['data'].columns
        for t, a in zip(titels, self.t):
            # Determine horizontal alignment
            halign = [text.halign.boxcenter, text.halign.flushcenter]
            if int(np.cos(a) * 10) < 0:
                halign = [text.halign.boxright, text.halign.flushright]
            elif int(np.cos(a) * 10) > 0:
                halign = [text.halign.boxleft, text.halign.flushleft]
            # Plot the text
            self.c.text(self.s * (self.r + 1) * np.cos(a), self.s * (self.r + 1) * np.sin(a),
                        unicode_to_latex(t), [text.parbox(5), *halign, text.valign.middle, color.gray(0.3)])

    def generateRadarPlot(self):
        # Generate the plot
        self.generateCanvas()

        # Teken de lijnen
        for i in self.dataBin:
            d = i['data']
            c = i['color']
            r = np.array(d) * self.s
            self.c.stroke(path.path(path.moveto(0, r[0]), *[path.lineto(r_ * np.cos(a), r_ * np.sin(a)) for r_, a in zip(r[1:], self.t[1:])], path.closepath()), [
                          color.rgbfromhexstring(c), style.linewidth(0.06), deco.filled([color.rgbfromhexstring(c), color.transparency(0.9)])])

    def addLayer(self, data, name='default', color=None):
        # Definieer het aantal items 
        if len(self.dataBin) ==0:  
            self.n = data.shape[1]
            self.t = np.linspace(0, 2 * np.pi, num=self.n,
                                endpoint=False) + np.pi / 2
        # Voeg gegevens toe
        self.dataBin.append({
            'name': name,
            'data': data,
            'color': it.cycle(self.colors) if color == None else color
        })

    def addLegend(self):
        # Definieer kleuren
        for i, pre, name, c in zip(range(3), names, [prov, woon, kern], colors):
            x = - self.s * self.r * 2.5
            y =  - self.s * (self.r + 3 - (i/2)*2)
            self.c.stroke(path.path(path.moveto(x,y), path.rlineto(1, 0)), [color.rgbfromhexstring(c), style.linewidth(0.06)])
            self.c.text(x + 1.1, y, pre.capitalize() + ' ' + name.capitalize(), [text.parbox(4), text.halign.boxleft, text.halign.flushleft, text.valign.middle, color.gray(0.3)])

    def save(self, name='test'):
        # Schrijf een PDF file weg
        self.generateCanvas()
        self.c.writePDFfile(os.path.join('src', name))


# In[2]: Load the data

df = pd.read_excel('20200214kernstudie.xlsx')

# In[3]: Loop over alle provincies
ids = df.groupby('ID')
for i, data in ids:
    if i > 2:
        exit
    # Loop over alle waardes
    plot = RadarPlot()
    plot.addLayer(data.iloc[:,1:], name='kernstudie', color='#B1DFD5')
    plot.save(f'{i}')

# %%
