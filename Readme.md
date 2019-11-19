# RadarPlot

A plot build using [PyX](https://pyx-project.org/), a Python package build for creating PostScript, PDF, and SVG files. It works together with the TeX/LaTeX interface to generate text. This package has been used because the Matplotlib, Pyplot or another package wasn't build to allow a great customisation of the plots.

```python
# In the run.py file a new class is defined
plot = RadarPlot(provincie, woongebied, kern)
```

This code will generate a `RadarPlot` instance. The plot can be saved using the following code:

```python
# Save the plot to a file
plot.save('filename')
```

(C) Gilles Trenson
