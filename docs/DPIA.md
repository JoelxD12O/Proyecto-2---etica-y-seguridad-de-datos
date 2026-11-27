# Evaluación de impacto del prototipo

**Alcance y finalidad.** El club propone usar actividad, sueño, frecuencia cardíaca, peso y grasa corporal para acompañar entrenamientos solicitados por el cliente. El uso secundario de actividad para estimar medias grupales es opcional. El club es el responsable propuesto. El entrenador actúa dentro de su asignación. El operador técnico custodia claves, respaldos y el presupuesto de privacidad. Supabase y Render serían proveedores del despliegue. La demostración local utiliza personas ficticias. Un archivo de investigación importado solo alimenta la estadística del estudio.

| Etapa | Datos y acceso | Decisión y riesgo residual |
|---|---|---|
| Obtención | CSV de investigación locales, registros voluntarios del programa | Documentar origen y finalidad. El permiso original de un estudio no autoriza contactar a participantes ni convertirlos en clientes. Antes de una operación real, definir y documentar la base para el seguimiento y revisar los términos de las fuentes. |
| Preparación | El operador valida actividad por persona y día. El identificador de origen se reemplaza por HMAC con clave independiente | Fechas y patrones de actividad pueden permitir vinculación incluso con seudónimo. Los archivos originales quedan fuera de Git y de los paneles. El modelo Gym se evalúa en su propia fuente. |
| Conservación | Mediciones y metas cifradas en el servidor. Las fechas y relaciones necesarias para autorizar consultas quedan visibles a la base | Separar claves y almacenamiento y restringir el operador. Definir un plazo de conservación y una vía de eliminación verificable antes de incorporar clientes reales. |
| Acceso individual | El cliente y su entrenador asignado consultan la ficha. Se registra el acceso. El administrador consulta eventos y publicaciones | Probar el intento de acceso cruzado, revisar asignaciones y retirar permisos al terminar una relación. El entrenador puede ver información sensible durante una sesión autorizada. |
| Estadísticas | El administrador publica una estimación por mes. El entrenador lee lo ya publicado. La participación de clientes operativos empieza desactivada | Mostrar propósito, método y efecto de retirar el permiso. Las consultas nuevas toman la preferencia vigente. Un resultado previamente divulgado permanece en el historial. |
| Respaldo y cierre | Copia cifrada y restauración verificada en entorno aislado | La operación requiere responsables, copias fuera del equipo, expiración verificable y recuperación del historial de publicaciones. Un borrado debe contemplar copias, accesos y plazo de purga. |

## Transferencia internacional prevista

El modo alojado propuesto usaría Supabase y Render fuera del equipo local. Antes de operar con clientes reales, el club debe documentar la región de alojamiento, los contratos con cada proveedor y las obligaciones aplicables de la Ley 29733 y su Reglamento. La API cifra las mediciones por campo antes de almacenarlas en la base; las claves no se guardan en el proveedor de la base de datos. El aviso al cliente debe explicar dónde se tratarían sus datos. La demostración actual usa SQLite local y personas ficticias; no se verificó un despliegue alojado.

## Riesgos y acciones

La prioridad combina probabilidad e impacto en esta demo. Se usa una escala cualitativa de probabilidad e impacto (bajo, medio, alto); la combinación con impacto alto y probabilidad media o alta se considera alta. El riesgo residual solo disminuye cuando el control está implementado y existe una prueba o un artefacto verificable. Los responsables propuestos deben reevaluarla al desplegar.

| Escenario y daño | Riesgo inicial → residual | Medida, comprobación y responsable |
|---|---|---|
| Un entrenador consulta medidas de otro cliente | Alto → medio | Autorizar cada objeto en la API y auditar denegaciones. Prueba con dos clientes de distintos entrenadores. Equipo backend. |
| Un tercero reconoce una rutina al comparar promedios | Alto → medio | Acotar un aporte por persona, perturbar suma y conteo, fijar consultas y conservar resultados. Pruebas de simultaneidad y presupuesto. Responsable de analítica. |
| Un perfil con menos días registrados queda subrepresentado, o el tope penaliza a personas muy activas | Medio → medio | Promediar por persona, distinguir ausencias y cuantificar el efecto del tope. En abril cambió la media de 34,69 a 34,05. Equipo de datos. |
| Una predicción sesgada cambia el plan de una persona | Alto → bajo en la demo | Restringir el modelo al laboratorio, comparar utilidad por grupo y mantener revisión humana. Las categorías disponibles dejan fuera otras experiencias. Entrenador y equipo de datos. |
| La participación en estadísticas se percibe como una condición del servicio | Alto → bajo | Pantalla de consentimiento con propósito, opción desactivada por defecto, retiro y registro de la preferencia. El cliente conserva acceso a su plan. Responsable del club. |
| Se filtra una copia o se vuelve a publicar tras restaurar un presupuesto antiguo | Alto → alto para producción | La copia se cifra y verifica, pero no se ha probado conciliación externa del presupuesto después de restaurar. Operador: bloquear nuevas publicaciones hasta verificar el historial. |

## Riesgos que permanecen abiertos

