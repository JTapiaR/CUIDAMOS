import streamlit as st
import pandas as pd
from datetime import datetime

# Cargar la tabla de cuidado para obtener valores de referencia
df_cuidado = pd.read_csv("Datos/tabla_cuidado.csv")

# Variable global para almacenar registros
registros_cuidado = []

# Función para registrar un cuidado
def registrar_cuidado():
    st.subheader("En este apartado puedes registrar los cuidados que realizas")   
    st.write("*las categorías de cuidados y sexo son las establecidas en la Cuenta Satélite del Trabajo NO Remunerado de los Hogares en México (INEGI) ")

    # Formulario para registrar cuidados
    tipo_cuidado = st.selectbox("Selecciona el tipo de cuidado realizado*:", df_cuidado["Concepto"].unique(), key="tipo_cuidado")
    genero_cuidador = st.radio("Selecciona tu sexo*:", ["Mujer", "Hombre"], key="genero_cuidador")
    num_personas = st.number_input("Número de personas cuidadas", min_value=0, value=0, key="num_personas")
    hours = st.number_input("Horas de cuidado realizadas", min_value=1, max_value=24, value=1, key="hours_cuidado")
    fecha = st.date_input("Fecha de cuidado", value=datetime.today(), key="fecha_cuidado")
    comentarios = st.text_area("En esta sección puedes registrar comentarios adicionales", "", key="comentarios_cuidado")

    # Botón para registrar el cuidado
    if st.button("Registrar Cuidado", key="btn_registrar_cuidado"):
        # Guardar los datos en la lista de registros
        registro = {
            "Fecha": fecha,
            "Tipo de Cuidado": tipo_cuidado,
            "Género Cuidador": genero_cuidador,
            "Número de Personas Cuidadas": num_personas,
            "Horas de Cuidado": hours,
            "Comentarios": comentarios
        }
        registros_cuidado.append(registro)
        st.success("Cuidado registrado exitosamente.")

# Función para mostrar los registros
def mostrar_registros():
    st.subheader("Registros de Cuidados Realizados")

    # Verificar si hay registros
    if len(registros_cuidado) > 0:
        # Convertir la lista de registros a un DataFrame
        df_registros = pd.DataFrame(registros_cuidado)

        # Mostrar los registros en una tabla
        st.table(df_registros)
    else:
        st.warning("No hay registros de cuidado aún.")


