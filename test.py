import streamlit as st
from pymongo import MongoClient, errors
from datetime import datetime, timedelta

# Conectar a MongoDB
try:
    client = MongoClient("mongodb+srv://datayanalitica:hDeF35XYwRgMgrT4@searchengine.qcnlr.mongodb.net/?retryWrites=true&w=majority&appName=SearchEngine")
    db = client["search_engine"]
    users_collection = db["users"]  # Colección que contiene RUC y códigos
    tiendas_collection = db["oz_search"]
    print("se conectó")
except errors.ConnectionError:
    print("no se conectó")
    st.error("No se pudo conectar a MongoDB. Verifique la URL y las credenciales.")
    st.stop()

for tienda in tiendas_collection.find():
    print(tienda)