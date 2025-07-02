from fastapi import FastAPI, Depends, Query
from .database import engine, get_session
from .models import Base
from .schemas import LogCreate
from .crud import insert_log
from .monitor import debug_log
from .simulador import validar_permissao, gerar_folha
from .websocket_handler import websocket_endpoint
from enum import Enum

app = FastAPI()

# Enum para tipos de folha
class TipoFolha(str, Enum):
    SOB = "SOB"
    REF = "REF"

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/processar")
async def processar_log(log: LogCreate, session=Depends(get_session)):
    inserted_log = await insert_log(session, log)
    return {"status": "OK", "log_id": inserted_log.id}

@app.get("/simular")
async def simular_folha(
    mes: str = Query(..., description="Mês"),
    ano: str = Query(..., description="Ano"),
    username: str = Query(..., description="Nome do usuário"),
    tipo_folha: TipoFolha = Query(..., description="Tipo de folha"),
    session=Depends(get_session)
):
    debug_msg = f"Usuário: {username} tenta simular folha {tipo_folha.value} do mês {mes}/{ano}"
    await debug_log(debug_msg)

    permissao_ok, msg = await validar_permissao(session, username, tipo_folha.value)
    if not permissao_ok:
        return {"status": "erro", "mensagem": msg}

    if tipo_folha == TipoFolha.SOB:
        resultado = await gerar_folha(session, username, tipo_folha.value)
        if "erro" in resultado:
            return {"status": "erro", "mensagem": resultado["erro"]}
        return {
            "status": "ok",
            "mensagem": resultado["msg"],
            "beneficiarios": resultado["dados"]
        }

    return {
        "status": "erro",
        "mensagem": "Simulação de Reforma ainda não implementada."
    }

# WebSocket route
app.add_api_websocket_route("/ws", websocket_endpoint)
