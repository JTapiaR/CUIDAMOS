import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# Datos de muestra para la tabla

data_muestra = {
    "Nombre de Empresa": ["Centro de Salud Familiar", "Asociación de Cuidados", "Guardería Arcoiris", "Residencia El Sol", "Clínica Nueva Vida"],
    "Tipo de oportunidad": ["Taller de cuidados a adultos mayores", "Formación para el trabajo", "Vacantes para personas cuidadoras", "Evento para personas cuidadoras", "Curso gratuito primeros auxilios para cuidadores"],
    "No. plazas": [5, 3, 4, 2, 6],
    "Contacto": ["contacto@saludfamiliar.com", "info@cuidados.org", "rrhh@guarderiarcoiris.com", "empleo@elsol.com", "reclutamiento@nuevavida.com"],
    "Latitud ": [19.4326, 19.4256, 19.4347, 19.4396, 19.4356],
    "Longitud": [-99.1332, -99.1342, -99.1323, -99.1353, -99.1300]
}


# DataFrame con los datos de muestra
df_vacantes = pd.DataFrame(data_muestra)

# Función para mostrar la tabla y el mapa de oportunidades
df_vacantes = pd.DataFrame(data_muestra)

# Función para mostrar la tabla y el mapa de oportunidades
def show_job_opportunities():
    st.subheader("Oportunidades de Empleo y Cursos para Cuidadores")
    st.write("Datos ficticios con fines ilustrativos")
    
    # Mostrar la tabla con los datos de vacantes y cursos
    st.write("### Tabla de Oportunidades Disponibles")
    st.table(df_vacantes)

    # Crear el mapa
    st.write("### Mapa de Oportunidades")
    st.write("Datos ficticios con fines ilustrativos")
    mapa = folium.Map(location=[19.4326, -99.1332], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(mapa)

    # Añadir marcadores al mapa
    for _, row in df_vacantes.iterrows():
        folium.Marker(
            location=[row["Latitud "], row["Longitud"]],
            popup=f"{row['Nombre de Empresa']} - Vacantes: {row['No. plazas']}",
            icon=folium.Icon(color="purple")
        ).add_to(marker_cluster)

    # Mostrar el mapa en Streamlit
    st_folium(mapa, width=700, height=500)

# Función para que los usuarios del gobierno y comercio suban información
def upload_job_opportunities(session_state):
    # Verificar si el usuario es Comercio/Profesionista o Gobierno
    if session_state.profile in ["Comercio/Profesionista", "Gobierno"]:
        st.subheader("Subir Nueva Información de Oportunidades")
        
        with st.form("upload_form"):
            nombre_empresa = st.text_input("Nombre de la Empresa o Dependencia")
            vacantes = st.number_input("Número de Vacantes", min_value=0, value=0)
            contacto = st.text_input("Información de Contacto")
            latitud = st.number_input("Latitud", value=19.4326)
            longitud = st.number_input("Longitud", value=-99.1332)
            
            # Botón para subir los datos
            if st.form_submit_button("Subir Información"):
                nuevo_dato = {
                    "Nombre de Empresa": nombre_empresa,
                    "No. plazas": vacantes,
                    "Contacto": contacto,
                    "Latitud ": latitud,
                    "Longitud": longitud
                }
                # Añadir el nuevo dato al DataFrame existente
                global df_vacantes
                df_vacantes = df_vacantes.append(nuevo_dato, ignore_index=True)
                st.success("Información subida exitosamente.")
    else:
        st.warning("Solo los usuarios de Comercio/Profesionista y Gobierno pueden subir información.")

# Función principal para mostrar la sección de oportunidades
def show_opportunities_section(session_state):
    st.sidebar.title("Oportunidades de Empleo y Cursos")
    option = st.sidebar.radio("Selecciona una opción:", ["Ver Oportunidades", "Subir Información"])

    if option == "Ver Oportunidades":
        show_job_opportunities()
    elif option == "Subir Información":
        upload_job_opportunities(session_state)