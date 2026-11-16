# Alcance detallado por fases — Agente de anime

Estado: fases 1, 2 y 3 aprobadas; fases 4 y 5 autorizadas conjuntamente e implementadas
para revisión. Estado detallado y comprobaciones pendientes en `00-plan.md`.
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

## Decisiones confirmadas al cerrar el paso 1

1. Universo inicial: catálogo completo con filtro por formato.
2. Ranking: no exigir mínimo de valoraciones por defecto; permitirlo como filtro opcional.
3. Mostrar cantidad de valoraciones junto a la puntuación cuando el campo esté validado.
4. El ranking define orden y desempate; los filtros definen quién participa.
5. El criterio de orden y los filtros aplicados deben ser visibles.

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
el dataset original. El usuario confirmó catálogo completo, ausencia de mínimo
obligatorio de valoraciones y continuación a la fase 2.

## Desarrollo requerido por cada fase

Esta sección especifica trabajo futuro. Documentar un requisito no significa que
esté implementado o aprobado. `00-plan.md` conserva el estado real de ejecución.
Las rutas de entregables indicadas abajo son propuestas de organización y se
concretarán durante cada fase; consultar el estado real en el plan y los cierres.

### Fase 1. Definir y revisar el alcance

**Entrada:** objetivo del usuario, proyecto de Messi y CSV local identificado.

**Trabajo requerido:**

- Acordar universo de formatos, períodos consultables y política de rankings.
- Definir búsqueda, detalle, filtros, comparación, agregación e historial.
- Precisar cuáles métricas están disponibles y cuáles dependen de validar la fuente.
- Registrar limitaciones, preguntas pendientes y criterios de aceptación por fase.
- Mantener separados decisiones confirmadas, propuestas y capacidades implementadas.

**Entregables:** este documento y `00-plan.md`, con registro de decisiones y estados.

**Aceptación:** las funciones tienen ejemplos comprobables; no hay decisiones de
producto presentadas como confirmadas sin respuesta del usuario. Las decisiones
necesarias para iniciar la fase 2 están resueltas y el usuario revisó el alcance.

**Revisión completada:** catálogo completo y mínimo de valoraciones opcional. Las preferencias
visuales y la selección del modelo pueden resolverse en sus fases, sin bloquear
trabajo independiente. Las dos decisiones se confirmaron explícitamente en mensajes
posteriores a la revisión inicial de los documentos.

### Fase 2. Preparar el proyecto

**Entrada:** alcance revisado y decisiones necesarias confirmadas.

**Trabajo requerido:**

- Revisar la estructura y dependencias del proyecto de Messi; reutilizar patrones
  de contrato, estado e historial, sustituyendo las entidades específicas de fútbol.
- Crear `apps/api` para FastAPI/Python y `apps/web` para Next.js/TypeScript.
- Reservar `apps/mcp` para la fase 9, sin anunciar una integración funcional aún.
- Separar código, datos originales, datos procesados, pruebas y documentación.
- Crear configuración de dependencias reproducible y ejemplos de variables sin secretos.
- Definir configuración de rutas del dataset, base del historial y conexión web/API.
- Crear comprobación de salud de API y una página base que permita verificar la conexión.
- Documentar comandos de PowerShell, versiones requeridas y puertos locales.
- Comprobar si existe repositorio Git propio; consultar antes de asociar un remoto
  o publicar. No modificar los repositorios usados como referencia.

**Entregables propuestos:** estructura del proyecto, archivos de dependencias,
`.env.example`, `.gitignore` y README de arranque local.

**Aceptación:** API y web arrancan con las instrucciones documentadas; la web
alcanza la API; la comprobación de salud no simula disponibilidad de datos o IA.
No hay dependencias de rutas privadas del proyecto de Messi ni secretos versionados.

**Revisión:** demostrar el arranque y describir qué partes son todavía estructura.

### Fase 3. Preparar y validar el dataset

**Entrada:** CSV seleccionado y repositorio de procedencia local.

**Trabajo requerido:**

- Copiar el CSV al proyecto conservando el original; fijar SHA-256, tamaño,
  nombre, commit de origen, fecha de incorporación y fecha declarada por la fuente.
- Revisar atribución y condiciones disponibles de reutilización; registrar cualquier
  ausencia de licencia explícita antes de decidir redistribuir públicamente los datos.
- Perfilar los 29 campos: tipos, nulos, ceros, rangos, duplicados y distribuciones.
- Normalizar títulos, identificadores, formatos, estados y listas separadas por `;`.
- Documentar unidades: puntuación sobre 10 y duración según la transformación del recolector.
- Resolver por campo los ceros usados como defecto; conservar valor original y
  motivo de normalización cuando una transformación afecte el significado.
