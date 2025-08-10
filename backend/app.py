from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Body

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime

from typing import Optional, List
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session, select, func

from ltamp import LtAmp, LtAmpAsync
import json

import asyncio

# database/api config

app = FastAPI(title="Twist API")

DATABASE_URL = "sqlite:///twist.db"
engine = create_engine(DATABASE_URL, echo=False)

# websocket stuff

class WsConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for conn in self.active_connections:
            await conn.send_text(message)

manager = WsConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# device status

class DeviceStore:
    def __init__(self):
        self.status: str = "offline"
        self.connections: List[WebSocket] = []
        self.details: dict = {}
        self.heartbeat_task = None
        self.amp: Optional[LtAmp] = None
        self.product_name: str = ''
        self.current_preset: dict = {}
        self.audition_status: str = ''
        self.firmware_version: str = ''
        self.memory_usage: dict = {}
        self.presets: List[dict] = []
        self.processor_usage: dict = {}

    async def broadcast(self):
        message = {
            "type": "status_update",
            "status": self.status,
            "details": self.details,
            "product_name": self.product_name,
            "current_preset": self.current_preset,
            "audition_status": self.audition_status,
            "firmware_version": self.firmware_version,
            "memory_usage": self.memory_usage,
            "processor_usage": self.processor_usage,
            "presets": self.presets,
        }
        for ws in self.connections.copy():
            try:
                await ws.send_json(message)
            except Exception:
                self.connections.remove(ws)

    async def set_status(self, status, details=None):
        self.status = status
        if details is not None:
            self.details = details
        await self.broadcast()

    
    async def load_presets(self):
        preset_idx = 1
        preset = True
        presets = []
        while preset and preset_idx <= 80:
            preset = self.amp.retrieve_preset(preset_idx)
            if preset and "data" in preset and preset["index"] == preset_idx:
                presets.append({"name": json.loads(preset["data"])["info"]["displayName"], "index": preset["index"]})
            preset_idx += 1
        device_store.presets = presets

    async def update_data(self):
        if self.amp:
            try:
                self.product_name =  await asyncio.to_thread(self.amp.request_product_id)
                self.current_preset =  await asyncio.to_thread(self.amp.request_current_preset)
                self.audition_status = await asyncio.to_thread(self.amp.request_audition_state)
                self.memory_usage = await asyncio.to_thread(self.amp.request_memory_usage)
                self.processor_usage = await asyncio.to_thread(self.amp.request_processor_utilization)
                self.firmware_version = await asyncio.to_thread(self.amp.request_firmware_version)
                await self.broadcast()
                await self.set_status("online")
            except Exception as e:
                await self.set_status("warning", {"error": str(e)})
device_store = DeviceStore()

# api config

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

## device api (mainly websockets)

async def heartbeat_loop():
    asyncio.create_task(device_store.load_presets())
    while device_store.status == "online":
        try:
            if device_store.amp:
                await asyncio.to_thread(device_store.amp.send_heartbeat)
                product = await asyncio.to_thread(device_store.amp.request_product_id)
                preset = await asyncio.to_thread(device_store.amp.request_current_preset)
                fw = await asyncio.to_thread(device_store.amp.request_firmware_version)
                audition = await asyncio.to_thread(device_store.amp.request_audition_state)
                memory = await asyncio.to_thread(device_store.amp.request_memory_usage)
                proc = await asyncio.to_thread(device_store.amp.request_processor_utilization)

                device_store.product_name = product
                device_store.current_preset = preset
                device_store.audition_status = audition
                device_store.firmware_version = fw
                device_store.memory_usage = memory
                device_store.processor_usage = proc
                await device_store.broadcast()
            await asyncio.sleep(0.8)
        except Exception as e:
            await device_store.set_status("warning", {"error": str(e)})
            await device_store.broadcast()
    device_store.status = "offline"
    await device_store.update_data()


