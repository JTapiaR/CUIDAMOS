# rewards_history.py

import streamlit as st
import pandas as pd

# Función para mostrar el historial de recompensas
def show_rewards_history():
    st.subheader("Historial de Recompensas")
    
    # Datos de ejemplo
    data = {
        "Fecha": ["2024-01-10", "2024-02-15", "2024-03-20"],
        "Actividad": ["Cuidado de persona mayor", "Cuidado de persona con discapacidad", "Cuidado de niño"],
        "Recompensa": ["Descuento en supermercado", "Consulta médica gratuita", "Membresía de gimnasio"]
    }
    
    # Crear un DataFrame
    df = pd.DataFrame(data)
    
    # Mostrar tabla en la aplicación
    st.table(df)
