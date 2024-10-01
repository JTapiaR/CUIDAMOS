import streamlit as st
import pandas as pd
from care_registration import registros_cuidado

# Función para mostrar el dashboard de cuidados registrados
def show_dashboard():
    st.write("En este apartado puedes ver el el total de horas, personas y cuidados")
    
    # Verificar si hay registros
    if len(registros_cuidado) > 0:
        # Convertir la lista de registros a un DataFrame
        df_registros = pd.DataFrame(registros_cuidado)

        # Calcular estadísticas
        total_cuidados = df_registros.shape[0]
        horas_totales = df_registros["Horas de Cuidado"].sum()
        personas_cuidadas = df_registros["Número de Personas Cuidadas"].sum()

        # Crear un DataFrame para mostrar las estadísticas como una tabla
        df_totales = pd.DataFrame({
            "Estadística": ["Total de Cuidados Registrados", "Total de Horas de Cuidado", "Total de Personas Cuidadas"],
            "Valor": [total_cuidados, horas_totales, personas_cuidadas]
        })

        # Mostrar la tabla con los totales calculados
        st.table(df_totales)

        # Mostrar tabla de registros detallados
        st.subheader("Detalles de Cuidados Registrados")
        st.write("En este apartado puedes visualizar los cuidados que has registrado")
        st.dataframe(df_registros[["Fecha", "Tipo de Cuidado", "Género Cuidador", "Número de Personas Cuidadas", "Horas de Cuidado", "Comentarios"]])
    else:
        st.warning("No hay registros de cuidado para mostrar en el dashboard.")