async def handle_ws_action(msg):
    action = msg.get("action")
    if action == "connect":
        if device_store.status in ("connecting", "syncing", "online"):
            await device_store.set_status("warning", {"error": "Already connecting or connected."})
        else:
            await device_store.set_status("connecting")
            try:
                device_store.amp = LtAmp()
                device_store.amp.connect()
                await device_store.set_status("syncing")
                device_store.amp.send_sync_begin()
                await asyncio.sleep(1)
                device_store.amp.send_sync_end()
                await device_store.set_status("online")
                if device_store.heartbeat_task is not None:
                    device_store.heartbeat_task.cancel()
                device_store.heartbeat_task = asyncio.create_task(heartbeat_loop())

                await device_store.update_data()
            except Exception as e:
                await device_store.set_status("offline", {"error": str(e)})
    elif action == "disconnect":
        if device_store.status not in ("connecting", "syncing", "online"):
            await device_store.set_status("warning", {"error": "Not connected."})
        else:
            try:
                if device_store.heartbeat_task is not None:
                    device_store.heartbeat_task.cancel()
                    device_store.heartbeat_task = None
                if device_store.amp:
                    await asyncio.to_thread(device_store.amp.disconnect)
                    device_store.amp = None
                await device_store.set_status("offline")
            except Exception as e:
                await device_store.set_status("warning", {"error": str(e)})
    elif action == "set_preset":
        idx = msg.get("index")
        if device_store.status != "online" or idx is None:
            await device_store.set_status("warning", {"error": "Device not online or missing index."})
        else:
            try:
                await asyncio.to_thread(device_store.amp.set_preset, idx)
                await device_store.update_data()
            except Exception as e:
                await device_store.set_status("warning", {"error": str(e)})
    elif action == "audition_preset":
        preset = msg.get("preset")
        if device_store.status != "online" or preset is None:
            await device_store.set_status("warning", {"error": "Device not online or missing preset data."})
        else:
            try:
                await asyncio.to_thread(device_store.amp.audition_preset, preset)
                await device_store.update_data()
            except Exception as e:
                await device_store.set_status("warning", {"error": str(e)})
    elif action == "refresh_status":
        if device_store.status != "online":
            await device_store.set_status("warning", {"error": "Device not online."})
        else:
            await device_store.update_data()
    elif action == "reconnect":
        if device_store.heartbeat_task is not None:
            device_store.heartbeat_task.cancel()
            device_store.heartbeat_task = None
        if device_store.amp:
            await asyncio.to_thread(device_store.amp.disconnect)
            device_store.amp = None
        await device_store.set_status("offline")
        await handle_ws_action({"action": "connect"})
    else:
        await device_store.set_status("warning", {"error": f"Unknown action: {action}"})


@app.websocket("/ws/device")
async def ws_device(websocket: WebSocket):
    await websocket.accept()
    device_store.connections.append(websocket)
    await device_store.broadcast()
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
                await handle_ws_action(msg)
            except Exception as e:
                await websocket.send_json({"type": "error", "error": str(e)})
    except WebSocketDisconnect:
        if websocket in device_store.connections:
            device_store.connections.remove(websocket)

@app.get("/device/status")
async def get_status():
    return {"status": device_store.status, "details": device_store.details}

## playlist api 

class PlaylistBase(SQLModel):
    name: str
    description: Optional[str] = None

class Playlist(PlaylistBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_updated: Optional[datetime] = Field(default_factory=datetime.utcnow)

class PlaylistItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  
    playlist_id: int = Field(foreign_key="playlist.id")
    preset_number: int  # 1-60
    note: Optional[str] = None
    position: int

class PlaylistOut(PlaylistBase):
    id: int
    size: int
    last_updated: datetime

    class Config:
        orm_mode = True

def get_playlist_size(session: Session, playlist_id: int) -> int:
    return session.exec(
        select(func.count()).where(PlaylistItem.playlist_id == playlist_id)
    ).one()

@app.post("/playlists/", response_model=PlaylistOut)
def create_playlist(playlist: PlaylistBase):
    with Session(engine) as session:
        db_playlist = Playlist(**playlist.dict(), last_updated=datetime.utcnow())
        session.add(db_playlist)
        session.commit()
        session.refresh(db_playlist)
        size = 0
        return PlaylistOut(
            id=db_playlist.id,
            name=db_playlist.name,
            description=db_playlist.description,
            last_updated=db_playlist.last_updated,
            size=size,
        )

@app.get("/playlists/", response_model=List[PlaylistOut])
def list_playlists():
    with Session(engine) as session:
        playlists = session.exec(select(Playlist)).all()
        result = []
        for pl in playlists:
            size = get_playlist_size(session, pl.id)
            result.append(
                PlaylistOut(
                    id=pl.id,
                    name=pl.name,
                    description=pl.description,
                    last_updated=pl.last_updated,
                    size=size,
                )
            )
        return result

@app.get("/playlists/{playlist_id}", response_model=dict)
def get_playlist(playlist_id: int):
    with Session(engine) as session:
        pl = session.get(Playlist, playlist_id)
        if not pl:
            raise HTTPException(status_code=404, detail="Playlist not found")
        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id)
        ).all()
        return {
            "id": pl.id,
            "name": pl.name,
            "description": pl.description,
            "last_updated": pl.last_updated,
            "size": len(items),
            "items": [item.preset_number for item in items],
        }

