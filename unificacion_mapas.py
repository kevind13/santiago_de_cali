import geopandas as gpd

mapa_cali_kevin = gpd.read_file('mapa_cali_kevin/Barrios.shp')
mapa_cali_daniela = gpd.read_file('mapa_cali_daniela/barrios/barrios.shp')
mapa_cali_kevin = mapa_cali_kevin.rename(columns = {'OBJECTID': 'id_barrio'})
mapa_cali_kevin['id_barrio'] = mapa_cali_kevin['id_barrio'].astype('int')
mapa_cali_daniela['id_barrio'] = mapa_cali_daniela['id_barrio'].astype('int')
mapa_cali_nuevo = mapa_cali_daniela.merge(mapa_cali_kevin[['id_barrio','BARRIO']],how='left',on='id_barrio')
mapa_cali_nuevo.columns
mapa_cali_nuevo = mapa_cali_nuevo[['id_barrio', 'BARRIO', 'comuna', 'estra_moda', 'area',
       'perimetro', 'Shape_Leng', 'Shape_Area', 'geometry']]
mapa_cali_nuevo.columns = ['id_barrio', 'barrio', 'comuna', 'estra_moda', 'area',
       'perimetro', 'Shape_Leng', 'Shape_Area', 'geometry']
mapa_cali_nuevo['barrio']=mapa_cali_nuevo['barrio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
mapa_cali_nuevo.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
mapa_cali_nuevo.to_file('mapa_cali/barrios.shp',driver='ESRI Shapefile')