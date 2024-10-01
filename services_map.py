import streamlit as st
import folium
import json
import pandas as pd
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import os
from geopy.distance import geodesic
import streamlit as st
from shapely.geometry import Polygon
from shapely import wkt  

# Cargar los datos
df_mercados = pd.read_csv('Datos/mercados.csv')
df_deportivas = pd.read_csv('Datos/instalaciones_deportivas.csv')
df_educacion = pd.read_csv('Datos/instalaciones_educacion_basica.csv')

# Función para obtener el centroide del polígono
def get_centroid(geometry):
    try:
        if isinstance(geometry, str):  # Validamos si es una cadena que representa un polígono
            # Convertir el valor de la columna geometry en un objeto de tipo Polygon
            polygon = wkt.loads(geometry)
            # Obtener el centroide del polígono
            return polygon.centroid.y, polygon.centroid.x
        else:
            return None, None  # Omitir si no es un polígono válido en formato WKT
    except Exception:
        return None, None  # Omitir errores silenciosamente

# Función para procesar las coordenadas de POINT Z
def extract_lat_lon_point_z(geometry_str):
    try:
        # Extraer las coordenadas de un 'POINT Z' ignorando la altitud
        coords = geometry_str.replace('POINT Z (', '').replace(')', '').split()
        lon = float(coords[0])
        lat = float(coords[1])
        return lat, lon
    except Exception:
        return None, None  # Omitir errores silenciosamente

# Función para mostrar el mapa de servicios con capas seleccionables
def show_services_map():
    st.subheader("Mapa de Servicios Públicos")
    
    # Crear el mapa centrado en CDMX
    map_center = [19.432608, -99.133209]  # Coordenadas de ejemplo (CDMX)
    mapa = folium.Map(location=map_center, zoom_start=12)
    
    # Opción para que el usuario seleccione la capa
    capa_seleccionada = st.multiselect("Selecciona las capas que quieres visualizar:", 
                                       ["Mercados", "Instalaciones Deportivas", "Instalaciones Educación Básica"])

    # Mostrar mercados si está seleccionada la capa de mercados
    if "Mercados" in capa_seleccionada:
        for index, row in df_mercados.iterrows():
            lat = row['COORGEOG_Y']
            lon = row['COORGEOG_X']
            mercado_info = f"{row['MERCADO']} - {row['DELEGACION']}<br>Dirección: {row['DIRECCION']}<br>Tipo: {row['TIPO']}<br>Superficie: {row['SUPERF_M2']} m²"
            folium.Marker([lat, lon], popup=mercado_info, tooltip=row['MERCADO'], icon=folium.Icon(color='green')).add_to(mapa)

    # Mostrar instalaciones deportivas si está seleccionada la capa de deportivas
    if "Instalaciones Deportivas" in capa_seleccionada:
        for index, row in df_deportivas.iterrows():
            lat, lon = extract_lat_lon_point_z(row['geometry'])
            if lat is not None and lon is not None:
                deportiva_info = f"{row['NOM_INSTA']} - {row['ALCALDIA']}<br>Dirección: {row['DIRECCION']}"
                folium.Marker([lat, lon], popup=deportiva_info, tooltip=row['NOM_INSTA'], icon=folium.Icon(color='blue')).add_to(mapa)

    # Mostrar instalaciones de educación básica si está seleccionada la capa de educación
    if "Instalaciones Educación Básica" in capa_seleccionada:
        for index, row in df_educacion.iterrows():
            lat, lon = get_centroid(row['geometry'])
            if lat is not None and lon is not None:
                educacion_info = f"Colonia: {row['colonia']}<br>Población: {row['pob_2010']}<br>Escuelas: {row['NoEqEduBas']}"
                folium.Marker([lat, lon], popup=educacion_info, tooltip=row['colonia'], icon=folium.Icon(color='red')).add_to(mapa)
    
    # Mostrar el mapa en la aplicación
    folium_static(mapa)

# Llamar a la función para mostrar el mapa de servicios
show_services_map()
