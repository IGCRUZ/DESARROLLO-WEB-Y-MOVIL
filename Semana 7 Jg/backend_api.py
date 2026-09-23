import os
import secrets
from fastapi import FastAPI, Header, HTTPException, Depends

app = FastAPI(
    title="Backend API - Biblioteca",
    description="API protegida que solo acepta llamadas del Gateway"
)

INTERNAL_GATEWAY_SECRET = os.getenv("INTERNAL_GATEWAY_SECRET")

if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError("INTERNAL_GATEWAY_SECRET no esta configurado")


def verify_gateway(x_gateway_secret: str = Header(default="")):
    valid = secrets.compare_digest(
        x_gateway_secret,
        INTERNAL_GATEWAY_SECRET
    )

    if not valid:
        raise HTTPException(
            status_code=403,
            detail="Solicitud no autorizada desde Gateway"
        )


@app.get("/health")
def health():
    return {"status": "OK"}


@app.get("/libros", dependencies=[Depends(verify_gateway)])
def libros(x_authenticated_client: str | None = Header(default=None)):
    return {
        "authenticated_client": x_authenticated_client,
        "libros": [
            {
                "id": 1,
                "titulo": "Cien años de soledad",
                "autor": "Gabriel García Márquez",
                "precio": 15990
            },
            {
                "id": 2,
                "titulo": "1984",
                "autor": "George Orwell",
                "precio": 12990
            }
        ]
    }


@app.get("/prestamos", dependencies=[Depends(verify_gateway)])
def prestamos(x_authenticated_client: str | None = Header(default=None)):
    return {
        "authenticated_client": x_authenticated_client,
        "prestamos": [
            {
                "id": 1001,
                "estado": "devuelto"
            },
            {
                "id": 1002,
                "estado": "pendiente"
            }
        ]
    }