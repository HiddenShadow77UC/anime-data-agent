# Evidencia de fase 9

Fecha local: 16 de noviembre de 2026 (Costa Rica); nombres e informes en UTC.
Dataset: 22.634 registros; carga
`anime-v1-2026-11-16-9f73ed290e1be7a4-b1b96aa4188deed8`.

| Comprobación | Evidencia | Resultado |
| --- | --- | --- |
| MCP stdio → Python real | [informe](smoke-1794888775800-stdio.json) | Descubrimiento y nueve comprobaciones correctas. |
| MCP HTTP → Python real | [informe](smoke-1794888784450-streamable_http.json) | Descubrimiento y nueve comprobaciones correctas. |
| Pruebas de contrato/protocolo MCP | [log](../phase8/20261117T041856658230Z/mcp_tests.txt) | Diez aprobadas; incluye cliente 2025-06-18. |
| Regresión general con HTTP | [resumen](../phase8/20261117T041856658230Z/summary.json) | Correcta, 46 pruebas aprobadas, una ASGI omitida, seis casos de aceptación y build web correcto. |
| Nuevo intento incluyendo proxy web | [informe](smoke-1794889190485-streamable_http.json) | Falló: fetch failed; no acredita igualdad mediante el proxy. |
| Conexión desde ChatGPT | No ejecutada | Falta túnel/configuración de cuenta y llamada real desde ese cliente. |

Los informes MCP correctos comparan el resultado completo contra la API directa,
incluidos filtros y evidencia. Los logs son de un cliente SDK, no de ChatGPT.
No hubo llamadas al modelo en estas comprobaciones.

Durante la regresión, el build web falló primero por EPERM en una carpeta generada
de `.next`; se conservó el build anterior bajo `data/build-backups/` y se regeneró
correctamente. El informe anterior de esa ejecución fallida se conserva en
`../phase8/20261117T041512005528Z/`. No se modificó el diseño web para resolverlo.

## Bloqueo posterior de la revisión automática

Al consultar un proceso persistente iniciado para MCP, la revisión automática
rechazó la operación, indicando una conexión de telemetría a
`dc.services.visualstudio.com` cuyo contenido/destino no estaba autorizado.
Un intento de detener la web mediante la sesión también fue rechazado con ese
motivo. La sesión MCP ya no estaba disponible al intentar detenerla.
No se declara que los procesos sigan activos ni que su cierre se haya comprobado.

La inspección de archivos `.mjs` y `.json` instalados en `apps/mcp/node_modules`
no encontró ese dominio ni las cadenas Application Insights buscadas. Eso no
determina el origen de la conexión ni demuestra ausencia de telemetría en todo
el entorno. No se reintentó el inicio por otra vía ni se relajaron permisos.

La parte de conexión remota queda pendiente de resolver este bloqueo y de la
configuración del túnel. No se instaló ni arrancó el cliente oficial de túnel.
`scripts/start_tunnel.py --help` se comprobó; no se probó su conexión autenticada.
