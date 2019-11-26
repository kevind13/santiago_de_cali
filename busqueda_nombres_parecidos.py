import geopandas as gpd
import pandas as pd
import difflib

df = pd.read_csv('hurto-personas/hurto-personas-2011.csv')
mapa_cali = gpd.read_file('mapa_cali/barrios.shp')
total_barrios = mapa_cali.barrio.values
nombre_barrios = df.barrio.unique()

for x in range(len(nombre_barrios)):
    try:
        tmp = difflib.get_close_matches(nombre_barrios[x], total_barrios, cutoff=0.4)[0]
    except:
        pass
        
    if nombre_barrios[x] != tmp:
        print('Barrio en base de datos: {}, barrio en mapa cali {}'.format(nombre_barrios[x],tmp))
        
        