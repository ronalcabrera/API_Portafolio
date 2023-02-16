from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from modelos import denso,CNN,CNN_AD_DO

app = FastAPI()

@app.get('/', response_class = HTMLResponse)
async def mensaje():
        return 'Api para consumir mis modelos'

@app.get('/denso')
async def mensaje():
        return denso

@app.get('/CNN')
async def mensaje():
        return CNN

@app.get('/CNN_AD_DO')
async def mensaje():
        return CNN_AD_DO

