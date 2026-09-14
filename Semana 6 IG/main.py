from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from contextlib import asynccontextmanager

# Configuracion de mongodb
MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "automotora"
COLL_NAME = "vehiculos"

client: AsyncIOMotorClient | None = None
db = None
coll = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db, coll
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    coll = db[COLL_NAME]
    yield
    client.close()

app = FastAPI(title="API Automotora", version="1.0.0", lifespan=lifespan)

class VehiculoIn(BaseModel):
    marca: str = Field(min_length=1, description="Marca del vehiculo")
    modelo: str = Field(min_length=1, description="Modelo específico")
    precio: float = Field(gt=0, description="Precio > 0")
    tags: List[str] = Field(default_factory=list)
    disponible: bool = True

class VehiculoOut(VehiculoIn):
    id: str

def doc_to_vehiculoout(doc) -> VehiculoOut:
    return VehiculoOut(
        id=str(doc["_id"]),
        marca=doc["marca"],
        modelo=doc["modelo"],
        precio=doc["precio"],
        tags=doc.get("tags", []),
        disponible=doc.get("disponible", True)
    )

# EndPoints
@app.get("/health", tags=["sistema"])
def health():
    return {"status": "ok"}

@app.get("/vehiculos", response_model=List[VehiculoOut])
async def listar_vehiculos(
    q: Optional[str] = Query(None, description="Filtro por marca que contenga 'q'"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    query = {}
    if q:
        query["marca"] = {"\(regex": q, "\)options": "i"}
    cursor = coll.find(query).skip(skip).limit(limit)
    vehiculos: list[VehiculoOut] = []
    async for doc in cursor:
        vehiculos.append(doc_to_vehiculoout(doc))
    return vehiculos

@app.post("/vehiculos", response_model=VehiculoOut, status_code=201, tags=["vehiculos"])
async def crear_vehiculo(vehiculo: VehiculoIn):
    res = await coll.insert_one(vehiculo.model_dump())
    doc = await coll.find_one({"_id": res.inserted_id})
    return doc_to_vehiculoout(doc)

# Nota: Tu profesor usó status_code=201 para este GET, lo mantenemos igual para que coincida con su pauta.
@app.get("/vehiculos/{vehiculo_id}", response_model=VehiculoOut, status_code=201)
async def obtener_vehiculo(vehiculo_id: str):
    if not ObjectId.is_valid(vehiculo_id):
        raise HTTPException(400, "id invalido")
    doc = await coll.find_one({"_id": ObjectId(vehiculo_id)})
    if not doc:
        raise HTTPException(404, "Vehiculo no encontrado")
    return doc_to_vehiculoout(doc)

@app.put("/vehiculos/{vehiculo_id}", response_model=VehiculoOut)
async def actualizar_vehiculo(vehiculo_id: str, vehiculo: VehiculoIn):
    if not ObjectId.is_valid(vehiculo_id):
        raise HTTPException(400, "id invalido")
    res = await coll.update_one(
        {"_id": ObjectId(vehiculo_id)},
        {"$set": vehiculo.model_dump()}
    )
    if res.matched_count == 0:
        raise HTTPException(404, "Vehiculo no encontrado")
    doc = await coll.find_one({"_id": ObjectId(vehiculo_id)})
    return doc_to_vehiculoout(doc)

@app.delete("/vehiculos/{vehiculo_id}", status_code=204, tags=["vehiculos"])
async def eliminar_vehiculo(vehiculo_id: str):
    if not ObjectId.is_valid(vehiculo_id):
        raise HTTPException(400, "id invalido")
    res = await coll.delete_one({"_id": ObjectId(vehiculo_id)})
    if res.deleted_count == 0:
        raise HTTPException(404, "Vehiculo no encontrado")
    return None