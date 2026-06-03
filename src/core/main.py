import qrcode
import zxingcpp
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, RoundedModuleDrawer
import os
import urllib.parse
from dotenv import load_dotenv

SERVICIOS = [
    "manicure",
    "pedicure",
    "corte",
    "tinte",
    "otro",
]

BOX_SIZE = 40  # pixels per module — yields ~25 cm QR at 300 DPI for a 100×100 cm poster
DPI = 300


def construir_mensaje(codigo_campana):
    opciones = " / ".join(SERVICIOS)
    return (
        f"Hola 👋 quiero agendar una cita. "
        f"Servicio de interés: {opciones} "
        f"(deja solo el que quieras). "
        f"ref:{codigo_campana}"
    )


def verificar_qr(img, url_esperada):
    resultados = zxingcpp.read_barcodes(img.convert("RGB"))
    if not resultados:
        print("  ADVERTENCIA: el QR no es escaneable — el logo puede estar cubriendo demasiado.")
        return
    leida = resultados[0].text
    if leida == url_esperada:
        print("  QR verificado — URL correcta y escaneable.")
    else:
        print(f"  ADVERTENCIA: URL leída no coincide.\n  Esperada: {url_esperada}\n  Leída:    {leida}")


def generated_qr(telefono_salon, mensaje):
    text_clean = urllib.parse.quote(mensaje)
    url_whatsapp = f"https://wa.me/{telefono_salon}?text={text_clean}"
    print(f"URL: {url_whatsapp}\n")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=BOX_SIZE,
        border=4,
    )
    qr.add_data(url_whatsapp)
    qr.make(fit=True)

    img_qr = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(),
        eye_drawer=RoundedModuleDrawer(),
    ).convert("RGBA")

    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(src_dir)
    logo_path = os.path.join(src_dir, "assets", "LogoSalon.png")
    logo = Image.open(logo_path)
    logo_size = int(img_qr.size[0] * 0.40)
    escala = logo_size / max(logo.size)
    logo_w, logo_h = int(logo.size[0] * escala), int(logo.size[1] * escala)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)

    pos = (
        (img_qr.size[0] - logo_w) // 2,
        (img_qr.size[1] - logo_h) // 2,
    )
    img_qr.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

    output_path = os.path.join(base_dir, "test", "qr_code.png")
    img_qr.save(output_path, dpi=(DPI, DPI))
    print(f"QR generado: {output_path}  ({img_qr.size[0]}×{img_qr.size[1]} px @ {DPI} DPI)")

    verificar_qr(img_qr, url_whatsapp)


def main():
    load_dotenv()
    telefono_salon = os.getenv("numero_telefonico")
    codigo_campana = os.getenv("codigo_campana")
    if not telefono_salon or not codigo_campana:
        missing = [k for k, v in [("numero_telefonico", telefono_salon), ("codigo_campana", codigo_campana)] if not v]
        raise ValueError(f"Faltan variables en .env: {', '.join(missing)}")
    mensaje = construir_mensaje(codigo_campana)
    generated_qr(telefono_salon, mensaje)


if __name__ == "__main__":
    main()
