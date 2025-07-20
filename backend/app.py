from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Body

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime

from typing import Optional, List
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, create_engine, Session, select, func

from ltamp import LtAmp, LtAmpAsync

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

    async def broadcast(self):
        message = {
            "type": "status_update",
            "status": self.status,
            "details": self.details,
            "product_name": self.product_name,
            "current_preset": self.current_preset,
            "audition_status": self.audition_status
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

    async def update_data(self):
        if self.amp:
            try:
                self.product_name = self.amp.request_product_id()
                self.current_preset = self.amp.request_current_preset()
                self.audition_status = self.amp.request_audition_state()
                await self.broadcast()
            except Exception as e:
                await self.set_status("warning", {"error": str(e)})

device_store = DeviceStore()

# api config

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

## device api

@app.websocket("/ws/device")
async def ws_device(websocket: WebSocket):
    await websocket.accept()
    device_store.connections.append(websocket)
    await websocket.send_json({
        "type": "status_update",
        "status": device_store.status,
        "details": device_store.details,
    })
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in device_store.connections:
            device_store.connections.remove(websocket)

async def heartbeat_loop():
    prev_product = None
    prev_preset = None
    prev_audition = None
    while device_store.status == "online":
        try:
            if device_store.amp:
                product = device_store.amp.request_product_id()
                preset = device_store.amp.request_current_preset()
                audition = device_store.amp.request_audition_state()
                changed = False
                if product != prev_product:
                    device_store.product_name = product
                    prev_product = product
                    changed = True
                if preset != prev_preset:
                    device_store.current_preset = preset["data"]
                    prev_preset = preset
                    changed = True
                if audition != prev_audition:
                    device_store.audition_status = audition
                    prev_audition = audition
                    changed = True
                if changed:
                    await device_store.broadcast()
            await asyncio.sleep(0.8)
        except Exception as e:
            await device_store.set_status("warning", {"error": str(e)})
            await device_store.broadcast()
            break

@app.post("/device/connect")
async def connect_device():
    if device_store.status in ("connecting", "syncing", "online"):
        raise HTTPException(status_code=400, detail="Device already connecting or connected.")
    await device_store.set_status("connecting")
    try:
        device_store.amp = LtAmp()
        device_store.amp.connect()
        await device_store.set_status("syncing")
        device_store.amp.send_sync_begin()
        asyncio.sleep(2)
        device_store.amp.send_sync_end()
        device_store.update_data()
        await device_store.set_status("online")
        if device_store.heartbeat_task is not None:
            device_store.heartbeat_task.cancel()
        device_store.heartbeat_task = asyncio.create_task(heartbeat_loop())
        return {"ok": True, "status": "online"}
    except Exception as e:
        await device_store.set_status("offline", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to connect: {e}")

@app.post("/device/disconnect")
async def disconnect_device():
    if device_store.status not in ("connecting", "syncing", "online"):
        raise HTTPException(status_code=400, detail="Device not connected.")
    try:
        if device_store.heartbeat_task is not None:
            device_store.heartbeat_task.cancel()
            device_store.heartbeat_task = None
        if device_store.amp:
            await device_store.amp.disconnect()
            device_store.amp = None
        await device_store.set_status("offline")
        return {"ok": True, "status": "offline"}
    except Exception as e:
        await device_store.set_status("warning", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to disconnect: {e}")

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
    id: Optional[int] = Field(default=None, primary_key=True)
    playlist_id: int = Field(foreign_key="playlist.id")
    preset_number: int  # 1-60

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
def add_items(playlist_id: int, preset_numbers: List[int]):
    for n in preset_numbers:
        if not (1 <= n <= 60):
            raise HTTPException(status_code=400, detail="Preset numbers must be between 1 and 60")
    with Session(engine) as session:
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        items = []
        for number in preset_numbers:
            item = PlaylistItem(playlist_id=playlist_id, preset_number=number)
            session.add(item)
            items.append(item)
        playlist.last_updated = datetime.utcnow()
        session.add(playlist)
        session.commit()
        for item in items:
            session.refresh(item)
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

@app.get("/playlists/{playlist_id}/items/", response_model=List[int])
def list_items(playlist_id: int):
    with Session(engine) as session:
        playlist = session.get(Playlist, playlist_id)
        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist not found")
        items = session.exec(
            select(PlaylistItem).where(PlaylistItem.playlist_id == playlist_id)
        ).all()
        return [item.preset_number for item in items]

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
