import streamlit as st
import pandas as pd
import sqlite3

# Título de la aplicación
st.title("Cruce de Bases de Datos y Operaciones de Inserción")

# Función para crear la tabla si no existe
def crear_tabla():
    conexion = sqlite3.connect('mi_base_de_datos.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            ID INTEGER PRIMARY KEY,
            Nombre TEXT,
            Apellido TEXT,
            Celular TEXT,
            Dirección TEXT,
            Turno TEXT,
            Horario TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

# Función para insertar un nuevo registro
def insertar_registro(id, nombre, apellido, celular, direccion, turno, horario):
    conexion = sqlite3.connect('mi_base_de_datos.db')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO usuarios (ID, Nombre, Apellido, Celular, Dirección, Turno, Horario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id, nombre, apellido, celular, direccion, turno, horario))
    conexion.commit()
    conexion.close()

# Función para inserción masiva desde un DataFrame
def insertar_masivo(df):
    conexion = sqlite3.connect('mi_base_de_datos.db')
    df.to_sql('usuarios', conexion, if_exists='append', index=False)
    conexion.close()

# Cargar archivo de Excel y realizar merge
uploaded_file = st.file_uploader("Cargar archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        Inf = pd.read_excel(uploaded_file, sheet_name='Inf')
        Turno = pd.read_excel(uploaded_file, sheet_name='Turnos')

        # Mostrar las hojas cargadas
        st.subheader("Datos de la hoja 'Inf'")
        st.write(Inf)

        st.subheader("Datos de la hoja 'Turnos'")
        st.write(Turno)

        # Realizar el cruce (merge) entre las dos hojas
        DB_Inf = Inf.merge(Turno, left_on=['ID'], right_on=['ID'], how='left')

        # Mostrar el DataFrame resultante
        st.subheader("Resultado del Cruce de Datos")
        st.write(DB_Inf)

    except Exception as e:
        st.error(f"Error al cargar las hojas de Excel: {e}")

# Formulario para insertar un nuevo registro
st.subheader("Agregar Nuevo Registro Manualmente")

with st.form("insertar_form"):
    id = st.number_input("ID", min_value=1)
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    celular = st.text_input("Celular")
    direccion = st.text_input("Dirección")
    turno = st.selectbox("Turno", ["Mañana", "Tarde", "Noche"])
    horario = st.text_input("Horario")
    
    submit = st.form_submit_button("Agregar Registro")

    if submit:
        insertar_registro(id, nombre, apellido, celular, direccion, turno, horario)
        st.success(f"Registro de {nombre} {apellido} agregado exitosamente.")

# Inserción masiva de un archivo Excel
st.subheader("Operaciones de Inserción Masiva")

uploaded_mass_file = st.file_uploader("Cargar archivo Excel para inserción masiva", type=["xlsx"], key="mass_upload")

if uploaded_mass_file is not None:
    try:
        df_mass = pd.read_excel(uploaded_mass_file)
        st.write("Datos a insertar:")
        st.write(df_mass)

        if st.button("Insertar Masivamente"):
            insertar_masivo(df_mass)
            st.success("Datos insertados masivamente en la base de datos.")

    except Exception as e:
        st.error(f"Error al cargar archivo para inserción masiva: {e}")

# Función para ver registros actuales en la base de datos
def ver_registros():
    conexion = sqlite3.connect('mi_base_de_datos.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    registros = cursor.fetchall()
    conexion.close()
    return registros

# Ver registros actuales
st.subheader("Ver Registros Existentes en la Base de Datos")
if st.button("Ver Registros"):
    registros = ver_registros()
    df_registros = pd.DataFrame(registros, columns=['ID', 'Nombre', 'Apellido', 'Celular', 'Dirección', 'Turno', 'Horario'])
    st.write(df_registros)

# Crear la tabla si no existe
crear_tabla()
