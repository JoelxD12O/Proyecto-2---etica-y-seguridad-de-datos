# Evaluación de impacto del prototipo

**Alcance y finalidad.** El club propone usar actividad, sueño, frecuencia cardíaca, peso y grasa corporal para acompañar entrenamientos solicitados por el cliente. El uso secundario de actividad para estimar tendencias grupales es opcional. El club es el responsable propuesto. El entrenador actúa dentro de su asignación. El operador técnico custodia claves, respaldos y el presupuesto de privacidad. Supabase y Render serían proveedores del despliegue. La demostración local utiliza personas ficticias. Un archivo de investigación importado solo alimenta la estadística del estudio.

| Etapa | Datos y acceso | Decisión y riesgo residual |
|---|---|---|
| Obtención | CSV de investigación locales, registros voluntarios del programa | Documentar origen y finalidad. El permiso original de un estudio no autoriza contactar a participantes ni convertirlos en clientes. Antes de una operación real, definir y documentar la base para el seguimiento y revisar los términos de las fuentes. |
| Preparación | El operador valida actividad por persona y día. El identificador de origen se reemplaza por HMAC con clave independiente | Fechas y patrones de actividad pueden permitir vinculación incluso con seudónimo. Los archivos originales quedan fuera de Git y de los paneles. El modelo Gym se evalúa en su propia fuente. |
| Conservación | Mediciones y metas cifradas en el servidor. Las fechas y relaciones necesarias para autorizar consultas quedan visibles a la base | Separar claves y almacenamiento y restringir el operador. Definir un plazo de conservación y una vía de eliminación verificable antes de incorporar clientes reales. |
| Acceso individual | El cliente y su entrenador asignado consultan la ficha. Se registra el acceso. El administrador consulta eventos y publicaciones | Probar el intento de acceso cruzado, revisar asignaciones y retirar permisos al terminar una relación. El entrenador puede ver información sensible durante una sesión autorizada. |
| Estadísticas | El administrador publica una estimación por mes. El entrenador lee lo ya publicado. La participación de clientes operativos empieza desactivada | Mostrar propósito, método y efecto de retirar el permiso. Las consultas nuevas toman la preferencia vigente. Un resultado previamente divulgado permanece en el historial. |
| Respaldo y cierre | Copia cifrada y restauración verificada en entorno aislado | La operación requiere responsables, copias fuera del equipo, expiración verificable y recuperación del historial de publicaciones. Un borrado debe contemplar copias, accesos y plazo de purga. |

## Transferencia internacional

En el modo alojado, Supabase (base de datos y autenticación) y Render (API y web) guardarían y procesarían los datos fuera del Perú. Es un flujo transfronterizo de datos personales, que la Ley 29733 y su Reglamento (D.S. 016-2024-JUS) regulan: el destino debe ofrecer un nivel de protección adecuado o el responsable debe garantizarlo por otros medios. Medidas previstas:

- **Cifrado antes de salir:** las mediciones se cifran por campo en la API y las claves no se guardan en el proveedor de base de datos.
- **Contrato de encargo** con cada proveedor, que limite el uso de los datos a la prestación del servicio y obligue a notificar incidentes. Elegir y documentar la región de alojamiento.
- **Transparencia:** el consentimiento informa que los datos se alojan fuera del país y con qué proveedores.
- **Modo demo local:** la demo y las pruebas usan SQLite en el equipo del grupo con personas ficticias, así que hoy no hay transferencia. Antes del piloto, revisar las obligaciones de comunicación a la ANPD que fije el Reglamento.

## Método de calificación

Cada riesgo se califica por probabilidad (P) e impacto (I): B = bajo (1), M = medio (2), A = alto (3). El nivel es P × I: **bajo** si vale 1–2, **medio** si vale 3–4 y **alto** si vale 6–9. El riesgo residual usa la probabilidad y el impacto que quedan después de las medidas: una medida puede bajar la probabilidad (un control de acceso probado) o el impacto (el cifrado, o un presupuesto que acota la pérdida). La categoría sigue LINDDUN. El riesgo residual presupone que funcionan los controles descritos; los responsables deben reevaluarlo al desplegar.

## Riesgos y acciones

| # | Etapa | Escenario de riesgo | LINDDUN | Inicial (P/I) | Residual (P/I) |
|---|---|---|---|---|---|
| R1 | Acceso | Un entrenador o cliente consulta la ficha de otro cliente (IDOR) | Disclosure | Alto (M/A) | Medio (B/A) |
| R2 | Estadística | Comparar promedios publicados permite reconocer la rutina de una persona | Linkability, Identifiability | Alto (M/A) | Medio (B/A) |
| R3 | Estadística | Republicar el mismo mes con ruido nuevo hasta promediarlo | Disclosure | Alto (M/A) | Bajo (B/M) |
| R4 | Recolección | Participar en la estadística se percibe como condición del servicio | Non-compliance, Unawareness | Alto (M/A) | Bajo (B/M) |
| R5 | Conservación | Robo de la base o de un respaldo con datos de salud en claro | Disclosure | Alto (M/A) | Medio (M/M) |
| R6 | Preparación | Fechas y patrones de actividad permiten reidentificar a pesar del seudónimo | Linkability | Medio (M/M) | Medio (M/M) |
| R7 | Uso | Una predicción sesgada cambia el plan de una persona | Ética: sesgo | Alto (M/A) | Bajo (B/M) |
| R8 | Estadística | Personas con pocos días quedan subrepresentadas, o el tope subestima a las muy activas | Ética: sesgo | Medio (A/B) | Medio (A/B) |
| R9 | Respaldo | Restaurar un respaldo antiguo "devuelve" presupuesto ya gastado | Disclosure | Medio (B/A) | Medio (B/A) |

