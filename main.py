from fastapi import FastAPI 
app = FastAPI()
@app.get('/clientes')
def ola_mundo():
    return {'mensagem': 'Minha primeira API em FastAPI!'}

@app.get('/sobre')
def sabe_muito():
    return {'mensagem': 'Minha primeira API em FastAPI!'}