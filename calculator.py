import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime

# Importar los registros de cuidados desde care_registration
from care_registration import registros_cuidado

# Cargar la tabla de cuidado para obtener valores de referencia
df_cuidado = pd.read_csv("Datos/tabla_cuidado.csv")

# Función para mostrar la calculadora de cuidado con reporte personalizado
def show_custom_calculator():
    st.subheader("CALCULADORA DE CUIDADO ")
    st.write("*los precios mostrados provienen de la Cuenta Satélite del Trabajo NO Remunerado de los Hogares en México (INEGI) Anexo/ Todos/ Costo por hora por método híbrido 2022")
    st.write("https://www.inegi.org.mx/app/tabulados/default.aspx?pr=26&vr=2&in=89&tp=20&wr=1&cno=1&idrt=3266&opc=p", label="Datos precios",)

    # Verificar si hay registros de cuidado
    if len(registros_cuidado) == 0:
        st.warning("No hay registros de cuidado aún. Por favor, registra tus cuidados primero.")
        return

    # Mostrar registros actuales
    df_registros = pd.DataFrame(registros_cuidado)
    st.write("**Registros de Cuidados Realizados:**")
    st.table(df_registros)

    # Selección de parámetros personalizados para el cálculo
    st.write("**Selecciona los parámetros para tu reporte personalizado:**")
    tipo_cuidado = st.multiselect("Selecciona los tipos de cuidado que quieres incluir en el reporte:", df_registros["Tipo de Cuidado"].unique())
    fecha_inicio = st.date_input("Fecha de inicio", value=datetime.today())
    fecha_fin = st.date_input("Fecha de fin", value=datetime.today())

    # Filtrar registros según el tipo de cuidado y rango de fechas
    df_filtrado = df_registros[
        (df_registros["Tipo de Cuidado"].isin(tipo_cuidado)) & 
        (pd.to_datetime(df_registros["Fecha"]) >= pd.to_datetime(fecha_inicio)) & 
        (pd.to_datetime(df_registros["Fecha"]) <= pd.to_datetime(fecha_fin))
    ]

    if st.button("Mostrar Resumen"):
        if not df_filtrado.empty:
            mostrar_resumen(df_filtrado)
        else:
            st.warning("No hay registros que coincidan con los filtros seleccionados.")

    #  reporte personalizado
    if st.button("Generar Reporte CSV"):
        if not df_filtrado.empty:
            generar_reporte_csv(df_filtrado)
        else:
            st.warning("No hay registros que coincidan con los filtros seleccionados. No se puede generar el reporte.")

# Función para mostrar el resumen de cuidados
def mostrar_resumen(df_filtrado):
    st.write("**Resumen de Cuidados Filtrados:**")
    
    total_horas = df_filtrado["Horas de Cuidado"].sum()
    total_personas = df_filtrado["Número de Personas Cuidadas"].sum()
    total_valor = 0  # Valor económico total basado en el cálculo

    # Calcular el valor económico basado en la tabla de cuidado
    for _, row in df_filtrado.iterrows():
        tipo = row["Tipo de Cuidado"]
        genero = row["Género Cuidador"]
        horas = row["Horas de Cuidado"]
        personas = row["Número de Personas Cuidadas"]
        
        # Obtener el valor por hora del cuidado desde df_cuidado
        matching_rows = df_cuidado[
            (df_cuidado["Concepto"] == tipo) & 
            (df_cuidado["Género"] == genero)
        ]

        if matching_rows.empty:
            st.warning(f"No se encontró el valor para el cuidado '{tipo}' y género '{genero}' en la tabla de referencia.")
            continue

        valor_cuidado = matching_rows["Valor (pesos)"].values[0]
        
        # Calcular el valor total de las horas de cuidado para esa fila
        valor_total_fila = horas * valor_cuidado * personas
        total_valor += valor_total_fila
    
    st.write(f"**Total de Horas de Cuidado:** {total_horas}")
    st.write(f"**Total de Personas Cuidadas:** {total_personas}")
    st.write(f"**Valor Económico Total:** ${total_valor:.2f}")

# Función para generar el reporte personalizado en CSV y descarga directa
def generar_reporte_csv(df_filtrado):
    try:
        # Agregar columna de valor económico
        df_filtrado["Valor Económico"] = df_filtrado.apply(calcular_valor_economico, axis=1)

        # Crear un CSV en memoria
        output = StringIO()
        df_filtrado.to_csv(output, index=False)
        csv_content = output.getvalue()

        # Descargar el archivo CSV
        st.download_button(
            label="Descargar Reporte Personalizado en CSV",
            data=csv_content,
            file_name="reporte_cuidado_personalizado.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error al generar el reporte: {e}")

# Función para calcular el valor económico de cada registro
def calcular_valor_economico(row):
    tipo = row["Tipo de Cuidado"]
    genero = row["Género Cuidador"]
    horas = row["Horas de Cuidado"]
    personas = row["Número de Personas Cuidadas"]

    # Obtener el valor por hora del cuidado desde df_cuidado
    matching_rows = df_cuidado[
        (df_cuidado["Concepto"] == tipo) & 
        (df_cuidado["Género"] == genero)
    ]

    if matching_rows.empty:
        return 0  # Si no se encuentra, devolver 0

    valor_cuidado = matching_rows["Valor (pesos)"].values[0]

    # Calcular el valor total de las horas de cuidado para esa fila
    valor_total_fila = horas * valor_cuidado * personas
    return valor_total_fila

# Llamar a la función para mostrar la calculadora personalizada
show_custom_calculator()





