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

print('session_state',st.session_state)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def authenticate_user(dni):
    user = users_login.find_one({"dni": dni})
    return user is not None

def change_state():
    st.session_state.logged_in = True

text = "**MI SOCIO KASNET**"
dni = st.text_input(text,placeholder="Ingrese su DNI y acredítese", max_chars=8)

field_names = {
    "id_codigo": "Código",
    "estado_kasnet": "Estado",
    "idPGY": "Terminal PGY",
    "Tienda": "Comercio",
    "RUC": "RUC",
    "titular": "Titular",
    "id_codigo": "Ubicación",
    "id_codigo": "Coordenadas",
    "id_codigo": "Región",
    "id_codigo": "Zona",
    "id_codigo": "Supervisor",
    "id_codigo": "OZ",
    "id_codigo": "Saldo inicial Kasnet (S/)",
    "id_codigo": "Recarga Prom. Kasnet (S/):",
    "id_codigo": "Saldo inicial PGY (S/)"
}


if st.session_state.logged_in:
    st.success(f"Bienvenido! Ahora puede realizar consultas")
    id_codigo = st.text_input("", placeholder="Ingrese el código de 6 o 9 dígitos a buscar", max_chars=9, key='id_codigo')

    if id_codigo.isdigit() and len(id_codigo) < 10:
        result = tiendas_collection.find_one({"id_codigo": id_codigo})
        if result:
            
            display_name = 'Código'
            value =  result.get("id_codigo", "N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {value}</div>", unsafe_allow_html=True)
            display_name = 'Estado'
            value =  result.get("estado_kasnet", "N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {value}</div>", unsafe_allow_html=True)
            display_name = 'Terminal PGY'
            value =  result.get("idPGY", "N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {value}</div>", unsafe_allow_html=True)
            display_name = 'Comercio'
            value =  result.get("Tienda", "N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {value}</div>", unsafe_allow_html=True)
            display_name = 'RUC'
            value =  result.get("RUC", "N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {value}</div>", unsafe_allow_html=True)
            display_name = 'Titular'
            value =  result.get("titular", "N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {value}</div>", unsafe_allow_html=True)
            display_name = 'Ubicación'
            departamento =  result.get("Departamento", "N/A")
            provincia =  result.get("Provincia", "N/A")
            distrito =  result.get("Distrito", "N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {departamento} - {provincia} - {distrito}</div>", unsafe_allow_html=True)
            display_name = 'Región'
            region = result.get("region","N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {region}</div>", unsafe_allow_html=True)
            display_name = 'Zona'
            zona = result.get("zona","N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {zona}</div>", unsafe_allow_html=True)
            display_name = 'Supervisor'
            supervisor = result.get("RESPONSABLE","N/A")
            st.markdown(f"<div class='stWrite'><strong>{display_name}:</strong> {display_name}</div>", unsafe_allow_html=True)

        else:
            st.error("No se encontró ninguna tienda con el código proporcionado")
    elif id_codigo:
        if not id_codigo.isdigit():
            st.error("El código debe ser numérico")
        elif len(id_codigo) != 6 and len(id_codigo) != 9 :
            st.error("El código debe tener exactamente 6 o 9 dígitos")
    

else:
    if st.button("Verificar autenticidad de DNI",on_click=change_state):
        if dni.isdigit() and len(dni) == 8:
            if authenticate_user(dni):
                st.session_state.logged_in = True
            else:
                st.error("Ingrese datos")
        else:
            st.error("Solo ingrese números")