- Comprobar especialmente `members`, `favorites`, `scored_by`, `rank` y `popularity`;
  si un campo no es fiable, deshabilitar sus consultas explicando la razón.
- Interpretar fechas con precisión disponible: una fecha solo de año o mes no
  recibirá día inventado. Identificar estrenos futuros respecto de una fecha de referencia explícita.
- Conservar campos desconocidos como nulos; no completar estudios o sinopsis con el modelo.
- Generar una carga procesada identificable y un procedimiento reproducible de regeneración.
- Informar cobertura real por año y formato; distinguir filas rechazadas, aceptadas
  con advertencia y excluidas por el alcance elegido. No descartar silenciosamente.

**Entregables propuestos:** copia en `data/raw`, carga en `data/processed`, script
de preparación, diccionario de datos, manifiesto e informe de calidad.

**Aceptación:** se reconcilian conteos originales, aceptados y rechazados; los IDs
procesados son únicos; los campos usados cumplen sus reglas; una segunda ejecución
sobre la misma entrada produce los mismos registros normalizados. Los errores de
datos impiden publicar una carga como válida y no reemplazan una carga válida previa.

**Revisión:** presentar cifras de calidad y decisiones de limpieza antes de cerrar.

### Fase 4. Crear las herramientas de consulta

**Entrada:** dataset validado y definiciones de métricas.

**Trabajo requerido:**

- Implementar herramientas tipadas de búsqueda, detalle, filtrado/ranking,
  comparación y agregación por año; permitir agrupar por género o estudio si la
  calidad y el alcance revisado lo permiten.
- Admitir filtros por formato, géneros, estudio, año de estreno, estado,
  puntuación, mínimo de valoraciones y máximo de episodios según campos fiables.
- Definir si varios géneros significan «cualquiera» o «todos»; mostrar el operador
  aplicado y pedir aclaración ante lenguaje ambiguo.
- Especificar límites, orden, desempate estable por ID y tratamiento de nulos.
- La búsqueda devuelve candidatos; una coincidencia ambigua no se convierte en
  selección automática de una temporada o película.
- Validar IDs de comparación y evitar comparar un registro consigo mismo.
- Para rankings, aplicar filtros antes del límite de resultados. Para agregaciones,
  contar toda la selección filtrada, no solamente el top mostrado.
- Devolver filtros efectivos, resultados, cantidad total, carga de datos y
  definición de métrica. Conservar evidencia suficiente para reproducir el cálculo.
- Exponer contratos API reutilizables por el agente web y posteriormente MCP.
- Manejar parámetros inválidos, registros desconocidos, selección vacía y carga ausente.

**Entregables propuestos:** servicio de consultas, esquemas de entrada/salida,
endpoints documentados en OpenAPI y pruebas de cálculo y filtrado.

**Aceptación:** casos representativos coinciden con cálculos independientes sobre
el CSV procesado; orden y desempate son reproducibles; un agregado reconcilia sus
conteos; ningún resultado viola filtros o usa métricas deshabilitadas por calidad.

**Revisión:** mostrar consultas y cifras verificadas, incluyendo un resultado vacío.

### Fase 5. Construir la conversación y el historial

**Entrada:** herramientas de consulta verificadas.

**Trabajo requerido:**

- Implementar en LangGraph resolución de intención, validación, consulta y composición.
- Empezar con interpretación acotada de los escenarios aprobados; indicar ese alcance.
- Conservar filtros, orden, límite, registros seleccionados y carga de datos por turno.
- Distinguir nueva consulta, refinamiento, comparación y detalle. Cambiar solo las
  condiciones expresadas; aclarar cuando no se pueda inferir la intención con seguridad.
- Resolver referencias como «estos dos» mediante IDs seleccionados y «solo TV»
  mediante el contexto previo; sin selección suficiente, pedir aclaración.
- Guardar turnos y resultados inmutables; recuperar un turno crea la base de la
  siguiente consulta sin reescribir el historial.
- Aislar conversaciones y validar que el turno base y los IDs pertenezcan a su contexto.
- Persistir historial local y verificar recuperación tras reiniciar el servidor.
- Ante error o aclaración, conservar el resultado anterior y no inventar uno nuevo.

**Entregables propuestos:** grafo, estado de conversación, persistencia, contrato
de turnos y pruebas de continuidad, recuperación y aislamiento.

**Aceptación:** ejecutar búsqueda/ranking → máximo de episodios → selección →
comparación → recuperación de turno → nuevo refinamiento. Confirmar los filtros
en cada paso y que las conversaciones no se mezclan. Un fallo no deja turnos parciales.

