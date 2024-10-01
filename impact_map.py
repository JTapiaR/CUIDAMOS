import streamlit as st
import folium
import pandas as pd
from shapely import wkt
from streamlit_folium import folium_static
import geopandas as gpd
from shapely.errors import WKTReadingError

def show_impact_map():
    # Cargar los DataFrames
    df_dependientes = pd.read_csv("Datos/Dependientes infancias y 60+ por manzana.csv")
    df_pcd = pd.read_csv("Datos/PCD por manzana.csv")

    # Función para manejar la conversión segura de WKT a geometría
    def safe_wkt_load(wkt_str):
        if isinstance(wkt_str, str):  # Verificar si el valor es una cadena de texto (WKT)
            try:
                return wkt.loads(wkt_str)
            except (WKTReadingError, ValueError):
                return None
        return None

    # Convertir la columna 'geometry' de WKT a geometrías usando shapely, manejando errores
    df_dependientes['geometry'] = df_dependientes['geometría manzana'].apply(safe_wkt_load)
    df_pcd['geometry'] = df_pcd['GEOMETRIA MANZANAS'].apply(safe_wkt_load)

    # Filtrar filas con geometría válida
    df_dependientes = df_dependientes[df_dependientes['geometry'].notnull()]
    df_pcd = df_pcd[df_pcd['geometry'].notnull()]

    # Crear GeoDataFrames
    gdf_dependientes = gpd.GeoDataFrame(df_dependientes, geometry='geometry')
    gdf_pcd = gpd.GeoDataFrame(df_pcd, geometry='geometry')

    # Opciones de columnas a visualizar (de ambos dataframes)
    opciones_dependientes = [
        '% Población 0 A 2 en la manzana',
        '%Población de 3 a 5 años en la manzana',
        '%Población de 6 a 11 años en la manzana',
        '% Población de 8 a 14 años',
        '% Población de 15 a 17 años',
        '%Población de 60 años y más',
        '% Personas dependientes infancias (0 a 17 años) en la manzana',
        '%Población dependiente infancias  y tercera edad en la manzana'
    ]

    opciones_pcd = [
        '%Población con discapacidad en la manzana',
        '%Población con discapacidad para caminar, subir o bajar en la manzana',
        '%Población con discapacidad para ver, aun usando lentes en la manzana',
        '%Población con discapacidad para hablar o comunicarse en la manzana',
        '%Población con discapacidad para oír, aun usando aparato auditivo en la manzana',
        '%Población con discapacidad para vestirse, bañarse o comer en la manzana',
        '%Población con limitación en la manzana',
        '%Población con algún problema o condición mental',
        '%Población con limitación para recordar o concentrarse en la manzana',
        '% Población con limitación para vestirse, bañarse o comer en la manzana',
        '%Población con limitación para oír, aun usando aparato auditivo',
        '%Población con limitación para hablar o comunicarse en la manzana',
    ]

    # Crear mapa base
    map_center = [19.432608, -99.133209]  # Centro de la Ciudad de México
    mapa = folium.Map(location=map_center, zoom_start=12)

    # Sidebar para seleccionar qué datos visualizar
    st.sidebar.title("Mapa de Impacto")
    capa_seleccionada = st.sidebar.selectbox("Selecciona la capa que quieres visualizar", ["Dependientes", "Personas con Discapacidad"])
    columna_seleccionada = None

    if capa_seleccionada == "Dependientes":
        columna_seleccionada = st.sidebar.selectbox("Selecciona el dato a visualizar", opciones_dependientes)
        gdf_seleccionado = gdf_dependientes
    elif capa_seleccionada == "Personas con Discapacidad":
        columna_seleccionada = st.sidebar.selectbox("Selecciona el dato a visualizar", opciones_pcd)
        gdf_seleccionado = gdf_pcd

    # Convertir la columna seleccionada a numérica, eliminando los valores no válidos
    gdf_seleccionado[columna_seleccionada] = pd.to_numeric(gdf_seleccionado[columna_seleccionada], errors='coerce')
    gdf_seleccionado = gdf_seleccionado.dropna(subset=[columna_seleccionada])  # Eliminar filas con valores NaN en la columna seleccionada

    # Crear una columna de ID única para la geometría
    gdf_seleccionado["id"] = gdf_seleccionado.index.astype(str)

    # Agregar polígonos al mapa según la selección del usuario
    if columna_seleccionada:
        folium.Choropleth(
            geo_data=gdf_seleccionado.to_json(),
            name="choropleth",
            data=gdf_seleccionado,
            columns=["id", columna_seleccionada],  # Usar 'id' como clave
            key_on="feature.id",  # Conectar con 'id'
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=columna_seleccionada,
        ).add_to(mapa)

    # Mostrar el mapa
    folium_static(mapa)




