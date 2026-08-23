from fastapi import APIRouter,WebSocket,WebSocketDisconnect

router=APIRouter(tags=["WebSocket"])

class ConnectionManager:
    def __init__(self):
        self.connections:list[WebSocket]=[]

    async def connect(self,websocket:WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self,websocket:WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self,message:str):
        for connection in self.connections:
            await connection.send_text(message)

manager=ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message=await websocket.receive_text()
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)