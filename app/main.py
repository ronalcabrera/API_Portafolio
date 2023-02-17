######################################################################################################################
#                                                       Librerias
######################################################################################################################

# Librerias tratamiento datos
import numpy as np

# Librerias para crear API
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

#Librerias para cargar modelo
import keras
from keras import layers

######################################################################################################################
#                                                       API
######################################################################################################################

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://www.ronalcabrera.github.io"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

@app.get('/', response_class=HTMLResponse)
async def mensaje():
        return 'API predicciones'

@app.get('/prediccion_denso({tensor4})',)
async def prediccion_denso(tensor4):
        # Recreo el modelo
        modelo_denso = keras.experimental.load_from_saved_model(
        'https://github.com/ronalcabrera/ronalcabrera.github.io/blob/main/Modelos/exportacion/modelo_denso/model.json')

        return modelo_denso.predict(tensor4)