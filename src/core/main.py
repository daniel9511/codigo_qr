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

    img_qr = qr.make_image(
        image_factory=StyledPilImage, 
        module_drawer=CircleModuleDrawer(),
        eye_drawer=RoundedModuleDrawer()
        )
    
    img_qr.save(f"test/qr_code.png")




def main ():

    load_dotenv()
    telefono_salon = os.getenv("numero_telefonico")
    mensaje = f"¡Hola! Soy un cliente interesado en tus servicios. ¿Podrías proporcionarme más información sobre tu salón de belleza?"

    generated_qr(telefono_salon,mensaje)

    print("Bienvenido al generador de códigos QR personalizados")

if __name__ == "__main__":
    main()