| # | Medida implementada | Cómo se verifica | Responsable |
|---|---|---|---|
| R1 | La API autoriza cada objeto por rol y por propietario, y audita las denegaciones. | Probado: el cliente recibe 403 al pedir la ficha de otro; el entrenador recibe 403 con un cliente no asignado. | Equipo de backend |
| R2 | Privacidad diferencial ε = 1 a nivel de persona, aporte acotado y umbral sobre el conteo con ruido. | Prueba de sensibilidad, experimento de 300 simulaciones y análisis con 30 semillas independientes. | Responsable de analítica |
| R3 | Presupuesto global ε = 2, cargo y publicación en la misma transacción, resultado guardado. | Probado: publicar dos veces devuelve el mismo valor y no gasta más ε. | Operador técnico |
| R4 | Pantalla de consentimiento con el propósito explicado, opción desactivada por defecto, retiro y registro de la preferencia. El cliente conserva su plan. | Recorrido en "Mi privacidad". | Responsable del club |
| R5 | Cifrado AES-256-GCM por campo con datos asociados. Respaldo cifrado con otra clave. Rotación de claves. | Una manipulación invalida el descifrado. Pruebas de respaldo y verificación. | Operador técnico |
| R6 | Seudónimo HMAC con clave separada. Los CSV originales quedan fuera de Git y de los paneles. | Revisión del repositorio y `.gitignore`. | Equipo de datos |
| R7 | El modelo se queda en el notebook (laboratorio). Revisión humana obligatoria y comparación de utilidad por grupo. Las categorías disponibles dejan fuera otras experiencias. | Sección de modelado del informe. | Entrenador y equipo de datos |
| R8 | Promedio por persona. El efecto del tope se cuantifica y se publica (34,69 → 34,05 en abril). | Informe, secciones de privacidad diferencial y robustez. | Equipo de datos |
| R9 | Procedimiento operativo (no automatizado): tras restaurar un respaldo, y antes de publicar, el operador compara el gasto registrado con las publicaciones ya divulgadas y no publica si no coinciden. | `backup verify` comprueba que el gasto coincide con las publicaciones del propio respaldo. La comparación con lo divulgado es manual. | Operador técnico |

En R1 y R2 las medidas bajan la probabilidad, pero el impacto sigue alto porque una falla expondría datos de salud. En R3 el presupuesto acota la pérdida máxima (ε = 2 en total). En R5 el cifrado reduce el impacto de un robo. En R7 la revisión humana impide que una predicción cambie un plan por sí sola.

R6 sigue en medio porque el seudónimo impide recuperar el identificador original, pero no cambia las fechas ni los patrones diarios, que son lo que permite vincular a una persona; las fechas no se generalizan porque el seguimiento individual las necesita. R8 sigue en medio porque el tope y el voto por persona son parte del método y se aplican en cada publicación (en abril el tope afectó a una persona); las medidas cuantifican y publican el efecto, y el impacto ya era bajo porque la cifra es grupal. En R9 la medida es manual y no baja la probabilidad ni el impacto, así que el residual es igual al inicial: la probabilidad ya era baja porque restaurar un respaldo antiguo es excepcional, y el impacto sigue alto porque se podría superar el presupuesto declarado sin que nadie lo note. Automatizar esa comparación queda pendiente. Ningún riesgo residual queda en nivel alto.

## Consulta a los afectados

La demo usa personas ficticias, así que aún no se consultó a clientes reales. Antes del piloto, el responsable del club enviará un aviso a los socios que explique qué datos se tratarán, la estadística grupal, el carácter opcional del consentimiento y el alojamiento fuera del país, junto con una encuesta breve (si se entiende la pantalla de consentimiento, si alguien se siente obligado a participar y qué usos les preocupan). Además, se probará la pantalla "Mi privacidad" con un grupo pequeño de socios. Los resultados se incorporarán a esta evaluación y, si hace falta, cambiarán las medidas.

## Decisión ética de diseño

Un día sin reloj no equivale a un día inactivo. La adherencia se calcula con sesiones programadas y declaradas como cumplidas. La barra de progreso usa una meta acordada y señala si faltan mediciones corporales. La alerta avisa de una sesión pendiente. El entrenador comprueba lo ocurrido con el cliente antes de cambiar el plan. La analítica grupal tiene ruido deliberado y se presenta con su unidad y periodo para evitar decisiones individuales basadas en una estimación del grupo.

**Antes de un piloto real:** desplegar con TLS, firmar los contratos de encargo y documentar la región de alojamiento; definir un plazo de conservación y una vía de eliminación verificable, incluidas las copias; acordar quién atiende las solicitudes de acceso, rectificación, cancelación y oposición (la aplicación todavía no permite que el cliente exporte o borre sus propios datos, así que por ahora se atenderían de forma manual y automatizarlo queda como trabajo futuro); definir un periodo de renovación del presupuesto ε (en la demo es global y fijo, solo dos publicaciones) y declarar la pérdida acumulada entre periodos; inscribir el banco de datos ante la ANPD; realizar la consulta a los socios; y ensayar un incidente con el equipo, incluida la comunicación a la ANPD dentro del plazo de 48 horas que establece el Reglamento (D.S. 016-2024-JUS). Esta evaluación de diseño registra esas decisiones pendientes.
