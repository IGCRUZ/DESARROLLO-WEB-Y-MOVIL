import os
from fastapi import FastAPI
import httpx

app = FastAPI(title="Local API Gateway - Biblioteca")

BACKEND_URL = "http://localhost:9000"

INTERNAL_GATEWAY_SECRET = os.getenv("INTERNAL_GATEWAY_SECRET")

if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError("INTERNAL_GATEWAY_SECRET no esta configurado")


@app.get("/api/libros")
async def libros():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/libros",
            headers={
                "X-Gateway-Secret": INTERNAL_GATEWAY_SECRET,
                "X-Authenticated-Client": "Gateway"
            }
        )

    return response.json()


@app.get("/api/prestamos")
async def prestamos():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/prestamos",
            headers={
                "X-Gateway-Secret": INTERNAL_GATEWAY_SECRET,
                "X-Authenticated-Client": "Gateway"
            }
        )

    return response.json()