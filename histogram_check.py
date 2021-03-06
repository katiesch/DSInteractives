'''
Interactive plotting window to look at various SME abundances
for GALAH K2 data.

To use this, you need the python bokeh, pandas, and numpy modules.
You also need to change the file location below to that of your local
machine. 

Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve histogram_check.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/histogram_check
in your browser.

This has been heavily modified but was built off of the selection_histogram.py example from bokeh
-k. schlesinger
'''
import numpy as np
import pandas as pd

from bokeh.plotting import figure, hplot, vplot
from bokeh.models import ColumnDataSource, HBox, VBoxForm,Range1d, HoverTool, BoxZoomTool, ResetTool, ResizeTool, PreviewSaveTool, PanTool, BoxSelectTool, LassoSelectTool, Paragraph
from bokeh.models.widgets import TextInput,Select,Slider
from bokeh.io import curdoc
from bokeh.charts import Histogram


## Function to create source file from selected data columns. 
def update_data(source, xname, yname, binval):

    axis_map = {
        "[Fe/H]": "feh_cannon",
        "[a/Fe]": "alpha_fe_cannon",
        "Teff" : "teff_cannon",
        "logg" : "logg_cannon",
        "Li": "li_abund_sme",
        "C" : "c_abund_sme",
        "O" : "o_abund_sme",
        "Na" : "na_abund_sme",
        "Mg" : "mg_abund_sme", 
        "Al" : "al_abund_sme", 
        "Si" : "si_abund_sme", 
        "K"  : "k_abund_sme",
        "Ca" : "ca_abund_sme", 
        "Sc" : "sc_abund_sme",
        "Ti" : "ti_abund_sme", 
        "V"  : "v_abund_sme",
        "Cr" : "cr_abund_sme", 
        "Mn" : "mn_abund_sme",
        "Co" : "co_abund_sme",
        "Ni" : "ni_abund_sme",
        "Cu" : "cu_abund_sme",
        "Zn" : "zn_abund_sme",
        "Y"  : "y_abund_sme",
        "Ba" : "ba_abund_sme",
        "La" : "la_abund_sme",
        "Nd" : "nd_abund_sme",
        "Eu" : "eu_abund_sme",
        "Rb" : "rb_abund_sme"
    }


    df = source
    x_name = axis_map[xname]
    y_name = axis_map[yname]

    xbinnum=int(binval)
    ybinnum=int(binval)

    ## Make horizontal histogram and write it into dataframe 
    hhist, hedges = np.histogram(df.loc[np.where(np.isnan(df[x_name])==False)[0],x_name], bins=xbinnum)
    lst=[np.nan]*(len(df)-xbinnum) 
    lst2=[np.nan]*(len(df)-(xbinnum+1)) 
    df['hhist']=pd.concat([pd.Series(hhist),pd.Series(lst)], ignore_index=True)
    df['hedges_left']=pd.concat([pd.Series(hedges[:-1]),pd.Series(lst2)], ignore_index=True)
    df['hedges_right']=pd.concat([pd.Series(hedges[1:]),pd.Series(lst2)], ignore_index=True)

    ## Make vertical histogram and write it into dataframe
    vhist, vedges = np.histogram(df.loc[np.where(np.isnan(df[y_name])==False)[0],y_name], bins=ybinnum)
    lst=[np.nan]*(len(df)-ybinnum) 
    lst2=[np.nan]*(len(df)-(ybinnum+1)) 
    df['vhist']=pd.concat([pd.Series(vhist),pd.Series(lst)], ignore_index=True)
    df['vedges_left']=pd.concat([pd.Series(vedges[:-1]),pd.Series(lst2)], ignore_index=True)
    df['vedges_right']=pd.concat([pd.Series(vedges[1:]),pd.Series(lst2)], ignore_index=True)

    ## Produce source file used for the other functions, etc. 
    source = ColumnDataSource(data=dict(x=df[x_name], y=df[y_name], hhist=df['hhist'], hedges_left=df['hedges_left'], hedges_right=df['hedges_right'], vhist=df['vhist'], vedges_left=df['vedges_left'], vedges_right=df['vedges_right'], sobject_id=df['sobject_id']))

    return source


