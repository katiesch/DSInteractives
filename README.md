# GALAHInteractives
Interactive bokeh codes to play with the GALAH data

We already have a bunch of parameter and abundance information for 
~27,000 GALAH targets that fall in K2 fields. I wanted to be able 
to quickly look at the shape of the abundance and parameter distributions 
and compare different values to each other. These interactive visualisations 
allow you to compare various properties against one another. With the hover 
tool in the bokeh programs you can also easily identify outliers for further 
checks. 

abundance_comp.py is preliminary code. ignore for now. 

histogram_check.py lets you compare various parameters in the 
wg4 output files for all of the K2 stars. It also plots the 
number density along each axis. Requires bokeh, pandas, numpy modules. 

abundance_embed.py expands the basic histogram_check.py code and extends it 
such that the interactive figure is embedded in a webpage via automated 
HTML and JS. The embedded material is currently at 
http://www.mso.anu.edu.au/~kschles/datavis/bokeh3.html

bokeh3.html and bokeh3.js are created by abundance_embed.py. 

The javascript directory has some scripts/html I've been playing with. The purpose 
is similar to bokeh3.html/.js, just in another language. It can be seen at 
http://www.mso.anu.edu.au/~kschles/datavis/k2_param_comp.html
