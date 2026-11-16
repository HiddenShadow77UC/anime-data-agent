# Alcance detallado por fases — Agente de anime

Estado: borrador para revisión del usuario. No autoriza todavía el paso 2.
Fecha de elaboración: 16 de noviembre de 2026.
Nombre técnico acordado: `anime-data-agent`. Nombre público e identidad visual pendientes.

## Objetivo

Consultar, explorar y comparar anime en español mediante una conversación que
conserva filtros y presenta tablas, gráficos y explicaciones verificables.
Las respuestas describen una captura del catálogo, no estadísticas en tiempo real.

## Decisiones confirmadas

- Proyecto local en `Innovacion/anime-data-agent`.
- Referencia de implementación: `../messi-wc-2022-data-agent`.
- Una única fuente inicial: `../Anime-dataset/data/raw/anime_seasonal_20261116.csv`.
- Interfaz Next.js y TypeScript; API FastAPI con Python; conversación con LangGraph.
- Paso 7: conexión real con un modelo, conservando herramientas y parámetros validados.
- Paso 9 incluido: servidor MCP en Node.js y TypeScript, que llama a la API Python.
- Las consultas y cálculos se implementan una sola vez en Python.
- El desarrollo avanza por etapas con descripción del trabajo y revisión al terminar.

## Evidencia de la fuente local

Inspección previa: 22.634 registros, 22.634 identificadores diferentes y 29 columnas.
El CSV incluye series, películas, OVA, ONA, especiales, música y otras categorías.
El nombre del archivo indica 2026-11-16; el momento exacto de recopilación por fila
no está documentado en ese CSV. No se presentará esa fecha como verificación de cada valor.

El recolector `../Anime-dataset/src/mal_api.py` usa MyAnimeList v2 y conserva
el ID de MyAnimeList en `anime_id`. Su transformación asigna cero como valor por
defecto a diversas estadísticas: esos ceros requieren revisión por campo en el paso 3.
En particular, `members` y `favorites` pueden reflejar datos no proporcionados
por el endpoint; no se asumirán conteos fiables sin comprobar su calidad.

No se ha certificado exhaustividad histórica ni cobertura total por temporada.
La procedencia, versión del repositorio y hash del CSV se fijarán en el paso 3.

## Funciones y criterios de aceptación

| Función | Ejemplo | Resultado verificable |
| --- | --- | --- |
| Buscar | Busca Death Note | Coincidencias por títulos disponibles, con ID y título; aclaración si hay ambigüedad. |
| Filtrar y ordenar | Muéstrame los 10 animes de fantasía mejor puntuados | Hasta diez registros, puntuación y cantidad de valoraciones; filtros y orden explícitos. |
| Refinar | Solo series de televisión de máximo 26 episodios | Conserva fantasía y límite anterior; añade formato y máximo de episodios. |
| Comparar | Compara Death Note con Shingeki no Kyojin | Identifica los dos registros; muestra atributos comparables sin inventar datos. |
| Agregar | ¿Cuántas series se estrenaron por año desde 2020? | Cuenta registros de TV por año de estreno dentro de la cobertura disponible. |
| Explicar | ¿Qué filtros aplicaste y de dónde vienen los datos? | Fuente, versión local, filtros, orden y definición de las métricas usadas. |
| Recuperar | Recuperar un turno desde el historial | Restaura el contexto y resultado de ese turno sin alterar los anteriores. |

Las frases son escenarios de aceptación. Su reconocimiento acotado corresponde
al paso 5; la interpretación flexible con modelo corresponde al paso 7.

## Reglas funcionales

1. Un ID identifica una entrega; temporadas, películas y especiales no se fusionan en una franquicia.
2. Se buscará en títulos principal, inglés y japonés presentes. No se supondrán traducciones españolas ausentes.
3. La puntuación se expresa sobre 10; la posición de popularidad mejora al disminuir.
4. Puntuación, popularidad, cantidad de valoraciones y seguidores tienen definiciones diferentes.
5. Campos ausentes se muestran como desconocidos. Un cero no se convierte automáticamente en ausencia ni en dato válido para todos los campos.
6. Los rankings por puntuación omiten puntuaciones no válidas y muestran `scored_by`.
7. Un valor desconocido de episodios no satisface un máximo de episodios.
8. Se indica el estado de emisión; una fecha futura no equivale a estreno ya ocurrido.
9. Tablas, gráficos y explicaciones derivan del mismo resultado de consulta.
10. Una consulta vacía no se rellena con títulos ajenos al filtro.
11. Una consulta ambigua pide aclaración y conserva el resultado anterior.
12. Cada turno conserva filtros, IDs de resultados, versión de datos y selección relevante.
13. Los conteos se describen como registros del dataset; no como totalidad mundial de anime.

## Presentaciones funcionales propuestas

- Búsqueda y ranking: tabla; gráfico de barras para puntuaciones.
- Comparación: tabla de atributos de los títulos seleccionados.
- Conteos por año: tabla y gráfico de barras.
- Detalle: ficha con atributos y sinopsis disponible.
- La elección de colores, estilo, imágenes, nombre público y diseño requiere preferencias del usuario en el paso 6.

## Decisiones para la revisión del paso 1

1. Universo inicial: solo series de TV o catálogo completo con filtro por formato.
2. Ranking: mínimo predeterminado de valoraciones o todos los títulos con puntuación válida.
   Cualquier mínimo debe ser visible y modificable; no se fijó un umbral sin decisión del usuario.

## Límites de la primera entrega

- No se calcularán puntuaciones históricas a partir de una captura actual.
- No se deducirá disponibilidad actual de streaming a partir de campos ausentes.
- Recomendación personalizada por historial de usuarios y unión con AniList quedan fuera del alcance acordado.
- No se ha elegido proveedor/modelo, credenciales, despliegue ni transporte MCP.
  Se resolverán en sus etapas respectivas antes de ejecutar acciones dependientes.
- Consultas locales no necesitan que Jikan responda. El descargador anterior no es un requisito de ejecución.

## Descripción del trabajo del paso 1

Se documentaron objetivo, fuente inicial, tecnologías confirmadas, funciones,
criterios de aceptación, continuidad de conversación y reglas de trazabilidad.
Se revisó el contrato del agente de Messi para reutilizar sus principios de estado
y resultados inmutables, y el recolector de MyAnimeList para detectar valores por
defecto que requieren validación. No se implementó aún la aplicación ni se modificó
el dataset original. Faltan las dos decisiones de esta sección y la revisión del usuario.
