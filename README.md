# JARVIS 2

Construcción incremental de un asistente personal de IA siguiendo **VISION CERO · Construye tu propio JARVIS**.

## Regla
Cada nivel debe funcionar antes de montar el siguiente.

1. Voz
2. Tools
3. Memoria
4. Sentidos
5. Agentes
6. Sistema operativo personal

### Estado actual
**Nivel 1 — Voz:** arquitectura y pipeline inicial.

Flujo:

`micrófono → STT → LLM → TTS → altavoz`

Primero usamos push-to-talk. Wake word, tools, memoria, visión y agentes quedan fuera del Nivel 1.

## Arquitectura

```
jarvis/
├── app.py
├── config.py
├── audio/
│   ├── __init__.py
│   ├── stt.py
│   ├── tts.py
│   └── audio.py
├── brain/
│   ├── __init__.py
│   └── llm.py
└── tests/
    └── test_imports.py
```

## Windows

Crear entorno:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configurar variables:

```powershell
$env:OPENAI_API_KEY="TU_API_KEY"
```

Ejecutar:

```powershell
python app.py
```

El programa escucha al pulsar **Enter**, graba una intervención y la procesa.

> El Nivel 1 no ejecuta comandos del sistema ni código arbitrario. Eso pertenece a Tools y tendrá una capa explícita de permisos.