@app.post("/playlists/{playlist_id}/items/", response_model=List[PlaylistItem])
def add_items(playlist_id: int, preset_numbers: List[int], notes: List[str]):
    print(playlist_id)
    for n in preset_numbers:
        if not (1 <= n <= 60):
            raise HTTPException(status_code=400, detail="Preset numbers must be between 1 and 60")
    with Session(engine) as session:
        playlist = session.get(Playlist, playlist_id)
        print(playlist, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        items = []
        for number in range(len(preset_numbers)):
            max_position = session.exec(
                select(func.max(PlaylistItem.position)).where(PlaylistItem.playlist_id == playlist_id)
            ).one()
            if max_position is None:
                max_position = 0

            item = PlaylistItem(playlist_id=playlist_id, preset_number=preset_numbers[number], note=notes[number], position=max_position + 1)
            session.add(item)
            items.append(item)
        playlist.last_updated = datetime.utcnow()
        session.add(playlist)
        session.commit()
        for item in items:
            session.refresh(item)
        return items

@app.post("/playlists/{playlist_id}/items/insert", response_model=List[PlaylistItem])
def insert_item(playlist_id: int, preset_number: int = Body(...), position: int = Body(...)):
    if not (1 <= preset_number <= 60):
        raise HTTPException(status_code=400, detail="Preset number must be between 1 and 60")
    with Session(engine) as session:
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id).order_by(PlaylistItem.position)
        ).all()

        for item in items:
            if item.position >= position:
                item.position += 1
                session.add(item)

        new_item = PlaylistItem(playlist_id=playlist_id, preset_number=preset_number, position=position)
        session.add(new_item)
        playlist.last_updated = datetime.utcnow()
        session.add(playlist)
        session.commit()

        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id).order_by(PlaylistItem.position)
        ).all()
        return items

@app.delete("/playlists/{playlist_id}/items/{item_id}", response_model=dict)
def delete_item(playlist_id: int, item_id: int):
    with Session(engine) as session:
        item = session.get(PlaylistItem, item_id)
        if not item or item.playlist_id != playlist_id:
            raise HTTPException(status_code=404, detail="Playlist item not found")
        position = item.position
        session.delete(item)
 
        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id)
        ).all()
        for i in items:
            if i.position > position:
                i.position -= 1
                session.add(i)
        playlist = session.get(Playlist, playlist_id)
        playlist.last_updated = datetime.utcnow()
        session.add(playlist)
        session.commit()
        return {"ok": True}

@app.patch("/playlists/{playlist_id}/items/{item_id}/move", response_model=List[PlaylistItem])
def move_item(playlist_id: int, item_id: int, new_position: int = Body(...)):
    with Session(engine) as session:
        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id).order_by(PlaylistItem.position)
        ).all()
        item = session.get(PlaylistItem, item_id)
        if not item or item.playlist_id != playlist_id:
            raise HTTPException(status_code=404, detail="Playlist item not found")
        old_position = item.position
        if new_position < 0 or new_position >= len(items):
            raise HTTPException(status_code=400, detail="Invalid new position")

        items.remove(item)

        items.insert(new_position, item)

        for idx, itm in enumerate(items):
            itm.position = idx
            session.add(itm)
        playlist = session.get(Playlist, playlist_id)
        playlist.last_updated = datetime.utcnow()
        session.add(playlist)
        session.commit()

        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id).order_by(PlaylistItem.position)
        ).all()
        return items

@app.patch("/playlists/{playlist_id}", response_model=PlaylistOut)
def update_playlist(
    playlist_id: int,
    name: Optional[str] = Body(None), 
    description: Optional[str] = Body(None)
):
    with Session(engine) as session:
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        if name is not None:
            playlist.name = name
        if description is not None:
            playlist.description = description
        playlist.last_updated = datetime.utcnow()
        session.add(playlist)
        session.commit()
        session.refresh(playlist)
        size = get_playlist_size(session, playlist_id)
        return PlaylistOut(
            id=playlist.id,
            name=playlist.name,
            description=playlist.description,
            last_updated=playlist.last_updated,
            size=size,
        )

@app.get("/playlists/{playlist_id}/items", response_model=List[PlaylistItem])
def list_items(playlist_id: int):
    with Session(engine) as session:
        playlist = session.get(Playlist, playlist_id)
        print(playlist)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id).order_by(PlaylistItem.position)
        ).all()
        return items

@app.delete("/playlists/{playlist_id}")
def delete_playlist(playlist_id: int):
    with Session(engine) as session:
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id)
        ).all()
        for item in items:
            session.delete(item)
        session.delete(playlist)
        session.commit()
        return {"ok": True}

@app.get("/")
def index():
    return FileResponse("../frontend/dist/index.html")

@app.get("/api/version")
def get_version():
    with open("VERSION") as f:
        return {"version": f.read().strip()}

app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")
