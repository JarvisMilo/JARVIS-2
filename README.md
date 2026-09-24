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

`micrófono → VAD/STT → LLM local → TTS → altavoz`

Implementación:

- Audio: Python + sounddevice.
- Push-to-talk: mantener ESPACIO pulsado; soltarlo termina la captura.
- STT: Faster-Whisper local con VAD del proveedor.
- LLM: **Ollama local**, aislado detrás de un Protocol de proveedor.
- TTS: Piper local, aislado detrás de un Protocol de proveedor.
- Estados: LISTO → ESCUCHANDO → TRANSCRIBIENDO → PENSANDO → HABLANDO → LISTO.
- Logs: latencia por etapa y ciclo completo.
- Errores: una etapa fallida no destruye el bucle principal.
- Proveedores: STT, LLM y TTS pueden sustituirse sin reescribir el orquestador.

El PDF propone Faster-Whisper o whisper.cpp para STT, Piper o Qwen3-TTS para TTS y Silero VAD o el VAD del proveedor. Esta implementación usa Faster-Whisper + su VAD integrado y Piper.

## Sin tokens de OpenAI

El cerebro del Nivel 1 funciona localmente con Ollama. **No se necesita una API key de OpenAI ni pagar tokens para ejecutar JARVIS.**

Ollama ejecuta el modelo en tu propio PC y expone una API local. El proyecto usa esa API mediante la librería Python `ollama`.

Modelo inicial:

`llama3.2`

Ollama ofrece variantes pequeñas y modelos de distintos tamaños; si tu PC tiene pocos recursos, podremos cambiar el modelo después sin cambiar el orquestador.

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

## Windows

1. Instala Ollama para Windows.
2. Abre Ollama y comprueba que esté ejecutándose.
3. En una terminal ejecuta:

```powershell
ollama pull llama3.2
```

4. Comprueba que aparece:

```powershell
ollama list
```

5. Desde la carpeta de JARVIS ejecuta:

```powershell
.\run.ps1
```

El script crea/activa `.venv`, instala las dependencias y comprueba que el modelo local esté disponible.

### Primer arranque

- Faster-Whisper puede descargar el modelo STT la primera vez.
- Piper descarga la voz configurada la primera vez.
- Ollama necesita descargar el modelo una sola vez.
- Las descargas iniciales necesitan Internet, pero las conversaciones posteriores pueden ejecutarse localmente.
- El micrófono y los altavoces deben estar disponibles para Windows.

## Uso

- JARVIS queda en estado **LISTO** y espera una acción.
- Mantén presionada **ESPACIO** mientras hablas.
- Suelta **ESPACIO** para enviar.
- JARVIS transcribe, piensa con Ollama y responde por voz.
- Pulsa **ESC** para apagar.
- Ctrl+C también detiene el proceso.

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

- No se almacenan API keys porque el Nivel 1 usa Ollama local.
- No existen tools ni ejecución arbitraria.
- No existe todavía una base de datos expuesta a red.

## Criterio para pasar a Nivel 2

Antes de continuar, Nivel 1 debe:

- funcionar sin trucos manuales;
- permitir medir latencia y fallos;
- tener proveedores intercambiables;
- tener una forma clara de detener el sistema;
- completar una conversación de extremo a extremo;
- mantener el bucle estable después de un error;
- no quedar bloqueado si se alcanza el límite de captura.
