# codigo_qr — Generador de QR para WhatsApp (Karina Salón)

Genera un código QR **estilizado** (módulos circulares + “ojos” redondeados) que abre el chat de WhatsApp del salón con un mensaje prellenado.

## ¿Qué hace este script?

1. Lee el número del salón desde un archivo `.env`
2. Construye un link `wa.me` (Click to Chat)
3. Codifica el mensaje para URL (espacios, signos, tildes)
4. Genera y guarda el QR como imagen `.png`

## Estructura recomendada

```text
codigo_qr/
├── src/
│   └── qr_generator.py
├── test/
│   └── (aquí se guardará qr_code.png)
├── .env              (NO se sube a GitHub)
├── .env.example
├── .gitignore
└── requirements.txt