**Revisión:** demostrar la conversación acotada e indicar que aún no usa un modelo.

### Fase 6. Construir y revisar la interfaz

**Entrada:** API conversacional estable y preferencias visuales del usuario.

**Trabajo requerido:**

- Consultar nombre público, estilo, colores, uso de imágenes y dispositivos objetivo
  antes de fijar la presentación. No heredar la estética futbolística de Messi.
- Implementar chat, historial recuperable, tabla, ficha, comparación y gráficos acordados.
- Hacer visibles filtros activos, métrica, fecha/versión de datos y acceso a evidencia.
- Mantener selección de registros consistente entre tabla, gráfico y comparación.
- Mostrar cantidad total y límite visible para no confundir top con catálogo completo.
- Usar barras con escalas identificadas y comparables; indicar los valores ausentes.
- Mostrar estados inicial, cargando, vacío, aclaración, error y datos no disponibles.
- Conservar resultados durante errores y permitir reintentar sin duplicar turnos.
- Permitir navegación por teclado, etiquetas legibles y comprensión sin depender solo del color.
- Verificar los tamaños de pantalla acordados. No prometer soporte móvil sin validarlo.
- Usar únicamente imágenes cuya fuente y condiciones se hayan revisado, si se aprueban.

**Entregables propuestos:** interfaz funcional, estilos, componentes visuales y
verificación en navegador de los recorridos acordados.

**Aceptación:** las acciones producen consultas reales; cifras de tabla, gráfico y
explicación coinciden; recargar conserva la conversación; controles y textos son
utilizables en los dispositivos elegidos. El usuario revisa la apariencia.

**Revisión:** presentar la aplicación y registrar ajustes visuales antes del cierre.

### Fase 7. Conectar un modelo de IA

**Entrada:** herramientas y conversación verificadas, proveedor/modelo elegido.

**Trabajo requerido:**

- Consultar proveedor, modelo disponible, forma de autenticar y presupuesto o
  límites de uso. Confirmar qué datos se enviarán al proveedor.
- Añadir un adaptador configurable y mantener las credenciales fuera del código y logs.
- Dar al modelo esquemas de herramientas y diccionario de métricas; validar los
  argumentos en el servidor antes de ejecutar cualquier consulta.
- Mantener cálculos, selección de registros y evidencia en las herramientas Python.
- Fundamentar explicaciones en resultados reales; títulos, cifras y referencias
  no pueden aparecer como resultados si la herramienta no los devolvió.
- Interpretar variantes de las preguntas acordadas, refinamientos y ambigüedades.
- Tratar sinopsis y contenido del dataset como datos, nunca como instrucciones.
- Limitar llamadas, tiempo de respuesta y tamaño de contexto; gestionar errores
  del proveedor y distinguir cualquier modo acotado de respaldo.
- No enviar el catálogo completo cuando basten filtros, esquema y resultados seleccionados.

**Entregables propuestos:** adaptador del modelo, configuración, instrucciones,
orquestación de herramientas y evaluación de preguntas en español.

**Aceptación:** distintas formulaciones producen consultas correctas; no se ejecutan
argumentos inválidos; una pregunta no sustentada pide aclaración o informa el límite.
Los cálculos se mantienen iguales a la fase 4 y un fallo del modelo conserva el resultado previo.

**Revisión:** mostrar llamadas reales, límites observados y consumo disponible sin
exponer secretos; no dar por completada la fase con respuestas simuladas.

### Fase 8. Validar y documentar la entrega local

**Entrada:** aplicación con modelo funcional.

**Trabajo requerido:**

- Consolidar pruebas de calidad, herramientas, API, conversación, interfaz y modelo.
- Preparar un conjunto de preguntas con resultados esperados independientes;
  separar pruebas deterministas de evaluaciones que requieren acceso al proveedor.
- Validar errores de datos, servicio no disponible, ambigüedades, consultas vacías
  y recuperación después de reinicios.
- Verificar que la consulta al dataset funciona sin Jikan; el modelo puede requerir red.
- Documentar instalación, preparación de datos, arranque, configuración y solución de problemas.
- Registrar versiones de dependencias, carga usada, comandos ejecutados y resultados reales.
- Preparar una demostración con ranking, refinamiento, comparación, agregado y evidencia.
- Documentar límites, campos deshabilitados y pendientes; no declarar pruebas no ejecutadas.

**Entregables propuestos:** README final de ejecución local, evidencia de validación,
guion de demostración y lista de limitaciones conocidas.

