import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# Datos de ejemplo para el tablero
data_apoyos = {
    "ID Cuidador": ["CUID001", "CUID002", "CUID003"],
    "Cantidad de Apoyos Brindados": [5, 3, 4],
    "Monto Monetario ($)": [15000, 9000, 12000],
    "Cantidad de Familias Apoyadas": [5, 3, 4],
    "Fecha de Apoyo": ["2024-09-01", "2024-09-05", "2024-09-10"]
}

# Crear un DataFrame con los datos de ejemplo
df_apoyos = pd.DataFrame(data_apoyos)

# Función para mostrar el tablero de apoyos
def show_support_dashboard(session_state):
    st.subheader("Tablero de Apoyos Brindados")

    # Mostrar los registros de apoyos en una tabla
    st.write("### Registros de Apoyos")
    st.table(df_apoyos)

    # Mostrar formulario para registrar nuevos apoyos
    st.write("### Registrar Nuevo Apoyo")
    with st.form("registro_apoyo"):
        id_cuidador = st.text_input("ID Cuidador")
        cantidad_apoyos = st.number_input("Cantidad de Apoyos Brindados", min_value=1, value=1)
        monto_monetario = st.number_input("Monto Monetario ($)", min_value=0, value=0)
        cantidad_familias = st.number_input("Cantidad de Familias Apoyadas", min_value=1, value=1)
        fecha_apoyo = st.date_input("Fecha de Apoyo")
        
        # Botón para registrar el apoyo
        if st.form_submit_button("Registrar Apoyo"):
            nuevo_apoyo = {
                "ID Cuidador": id_cuidador,
                "Cantidad de Apoyos Brindados": cantidad_apoyos,
                "Monto Monetario ($)": monto_monetario,
                "Cantidad de Familias Apoyadas": cantidad_familias,
                "Fecha de Apoyo": fecha_apoyo.strftime("%Y-%m-%d")
            }
            df_apoyos.loc[len(df_apoyos)] = nuevo_apoyo
            st.success("Apoyo registrado exitosamente.")

    # Botón para generar el reporte en PDF
    if st.button("Generar Reporte PDF"):
        generar_reporte_pdf(df_apoyos)

# Función para generar el reporte en PDF
def generar_reporte_pdf(df_apoyos):
    try:
        # Crear el objeto PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título del reporte
        pdf.cell(200, 10, txt="Reporte de Apoyos Brindados", ln=True, align="C")

        # Agregar tabla con los registros de apoyo
        for index, row in df_apoyos.iterrows():
            pdf.cell(200, 10, txt=f"ID Cuidador: {row['ID Cuidador']}, Cantidad de Apoyos: {row['Cantidad de Apoyos Brindados']}, "
                                  f"Monto: ${row['Monto Monetario ($)']}, Familias Apoyadas: {row['Cantidad de Familias Apoyadas']}, "
                                  f"Fecha: {row['Fecha de Apoyo']}", ln=True)

        # Guardar el archivo PDF
        pdf_path = "Datos/reporte_apoyos.pdf"
        pdf.output(pdf_path)

        # Verificar si el archivo se creó correctamente
        if os.path.exists(pdf_path):
            st.success("Reporte generado exitosamente.")
            st.markdown(f"[Descargar Reporte PDF](sandbox:{pdf_path})")
        else:
            st.error("No se pudo generar el reporte. Verifica los permisos y la ruta de archivo.")
    except Exception as e:
        st.error(f"Error al generar el reporte: {e}")
