# RadarPlot

>AANDACHT: Onderstaande handleiding werd opgesteld voor de vorige versie van RadarPlot. De code is aangepast (meer generieker), maar wordt momenteel nog geplaagd door enkele bugs.

A plot build using [PyX](https://pyx-project.org/), a Python package build for creating PostScript, PDF, and SVG files. It works together with the TeX/LaTeX interface to generate text. This package has been used because the Matplotlib, Pyplot or another package wasn't build to allow a great customisation of the plots.

```python
# In the run.py file a new class is defined
plot = RadarPlot()
```

This code will generate a `RadarPlot` instance. You can define the amount of gridlines by defining `gridlines=` and the amount of items (edges) with `items=`. 

To add data to the plot, a new layer should be created, using:

```python
# Add a new layer to the plot
plot.addLayer(<dataSeries>, name=<name>, color=<hex-color>)
```

The plot can be saved using the following code:

```python
# Save the plot to a file
plot.save('filename', legend=<boolean>)
```

## Getting started

To get started, I would recommend you to start a new `virtualenv`, preferably by using a tool like `mkvirtualenv <NameOfYourEnv:RadarPlot>`. Next, activate your environment by using `workon <NameOfYourEnv:RadarPlot>`.

Run the following command to install al dependencies:

```shell
# This will install all dependencies
pip install -r requirements.txt
```

Go ahead and run the python script to generate the plots

```shell
python run.py
```

## Common issues

Make sure you have installed `Tex` on your computer. For windows, download [MikTex](https://miktex.org/download) and install for the current User only (Sweco doens't allow you to install it for all users).

Made with ♥️ by Gilles Trenson
