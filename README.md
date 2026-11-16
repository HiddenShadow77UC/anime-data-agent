# Anime Data Agent

Aplicación local en construcción para explorar el catálogo de anime en español.
FastAPI/Python ofrece las consultas; LangGraph interpreta los mensajes acotados
y SQLite conserva el historial. Next.js/TypeScript ofrece portada y espacio de análisis.

## Estado

- Alcance: catálogo completo con filtros por formato.
- Rankings: criterio explícito; cantidad de valoraciones visible cuando esté validada.
  No se exige un mínimo por defecto; se permitirá como filtro opcional.
- API: comprobación de salud real en `/api/health` y documentación en `/docs`.
- Web: portada parallax con carrusel enlazado y análisis separado con chat, tablas y gráficos.
- Datos: carga local verificada, 22.634 registros.
- Consultas: búsqueda, filtros, rankings, detalle, comparación y agregación por API.
- Conversación: reglas acotadas, selección de registros, recuperación e historial persistente.
- Modelo de IA y MCP: todavía no integrados; fases 7 y 9 respectivamente.
- Interfaz de fase 6: implementada, pendiente de revisión visual y aceptación.

El CSV previsto es `anime_seasonal_20261116.csv` de LeoRigasaki/Anime-dataset.
Se consulta la copia identificada en la fase 3, sin necesitar Jikan ni el repositorio vecino.

## Preparación de datos (fase 3)

Desde la raíz del proyecto, sin necesitar acceso a Jikan:

```powershell
python scripts/prepare_dataset.py
python -m unittest discover -s scripts -p test_prepare_dataset.py -v
```

La entrada predeterminada es el CSV del repositorio vecino `../Anime-dataset`.
`data/processed/current.json` identifica una carga completa con copia original,
registros normalizados, informe de calidad y manifiesto. Repetir la preparación
con la misma entrada y transformación conserva la carga sin sobrescribirla.
La API resuelve ese puntero y verifica sus hashes. La carga se fija durante
la vida del proceso; reiniciar la API para incorporar una nueva carga preparada.

Ver [informe de calidad](docs/03-dataset.md) y [diccionario](docs/03-diccionario-datos.md).

## Requisitos

Python 3.11 o superior, Node.js 20.9 o superior y npm.
Se usa venv/pip para Python y npm para la web. Trabajar desde esta carpeta.

## Instalar en PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .\apps\api
npm.cmd --prefix apps/web install
```

La primera instalación requiere conexión a los registros de paquetes.
`apps/web/package-lock.json` fija las dependencias de la web: para reinstalaciones
usar `npm.cmd --prefix apps/web ci`.
`apps/api/requirements-windows-py312.txt` registra las versiones Python instaladas
en Windows/Python 3.12; no es un bloqueo universal. Para reproducir ese entorno:

```powershell
.\.venv\Scripts\python.exe -m pip install -r .\apps\api\requirements-windows-py312.txt
.\.venv\Scripts\python.exe -m pip install --no-deps -e .\apps\api
```

No ejecutar los recolectores de referencia.

## Ejecutar

Primera terminal, desde la raíz de `anime-data-agent`:

```powershell
.\.venv\Scripts\python.exe -m uvicorn anime_agent.main:app --host 127.0.0.1 --port 8000
```

Segunda terminal, desde la misma carpeta:

```powershell
npm.cmd --prefix apps/web run dev
```

Abrir http://127.0.0.1:3000 para explorar y http://127.0.0.1:3000/analisis para conversar. También se puede
consultar http://127.0.0.1:8000/api/health o http://127.0.0.1:8000/docs.
Detener cada proceso con Ctrl+C. Si un puerto ya está ocupado, detener el proceso
propio que lo usa o elegir otro puerto y ajustar `API_URL` de forma coherente.

## Configuración

`.env.example` documenta las variables; no se carga automáticamente desde la raíz.
Por ejemplo, antes de arrancar Next.js:

```powershell
$env:API_URL = 'http://127.0.0.1:8000'
```

`ANIME_DATASET_PATH` y `ANIME_CONVERSATION_DB` admiten rutas absolutas o relativas
a la raíz del proyecto. El primero apunta a `data/processed/current.json`, no a
un JSON de registros sin manifiesto. El segundo guarda el historial SQLite.
No se necesitan claves de un modelo para estas fases.

## Probar consultas y conversación (fases 4 y 5)

Con la API reiniciada y la carga preparada:

```powershell
.\.venv\Scripts\python.exe scripts/smoke_api.py
```

El comando comprueba las rutas por HTTP y crea una conversación de demostración.
Se pueden explorar los contratos en http://127.0.0.1:8000/docs.
Para ejecutar una demostración directa sin red y las pruebas:

```powershell
.\.venv\Scripts\python.exe scripts/demo_local.py
.\.venv\Scripts\python.exe -m unittest discover -s apps/api/tests -v
```

La suite usa el dataset real y bases temporales aisladas. El caso ASGI queda
omitido por defecto porque esta sesión no pudo ejecutar su bucle de eventos;
no equivale a HTTP aprobado. Ver evidencia y limitaciones en los documentos de fases 4 y 5.
Para incluirlo en un entorno que permita ejecutarlo: `$env:ANIME_HTTP_TESTS = '1'`.

## Comprobaciones

```powershell
npm.cmd --prefix apps/web run typecheck
npm.cmd --prefix apps/web run build
Invoke-RestMethod http://127.0.0.1:8000/api/health
Invoke-RestMethod http://127.0.0.1:3000/api/health
```

La segunda consulta HTTP verifica el proxy de la web hacia la API.
El estado `ok` solo confirma que la API atiende; los demás campos declaran las
capacidades pendientes. Los resultados ejecutados se registran en `docs/02-proyecto.md`.

## Documentación y referencias

- [Plan](docs/00-plan.md).
- [Alcance detallado](docs/01-alcance.md).
- [Entrega de la fase 2](docs/02-proyecto.md).
- [Consultas, fase 4](docs/04-consultas.md).
- [Conversación e historial, fase 5](docs/05-conversacion.md).
- [Interfaz, fase 6](docs/06-interfaz.md).

## Imágenes y presentación

El tema sigue la preferencia claro/oscuro del navegador, con claro como respaldo.
La primera versión se dirige a escritorio; el diseño móvil se deja para beta.
Las imágenes son referencias externas opcionales, asociadas al mismo ID del anime;
si fallan, las fichas y consultas siguen funcionando. Para regenerar su índice:

```powershell
python scripts/prepare_media.py
```

El archivo auxiliar de AniList aporta solo imágenes; las estadísticas siguen
procediendo exclusivamente de la carga MyAnimeList validada. Ver condiciones,
cobertura visual y limitaciones en el documento de fase 6.
- Arquitectura de referencia: https://github.com/marcor0311/messi-wc-2022-data-agent
- Datos: https://github.com/LeoRigasaki/Anime-dataset

El código base de esta fase se escribió para anime; no se copiaron la galería,
imágenes, componentes deportivos ni credenciales del proyecto de referencia.
