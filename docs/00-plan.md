# Plan de trabajo

Cada etapa termina con una descripción de lo realizado y revisión del usuario.
No se inicia la siguiente hasta resolver esa revisión.

Este archivo es el resumen y seguimiento. El detalle de requisitos, entregables,
aceptación y revisiones de cada fase está en [01-alcance.md](01-alcance.md).
La documentación de una fase futura no significa que esté implementada.

| Paso | Entregable | Estado |
| --- | --- | --- |
| 1. Alcance | `01-alcance.md`, detallado para las nueve fases | Aprobado: catálogo completo; mínimo de valoraciones opcional, sin mínimo por defecto. |
| 2. Proyecto | Estructura Next.js, FastAPI y LangGraph; instrucciones | Aprobada por el usuario tras verificar conexión, desconexión y recuperación. |
| 3. Dataset | Copia identificada, normalización e informe de calidad | Aprobada por el usuario. Ver `03-dataset.md`. |
| 4. Consultas | Búsqueda, filtros, ranking, comparación, detalle y agregados | Aprobada por el usuario tras pruebas directas y HTTP real. |
| 5. Conversación | Estado, historial y consultas encadenadas | Aprobada por el usuario tras verificar LangGraph/SQLite y HTTP. |
| 6. Interfaz | Chat, tablas, gráficos y detalle; diseño acordado | Implementada primera versión: parallax, carrusel, tema automático y análisis. TypeScript/build correctos; revisión visual y aprobación pendientes. Ver `06-interfaz.md`. |
| 7. Modelo de IA | Interpretación flexible mediante herramientas validadas | Pendiente |
| 8. Validación | Pruebas, evidencia y README reproducible | Pendiente |
| 9. MCP | Node.js y TypeScript conectado a la API Python | Pendiente |

## Material previo

`scripts/download_anime.py` se preparó para Jikan, pero la descarga falló por
conectividad. No constituye un dataset descargado ni una etapa completada.
La fuente acordada ahora es el CSV local del repositorio `Anime-dataset`.

## Última actualización

Se amplió el alcance con entradas, trabajo requerido, entregables, criterios de
aceptación y revisión para las nueve fases. También se registraron dependencias,
decisiones pendientes y la descripción requerida al cerrar cada fase.
Posteriormente el usuario aprobó catálogo completo y mínimo de valoraciones opcional.
Se creó la estructura base de la fase 2. Tras los bloqueos iniciales de esta sesión,
el usuario instaló las dependencias. TypeScript y build pasaron y el usuario
confirmó conexión web/API, error al detener la API y recuperación al reiniciarla.
El usuario aprobó la fase 2. La fase 3 preparó 22.634 registros, manifiesto,
diccionario e informe de calidad. Cinco pruebas y repetición reproducible pasaron.
Siete estadísticas de usuarios quedan deshabilitadas por falta de datos fiables.
El usuario aprobó la fase 3 y autorizó desarrollar las fases 4 y 5 juntas.
Se implementaron consultas y conversación persistente con evidencia compartida.
La prueba ASGI quedó bloqueada y no se marca aprobada; se ofrece comprobación
HTTP real desde la terminal del usuario, que fue ejecutada con éxito. Falta
aprobación conjunta del usuario. No se inició la fase 6.
