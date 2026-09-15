from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from contextlib import asynccontextmanager

# Configuracion de mongodb
MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "biblioteca"
COLL_NAME = "libros"

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

app = FastAPI(title="API Biblioteca", version="1.0.0", lifespan=lifespan)

class LibroIn(BaseModel):
    titulo: str = Field(min_length=1, description="Título del libro")
    autor: str = Field(min_length=1, description="Autor principal")
    precio: float = Field(gt=0, description="Precio > 0")
    tags: List[str] = Field(default_factory=list)
    en_stock: bool = True

class LibroOut(LibroIn):
    id: str

def doc_to_libroout(doc) -> LibroOut:
    return LibroOut(
        id=str(doc["_id"]),
        titulo=doc["titulo"],
        autor=doc["autor"],
        precio=doc["precio"],
        tags=doc.get("tags", []),
        en_stock=doc.get("en_stock", True)
    )

# EndPoints
@app.get("/health", tags=["sistema"])
def health():
    return {"status": "ok"}

@app.get("/libros", response_model=List[LibroOut])
async def listar_libros(
    q: Optional[str] = Query(None, description="Filtro por título que contenga 'q'"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    query = {}
    if q:
        query["titulo"] = {"\(regex": q, "\)options": "i"}
    cursor = coll.find(query).skip(skip).limit(limit)
    libros: list[LibroOut] = []
    async for doc in cursor:
        libros.append(doc_to_libroout(doc))
    return libros

@app.post("/libros", response_model=LibroOut, status_code=201, tags=["libros"])
async def crear_libro(libro: LibroIn):
    res = await coll.insert_one(libro.model_dump())
    doc = await coll.find_one({"_id": res.inserted_id})
    return doc_to_libroout(doc)

@app.get("/libros/{libro_id}", response_model=LibroOut, status_code=201)
async def obtener_libro(libro_id: str):
    if not ObjectId.is_valid(libro_id):
        raise HTTPException(400, "id invalido")
    doc = await coll.find_one({"_id": ObjectId(libro_id)})
    if not doc:
        raise HTTPException(404, "Libro no encontrado")
    return doc_to_libroout(doc)

@app.put("/libros/{libro_id}", response_model=LibroOut)
async def actualizar_libro(libro_id: str, libro: LibroIn):
    if not ObjectId.is_valid(libro_id):
        raise HTTPException(400, "id invalido")
    res = await coll.update_one(
        {"_id": ObjectId(libro_id)},
        {"$set": libro.model_dump()}
    )
    if res.matched_count == 0:
        raise HTTPException(404, "Libro no encontrado")
    doc = await coll.find_one({"_id": ObjectId(libro_id)})
    return doc_to_libroout(doc)

@app.delete("/libros/{libro_id}", status_code=204, tags=["libros"])
async def eliminar_libro(libro_id: str):
    if not ObjectId.is_valid(libro_id):
        raise HTTPException(400, "id invalido")
    res = await coll.delete_one({"_id": ObjectId(libro_id)})
    if res.deleted_count == 0:
        raise HTTPException(404, "Libro no encontrado")
    return None