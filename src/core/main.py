import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
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

def construir_mensaje(codigo_campana):
    opciones = " / ".join(SERVICIOS)
    return (
        f"Hola 👋 quiero agendar una cita. "
        f"Servicio de interés: {opciones} "
        f"(deja solo el que quieras). "
        f"ref:{codigo_campana}"
    )

def generated_qr(telefono_salon, mensaje):

    text_clean = urllib.parse.quote(mensaje)
    url_whatsapp = f"https://wa.me/{telefono_salon}?text={text_clean}"

    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4,
    )

    qr.add_data(url_whatsapp)
    print(f"{url_whatsapp}")
    qr.make(fit=True)

    # === NUEVO: ruta absoluta al logo ===
    # __file__ = src/qr_generator.py
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # sube de src/ a raiz
    logo_path = os.path.join(base_dir, "assets", "LogoSalon.png")
    print(f"Ruta del logo: {logo_path}\n")

    # Cargar y redimensionar logo (por si es muy grande)
    logo = Image.open(logo_path)
    logo_size = 450  # píxeles (ajusta según veas)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Generar QR básico (blanco/negro o con estilos si quieres)
    img_qr = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(),
        eye_drawer=RoundedModuleDrawer(),
        # opcional: color_mask=SolidFillColorMask(back_color=(255,255,255), front_color=(0,64,255)),
    ).convert("RGBA")

    # Pegar logo en el centro
    pos = (
        (img_qr.size[0] - logo_size) // 2,
        (img_qr.size[1] - logo_size) // 2,
    )
    img_qr.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)
    
    output_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "test", "qr_code.png"
    )
    img_qr.save(output_path)




def main():
    load_dotenv()
    telefono_salon = os.getenv("numero_telefonico")
    codigo_campana = os.getenv("codigo_campana")
    if not telefono_salon or not codigo_campana:
        missing = [v for v, k in [("numero_telefonico", telefono_salon), ("codigo_campana", codigo_campana)] if not k]
        raise ValueError(f"Faltan variables en .env: {', '.join(missing)}")
    mensaje = construir_mensaje(codigo_campana)
    generated_qr(telefono_salon, mensaje)
    print("QR generado en test/qr_code.png")

if __name__ == "__main__":
    main()