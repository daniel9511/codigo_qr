# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Generates a styled WhatsApp QR code for the physical advertising of a beauty
salon. The QR encodes a `wa.me` Click-to-Chat URL whose pre-filled message is a
**pre-classifier message** (see below) and is saved as a `.png` image. Styling
uses circular modules and rounded "eyes" via `qrcode[pil]`.

### Why the message matters

A `wa.me` QR can only open WhatsApp on the customer's phone with a pre-filled
message — that text is the only thing we control. So instead of a generic
greeting, the message does double duty: it lets the customer pre-select a service
and it carries a campaign code for future origin attribution. This adds **zero
friction** for the customer (they just tap send, or lightly edit first).

Note: capturing the customer's phone number or analyzing chats automatically is
**out of scope for now** — that will be handled later via YCloud + a bot. This
repo is only the QR generator.

## Setup

This project uses [`uv`](https://docs.astral.sh/uv/) for environment and
dependency management (not `venv`/`pip`).

```bash
# Install uv once (per machine)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install/sync dependencies from pyproject.toml + uv.lock
uv sync
```

To add a new dependency later: `uv add <package>`. This updates `pyproject.toml`
and `uv.lock` automatically. There is no `requirements.txt` and no manual
environment activation — `uv run` handles the environment.

### Environment variables (`.env`)

```
numero_telefonico=<salon phone with country code, e.g. 573144156309>
codigo_campana=<short campaign code, emitted in the QR message as ref:<code>, e.g. vitrina2025>
```

## Run

```bash
uv run python src/core/main.py
```

The QR PNG is written to `test/qr_code.png`.

## Dependencies

| Package | Purpose |
|---|---|
| `qrcode[pil]` | QR generation + styled image factory |
| `pillow` | Image rendering |
| `python-dotenv` | Load `.env` variables |
| `zxing-cpp` | QR decode for post-generation scannability check |

## Architecture

The entire logic lives in `src/core/main.py`:

- `SERVICIOS` — editable list of salon services shown in the pre-classifier
  message.
- `BOX_SIZE` / `DPI` — print resolution constants. Current values target ~25 cm
  QR at 300 DPI, suitable for a 100×100 cm poster.
- `construir_mensaje(codigo_campana)` — builds the pre-classifier message:
  greeting + service options joined by `/` + `ref:<codigo_campana>`.
- `generated_qr(telefono_salon, mensaje)` — URL-encodes the message, builds the
  `wa.me` URL, creates the styled QR (circular modules, rounded eyes,
  `ERROR_CORRECT_H`), embeds the logo at 40% of the QR width (proportional
  resize preserving aspect ratio), saves the PNG with DPI metadata.
- `verificar_qr(img, url_esperada)` — decodes the generated QR with `zxingcpp`
  and confirms the embedded URL matches what was intended. Warns if the logo
  covers too much and breaks scannability.
- `main()` — loads `.env`, reads `numero_telefonico` and `codigo_campana`,
  calls `construir_mensaje`, then `generated_qr`.

The `test/` directory is only an output folder for the generated image, not a
test suite.

## Mejoras futuras

### Funcionalidades nuevas

- **Multi-campaña:** aceptar `codigos_campana=vitrina2025,recepcion2025` (comma-
  separated) en `.env` y generar un PNG por código (`qr_vitrina2025.png`,
  `qr_recepcion2025.png`) en una sola ejecución. Útil cuando el mismo salón
  necesita códigos distintos para vitrina, recepción, volante, etc.

- **Color de marca configurable:** `COLOR_MODULOS` en `.env` para pintar los
  módulos del QR con el color corporativo del salón (e.g. `#A0522D`). Se
  implementa con `SolidFillColorMask` que ya está en el proyecto. Útil para
  que el QR combine con el diseño del poster.

- **CLI con argumentos:** reemplazar el `.env` por argumentos de línea de
  comando (`--telefono`, `--campana`, `--logo`, `--logo-size`). Permite
  generar QRs sin editar archivos, útil para automatización o uso por alguien
  no técnico desde terminal.

- **Logo configurable:** `logo_path` en `.env` en vez de hardcodeado a
  `src/assets/LogoSalon.png`. Permite cambiar el logo sin tocar el código,
  útil si el salón rediseña su logo o si el proyecto se reutiliza para otro
  cliente.

### Calidad e integración

- **Exportación a PDF print-ready:** generar un PDF con marcas de corte y
  sangrado además del PNG, listo para enviar directamente a imprenta. Pillow
  soporta save a PDF; las marcas de corte se pueden dibujar con `ImageDraw`.

- **Preview en miniatura:** generar automáticamente un `qr_preview.png` de
  300×300 px junto al PNG de alta resolución, para verificar visualmente
  cómo queda sin abrir un archivo de ~800 KB.

- **Integración YCloud + bot:** cuando el salón empiece a usar YCloud para
  leer los mensajes entrantes, el `ref:<codigo>` del mensaje permite
  atribuir automáticamente cada nuevo chat a una pieza publicitaria. El bot
  puede leer el código y registrar el origen sin intervención manual.

- **Estadísticas de campaña:** con YCloud activo, cruzar el `ref:` de cada
  chat con la fecha para saber cuántas consultas generó cada pieza (vitrina
  vs. recepción vs. volante) y en qué horarios.

### Deuda técnica menor

- Reemplazar la cadena de `os.path.dirname` por `pathlib.Path(__file__).parents[n]`
  para rutas más legibles y robustas si el proyecto crece.
- Agregar `os.makedirs(exist_ok=True)` antes de `img_qr.save()` como guarda
  defensiva si `test/` se elimina manualmente.
- Conseguir `LogoSalon.png` en mayor resolución (actualmente 500×405 px);
  al escalar al 40% del QR (1424 px) se interpola y puede verse borroso en
  impresión de alta calidad.

## Pre-classifier message (QR design decision)

The `wa.me` pre-filled message is designed to do double duty:

- **Service pre-classification.** Instead of a generic greeting, the message lists
  the salon's services joined by `/` and invites the customer to keep only the one
  they want, e.g.:
  `Hola 👋 quiero agendar una cita. Servicio de interés: manicure / corte / tinte / otro (deja solo el que quieras). ref:<campaign_code>`
  The customer can edit the text before sending, so most will delete the options
  that don't apply, leaving a clean, predictable keyword in the salon's inbox.
- **Campaign attribution.** The campaign code is appended with a fixed `ref:`
  prefix (e.g. `ref:vitrina2025`). Print a different code per advertising piece
  (window display, reception sign, future flyers) to attribute origin.

**Why the `ref:` prefix:** it keeps the campaign code easy to spot in the chat and
ready for the future YCloud/bot stage that will read these messages. Keep the
prefix stable so that later tooling can rely on it.

**Implementation notes the generator must follow:**
- The service list is a single editable config value (a `SERVICIOS` list at the
  top of `main.py`) so it can be changed without touching logic.
- The full message must be URL-encoded (`urllib.parse.quote`) before being placed
  in the `wa.me?text=` URL — spaces, emojis and `/` break the URL otherwise.
- Use `ERROR_CORRECT_H` for the QR so it stays scannable if a center logo is added
  later.

**Known limitation:** the customer cannot be forced to edit the message; some will
send it with all options intact (ambiguous intent). That's acceptable for the
print/advertising goal of this repo.