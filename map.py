import pandas as pd
from geopy.geocoders import Nominatim
import folium as fo
#importung dataframe
df = pd.read_excel("data_2014.xlsx", header=None)
df = df.iloc[:,2:6]

#Refining the city and country columns taking only first 101 Countries data
city=list(df.iloc[:,1].str.replace(r"\(.*\)",""))
con =list(df.iloc[:,0].str.replace(r"\(.*\)",""))
pm = list(df.iloc[:,2])
year = list(df.iloc[:,3])
places = []

#combining city and contyr together
for i , j  in zip(city,con):
    places.extend([i + "," + j])
   

#Finding Latitude and longitude for the places
nom = Nominatim(scheme='http',user_agent="my-application")
lat=[]
lon=[]
for i in places:
    a = nom.geocode(i)
    if a and a.latitude and a.longitude is not None:
        lat.append(str(a.latitude))
        lon.append(str(a.longitude))
    else:
        lat.append(None)
        lon.append(None)


map = fo.Map(location = [28.6517178, 77.2219388],zoom_start=6,tiles = "OpenStreetMap")

def color_coder(pm):
    if pm <= 50:
        return 'green'
    if 51 < pm <= 100:
        return 'yellow'
    if 101<= pm <150:
        return 'orange'
    if 151 <= pm < 200:
        return 'red'
    if 201<= pm < 300:
        return 'purple'
    else:
        return 'grey'
fop = fo.FeatureGroup(name="Pollution level")



"""after poping out none value index from all list
lon.pop(9)
lon.pop(121)
lat.pop(9)
lat.pop(121)
pm.pop(9)
pm.pop(121)
year.pop(9)
year.pop(121)
places.pop(9)
places.pop(121)
No need to do this step if there is no none value"""

for lt,ln,p,yr,pl in zip(lat,lon,pm,year,places):
    fop.add_child(fo.CircleMarker(location=[float(lt),float(ln)], radius = 15, fill_color=color_coder(p), color = 'grey',
                                  popup=pl + " Air Quality " +str(p) + " in year " + str(yr)+"  " + str(lt)+ "," + str(ln),
                                  fill=True, fill_opacity=0.7))


    
map.add_child(fop)
map.save("Pollution_Map.html")
