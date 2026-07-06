import streamlit as st
import pandas as pd

# Configuración de la página (opcional, para que se vea ancha)
st.set_page_config(page_title="Visualizador de Datos", layout="wide")

st.title("📊 DX FTTH MEDITERRANEA NORTE")
st.write("Filtra la información del archivo de forma dinámica.")

# 1. Cargar el archivo Excel de forma eficiente
@st.cache_data
def cargar_datos():
    # Reemplaza 'DX FTTH.xlsx' por el nombre exacto de tu archivo
    return pd.read_excel("DX FTTH.xlsx")

try:
    df = cargar_datos()
# --- SECCIÓN DE FILTROS (Barra Lateral) ---
    st.sidebar.header("Filtros de Búsqueda")

    # 1. Buscador de texto libre
    busqueda = st.sidebar.text_input("🔍 Buscar por texto libre:")

    # 2. DEFINIR LAS DOS COLUMNAS A FILTRAR
    # Cambiá estos nombres por los encabezados reales de tu Excel
    columna_1 = 'route_criteria_cd'
    columna_2 = 'sector_operativo'

    # Copia inicial de los datos para ir aplicando los filtros en cadena
    df_filtrado = df.copy()

    # Filtro para la Primera Columna (si existe en el Excel)
    if columna_1 in df.columns:
        opciones_1 = df[columna_1].dropna().unique()
        seleccion_1 = st.sidebar.multiselect(f"Filtrar por {columna_1}:", opciones_1, default=opciones_1)
        # Filtramos
        df_filtrado = df_filtrado[df_filtrado[columna_1].isin(seleccion_1)]

    # Filtro para la Segunda Columna (si existe en el Excel)
    if columna_2 in df.columns:
        opciones_2 = df[columna_2].dropna().unique()
        seleccion_2 = st.sidebar.multiselect(f"Filtrar por {columna_2}:", opciones_2, default=opciones_2)
        # Volvemos a filtrar sobre lo que ya estaba filtrado
        df_filtrado = df_filtrado[df_filtrado[columna_2].isin(seleccion_2)]

    # Aplicamos la búsqueda por texto si escribieron algo
    if busqueda:
        df_filtrado = df_filtrado[df_filtrado.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]


    # --- SECCIÓN DE RESULTADOS ---
    st.metric(label="Registros encontrados", value=len(df_filtrado))
    st.dataframe(df_filtrado, use_container_width=True)
    



except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo 'datos.xlsx'. Asegúrate de subirlo al mismo repositorio de GitHub.")
except Exception as e:
    st.error(f"❌ Ocurrió un error al procesar el Excel: {e}")
