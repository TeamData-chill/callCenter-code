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
