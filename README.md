# QR Generator — WhatsApp Click-to-Chat para Salón de Belleza

Genera un código QR estilizado listo para imprimir en **posters de 100×100 cm**. Al escanearlo, el cliente abre WhatsApp con un mensaje prellenado que le permite pre-seleccionar su servicio de interés y lleva un código de campaña para atribución de origen.

## Cómo funciona

El QR codifica una URL `wa.me` con un mensaje de pre-clasificación:

```
Hola 👋 quiero agendar una cita. Servicio de interés: manicure / pedicure / corte / tinte / otro (deja solo el que quieras). ref:vitrina2025
```

El cliente simplemente elimina las opciones que no aplican y envía. El salón recibe un mensaje limpio con el servicio de interés y el código de la pieza publicitaria que lo originó.

## Requisitos

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) (gestor de paquetes)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Instalación

```bash
git clone https://github.com/daniel9511/codigo_qr.git
cd codigo_qr
uv sync
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto (ver `.env.example`):

```env
numero_telefonico=573XXXXXXXXXXX
codigo_campana=vitrina2025
```

| Variable | Descripción | Ejemplo |
|---|---|---|
| `numero_telefonico` | Número del salón con código de país, sin `+` ni espacios | `573XXXXXXXXX` |
| `codigo_campana` | Código corto de la pieza publicitaria para atribución | `vitrina2025` |

## Uso

```bash
uv run python src/core/main.py
```

El QR se guarda en `test/qr_code.png`. La consola confirma la URL generada y verifica que el QR sea escaneable:

```
URL: https://wa.me/5731xxxxxxxx?text=Hola%20...

QR generado: .../test/qr_code.png  (3560×3560 px @ 300 DPI)
  QR verificado — URL correcta y escaneable.
```

### Personalizar servicios

Edita la lista `SERVICIOS` al inicio de `src/core/main.py`:

```python
SERVICIOS = [
    "manicure",
    "pedicure",
    "corte",
    "tinte",
    "otro",
]
```

### Personalizar tamaño del logo

La constante `logo_size` en `generated_qr()` controla el tamaño del logo como proporción del QR. El máximo seguro con `ERROR_CORRECT_H` es `0.30`:

```python
logo_size = int(img_qr.size[0] * 0.40)  # 40% del ancho del QR
```

### Cambiar campaña

Solo actualiza `codigo_campana` en `.env` y vuelve a ejecutar. Imprime una pieza distinta por cada punto físico (vitrina, recepción, volante) para saber de dónde viene cada cliente.

## Salida

| Propiedad | Valor |
|---|---|
| Resolución | 3560×3560 px |
| DPI | 300 |
| Tamaño de impresión | ~30 cm × 30 cm a 300 DPI |
| Formato | PNG con metadatos DPI |
| Corrección de error | `ERROR_CORRECT_H` (30% redundancia) |

## Estructura del proyecto

```
codigo_qr/
├── src/
│   ├── assets/
│   │   └── LogoSalon.png       # Logo centrado en el QR
│   └── core/
│       └── main.py             # Toda la lógica
├── test/
│   └── qr_code.png             # Imagen generada
├── .env                        # Variables privadas
├── .env.example                # Plantilla de variables
├── pyproject.toml              # Dependencias (uv)
├── uv.lock                     # Lock file
└── CLAUDE.md                   # Guía para Claude Code
```

## Dependencias

| Paquete | Propósito |
|---|---|
| `qrcode[pil]` | Generación de QR con estilos |
| `pillow` | Renderizado de imagen |
| `python-dotenv` | Carga de variables `.env` |
| `zxing-cpp` | Verificación de escaneabilidad post-generación |

## Licencia

Uso interno — Karina Salón de Belleza.
