from fastapi import WebSocket, WebSocketDisconnect
from .database import get_session
from .crud import get_item, create_item, update_item
from .schemas import ItemCreate
import json

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for session in get_session():
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)

                action = message.get("action")
                payload = message.get("payload")

                if action == "get":
                    item = await get_item(session, payload["id"])
                    await websocket.send_json({"result": item.__dict__ if item else None})

                elif action == "create":
                    item_in = ItemCreate(**payload)
                    item = await create_item(session, item_in)
                    await websocket.send_json({"result": item.__dict__})

                elif action == "update":
                    item_in = ItemCreate(**payload)
                    item = await update_item(session, payload["id"], item_in)
                    await websocket.send_json({"result": item.__dict__ if item else None})

        except WebSocketDisconnect:
            print("Cliente desconectado")
            break
