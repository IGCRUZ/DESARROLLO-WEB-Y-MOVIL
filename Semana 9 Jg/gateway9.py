import os
import httpx
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI(
    title="Secure Local API Gateway - Biblioteca",
    description="API Gateway con Vault y Auth Service"
)

security = HTTPBearer(auto_error=False)

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "dev-only-token")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:9000")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")

if not VAULT_TOKEN:
    raise RuntimeError("VAULT_TOKEN no configurado")


async def get_gateway_secrets():
    url = f"{VAULT_ADDR}/v1/secret/data/gateway"
    headers = {"X-Vault-Token": VAULT_TOKEN}

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="No fue posible acceder a Vault")

    return response.json()["data"]["data"]


async def authenticate_client(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Bearer token requerido")

    gateway_secrets = await get_gateway_secrets()
    introspection_secret = gateway_secrets.get(
        "auth_introspection_secret",
        "demo-introspection-secret"
    )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{AUTH_SERVICE_URL}/introspect",
                json={"token": credentials.credentials},
                headers={"X-Gateway-Auth-Secret": introspection_secret}
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Authentication Service no disponible"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Error consultando Authentication Service"
        )

    identity = response.json()

    if not identity.get("active", False):
        raise HTTPException(
            status_code=401,
            detail="Token invalido o expirado"
        )

    return {
        "user_id": identity["user_id"],
        "username": identity["username"],
        "roles": identity["roles"],
        "backend_secret": gateway_secrets["backend_shared_secret"]
    }


@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "API Gateway Biblioteca"
    }


@app.api_route(
    "/api/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"]
)
async def proxy(
    path: str,
    request: Request,
    auth=Depends(authenticate_client)
):

    if path == "prestamos" and "admin" not in auth["roles"]:
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para ver los prestamos"
        )

    target_url = f"{BACKEND_URL}/{path}"
    body = await request.body()

    gateway_headers = {
        "X-Gateway-Secret": auth["backend_secret"],
        "X-Authenticated-Client": auth["user_id"],
        "X-Authenticated-User": auth["username"],
        "X-Authenticated-Roles": ",".join(auth["roles"])
    }

    content_type = request.headers.get("content-type")
    if content_type:
        gateway_headers["content-type"] = content_type

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.request(
                method=request.method,
                url=target_url,
                params=request.query_params,
                content=body,
                headers=gateway_headers
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=502,
            detail="Backend no disponible"
        )

    response_headers = {}
    if "content-type" in upstream.headers:
        response_headers["content-type"] = upstream.headers["content-type"]

    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers=response_headers
    )
    