**Aceptación:** la aplicación puede reproducirse con las instrucciones y los datos
indicados; los escenarios acordados pasan o sus bloqueos quedan explícitos para revisión.
Esta fase valida la aplicación local; la integración MCP se certifica en la fase 9.

**Revisión:** presentar qué pasó, qué no se pudo comprobar y qué queda pendiente.

### Fase 9. Integrar MCP en Node.js y TypeScript

**Entrada:** herramientas API estables, documentación y cliente MCP elegido.

**Trabajo requerido:**

- Elegir con el usuario el cliente de destino y el transporte compatible:
  stdio para integración local o HTTP para clientes que lo requieran.
- Revisar documentación vigente del SDK y del cliente al implementar la integración.
- Crear `apps/mcp` con Node.js/TypeScript y herramientas de solo lectura que
  deleguen en la API: búsqueda, ranking, comparación, detalle y agregación.
- Publicar esquemas, descripciones, filtros admitidos, unidades y errores comprensibles.
- Reutilizar las reglas y resultados de Python, sin mantener un segundo motor de cálculos.
- Gestionar URL de API, límites, tiempos de espera y errores; mantener logs fuera
  del canal de protocolo cuando se use stdio.
- Definir explícitamente el contexto: si las herramientas son independientes,
  reciben todos los filtros; si se expone conversación, usar los IDs y aislamiento
  del backend, sin estado global compartido entre usuarios.
- Si el cliente necesita acceso remoto, configurar conexión, autenticación y
  túnel compatible una vez acordados. Un túnel no sustituye al servidor MCP.
- Registrar descubrimiento de herramientas y ejecutar consultas reales desde el cliente.
- Comparar el mismo filtro en web/API/MCP y comprobar igualdad de resultados y evidencia.
- Actualizar README y evidencia con instalación, arranque y diagnóstico del MCP.

**Entregables propuestos:** servidor MCP, configuración de ejemplo sin secretos,
instrucciones de conexión y evidencia de una consulta real de extremo a extremo.

**Aceptación:** el cliente descubre herramientas, obtiene resultados verificables
desde la carga local y recibe errores claros si la API no está disponible. La
integración no se declara completa solo porque el proceso Node inicia o lista herramientas.

**Revisión:** demostrar al menos ranking y comparación desde el cliente elegido;
documentar si hubo túnel y qué conectividad permanece necesaria.

## Dependencias y decisiones que no deben anticiparse

| Momento | Decisión pendiente | Efecto |
| --- | --- | --- |
| Cierre de fase 1 — resuelto | Catálogo completo; mínimo de valoraciones opcional, ninguno por defecto | Reglas de consulta y universo inicial. |
| Fase 2 | Versiones compatibles, gestor de dependencias y estado de Git | Arranque reproducible; no implica publicar un repositorio. |
| Fase 3 | Interpretación de ceros y fiabilidad de estadísticas | Habilitar o excluir métricas con evidencia. |
| Fase 4 | Operador de múltiples géneros y alcance de comparación | Consultas inequívocas y límites visibles. |
| Antes de fase 6 | Nombre, estilo, imágenes y dispositivos | Presentación aprobada por el usuario. |
| Antes de fase 7 | Proveedor/modelo, credenciales y límites de consumo | Integración real con IA. |
| Antes de fase 9 | Cliente MCP, transporte y necesidad de túnel | Conexión comprobable de extremo a extremo. |

Las decisiones se consultan cuando condicionan el siguiente trabajo; no se piden
todas por adelantado. Publicación, hosting o repositorio remoto no están incluidos
como decisiones ya aprobadas por este documento.

## Cierre y descripción obligatoria de cada fase

Al terminar una fase, actualizar el plan y registrar:

1. Qué se hizo y qué comportamiento quedó disponible.
2. Archivos creados o modificados y finalidad de cada grupo.
3. Comprobaciones ejecutadas, resultados y evidencia relevante.
4. Limitaciones o bloqueos observados y decisiones aún pendientes.
5. Solicitud de revisión del usuario y estado: en revisión, requiere ajustes o aprobado.

La siguiente fase comienza después de resolver esa revisión. Si un hallazgo cambia
el alcance o contradice una expectativa, se explica y se consulta antes de adoptar
la decisión. No se eliminan datos o trabajo previo para avanzar de fase.

## Definición de entrega completa

El proyecto estará completo cuando las nueve fases hayan sido revisadas y el
usuario pueda consultar el dataset local desde la web y desde el cliente MCP
acordado, formular variantes en español mediante un modelo real, recuperar
contexto y comprobar fuente, filtros y resultados. Los límites de cobertura y
calidad deben permanecer visibles en la aplicación y en la documentación.
