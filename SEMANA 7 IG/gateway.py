from fastapi import FastAPI
import httpx

app = FastAPI(title="Local API Gateway - Automotora")

BACKEND_URL = "http://localhost:9000"

@app.get("/api/vehiculos")
async def vehiculos():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/vehiculos")
    return response.json()

@app.get("/api/reservas")
async def reservas():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/reservas")
    return response.json()