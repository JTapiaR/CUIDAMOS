import streamlit as st
import pandas as pd
from user_management import login_form, logout, handle_predefined_login
from care_registration import registrar_cuidado, mostrar_registros
from dashboard import show_dashboard
from calculator import show_custom_calculator
from services_map import show_services_map
from rewards_history import show_rewards_history
from solidarity_map import show_extended_services_map  
from job_opportunities import show_opportunities_section  
from support_dashboard import show_support_dashboard
from impact_map import show_impact_map

df_cuidado = pd.read_csv("Datos/tabla_cuidado.csv")

predefined_users = {
    "Cuidador": {"username": "cuidador1", "password": "cuidador_pass"},
    "Comercio/Profesionista": {"username": "comercio1", "password": "comercio_pass"},
    "Gobierno": {"username": "gobierno1", "password": "gobierno_pass"}
}

# Título de la aplicación
st.image("Portada.png")

# Menú de selección de perfil en la barra lateral
st.sidebar.title("Acceso")
option = st.sidebar.selectbox("Selecciona tu perfil:", ["Cuidador", "Comercio/Profesionista", "Gobierno"])

# Variables para almacenar el estado de inicio de sesión
session_state = st.session_state

# Inicializar variables en session_state si no existen
if "logged_in" not in session_state:
    session_state.logged_in = False
if "username" not in session_state:
    session_state.username = ""
if "profile" not in session_state:
    session_state.profile = ""

# Mostrar formulario de inicio de sesión según el perfil seleccionado
if option == "Cuidador":
    if not session_state.logged_in:
        login_form("Cuidador", predefined_users, session_state)
    else:
        if session_state.profile == "Cuidador":
            st.sidebar.button("Cerrar Sesión", on_click=logout, args=(session_state,))
            # Sección 1: Registrar Cuidados
            st.header("REGISTRO DE CUIDADOS")
            registrar_cuidado()
            st.divider()
            # Sección 2: Dashboard de Cuidados
            st.header("DASHBOARD DE CUIDADOS")
            show_dashboard()
            st.divider()
            # Sección 3: Otras Funcionalidades
            st.header("Otras Funcionalidades")
            if st.checkbox("Mostrar Calculadora de Cuidado"):
                show_custom_calculator()
                st.divider()
            if st.checkbox("MAPA DE COMERCIOS/PROFESIONISTAS/GOBIERNOS SOLIDARIOS"):
                show_extended_services_map()
                st.divider()    
            if st.checkbox("MAPA DE SERVICIOS DE CUIDADO"):
                show_services_map()
                st.divider()
            if st.checkbox("TABLERO DE OPORTUNIDADES"):
                show_opportunities_section(session_state) 
                st.divider()              
            if st.checkbox("HISTORIAL DE RECOMPENSAS"):
                show_rewards_history()
                st.divider()
elif option == "Comercio/Profesionista":
    if not session_state.logged_in:
        login_form("Comercio/Profesionista", predefined_users, session_state)
    else:
        if session_state.profile == "Comercio/Profesionista":
            st.sidebar.button("Cerrar Sesión", on_click=logout, args=(session_state,))
            st.write(f"Bienvenido, {session_state.username}! Consulta y gestiona las recompensas ofrecidas a cuidadores.")
            st.divider()
            show_support_dashboard(session_state)
            st.divider()
            show_opportunities_section(session_state)
            st.divider()
            if st.checkbox("Mostrar Mapa de Impacto"):  # Añadir opción para mostrar el Mapa de Impacto
                show_impact_map()
              # Mostrar oportunidades de empleo y cursos
elif option == "Gobierno":
    if not session_state.logged_in:
        login_form("Gobierno", predefined_users, session_state)
    else:
        if session_state.profile == "Gobierno":
            st.sidebar.button("Cerrar Sesión", on_click=logout, args=(session_state,))
            st.write(f"Bienvenido, {session_state.username}! Administra las deducciones y recompensas gubernamentales para cuidadores.")
            st.divider()
            show_support_dashboard(session_state)
            st.divider()  # Mostrar tablero de apoyos
            show_opportunities_section(session_state)  # Mostrar oportunidades de empleo y cursos
            st.divider()
            if st.checkbox("Mostrar Mapa de Impacto"):  # Añadir opción para mostrar el Mapa de Impacto
                show_impact_map()

# Información adicional sobre la plataforma
st.divider()
st.write("¿Qué buscamos?")
st.write("Abrir la conversación sobre como valorizar y pagar el trabajo de cuidado")
st.write("* El contenido de esta aplicación es ficticio, salvo las aquellos datos que se indiquen son parte de plataformas de datos abiertos")
st.write("* No recabamos datos personales en esta simulación, pero tenemos una propuesta de aviso de datos personales que puedes consultar aquí.")
st.write("https://docs.google.com/document/d/1fNuy42jke8yKlETgv790rxfgHSY8a--Tn2SzhAMtHt8/edit?usp=sharing")


column1, column2, column3 = st.columns(3)
with column1:
    st.image("Cuidadores.png")
    st.write('- **Para Cuidadores:** Registra tus actividades, accede a recompensas y obtén información útil.')
with column2:
    st.image("profesionistas.png")
    st.write(' - **Para Comercios/Profesionistas:** Ofrece recompensas a cuidadores y recibe  desde reconocimiento social hasta deducciones fiscales.')
with column3:
    st.image("Gobierno.png")
    st.write(' - **Para el Gobierno:** Gestiona apoyos, deducciones y recompensas a través de políticas de apoyo a cuidadores.')    
st.write(
   
)

