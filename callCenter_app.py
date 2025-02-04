#pip install streamlit pymongo
#python.exe -m pip install --upgrade pip
#pip install streamlit pymongo
#cd \Globokas\ScoringPython
#cd \Red Comercial\AutomatizaciónTrx\Procesos Plantillas\PythonProcesos\Web_Streamlit_Python_Mongo

import ssl
import streamlit as st
from pymongo import MongoClient, errors
from datetime import datetime, timedelta

# Conectar a MongoDB
try:
    client = MongoClient("mongodb+srv://datayanalitica:hDeF35XYwRgMgrT4@searchengine.qcnlr.mongodb.net/?retryWrites=true&w=majority&appName=SearchEngine",
                        tls=True,
                        serverSelectionTimeoutMS=5000)
    db = client["search_engine"]
    users_collection = db["users"]  # Colección que contiene RUC y códigos
    tiendas_collection = db["oz_search"]
except errors.ServerSelectionTimeoutError:
    st.error("No se pudo conectar a MongoDB. Verifique la URL y las credenciales.")
    st.stop()

# CSS personalizado para mejorar el diseño
st.markdown(
    """
    <style>
    .custom-input-label {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 10px;
    }
    .stTextInput>div>div>input {
        font-size: 13px;
        border-radius: 5px;
        padding: 8px;
    }
    
    .stTextInput>div>div {
        flex: 1;
    }
    .stWrite {
        margin-bottom: 0px;
        color: #333;
        font-size: 13px;
    }
    .stWrite strong {
        color: #007bff;
    }
    /* Eliminar los bordes del contador de caracteres */
    .stTextInput div[data-testid="stTextInputCounter"] {
        border: none;
        background-color: transparent;
        font-size: 12px;
        color: #555; /* Puedes ajustar el color si es necesario */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Definir los nombres de los campos
field_names = {
    "id_codigo": "Id agente",
    "Tienda": "Comercio",
    "coordinador": "Coordinador",
    "ZONA": "Zona",
    "TipoPGY": "PAGAYA",

    "202402_PGY": "Febrero 24",
    "202403_PGY": "Marzo 24",
    "202404_PGY": "Abril 24",
    "202405_PGY": "Mayo 24",
    "202406_PGY": "Junio 24",
    "202407_PGY": "Julio 24",
    "202408_PGY": "Agosto 24",
    "202409_PGY": "Septiembre 24",
    "202410_PGY": "Octubre 24",
    "202411_PGY": "Noviembre 24",
    "202412_PGY": "Diciembre 24",
    "202501_PGY": "Enero 25",
    "202502_PGY": "Febrero 25",
    
    "idPGY": "Terminal PGY",
    "Provincia": "Provincia",
    "Distrito": "Distrito",
    "categoria": "Categoría",
    "RESPONSABLE DE ZONA (OZ)": "Operador Zonal",
    "TipoAgente": "KASNET",
    
    "202402_Kas": "Febrero 24",
    "202403_Kas": "Marzo 24",
    "202404_Kas": "Abril 24",
    "202405_Kas": "Mayo 24",
    "202406_Kas": "Junio 24",
    "202407_Kas": "Julio 24",
    "202408_Kas": "Agosto 24",
    "202409_Kas": "Septiembre 24",
    "202410_Kas": "Octubre 24",
    "202411_Kas": "Noviembre 24",
    "202412_Kas": "Diciembre 24",
    "202501_Kas": "Enero 25",
    "202502_Kas": "Kasnet Actual",

    "EstadoPGY":"EstadoPGY",
    "Nro Contómetros":"Contómetros (Unidad)",
    "Estado":"Situación",

    "Departamento": "Departamento",
    "region": "Región",
    "ZONAL": "Nombre del Supervisor",
    "Motivo_Garantía": "Motivo de Garantía",
    "Monto_Garantía": "Monto de Garantía",
    "Alcance_Trx_Kasnet":"Trx Garantía",
    "Status_Garantia":"Status_Garantia",

    
    "202402": "Total Feb 24",
    "202403": "Total Mar 24",
    "202404": "Total Abr 24",
    "202405": "Total May 24",
    "202406": "Total Jun 24",
    "202407": "Total Jul 24",
    "202408": "Total Agt 24",
    "202409": "Total Spt 24",
    "202410": "Total Oct 24",
    "202411": "Total Nov 24",
    "202412": "Total Dic 24",
    "202501": "Total Ene 25",
    "202502": "Total Feb 25"

}

# Obtener la fecha de hoy
hoy = datetime.now()
# Restar un día si es necesario
hoy_menos_uno = hoy - timedelta(days=1)
# Formatear la fecha como texto (puedes ajustar el formato según tus necesidades)
fecha_formateada = hoy_menos_uno.strftime("%d-%m-%Y")
# Concatenar con el texto original
Texto = f"**BUSCADOR DE AGENTES KASNET - ACTUALIZADO AL {fecha_formateada}**"

#Texto = "**BUSCADOR DE AGENTES KASNET**"

# Función para autenticar usuarios
def authenticate_user(ruc, codigo):
    user = users_collection.find_one({"ruc": ruc, "codigo": codigo})
    return user is not None

# Manejar el estado de la sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    # Mostrar la página principal si el usuario está autenticado
    id_codigo = st.text_input(Texto, placeholder="Código", max_chars=6, key='id_codigo')

    if id_codigo.isdigit() and len(id_codigo) < 10:
        result = tiendas_collection.find_one({"id_codigo": id_codigo})
        if result:
            # Dividir los campos en tres grupos
            fields_col1 = [
                "id_codigo","Tienda","categoria","region","ZONA","RESPONSABLE DE ZONA (OZ)","TipoPGY",
                "202402_PGY","202403_PGY","202404_PGY","202405_PGY","202406_PGY","202407_PGY",
                "202408_PGY","202409_PGY","202410_PGY","202411_PGY","202412_PGY","202501_PGY","202502_PGY"
            ]
            fields_col2 = [
                "idPGY","EstadoPGY","coordinador", "ZONAL","TipoAgente",
                "202402_Kas","202403_Kas","202404_Kas","202405_Kas","202406_Kas",
                "202407_Kas","202408_Kas","202409_Kas","202410_Kas","202411_Kas","202412_Kas","202501_Kas","202502_Kas"
            ]
            fields_col3 = [
                "Departamento", "Provincia", "Distrito", "Motivo_Garantía", "Monto_Garantía","Nro Contómetros","Estado",
                "Alcance_Trx_Kasnet","Status_Garantia","202402","202403","202404","202405","202406","202407","202408",
                "202409","202410","202411","202412","202501","202502"
            ]


            col1, col2, col3 = st.columns(3)

            # Mostrar los campos en columnas con nombres renombrados
            for col, fields in zip([col1, col2, col3], [fields_col1, fields_col2, fields_col3]):
                with col:
                    for field in fields:
                        display_name = field_names.get(field, field)
                        value = result.get(field, "N/A")
                        st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {value}</div>", unsafe_allow_html=True)
        else:
            st.error("No se encontró ninguna tienda con el código proporcionado")
    elif id_codigo:
        if not id_codigo.isdigit():
            st.error("El código debe ser numérico")
        elif len(id_codigo) != 6 and len(id_codigo) != 9 :
            st.error("El código debe tener exactamente 6 o 9 dígitos")
else:
    # Mostrar formulario de login si el usuario no ha iniciado sesión
    st.markdown("<h2 style='text-align: center;'>Inicio de Sesión</h2>", unsafe_allow_html=True)

    ruc = st.text_input("",placeholder="Ingrese su usuario", max_chars=10)
    codigo = st.text_input("",placeholder="Ingrese su contraseña", max_chars=12, type="password")

    if st.button("Acceder y Confirmar"):
        if ruc.isdigit() and codigo.isdigit() and len(ruc) == 2 and len(codigo) == 3:
            if authenticate_user(ruc, codigo):
                st.session_state.logged_in = True
                st.success("¡Conexión exitosa! Por seguridad, presione nuevamente el botón 'Acceder y Confirmar'")
                # No usar st.experimental_rerun() aquí
            else:
                st.error("RUC o código incorrectos")
        else:
            st.error("Ingrese un RUC y código válidos")
