# JARVIS 2

Construcción incremental de un asistente personal de IA siguiendo **VISION CERO · Construye tu propio JARVIS**.

## Regla de construcción

Cada nivel debe funcionar antes de montar el siguiente:

1. Voz
2. Tools
3. Memoria
4. Sentidos
5. Agentes
6. Sistema operativo personal

**Estado actual: Nivel 1 — Voz.**

No se añaden Tools, memoria, visión, agentes, event bus ni HUD gráfico antes de validar esta capa.

## Nivel 1 — Voz

Pipeline:

`micrófono → VAD/STT → LLM → TTS → altavoz`

Implementación:

- Audio: Python + sounddevice.
- Push-to-talk: mantener ESPACIO pulsado; soltarlo termina la captura.
- STT: Faster-Whisper local con VAD del proveedor.
- LLM: OpenAI Responses API, aislado detrás de un Protocol de proveedor.
- TTS: Piper local, aislado detrás de un Protocol de proveedor.
- Estados: LISTO → ESCUCHANDO → TRANSCRIBIENDO → PENSANDO → HABLANDO → LISTO.
- Logs: latencia por etapa y ciclo completo.
- Errores: una etapa fallida no destruye el bucle principal.
- Proveedores: STT, LLM y TTS pueden sustituirse sin reescribir el orquestador.

El PDF propone Faster-Whisper o whisper.cpp para STT, Piper o Qwen3-TTS para TTS y Silero VAD o el VAD del proveedor. Esta implementación usa Faster-Whisper + su VAD integrado y Piper.

## Estructura del Nivel 1

```
JARVIS-2/
├── main.py
├── config.py
├── audio.py
├── stt.py
├── llm.py
├── tts.py
├── tests/
│   ├── test_imports.py
│   └── test_config.py
├── requirements.txt
├── run.ps1
└── .env.example
```

Esta estructura sigue el arranque que indica el PDF: `main.py / stt.py / llm.py / tts.py / audio.py / config.py`.

## Windows / PowerShell

1. Abre PowerShell dentro de la carpeta del repositorio.
2. Ejecuta:

```powershell
.\run.ps1
```

El script crea/activa `.venv`, instala dependencias y arranca `main.py`.

También puedes crear `.env` desde `.env.example`; JARVIS lo carga automáticamente.

### Primer arranque

- Faster-Whisper puede descargar el modelo STT la primera vez.
- Piper descarga la voz configurada la primera vez.
- Necesitas Internet para esas descargas y para el LLM.
- El micrófono y los altavoces deben estar disponibles para Windows.

### Uso

- Pulsa Enter en `JARVIS >`.
- Mantén presionada **ESPACIO** mientras hablas.
- Suelta **ESPACIO** para enviar.
- JARVIS transcribe, piensa y responde por voz.
- Escribe `salir` para terminar.
- Ctrl+C detiene el proceso.

## Lo que todavía NO se implementa

- Wake word / openWakeWord.
- Tools / function calling.
- Memoria / SQLite / Qdrant.
- Cámara / visión.
- Agentes / LangGraph.
- Event bus.
- UI/HUD gráfica.
- Arquitectura de Personal AI OS.

Se incorporará únicamente después de validar Nivel 1.

## Seguridad

- No se almacenan API keys en el repositorio.
- `.env` está ignorado por Git.
- En Nivel 1 no existen tools ni ejecución arbitraria.
- No existe todavía una base de datos expuesta a red.

## Criterio para pasar a Nivel 2

Antes de continuar, Nivel 1 debe:

- funcionar sin trucos manuales;
- permitir medir latencia y fallos;
- tener proveedores intercambiables;
- tener una forma clara de detener el sistema;
- completar una conversación de extremo a extremo.
