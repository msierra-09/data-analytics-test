# Load the required libraries
import pandas as pd
from pandas_profiling import ProfileReport
from googlemaps import Client as GoogleMaps
import googlemaps
import gmaps
from keplergl import KeplerGl
import geopandas as gpd
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster


# Load and explore the data
addresses = pd.read_csv("data.csv")
# Look at the top few rows
addresses.head()
# Understand data types
addresses.describe()

# Pandas profiling
prof = ProfileReport(addresses)
prof

# New column called Full Address
addresses['Full_Address'] = addresses['City'].astype(str) + ', ' + \
                addresses['Country']
addresses.head()

#API key
gmaps = googlemaps.Client(key="AIzaSyDGyZlznAK4ptH0535EMac3xzoxF3Ty1dk")

addresses1= addresses.iloc[:,-1:].copy()
addresses1.head()

addresses1['long'] = ""
addresses1['lat'] = ""

for x in range(len(addresses1)):
    geocode_result = gmaps.geocode(addresses1['Full_Address'][x])
    addresses1['lat'][x] = geocode_result[0]['geometry']['location'] ['lat']
    addresses1['long'][x] = geocode_result[0]['geometry']['location']['lng']

# Join the results with original file
addresses['Lat']=addresses1['lat']
addresses['Lon']= addresses1['long']
df = addresses.fillna('')
df.head()

#empty map
world_map= folium.Map(tiles="cartodbpositron")
marker_cluster = MarkerCluster().add_to(world_map)

for i in range(len(df)):
        lat = df.iloc[i]['Lat']
        long = df.iloc[i]['Lon']
        radius=5
        
        folium.CircleMarker(location = [lat, long], radius=radius, fill =True).add_to(marker_cluster)
#show the map
world_map.save("index.html")