# Load libraries
from __future__ import division
import os
os.environ['PROJ_LIB'] = 'C:/Users/kiran/Anaconda3/Library/share'
import pandas as pd
from itertools import groupby
import operator
import matplotlib.pyplot as plt
import matplotlib.cm
%matplotlib inline
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import numpy as np
import seaborn as sns
import math

#cwd = os.getcwd()  # Get the current working directory (cwd)
#files = os.listdir(cwd)  # Get all the files in that directory
#print("Files in %r: %s" % (cwd, files))

data = pd.read_csv("india-covid-19.csv")

# Group the data state-wise
states_group = data.groupby(by = "State name")

# List for storing tuples which contain state-name and its corresponding infection rate
affected_rate = []
# Population of india
total_pop=1350000000

for key , group in states_group:
    infected_people = 0
    for row in group.iterrows():
        infected_people += row[1][1]
    
    # Calculate percent, I just trying in 10000000
    rate = (infected_people/total_pop)*10000000
    affected_rate.append((key,rate))

# Create figure 
fig, ax = plt.subplots()
# Create a map with the coordinates determined by the Bounding Box tool
m = Basemap(projection='merc',lat_0=54.5, lon_0=-4.36,llcrnrlon=68.1, llcrnrlat= 6.5, urcrnrlon=97.4, urcrnrlat=35.5)
# Draw map boundary and set the color
m.drawmapboundary(fill_color='#46bcec')
# Fill continents and lakes
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
# Draw coast lines
m.drawcoastlines()

# Load the shape file of India
m.readshapefile("C:/Users/kiran/Projects/python/India/india","INDIA")

# An empty list to hold infection rates
aff_rate = []
for state_info in m.INDIA_info:
    state = state_info['ST_NAME'].upper()
    rate = 0
    
    # In affected_rate (containing tuples of state name and infection rates), search for state 'state'
    # Append its corresponding count rate to aff_rate
    for x in affected_rate:
        if x[0].upper() == state:
            rate = x[1]
            break
    aff_rate.append(rate)
    
# A dataframe containing shapes, state names and rates    
df_poly = pd.DataFrame({
        'shapes': [Polygon(np.array(shape), True) for shape in m.INDIA],
        'area': [area['ST_NAME'] for area in m.INDIA_info],
        'aff_rate' : aff_rate
    })

# Get all the shapes
shapes = [Polygon(np.array(shape), True) for shape in m.INDIA]
# Colormap
cmap = plt.get_cmap('Greys')   
# A patch collection. Create patches on the top of the map, not beneath it (zorder=2)
pc = PatchCollection(shapes, zorder=2)

norm = Normalize()
# Set color according to the infection rate of the state
pc.set_facecolor(cmap(norm(df_poly['aff_rate'].fillna(0).values)))
ax.add_collection(pc)

# A mapper to map color intensities to values
mapper = matplotlib.cm.ScalarMappable(cmap=cmap)
mapper.set_array(aff_rate)
plt.colorbar(mapper, shrink=0.4)
# Set title for the plot
ax.set_title("COVID-19 INFECTION RATE IN INDIA")
plt.figtext(0,0,'@kiranlm')
# Change plot size and font size
plt.rcParams['figure.figsize'] = (15,15)
plt.rcParams.update({'font.size': 20})
plt.show()