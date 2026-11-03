
import stomp
import argparse
import json
from decimal import Decimal, InvalidOperation
import xml.etree.ElementTree as ET

DESTINO = "/queue/videojuegos"

def construir_mensaje(formato: str, videojuego: dict, texto: str) -> tuple[str, str]:
    if formato == "texto":
        return texto, "text/plain; charset=utf-8"
    if formato == "fijo":
        identificador = str(videojuego["id"])
        juego = str(videojuego["juego"])
        precio = Decimal(videojuego["precio"])
        precio_campo = f"{precio:010.2f}"
        if not (identificador.isascii() and identificador.isdigit() and len(identificador) <= 6):
            raise ValueError("En formato fijo, --id debe tener hasta 6 digitos ASCII")
        if len(juego) > 20 or any(ord(c) > 127 for c in juego):
            raise ValueError("En formato fijo, --juego admite hasta 20 caracteres ASCII")
        if precio < 0 or len(precio_campo) != 10:
            raise ValueError("En formato fijo, --precio debe estar entre 0 y 99999999.99")
        return f"{identificador.zfill(6)}{juego:<20}{precio_campo}", "text/plain; charset=utf-8"
    if formato == "json":
        return json.dumps(videojuego, ensure_ascii=False), "application/json; charset=utf-8"
    if formato == "xml":
        raiz = ET.Element("videojuego")
        for clave, valor in videojuego.items():
            ET.SubElement(raiz, clave).text = str(valor)
        return ET.tostring(raiz, encoding="unicode"), "application/xml; charset=utf-8"
    raise ValueError(f"Formato desconocido: {formato}")

def main():
    parser = argparse.ArgumentParser(description="Productor STOMP")
    parser.add_argument("--formato", choices=["texto", "fijo", "xml", "json"], required=True)
    parser.add_argument("--mensaje", default="Nuevo videojuego agregado al inventario")
    parser.add_argument("--id", default="123")
    parser.add_argument("--juego", default="GTA V")
    parser.add_argument("--precio", default="29990.00")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=61613)
    parser.add_argument("--usuario", default="demo")
    parser.add_argument("--clave", default="demo123")
    args = parser.parse_args()

    try:
        precio = Decimal(args.precio)
        if not precio.is_finite():
            raise ValueError("El precio debe ser un número finito")
    except InvalidOperation:
        parser.error(f"Precio no válido: {args.precio}")

    videojuego = {"id": args.id, "juego": args.juego, "precio": str(precio)}
    try:
        cuerpo, mime = construir_mensaje(args.formato, videojuego, args.mensaje)
    except ValueError as exc:
        parser.error(str(exc))

    conexion = stomp.Connection12([(args.host, args.port)], vhost="/")
    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.send(
            destination=DESTINO,
            body=cuerpo,
            headers={
                "content-type": mime,
                "x-formato": args.formato,
                "persistent": "true",
            },
        )
        print(f"Videojuego enviado a {DESTINO} (formato={args.formato}):\n{cuerpo}")
    finally:
        if conexion.is_connected():
            conexion.disconnect()

if __name__ == "__main__":
    main()
