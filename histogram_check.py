'''
Interactive plotting window to look at various SME abundances
for GALAH K2 data. 
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve histogram_check.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/histogram_check
in your browser.
'''
import numpy as np
import pandas as pd

from bokeh.plotting import figure, hplot, vplot
from bokeh.models import ColumnDataSource, HBox, VBoxForm,Range1d, HoverTool, BoxZoomTool, ResetTool, ResizeTool, PreviewSaveTool, PanTool, BoxSelectTool, LassoSelectTool, Paragraph
from bokeh.models.widgets import TextInput,Select
from bokeh.io import curdoc
from bokeh.charts import Histogram

def update_data(source, xname, yname):

    axis_map = {
        "[Fe/H]": "feh_cannon",
        "[a/Fe]": "alpha_fe_cannon",
        "Ca": "ca_abund_sme",
        "Mg": "mg_abund_sme",
    }


    df = source
    x_name = axis_map[xname]
    y_name = axis_map[yname]
    #ph.xaxis.axis_label = xname
    #ph.yaxis.axis_label = yname

    test=np.where(np.isnan(df[x_name])==False)[0]
    hhist, hedges = np.histogram(df.loc[test,x_name], bins=20)
    lst=[np.nan]*(len(df)-20) 
    lst2=[np.nan]*(len(df)-21) 
    df['hhist']=pd.concat([pd.Series(hhist),pd.Series(lst)], ignore_index=True)
    df['hedges_left']=pd.concat([pd.Series(hedges[:-1]),pd.Series(lst2)], ignore_index=True)
    df['hedges_right']=pd.concat([pd.Series(hedges[1:]),pd.Series(lst2)], ignore_index=True)
    
    test=np.where(np.isnan(df[y_name])==False)[0]
    vhist, vedges = np.histogram(df.loc[test,y_name], bins=20)
    lst=[np.nan]*(len(df)-20) 
    lst2=[np.nan]*(len(df)-21) 
    df['vhist']=pd.concat([pd.Series(vhist),pd.Series(lst)], ignore_index=True)
    df['vedges_left']=pd.concat([pd.Series(vedges[:-1]),pd.Series(lst2)], ignore_index=True)
    df['vedges_right']=pd.concat([pd.Series(vedges[1:]),pd.Series(lst2)], ignore_index=True)
    
    source = ColumnDataSource(data=dict(x=df[x_name], y=df[y_name], hhist=df['hhist'], hedges_left=df['hedges_left'], hedges_right=df['hedges_right'], vhist=df['vhist'], vedges_left=df['vedges_left'], vedges_right=df['vedges_right'], sobject_id=df['sobject_id']))

    return source


def make_scatter_plot(source): 

    TOOLS= [BoxZoomTool(), ResetTool(), ResizeTool(), PreviewSaveTool(), PanTool(), HoverTool(tooltips=[("sobject_id","@sobject_id")])]
    # create the scatter plot
    scatter_plot = figure(tools=TOOLS, plot_width=600, plot_height=600, title=None, min_border=10, min_border_left=50)
    r = scatter_plot.scatter('x','y', size=3, source=source, color="#3A5785", alpha=0.6)

    scatter_plot.select(BoxSelectTool).select_every_mousemove = False
    scatter_plot.select(LassoSelectTool).select_every_mousemove = False
    scatter_plot.min_border_right = 10

    # create the horizontal histogram
    LINE_ARGS = dict(color="#3A5785", line_color=None)

    ph = figure(toolbar_location=None, plot_width=scatter_plot.plot_width, plot_height=200, x_range=scatter_plot.x_range,
                title=None, min_border=10, min_border_left=50)
    ph.xgrid.grid_line_color = None

    ph.quad(bottom=0, left='hedges_left', right='hedges_right', top='hhist', color="white", line_color="#3A5785", source=source)
    ph.min_border_top = 10
    ph.min_border_right = 10
    
    # create the vertical histogram
    th = 42 # need to adjust for toolbar height, unfortunately
    pv = figure(toolbar_location=None, plot_width=200, plot_height=scatter_plot.plot_height+th-10,
                y_range=scatter_plot.y_range, title=None, min_border=10, min_border_top=th)
    pv.ygrid.grid_line_color = None
    pv.xaxis.major_label_orientation = -3.14/2

    pv.quad(left=0, bottom='vedges_left', top='vedges_right', right='vhist', color="white", line_color="#3A5785", source=source)
    #vh1 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.5, **LINE_ARGS)
    #vh2 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.1, **LINE_ARGS)

    pv.min_border_top = 80
    pv.min_border_left = 0
 
    return scatter_plot,ph,pv

# set up callbacks
def update_scatter_plot(attr, old, new):
    x_value=select_x.value
    y_value=select_y.value

    src = update_data(abund, x_value, y_value)
    source.data.update(src.data)


# Set up widgets
axis_map = {
    "[Fe/H]": "feh_cannon",
    "[a/Fe]": "alpha_fe_cannon",
    "Ca": "ca_abund_sme",
    "Mg": "mg_abund_sme",
}

select_x=Select(title="X axis:", value="[Fe/H]", options=axis_map.keys())
select_y=Select(title="Y axis:", value="[a/Fe]", options=axis_map.keys())

from astropy.table import Table
abund=Table.read('/Users/kschles/Documents/GALAH/wg4output/wg4_04292016/sobject_iraf_k2.fits', format='fits')
abund=Table.to_pandas(abund)

x_value="[Fe/H]"
y_value="[a/Fe]"

## Set up initial data: 
source = update_data(abund, x_value, y_value)

## Produce main scatter plot: 
plot, ph, pv=make_scatter_plot(source)

## Produce horizontal histogram:
#ph=make_hor_hist(source, plot)

## Produce vertical histogram
#pv=make_vert_hist(source, plot)

layout = vplot(hplot(select_x, select_y), hplot(plot, pv), hplot(ph, Paragraph(width=200)), width=800, height=800)


for w in [select_x, select_y]:
    w.on_change('value', update_scatter_plot)
