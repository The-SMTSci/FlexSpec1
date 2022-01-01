import sys
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Range1d
from astropy.io import fits
import numpy as np
from PIL import Image as im


# https://www.publicdomainpictures.net/pictures/180000/velka/tree-1465369020Wxg.jpg
treeimg  = "/static/tree.jpeg"
image_src = ColumnDataSource(dict(url = [treeimg]))

page_img                       = figure(plot_width = 500, plot_height = 500, title="")
#page_img.toolbar.img          = None
#page_img.toolbar_location      = None
#page_img.x_range               = Range1d(start=0, end=1)
#page_img.y_range               = Range1d(start=0, end=1)
#page_img.xaxis.visible         = None
#page_img.yaxis.visible         = None
#page_img.xgrid.grid_line_color = None
#page_img.ygrid.grid_line_color = None

basename = "/home/git/external/FlexSpec1/Code/FlexSpec/UserInterface/FITS/static/stars005.fits"
#print(f"{sys.path}") #page_img.outline_line_alpha = 0



f     = fits.open(basename)
h     = f[0].header
d     = f[0].data
img = im.fromarray(d//256)   # turn into 8 bit data

if(0):  # hack to see the cards
    cards = h._cards    # array of tuples of (k,v,comment)
    for a,b,c in cards:
        if('COMMENT' not in a):
            print(f"{a:8s} {b}")




#page_img.image_url(url='url', x=0.05, y = 0.85, h=0.7, w=0.9, source=image_src)


#curdoc().add_root(page_img)
