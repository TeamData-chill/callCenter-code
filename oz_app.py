import streamlit as st
from pymongo import MongoClient, errors
from datetime import datetime, timedelta

# Conectar a MongoDB
try:
    client = MongoClient("mongodb+srv://datayanalitica:hDeF35XYwRgMgrT4@searchengine.qcnlr.mongodb.net/?retryWrites=true&w=majority&appName=SearchEngine")
    db = client["search_engine"]
    tiendas_collection = db["oz_search"]
    users_login = db["users_login"]
except errors.ConnectionError:
    st.error("No se pudo conectar a MongoDB. Verifique la URL y las credenciales.")
    st.stop()

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



def authenticate_user(dni):
    user = users_login.find_one({"dni": dni})
    return user is not None

def change_state():
    st.session_state.logged_in = True

hoy = datetime.now()
fecha_ayer =  (hoy - timedelta(days=1)).strftime("%d-%m-%Y")
text = "**MI SOCIO KASNET**"



print('session_state',st.session_state)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.success(f"Bienvenido! Ahora puede realizar consultas")
    id_codigo = st.text_input("", placeholder="Ingrese el código de 6 o 9 dígitos a buscar", max_chars=9, key='id_codigo')

    if id_codigo.isdigit() and len(id_codigo) < 10:
        result = tiendas_collection.find_one({"id_codigo": id_codigo})

        if result:
            concatenations = {

                "Código": f"{result.get('id_codigo', 'N/A')} - {result.get('TipoAgente', 'N/A')} - {result.get('categoria', 'N/A')}",
                "Estado": f"{result.get('estado_kasnet', 'N/A')} - {result.get('FechaInstalacion', 'N/A')}",
                "Terminal PGY": f"{result.get('idPGY', 'N/A')}  - {result.get('EstadoPGY', 'N/A')}",
                "Comercio": f"{result.get('Tienda', 'N/A')}",
                "RUC": result.get('RUC', 'N/A'),
                "Titular": result.get('titular', 'N/A'),
                "Ubicación": f"{result.get('Departamento', 'N/A')} - {result.get('Provincia', 'N/A')} - {result.get('Distrito', 'N/A')}",
                "Coordenadas": f'<a href="https://www.google.com/maps/search/?api=1&query={result.get("Latitude", "N/A")},{result.get("Longitude", "N/A")}" target="_blank">Ver en Google Maps</a>',
                "Región": result.get('region', 'N/A'),
                "Zona": result.get('ZONA', 'N/A'),
                "Supervisor": result.get('ZONAL', 'N/A'),
                "OZ": result.get('RESPONSABLE DE ZONA (OZ)', 'N/A'),
                "Saldo inicial Kasnet (S/)": result.get('Saldo_kasnet', 'N/A'),
                "Recarga Prom. Kasnet (S/)": result.get('Recarga promedio kas', 'N/A'),
                "Saldo inicial PGY (S/)": result.get('saldosPGY', 'N/A'),

                "----------------------------------------------------<br>"
                "Trx Dic": f"PGY:{result.get('202412_PGY', 'N/A')}  Kas:{result.get('202412_Kas', 'N/A')}  Total:{result.get('202412', 'N/A')}",
                "Trx Ene": f"PGY:{result.get('202501_PGY', 'N/A')}  Kas:{result.get('202501_Kas', 'N/A')}  Total:{result.get('202501', 'N/A')}",
                "Trx Feb": f"PGY:{result.get('202502_PGY', 'N/A')}  Kas:{result.get('202502_Kas', 'N/A')}  Total:{result.get('202502', 'N/A')}",
                
                f"----------------------------------------------------<br>Trx PGY Regular {fecha_ayer}": result.get('202502_PGY_sin_inter', 'N/A'),
                f"Trx PGY Interoperabilidad {fecha_ayer}": result.get('202502_PGY_inter', 'N/A'),
                f"Total {fecha_ayer}": f"{result.get('202502_PGY', 'N/A')}",

                f"----------------------------------------------------<br>Trx Banco Nación ({fecha_ayer})": f" ({result.get('ESTADO_BN', 'N/A')}) {fecha_ayer}: {result.get('ACTUAL_Kas_BN', 'N/A')}",

                f"Trx Kasnet Regular {fecha_ayer}": f"{result.get('ACTUAL_Kas_sin_BN', 'N/A')}",
                f"Total Kasnet {fecha_ayer}": f"{result.get('202502_Kas', 'N/A')}",
                
                # f"----------------------------------------------------<br>Compartivo diario / Ene vs Feb<br>Avance {fecha_ayer}": result.get('Avance_antes', 'N/A'),
                f"----------------------------------------------------<br>Compartivo diario / Ene vs Feb<br>"
                f"Avance {fecha_ayer}": result.get('202502', 'N/A'),
                "Proyectado Feb": result.get('Proyeccion', 'N/A'),
                f"Variación Ene vs Feb": f"{result.get('Diferencia_Ultimos_Meses', 'N/A')}%",
                "¿Visitó en el mes?": result.get('¿Visitó_Mes_Actual?', 'N/A'),

                "----------------------------------------------------<br>"
                "CAMPAÑA FEBRERO": result.get('CAMPAÑA_FEBRERO', 'N/A'),
            }

            for key, value in concatenations.items():
                st.markdown(f"<div class='stWrite'><strong>{key}:</strong> <b>{value}</b></div>", unsafe_allow_html=True)

        else:
            st.error("No se encontró ninguna tienda con el código proporcionado")
    elif id_codigo:
        if not id_codigo.isdigit():
            st.error("El código debe ser numérico")
        elif len(id_codigo) != 6 and len(id_codigo) != 9 :
            st.error("El código debe tener exactamente 6 o 9 dígitos")
else:
    dni = st.text_input(text,placeholder="Ingrese su DNI y acredítese", max_chars=8)
    if st.button("Verificar autenticidad de DNI",on_click=change_state):
        if dni.isdigit() and len(dni) == 8:
            if authenticate_user(dni):
                st.session_state.logged_in = True
            else:
                st.error("Ingrese datos")
        else:
            st.error("Solo ingrese números")