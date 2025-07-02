from fastapi import WebSocket
from typing import List

active_connections: List[WebSocket] = []


async def enviar_debug(message: str):
    # Implemente a sua lógica de envio de WebSocket
    print(f"DEBUG (enviar_debug): {message}")  # Simulação de envio para WebSocket
    # No real: await your_websocket_client.send(message)

async def debug_log(msg: str):
    print(msg)
    await enviar_debug(msg)
async def conectar(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"Nova conexão WebSocket aceita. Total: {len(active_connections)}")

async def desconectar(websocket: WebSocket):
    if websocket in active_connections:
        active_connections.remove(websocket)
        print(f"Conexão WebSocket removida. Total: {len(active_connections)}")

async def enviar_debug(message: str):
    if not active_connections:
        print("Nenhuma conexão WebSocket ativa para enviar debug.")
        return

    to_remove = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Erro ao enviar para conexão: {e}")
            to_remove.append(connection)

    for conn in to_remove:
        await desconectar(conn)