| Amenaza (LINDDUN) | Exposición y tratamiento pendiente | Responsable y decisión |
|---|---|---|
| Vinculación e identificación | Un seudónimo HMAC no oculta fechas ni patrones singulares de actividad. Datos auxiliares podrían permitir reconocer a una persona. No se ha medido este riesgo con un ataque de enlace específico. | Equipo de datos: limitar acceso a fechas y estudiar agregación antes de un piloto. Riesgo residual no cuantificado. |
| Inferencia de atributos y salud | El acceso legítimo a varias mediciones puede revelar hábitos o condiciones sensibles. El cifrado protege el almacenamiento, no impide que un usuario autorizado infiera información. | Club y entrenadores: necesidad de acceso por función, formación y revisión periódica. Riesgo residual medio. |
| Inferencia de membresía | En el laboratorio Gym el AUC del ataque por confianza fue cercano a 0,5 tanto sin protección como con ruido. Ese resultado no demuestra una reducción empírica del riesgo. | Equipo de datos: mantener el modelo fuera del servicio y reevaluar con una amenaza definida antes de publicarlo. |
| Compromiso de claves y restauración | La demo guarda claves locales. Un respaldo que reponga un presupuesto antiguo permitiría nuevas publicaciones sobre el mismo grupo. | Operador: custodiar claves fuera de la base, registrar rotación y conciliar historial y presupuesto antes de permitir publicaciones tras restaurar. Sin validación operativa, riesgo residual alto para producción. |

La decisión de esta DPIA se limita a la demostración académica. El despliegue con datos de clientes reales requiere demostrar consentimiento para el tratamiento principal de salud, plazos y eliminación, custodia de claves, respuesta a incidentes y restauración sin retroceso del presupuesto. Hasta entonces no se considera aprobado un piloto real.

## Consulta a los afectados

La demo usa personas ficticias, así que no se ha consultado a clientes reales. Antes de cualquier piloto, el club debe presentar un aviso sobre datos tratados, estadística grupal opcional y alojamiento propuesto, y comprobar con usuarios si comprenden la pantalla de consentimiento y si sienten presión para participar. Sus respuestas deberán incorporarse a una nueva evaluación de riesgos.

## Decisión ética de diseño

Un día sin reloj no equivale a un día inactivo. La adherencia se calcula con sesiones programadas y declaradas como cumplidas. La barra de progreso usa una meta acordada y señala si faltan mediciones corporales. La alerta avisa de una sesión pendiente. El entrenador comprueba lo ocurrido con el cliente antes de cambiar el plan. La analítica grupal tiene ruido deliberado y se presenta con su unidad y periodo para evitar decisiones individuales basadas en una estimación del grupo.

**Antes de un piloto real**, acordar quién atiende solicitudes de acceso, rectificación y eliminación, revisar la conservación y las transferencias de los proveedores elegidos, verificar consentimiento y accesibilidad con usuarios y ensayar un incidente con el equipo. Esta evaluación de diseño registra esas decisiones pendientes. La decisión coincide con el informe: demostración académica permitida, piloto real no aprobado mientras R9 siga alto.

## Conciliación con los nueve riesgos del informe

La numeración y los residuales siguientes corresponden a la sección «Evaluación de impacto (DPIA)» del informe. La probabilidad y el impacto son juicios cualitativos; no son tasas observadas. Solo se atribuye una reducción de riesgo al alcance efectivamente probado.

| Riesgo | Control implementado y evidencia | Responsable | Residual y límite |
|---|---|---|---|
| R1 Acceso cruzado | Autorización por objeto en `backend/service.py`; `test_acl_csrf_sessions` | Backend | Bajo en demo; revisar asignaciones reales |
| R2 Reconocimiento por estadísticas | `backend/privacy.py`, media por persona y `evidence/experimentos.json` | Analítica | Medio; no se midió enlace con datos auxiliares |
| R3 Repetición con ruido nuevo | Transacción y caché en `backend/service.py`; `test_concurrent_release_cache_and_budget` | Backend | Bajo en demo; depende de conservar el historial |
| R4 Consentimiento condicionado | Preferencia inicialmente desactivada y revocable; `test_consent_selects_contributors` | Club | Bajo en demo; validar comprensión con usuarios reales |
| R5 Robo de base o copia | AES-GCM, AAD y respaldo cifrado; `test_measurements_aad_rotation_backup` | Operador | Medio; custodia operativa de llaves pendiente |
| R6 Reidentificación por fechas | HMAC en `backend/vault.py::pseudo`; las fechas siguen visibles | Datos | Medio; falta ensayo de reidentificación |
| R7 Modelo sesgado | Modelo solo offline; `backend/experiment.py` y notebook 03 | Datos y entrenador | Bajo solo en demo; no se autoriza uso decisorio |
| R8 Cobertura y clipping | 34,692 frente a 34,048 min/día en `evidence/experimentos.json` | Datos | Medio; evaluar otros periodos y límites |
| R9 Restauración de presupuesto | Respaldo cifrado en `backend/backup.py`; no hay prueba de conciliación externa | Operador | Alto para producción; bloquear publicaciones tras restauración hasta verificar gasto |

El flujo cruza archivos originales, importación, base, API, navegador y publicación. También incluye respaldo, restauración y eliminación. El identificador Fitbit se transforma mediante HMAC-SHA-256 antes de insertarse en la base de investigación; el seudónimo, fechas, fuente y patrón de actividad aún permiten vinculación potencial. Seudonimización no equivale a anonimización: quien posee la clave puede reconstruir la correspondencia por ensayo de identificadores. AES-GCM protege mediciones almacenadas; la privacidad diferencial protege la salida estadística bajo su vecindad declarada. Gym y Fitbit no comparten identificador verificable; `backend/seedfiles.py` construye solo perfiles simulados locales, etiquetados como tales.