def make_scatter_plot(source, xname,yname): 

    ## Select tools for top right of figure
    TOOLS= [BoxZoomTool(), ResetTool(), ResizeTool(), PanTool(), HoverTool(tooltips=[("sobject_id","@sobject_id")])]

    ## create the scatter plot
    scatter_plot = figure(tools=TOOLS, plot_width=600, plot_height=600, title=None, min_border=10, min_border_left=50)
    scatter_plot.scatter('x','y', size=3, source=source, color="#3A5785", alpha=0.6)
    scatter_plot.min_border_right = 10

    ## create the horizontal histogram
    LINE_ARGS = dict(color="#3A5785", line_color=None)
    ph = figure(toolbar_location=None, plot_width=scatter_plot.plot_width, plot_height=200, x_range=scatter_plot.x_range,
                title=None, min_border=10, min_border_left=50)
    ph.xgrid.grid_line_color = None
    ph.quad(bottom=0, left='hedges_left', right='hedges_right', top='hhist', color="white", line_color="#3A5785", source=source)
    ph.min_border_top = 10
    ph.min_border_right = 10

    ## create the vertical histogram
    th = 42 ## need to adjust for toolbar height
    pv = figure(toolbar_location=None, plot_width=200, plot_height=scatter_plot.plot_height+th-10,
                y_range=scatter_plot.y_range, title=None, min_border=10, min_border_top=th)
    pv.ygrid.grid_line_color = None
    pv.xaxis.major_label_orientation = -3.14/2
    pv.quad(left=0, bottom='vedges_left', top='vedges_right', right='vhist', color="white", line_color="#3A5785", source=source)
    pv.min_border_top = 80
    pv.min_border_left = 0
 
    return scatter_plot,ph,pv

## set up callbacks
def update_scatter_plot(attr, old, new):
    x_value=select_x.value
    y_value=select_y.value
    bin_value=binnum.value

    ## Change axis labels 
    plot.xaxis.axis_label=x_value
    plot.yaxis.axis_label=y_value

    src = update_data(abund, x_value, y_value,bin_value)
    source.data.update(src.data)


# Set up widgets
axis_map = {
    "[Fe/H]": "feh_cannon",
    "[a/Fe]": "alpha_fe_cannon",
    "Teff" : "teff_cannon",
    "logg" : "logg_cannon",
    "Li": "li_abund_sme",
    "C" : "c_abund_sme",
    "O" : "o_abund_sme",
    "Na" : "na_abund_sme",
    "Mg" : "mg_abund_sme", 
    "Al" : "al_abund_sme", 
    "Si" : "si_abund_sme", 
    "K"  : "k_abund_sme",
    "Ca" : "ca_abund_sme", 
    "Sc" : "sc_abund_sme",
    "Ti" : "ti_abund_sme", 
    "V"  : "v_abund_sme",
    "Cr" : "cr_abund_sme", 
    "Mn" : "mn_abund_sme",
    "Co" : "co_abund_sme",
    "Ni" : "ni_abund_sme",
    "Cu" : "cu_abund_sme",
    "Zn" : "zn_abund_sme",
    "Y"  : "y_abund_sme",
    "Ba" : "ba_abund_sme",
    "La" : "la_abund_sme",
    "Nd" : "nd_abund_sme",
    "Eu" : "eu_abund_sme",
    "Rb" : "rb_abund_sme"
}

select_x=Select(title="X axis:", value="[Fe/H]", options=axis_map.keys())
select_y=Select(title="Y axis:", value="[a/Fe]", options=axis_map.keys())
binnum = TextInput(title="Number of Bins:", value='25')

#################################################
##### CHANGE FILE LOCATION FOR PERSONAL USE #####
#################################################

## Read in data table from fits file. When you use this on your own machine, will need to change the file location
from astropy.table import Table
abund=Table.read('/Users/kschles/Documents/GALAH/wg4output/wg4_04292016/sobject_iraf_k2.fits', format='fits')
abund=Table.to_pandas(abund)

x_value="[Fe/H]"
y_value="[a/Fe]"
bin_value='25'
## Set up initial data: 
source = update_data(abund, x_value, y_value,bin_value)

## Produce plots: 
plot, ph, pv=make_scatter_plot(source, x_value, y_value)

ph.yaxis.axis_label = 'Number'
pv.xaxis.axis_label = 'Number'
plot.xaxis.axis_label=x_value
plot.yaxis.axis_label=y_value

layout = vplot(hplot(select_x, select_y,binnum), hplot(plot, pv), hplot(ph, Paragraph(width=200)), width=800, height=800)


for w in [select_x, select_y, binnum]:
    w.on_change('value', update_scatter_plot)
