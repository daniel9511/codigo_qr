import qrcode
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import os
import urllib.parse
from dotenv import load_dotenv

def generated_qr(telefono_salon,mensaje):

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
    
    img_qr.save(f"test/qr_code.png")




def main ():

    load_dotenv()
    telefono_salon = os.getenv("numero_telefonico")
    mensaje = f"¡Hola! Soy un cliente interesado en tus servicios. ¿Podrías proporcionarme más información sobre tu salón de belleza?"

    generated_qr(telefono_salon,mensaje)

    print("Bienvenido al generador de códigos QR personalizados")

if __name__ == "__main__":
    main()