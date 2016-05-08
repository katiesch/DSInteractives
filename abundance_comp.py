''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve abundance_comp.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/abundance_comp
in your browser.
'''
import numpy as np

from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HBox, VBoxForm
from bokeh.models.widgets import Slider, TextInput,Select
from bokeh.io import curdoc

# Set up data
from astropy.table import Table
abund=Table.read('/Users/kschles/Documents/GALAH/wg4output/wg4_04292016/sobject_iraf_k2.fits', format='fits')
abund=Table.to_pandas(abund)

source = ColumnDataSource(data=dict(x=abund.loc[0:100,'feh_cannon'], y=abund.loc[0:100,'alpha_fe_cannon']))

# Set up plot
plot = Figure(plot_height=400, plot_width=400, title="My Abundance Plot",
              tools="crosshair,pan,reset,resize,save,box_zoom",
              x_range=[-2,1.0], y_range=[-0.2,1.0])
plot.xaxis.axis_label = "[Fe/H]"
plot.yaxis.axis_label = "[a/Fe]"

plot.scatter('x', 'y', source=source, color='black')

axis_map = {
    "[Fe/H]": "feh_sme",
    "[a/Fe]": "alpha_fe_sme",
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

    source.data = dict(x=df.loc[0:100,x_name], y=df.loc[0:100,y_name])

for w in [select_x,select_y]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = VBoxForm(children=[text,select_x,select_y])

curdoc().add_root(HBox(children=[inputs, plot], width=800))

