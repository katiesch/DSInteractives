'''
Interactive plotting window to look at various SME abundances
for GALAH K2 data. 
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve abundance_comp.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/abundance_comp
in your browser.
'''
import numpy as np

from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HBox, VBoxForm,Range1d, HoverTool, BoxZoomTool, ResetTool, ResizeTool, PreviewSaveTool, PanTool
from bokeh.models.widgets import TextInput,Select
from bokeh.io import curdoc


# Set up data
from astropy.table import Table
abund=Table.read('/Users/kschles/Documents/GALAH/wg4output/wg4_04292016/sobject_iraf_k2.fits', format='fits')
abund=Table.to_pandas(abund)

source = ColumnDataSource(data=dict(x=abund.loc[0:100,'feh_cannon'], y=abund.loc[0:100,'alpha_fe_cannon'], sobject_id=abund.loc[0:100,'sobject_id']))

# Set up plot
#plot = Figure(plot_height=400, plot_width=400, title="My Abundance Plot",
#              tools="crosshair,pan,reset,resize,save,box_zoom")
TOOLS= [BoxZoomTool(), ResetTool(), ResizeTool(), PreviewSaveTool(), PanTool(), HoverTool(tooltips=[("sobject_id","@sobject_id")])]
plot = Figure(plot_height=400, plot_width=400, title="My Abundance Plot",tools=TOOLS)
plot.xaxis.axis_label = "[Fe/H]"
plot.yaxis.axis_label = "[a/Fe]"

plot.scatter('x', 'y', source=source, color='black')

# create the horizontal histogram
x1 = np.random.normal(loc=5.0, size=400) * 100
hhist, hedges = np.histogram(x1, bins=20)
hzeros = np.zeros(len(hedges)-1)
hmax = max(hhist)*1.1

ph = Figure(toolbar_location=None, plot_width=plot.plot_width, plot_height=200, x_range=plot.x_range,
            y_range=(-hmax, hmax), title=None, min_border=10, min_border_left=50)
ph.xgrid.grid_line_color = None

axis_map = {
    "[Fe/H]": "feh_cannon",
    "[a/Fe]": "alpha_fe_cannon",
    "Ca": "ca_abund_sme",
    "Mg": "mg_abund_sme",
}



# Set up widgets
text = TextInput(title="title", value='my abundance plot')
select_x=Select(title="X axis:", value="[Fe/H]", options=axis_map.keys())
select_y=Select(title="Y axis:", value="[a/Fe]", options=axis_map.keys())

# Set up callbacks
def update_title(attrname, old, new):
    plot.title = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    df = abund
    x_name = axis_map[select_x.value]
    y_name = axis_map[select_y.value]
    plot.xaxis.axis_label = select_x.value
    plot.yaxis.axis_label = select_y.value
    
    source.data = dict(x=df.loc[0:100,x_name], y=df.loc[0:100,y_name],sobject_id=df.loc[0:100,'sobject_id'])

for w in [select_x,select_y]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = VBoxForm(children=[text,select_x,select_y])
pwindows=VBoxForm(children=[plot,ph])
curdoc().add_root(HBox(children=[inputs, pwindows], width=1000))

