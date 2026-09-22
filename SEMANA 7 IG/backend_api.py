import os
import secrets
from fastapi import FastAPI, Header, HTTPException, Depends

app = FastAPI(
    title="Backend API - Automotora",
    description="API protegida que solo acepta llamadas del Gateway"
)

# Lectura de la contraseña configurada en la consola
INTERNAL_GATEWAY_SECRET = os.getenv("INTERNAL_GATEWAY_SECRET")

if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError("INTERNAL_GATEWAY_SECRET no esta configurado")

# Candado de seguridad (Paso 6)
def verify_gateway(x_gateway_secret: str = Header(default="")):
    valid = secrets.compare_digest(x_gateway_secret, INTERNAL_GATEWAY_SECRET)
    if not valid:
        raise HTTPException(status_code=403, detail="Solicitud no autorizada desde Gateway")

@app.get("/health")
def health():
    return {"status": "OK"}

# Endpoint de vehículos protegido
@app.get("/vehiculos", dependencies=[Depends(verify_gateway)])
def vehiculos(x_authenticated_client: str | None = Header(default=None)):
    return {
        "authenticated_client": x_authenticated_client,
        "vehiculos": [
            {"id": 1, "marca": "Ford", "modelo": "Territory", "precio": 24990000},
            {"id": 2, "marca": "Toyota", "modelo": "RAV4", "precio": 22500000}
        ]
    }

# Endpoint de reservas protegido
@app.get("/reservas", dependencies=[Depends(verify_gateway)])
def reservas(x_authenticated_client: str | None = Header(default=None)):
    return {
        "authenticated_client": x_authenticated_client,
        "reservas": [
            {"id": 1001, "estado": "pagada"},
            {"id": 1002, "estado": "pendiente"}
        ]
    }