from fastapi import WebSocket, WebSocketDisconnect
from .monitor import conectar, desconectar

async def websocket_endpoint(websocket: WebSocket):
    await conectar(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantém a conexão aberta
    except WebSocketDisconnect:
        await desconectar(websocket)
        print("Cliente WebSocket desconectado")
