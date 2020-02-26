# In[0]: Importeer de dependencies

import os
from pyx import *
import numpy as np
import pandas as pd
import itertools as it
from pylatexenc.latexencode import unicode_to_latex

# In[1]: Standaard instellingen

unit.set(wscale=2)
text.set(text.LatexEngine)
text.preamble(
    r'\usepackage[scaled]{helvet}\renewcommand\familydefault{\sfdefault} ')

if not os.path.exists('export/'):
    os.mkdir('export/')

# In[2]: RadarPlot klasse

class RadarPlot(object):

    s = 0.5     # Schaal
    r = 5       # Straal
    g = None    # Aantal gridlijnen
    n = None    # Aantal items = f(data)
    t = None    # Array met de hoeken

    # Definieer de standaard kleuren
    colors = it.cycle(['#B1DFD5', '#E1D2C6', '#03A698'])

    def __init__(self, **kwargs):
        # Vul parameters aan
        self.s = kwargs.get('schaal', self.s)
        self.r = kwargs.get('straal', self.r)
        self.g = kwargs.get('gridlines', None)
        self.n = kwargs.get('items', None)
        # Als het aantal items gedefinieerd is, maak dan een 
        # lijst met de verschillende hoeken aan
        if self.n != None:
            # Start bovenaan, op de hoek pi/2 of 90°
            self.t = np.linspace(0, 2 * np.pi, num=self.n,
                                endpoint=False) + np.pi / 2
        # Maak layers aan
        self.layers = []
        # Maak context aan - hierop wordt getekend
        self.c = canvas.canvas()

    def generateCanvas(self):
        # 1. Maak rechte lijnen
        for a in self.t:
            self.c.stroke(
                path.path(
                    path.moveto(0, 0),
                    path.lineto(self.s * self.r * np.cos(a),
                    self.s * self.r * np.sin(a))
                ), 
                [style.linestyle.solid, color.gray(0.9)]
            )
        # 2. Maak het grid aan - aantal lijnen = gridlines - 1 (buitenlijn)
        for r in np.linspace(0, self.r, self.g + 1):
            clr = [style.linestyle.solid, color.gray(0.9)]
            if r < self.r:
                clr = [
                    # Stippellijn
                    style.linestyle(
                        style.linecap.round, 
                        style.dash([0, 2])
                    ), 
                    # Donker grijze kleur
                    color.gray(0.3)
                ]
            self.c.stroke(
                path.path(
                    path.moveto(0, self.s * r),
                    *[path.lineto(self.s * r * np.cos(a), self.s * r * np.sin(a)) for a in self.t],
                    path.closepath()
                ), 
                # Geef de stijl mee = f(r)
                clr
            )
        # 3. Voeg titels toe - Index van pandas Series
        titels = self.layers[0]['data'].index
        for t, a in zip(titels[:self.n], self.t):
            # Bepaal de horizontale uitlijning
            halign = [text.halign.boxcenter, text.halign.flushcenter]
            if int(np.cos(a) * 10) < 0:
                halign = [text.halign.boxright, text.halign.flushright]
            elif int(np.cos(a) * 10) > 0:
                halign = [text.halign.boxleft, text.halign.flushleft]
            # Voeg de tekst toe aan de context
            self.c.text(
                self.s * (self.r + 1) * np.cos(a),
                self.s * (self.r + 1) * np.sin(a),
                # Trancodeer de text naar Latex code
                unicode_to_latex(t), 
                # Geef mee hoe de tekstbox gedefinieerd is
                [text.parbox(5), *halign, text.valign.middle, color.gray(0.3)]
            )
        
    def generateRadarPlot(self):
        # Maak een lege canvas aan
        self.generateCanvas()
        # Itereer over de lagen en voeg hen toe
        for i in self.layers:
            d = i['data'].values
            c = i['color']
            r = d * self.s
            self.c.stroke(
                path.path(
                    path.moveto(0, r[0]), 
                    *[path.lineto(r_ * np.cos(a), r_ * np.sin(a)) for r_, a in zip(r[1:], self.t[1:])], 
                    path.closepath()
                ), 
                [
                    # Zet het kleur om naar een rgb waarde
                    color.rgbfromhexstring(c), 
                    style.linewidth(self.s * 0.06), 
                    # Hieronder wordt de vulkleur gedefinieerd - transparency = 90%
                    deco.filled([color.rgbfromhexstring(c), color.transparency(0.9)])
                ]
            )

    def addLayer(self, data, name='default', color=None):
        # Definieer het aantal items 
        if self.n == None:  
            self.n = data.shape[1]
            self.t = np.linspace(0, 2 * np.pi, num=self.n,
                                endpoint=False) + np.pi / 2
        # Voeg gegevens toe
        self.layers.append({
            'name': name,
            'data': data,
            'color': next(self.colors) if color == None else color
        })

    def addLegend(self):
        # Definieer kleuren
        j = 0
        for layer in self.layers:
            # Als geen naam toegekend is, doe verder
            if layer['name'] == 'default':
                continue 
            # Positie = f(huidige index)
            x = - self.s * self.r * 2.5
            y =  - self.s * (self.r + 3 - (j/2)*2)
            self.c.stroke(
                path.path(
                    path.moveto(x,y),
                    # Voeg relatieve lijn toe 
                    path.rlineto(1, 0)
                ), 
                [color.rgbfromhexstring(layer['color']), style.linewidth(0.06)]
            )
            self.c.text(
                x + 1.1, 
                y, 
                # Legende titel
                layer['name'].capitalize(), 
                # Stijl van de tekst
                [text.parbox(4), text.halign.boxleft, text.halign.flushleft, text.valign.middle, color.gray(0.3)]
            )
            # Verhoog de index
            j += 1

    def save(self, name='test', legend=False):
        # Schrijf een PDF file weg
        self.generateRadarPlot()
        # Voeg legende toe
        if legend == True:
            self.addLegend()
        # Schrijf het weg naar een .svg bestand
        self.c.writeSVGfile(os.path.join('export', name))


# In[2]: Laad de data

df = pd.read_excel('data/20200226.xlsx')

# In[3]: Normaliseer de data

df[df.columns[1:]] = df[df.columns[1:]] / df[df.columns[1:]].max() * 5

# In[4]: Loop over alle indices

# Groepeer eventuele duplicaten
ids = df.groupby('ID')
for i, data in ids:
    # TIJDENS DEBUGGEN - VERWIJDER IN PRODUCTIE
    #if i > 0:
    #    break
    # Loop over alle waardes
    plot = RadarPlot(items=5,gridlines=5)
    # De data die je aan de lagen toevoegd is van het type
    # Pandas DataSeries en dus geen DataFrame!
    plot.addLayer(data.iloc[0,1:], name='kernstudie')
    # Bewaar de plot met als bestandsnaam het ID-nummer
    # Standaard wordt de legende verborgen
    plot.save(f'{i}', legend=True)
