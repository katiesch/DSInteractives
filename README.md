# GALAHInteractives
Interactive bokeh codes to play with the GALAH data

abundance_comp.py is preliminary code. ignore for now. 

histogram_check.py lets you compare various parameters in the 
wg4 output files for all of the K2 stars. It also plots the 
number density along each axis. Requires bokeh, pandas, numpy modules. 

abundance_embed.py expands the basic histogram_check.py code and extends it 
such that the interactive figure is embedded in a webpage via automated 
HTML and JS. The embedded material is currently at 
http://www.mso.anu.edu.au/~kschles/d3tests/bokeh3.html

bokeh3.html and bokeh3.js are created by abundance_embed.py. 
