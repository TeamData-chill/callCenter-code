#pip install streamlit pymongo
#python.exe -m pip install --upgrade pip
#pip install streamlit pymongo
#cd \Globokas\ScoringPython
#cd \Red Comercial\AutomatizaciónTrx\Procesos Plantillas\PythonProcesos\Web_Streamlit_Python_Mongo

import streamlit as st
from pymongo import MongoClient, errors
from datetime import datetime, timedelta

# Conectar a MongoDB
try:
    client = MongoClient("mongodb+srv://mhuaman:0AcY7h5YMFqWCvRS@innova.gfmnmzd.mongodb.net/?retryWrites=true&w=majority&appName=Innova")
    db = client["mhuaman"]
    users_collection = db["usuarios"]  # Colección que contiene RUC y códigos
    tiendas_collection = db["tb_tiendas"]
except errors.ConnectionError:
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
    "idCodigo": "Id agente",
    "Tienda": "Comercio",
    "Coordinador": "Coordinador",
    "Zona": "Zona",
    "TipoPGY": "PAGAYA",

    "trxPGYDic": "Diciembre 23",
    "trxPGYEne": "Enero 24",
    "trxPGYFeb": "Febrero 24",
    "trxPGYMar": "Marzo 24",
    "trxPGYAbr": "Abril 24",
    "trxPGYMay": "Mayo 24",
    "trxPGYJun": "Junio 24",
    "trxPGYJul": "Julio 24",
    "trxPGYAgt": "Agosto 24",
    "trxPGYSept": "Septiembre 24",
    "trxPGYOct": "Octubre 24",
    "trxPGYNov": "Noviembre 24",
    "trxPGYActual": "PGY Actual",
    
    "idPGY": "Terminal PGY",
    "Provincia": "Provincia",
    "Distrito": "Distrito",
    "Categoría": "Categoría",
    "Operador Zonal": "Operador Zonal",
    "Tipo_Agente": "KASNET",
    
    "Dic_23_Kas": "Diciembre 23",
    "Ene_24_Kas": "Enero 24",
    "Feb_24_Kas": "Febrero 24",
    "Mar_24_Kas": "Marzo 24",
    "Abr_24_Kas": "Abril 24",
    "May_24_Kas": "Mayo 24",
    "Jun_24_Kas": "Junio 24",
    "Jul_24_Kas": "Julio 24",
    "Agt_24_Kas": "Agosto 24",
    "Sept_24_Kas": "Septiembre 24",
    "Oct_24_Kas": "Octubre 24",
    "Nov_24_Kas": "Noviembre 24",
    "KasActual": "Kasnet Actual",

    "EstadoPGY":"EstadoPGY",
    "Nro Contómetros":"Contómetros (Unidad)",
    "Estado":"Situación",

    "Departamento": "Departamento",
    "Región": "Región",
    "Supervisor": "Nombre del Supervisor",
    "Motivo_Garantía": "Motivo de Garantía",
    "Monto_Garantía": "Monto de Garantía",
    "Alcance_Trx_Kasnet":"Trx Garantía",
    "Status_Garantia":"Status_Garantia",

    "Dic_23": "Total Dic 23",
    "En_24": "Total Ene 24",
    "Feb_24": "Total Feb 24",
    "Mar_24": "Total Mar 24",
    "Abr_24": "Total Abr 24",
    "May_24": "Total May 24",
    "Jun_24": "Total Jun 24",
    "Jul_24": "Total Jul 24",
    "Agt_24": "Total Agt 24",
    "Spt_24": "Total Spt 24",
    "Oct_24": "Total Oct 24",
    "nov_24": "Total Nov 24",
    "avanActual": "Total Dic"

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
        result = tiendas_collection.find_one({"idCodigo": id_codigo})
        if result:
            # Dividir los campos en tres grupos
            fields_col1 = [
                "idCodigo", "Tienda", "Categoría", "Región", "Zona", "Operador Zonal", "TipoPGY",
                "trxPGYDic", "trxPGYEne", "trxPGYFeb", "trxPGYMar", "trxPGYAbr", "trxPGYMay",
                "trxPGYJun", "trxPGYJul",  "trxPGYAgt", "trxPGYSept","trxPGYOct", "trxPGYNov", "trxPGYActual"
            ]
            fields_col2 = [
                "idPGY","EstadoPGY","Coordinador", "Supervisor","Tipo_Agente",
                "Dic_23_Kas", "Ene_24_Kas", "Feb_24_Kas", "Mar_24_Kas", "Abr_24_Kas", "May_24_Kas", 
                "Jun_24_Kas", "Jul_24_Kas", "Agt_24_Kas", "Sept_24_Kas","Oct_24_Kas","Nov_24_Kas","KasActual"
            ]
            fields_col3 = [
                "Departamento", "Provincia", "Distrito", "Motivo_Garantía", "Monto_Garantía","Nro Contómetros","Estado",
                "Alcance_Trx_Kasnet","Status_Garantia","Dic_23","En_24",
                "Feb_24", "Mar_24", "Abr_24", "May_24", "Jun_24", "Jul_24","Agt_24","Spt_24", "Oct_24","nov_24",
                "avanActual"
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

    ruc = st.text_input("",placeholder="Ingrese su RUC", max_chars=2)
    codigo = st.text_input("",placeholder="Ingrese su id de 3 dígitos", max_chars=3, type="password")

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

