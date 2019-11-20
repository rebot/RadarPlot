import os
from pyx import *
import numpy as np
import pandas as pd
from pylatexenc.latexencode import unicode_to_latex

# In[0]: Default settings

unit.set(wscale=2)
text.set(text.LatexEngine)
text.preamble(
    r'\usepackage[scaled]{helvet}\renewcommand\familydefault{\sfdefault} ')

if not os.path.exists('src/'):
    os.mkdir('src/')


# In[1]: Make the generateRadarPlot function

class RadarPlot(object):

    s = 0.5  # Scale
    r = 9   # Radius
    g = 10  # Gridlines

    def __init__(self, prov, woon, kern):
        self.p = prov
        self.w = woon
        self.k = kern
        # Number of items
        self.n = prov.shape[0]
        self.t = np.linspace(0, 2 * np.pi, num=self.n,
                             endpoint=False) + np.pi / 2
        # Generate canvas
        self.c = canvas.canvas()

    def generateCanvas(self):

        for a in self.t:
            self.c.stroke(path.path(path.moveto(0, 0), path.lineto(self.s * self.r * np.cos(
                a), self.s * self.r * np.sin(a))), [style.linestyle.solid, color.gray(0.9)])

        grid = range(1, self.g)
        for r in grid:
            clr = [style.linestyle.solid, color.gray(0.1)]
            if r < 9:
                clr = [style.linestyle(
                    style.linecap.round, style.dash([0, 2])), color.gray(0.3)]
            self.c.stroke(path.path(path.moveto(0, self.s * r), *[path.lineto(self.s * r * np.cos(
                a), self.s * r * np.sin(a)) for a in self.t], path.closepath()), clr)

        for t, a in zip(self.p.index, self.t):
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
        # Definieer de kleuren
        colors = ['#9CD5E7', '#E1D2C6', '#03A698']

        for d, c in zip([self.p, self.w, self.k], colors):
            r = np.array(d) * self.s
            self.c.stroke(path.path(path.moveto(0, r[0]), *[path.lineto(r_ * np.cos(a), r_ * np.sin(a)) for r_, a in zip(r[1:], self.t[1:])], path.closepath()), [
                          color.rgbfromhexstring(c), style.linewidth(0.06), deco.filled([color.rgbfromhexstring(c), color.transparency(0.9)])])

    def addLegend(self, prov, woon, kern):
        # Definieer kleuren
        colors = ['#9CD5E7', '#E1D2C6', '#03A698']
        names = ['Provincie', 'Woongebied', 'Kern']

        for i, pre, name, c in zip(range(3), names, [prov, woon, kern], colors):
            x = - self.s * self.r * 2.5
            y =  - self.s * (self.r + 3 - (i/2)*2)
            self.c.stroke(path.path(path.moveto(x,y), path.rlineto(1, 0)), [color.rgbfromhexstring(c), style.linewidth(0.06)])
            self.c.text(x + 1.1, y, pre.capitalize() + ' ' + name.capitalize(), [text.parbox(4), text.halign.boxleft, text.halign.flushleft, text.valign.middle, color.gray(0.3)])

    def save(self, name='test'):
        # Schrijf een PDF file weg
        self.generateRadarPlot()
        self.c.writePDFfile(os.path.join('src', name))


# In[2]: Load the data

df = pd.read_excel('data.xlsx')

# Loop over alle provincies
provincies = df.groupby('Provincie')
for provincie, data in provincies:
    prov_gem = data.mean()
    # Loop over alle woongebieden
    woongebieden = data.groupby('Woongebied')
    for woongebied, data in woongebieden:
        woon_gem = data.mean()
        # Loop over alle kernen
        kernen = data.groupby('Kern')
        for kern, data in kernen:
            kern_gem = data.mean()
            # Genereer een plot voor elke kern
            plot = RadarPlot(prov_gem, woon_gem, kern_gem)
            plot.addLegend(provincie.capitalize(), woongebied.capitalize(), kern.capitalize())
            plot.save(provincie.lower() + '_' +
                      woongebied.lower() + '_' + kern.lower())
