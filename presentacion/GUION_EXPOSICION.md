# Guion de exposición — Alzace Fitness (DS3031)

Versión de la presentación definitiva de **18 diapositivas**. Las cifras proceden de `evidence/experimentos.json`, `evidence/robustez.json` y el informe final. La decisión de la DPIA es **demostración académica**, sin aprobación de piloto real.

**Reparto:** Josué expone las diapositivas 1–16 y 18; Joel realiza la demostración de la 17. Los tiempos son orientativos.

| Diap. | Tema | Quién | Tiempo |
|---:|---|---|---:|
| 1 | Alzace Fitness | Josué | 0:30 |
| 2 | Lo que pedía el proyecto final | Josué | 0:35 |
| 3 | Datos de salud en el entrenamiento virtual | Josué | 0:45 |
| 4 | Dos fuentes, analizadas por separado | Josué | 0:45 |
| 5 | Arquitectura y protección de datos | Josué | 0:50 |
| 6 | Fitbit: mecanismo y presupuesto | Josué | 1:00 |
| 7 | Por qué IBM diffprivlib 0.6.6 | Josué | 0:50 |
| 8 | Fitbit: elección de ε y robustez | Josué | 1:00 |
| 9 | Gym: metodología del clasificador | Josué | 0:45 |
| 10 | Gym: ε elegido en validación | Josué | 0:50 |
| 11 | Gym: utilidad y diferencias por grupo | Josué | 1:00 |
| 12 | DPIA: ciclo de vida y confianza | Josué | 0:45 |
| 13 | DPIA: LINDDUN y nueve riesgos | Josué | 0:50 |
| 14 | Ética: interpretar límites y consentimiento | Josué | 0:45 |
| 15 | Seguridad y tríada CIA | Josué | 0:55 |
| 16 | Cumplimiento y limitaciones | Josué | 0:40 |
| 17 | Demostración: el presupuesto se agota | Joel | 3:00 |
| 18 | Conclusiones | Josué | 0:50 |

## Exposición por diapositiva

### 1. Alzace Fitness — Josué

Proyecto final DS3031: Alzace Fitness. Se presenta una demostración académica local; no se solicita aprobación de piloto con clientes reales.

### 2. Lo que pedía el proyecto final — Josué

Requisitos de negocio, privacidad y técnica del esquema final. La evidencia se resume en los resultados y la DPIA; los límites operativos quedan explícitos.

### 3. Datos de salud en el entrenamiento virtual — Josué

Fitbit permite estimar medias grupales de minutos activos en meses observados; estos datos no demuestran tendencias temporales. Los datos de salud son sensibles bajo la Ley 29733.

### 4. Dos fuentes, analizadas por separado — Josué

Fitbit y Gym se analizan por separado. No comparten un identificador verificable; unirlos al azar inventaría personas. Fitbit tiene 33 participantes y 940 días persona en el archivo, de los que 611 son de abril y 329 de mayo. La protección Fitbit es por persona.

### 5. Arquitectura y protección de datos — Josué

Next.js presenta la interfaz; FastAPI comprueba rol y titular en cada operación; SQLite es la base de la demo. HMAC-SHA-256 transforma IDs Fitbit, sin volver anónimos los registros: fechas y patrones permanecen potencialmente vinculables. AES-256-GCM cifra datos almacenados. La privacidad diferencial centralizada se aplica en la API a la salida estadística grupal, antes de publicar. PostgreSQL no quedó verificado en esta ejecución.

### 6. Fitbit: mecanismo y presupuesto — Josué

Vecindad: agregar o remover todos los días de una persona. El aporte de cada persona es su media de días observados, acotada a 0–120. Tras centrar en 60, la sensibilidad de la suma es 60; la del conteo es 1. Se asigna 0,5 a cada mecanismo Laplace, así que la composición secuencial ideal da (1,0)-DP. Umbral basado en el conteo ruidoso, cociente, recorte y redondeo son posprocesamiento. La API limita el presupuesto global a 2 y guarda resultado y gasto transaccionalmente; la restauración antigua es un riesgo residual.

### 7. Por qué IBM diffprivlib 0.6.6 — Josué

IBM diffprivlib 0.6.6 está fijada en backend/requirements.txt y requirements-lock.txt. Holohan, Braghin, Mac Aonghusa y Levacher (2019) describen la biblioteca y sus mecanismos: https://arxiv.org/abs/1907.02444. Holohan y Braghin (2021) estudian un ataque concreto por inversión del muestreo de Laplace a precisión finita y una solución de muestreo: https://arxiv.org/abs/2107.10138. NIST SP 800-226, Guidelines for Evaluating Differential Privacy Guarantees (2025), explica factores de evaluación y peligros de implementación: https://csrc.nist.gov/pubs/sp/800/226/final. Estas fuentes respaldan la elección técnica y la cautela al declarar garantías, pero no validan automáticamente toda la implementación ni recomiendan ε=1, tope de 120 minutos o tolerancia de MAE de cinco minutos para Alzace; son elecciones académicas evaluadas con los experimentos.

### 8. Fitbit: elección de ε y robustez — Josué

La selección Fitbit es ε=1 por el criterio académico de MAE hasta cinco minutos y al menos 95 % de respuestas, fijado para una media de unos 34 minutos diarios. La primera simulación de abril registró MAE 4,715 y respuesta 100 %. Robustez: 30 semillas con 300 simulaciones cada una; abril tope 120 MAE 4,131, DE 0,235, IC 4,044–4,219; mayo 4,632, DE 0,258; abril tope 90 2,902; abril tope 150 5,424 y no satisface el umbral. Estos IC solo capturan variación entre semillas sobre participantes fijos. No demuestran tendencias temporales. Fuente: evidence/experimentos.json y evidence/robustez.json.

### 9. Gym: metodología del clasificador — Josué

Gym usa 973 registros: 510 de entrenamiento, 171 de validación y 292 de prueba, estratificados por clase. Predice sesión de al menos 75 minutos mediante experiencia y frecuencia semanal. El umbral es didáctico y no clínico. El histograma tiene 42 celdas; bajo vecindad por fila de entrenamiento su sensibilidad L1 es 1, y cada celda recibe ruido Laplace de escala 1/ε. Recortar conteos negativos y suavizar son posprocesamiento. La selección y métricas exactas de validación o prueba no heredan automáticamente la garantía del histograma con epsilon fijo.

### 10. Gym: ε elegido en validación — Josué

La regla se aplica exclusivamente a validación: seleccionar el menor ε con una pérdida media de accuracy y balanced accuracy de a lo sumo cinco puntos porcentuales frente al histograma sin ruido, y brecha TPR a lo sumo 0,15. Los cuatro candidatos cumplen; se elige ε=0,1. Las tolerancias son decisiones académicas para este caso y no estándares científicos. La fuente Gym y resultados de prueba anteriores ya se habían observado en una versión previa; la prueba final se debe interpretar descriptivamente. Fuente: evidence/experimentos.json y evidence/robustez.json.

### 11. Gym: utilidad y diferencias por grupo — Josué

Tras seleccionar ε=0,1 en validación, se reajustó el histograma y se evaluó en prueba. Exactitud sin ruido 68,49 %; privada 66,21 %, pérdida de 2,28 puntos. Exactitud balanceada 68,07 % y 66,44 %. La referencia trivial de clase mayoritaria es 52,05 %. La exactitud Female cambia de 66,67 % sin DP a 64,28 % con DP; Male de 70,27 % a 68,09 %. En el modelo privado, Female n=144, TPR 0,5905, FPR 0,3019; Male n=148, TPR 0,6265, FPR 0,2586. Brechas TPR 0,036 y FPR 0,043. Estas diferencias de una partición no identifican causa ni demuestran ausencia de sesgo. El ataque de inferencia de membresía obtuvo AUC 0,5369 sin ruido y 0,5379 con DP; este ensayo no demuestra una reducción empírica del riesgo, aunque la garantía matemática del histograma tenga su propio alcance. La prueba ya había sido observada históricamente; no confirma generalización independiente. Fuente: evidence/experimentos.json.

### 12. DPIA: ciclo de vida y confianza — Josué

La DPIA recorre recolección, preparación, conservación, acceso, análisis, publicación, respaldo/restauración y eliminación. La primera frontera va de archivos originales a servidor; la segunda de la API al navegador y a las estadísticas publicadas. Los CSV locales conservan identificadores. HMAC crea seudónimos, pero fechas y patrones siguen siendo potencialmente identificables. La conservación y eliminación operativas no se han validado. Restaurar una copia antigua podría retroceder el presupuesto: R9 permanece alto para producción.

### 13. DPIA: LINDDUN y nueve riesgos — Josué

LINDDUN orientó la identificación de amenazas de vinculación, identificación, revelación y falta de cumplimiento; no cuantifica por sí solo probabilidad. Riesgo inicial y residual se clasifican cualitativamente a partir de probabilidad e impacto, tal como detalla el informe. R1 acceso cruzado alto a bajo; R2 reconocimiento alto a medio; R3 repetición con ruido nuevo alto a bajo; R4 consentimiento condicionado alto a bajo; R5 robo de base o respaldo alto a medio; R6 reidentificación por fechas medio a medio; R7 modelo sesgado alto a bajo solo en demo; R8 cobertura y clipping medio a medio; R9 restauración de presupuesto medio a alto para producción. En R9, el procedimiento no impide automáticamente reutilizar presupuesto anterior tras una restauración, por lo que el residual se eleva. Los responsables y evidencias están en la tabla. No se aprueba piloto real.

### 14. Ética: interpretar límites y consentimiento — Josué

El análisis por grupos muestra diferencias descriptivas de una sola partición. No atribuimos causalidad al ruido ni afirmamos ausencia de sesgo. Transparencia exige comunicar que Fitbit estima medias grupales bajo clipping y ruido, y que el modelo Gym es de laboratorio. La opción de analítica está separada y desactivada por defecto; se puede retirar, aunque una publicación ya realizada no se revierte. El consentimiento opcional de estadísticas no sustituye los requisitos legales para el tratamiento principal de datos de salud. No se validó la comprensión con usuarios reales.

### 15. Seguridad y tríada CIA — Josué

Tríada CIA: confidencialidad por autorización, HMAC y AES-256-GCM; integridad por etiqueta autenticada GCM y AAD que vincula tabla, titular, fecha y versión de clave; disponibilidad por respaldo cifrado y restauración verificada. AES-GCM usa clave de 256 bits y nonce aleatorio de 96 bits por cifrado. bcrypt usa sal individual y coste 12 en la demo. La copia no resuelve el riesgo R9 de retroceso del presupuesto. Evidencia final: 12 pruebas automáticas aprobadas y una omitida por falta de PostgreSQL externo; tres notebooks ejecutados; compilación de frontend correcta. El escaneo ZAP fue pasivo, con tres alertas informativas y cuatro estados de acceso: sin sesión y tres roles. No hay despliegue cloud verificado ni ZAP activo. Rotación: detener escrituras, copiar, generar versión AES nueva, recifrar transaccionalmente y mantener versiones antiguas hasta expirar respaldos. HMAC requiere migración separada; no hay rotación automática.

### 16. Cumplimiento y limitaciones — Josué

Matriz de cumplimiento académico según el informe final y REVISION_FINAL_RUBRICA.md: se implementaron y evaluaron privacidad diferencial, utilidad de análisis y modelado, DPIA del ciclo de vida, reflexión sobre sesgo, transparencia y consentimiento, una base de datos, frontend y backend, y justificación científica de librería y parámetros. Tres notebooks ejecutados y 12 pruebas aprobadas; una prueba PostgreSQL se omitió al faltar la base externa. La utilidad se considera cumplida dentro del alcance experimental. Limitaciones: la prueba Gym ya se había observado históricamente; no demuestra generalización; no se verificó despliegue real con TLS ni ZAP activo; conservación y eliminación operativas faltan; R9 mantiene residual alto para producción. La decisión es demostración académica, sin aprobación de piloto real.

### 17. Demostración: el presupuesto se agota — Joel

Recorrido local propuesto: el cliente registra medición y consentimiento; el entrenador ve únicamente asignados y recibe 403 al intentar una ficha ajena. El administrador publica abril y consume una unidad de ε. Republicar abril devuelve exactamente el valor guardado y no gasta presupuesto. Publicar mayo consume la segunda unidad, total 2. Una tercera consulta distinta se rechaza con HTTP 409 por presupuesto agotado. Se abre la auditoría y se muestran los eventos de denegación y publicación. La demostración es académica y no autoriza uso con clientes reales.

### 18. Conclusiones — Josué

Cierre: Fitbit protege a la persona al publicar una media grupal mediante suma y conteo ruidosos. El error observado responde a un criterio académico y no establece tendencias temporales. En Gym la privacidad del histograma con epsilon fijo se acompaña de una pérdida descriptiva de 2,28 puntos de exactitud y diferencias por grupo que requieren estudio nuevo. La selección y publicación de métricas exactas no heredan automáticamente DP. El riesgo de retroceso del presupuesto al restaurar queda alto; la DPIA permite únicamente la demostración académica, sin aprobación de piloto real. Gracias.

## Demostración en vivo — Joel, diapositiva 17

### Preparación

1. Usar un estado **local y descartable** de la demo con presupuesto sin gastar. Confirmar que `data/raw/`, `.local/`, bases y llaves no se subieron al repositorio.
2. En la carpeta del proyecto, activar el entorno Python y levantar el servicio con `./scripts/iniciar.ps1` en PowerShell. Abrir `http://127.0.0.1:3000` y comprobar la salud de la API.
3. Si la demo local aún no tiene datos, ejecutar `python -m backend.cli init` y `python -m backend.cli import-fitbit data/raw/dailyActivity_merged.csv` con un CSV local autorizado. No reiniciar un estado que deba conservarse.
4. Preparar los usuarios ficticios: Lucía Valle (cliente de Diego Ríos), Mateo Rojas (cliente de Eva Lira), Diego Ríos (entrenador) y Alex Vega (administrador).

### Recorrido visible

1. **Cliente:** entrar como Lucía, registrar una medición y mostrar que el consentimiento de analítica empieza desactivado, se activa y se puede retirar.
2. **Entrenador:** entrar como Diego. Mateo no aparece entre sus asignados. Intentar pedir su ficha directamente al servidor; debe responder **403**. Una consulta de ejemplo desde la consola, si la sesión y la ruta de demo siguen disponibles:
   ```js
   fetch('/api/clients/demo-mateo',{headers:{'x-alzace-request':'web'}}).then(r=>r.status)
   ```
3. **Administrador:** entrar como Alex y publicar abril de 2016 con ε = 1. El presupuesto pasa de 0 a 1. La referencia acotada del laboratorio es 34,05 min/día; la salida de la API contiene ruido y puede variar entre instalaciones.
4. **Repetición:** solicitar abril otra vez. Debe devolverse exactamente el valor guardado, sin gasto adicional.
5. **Segundo mes:** publicar mayo; el gasto global llega a ε = 2.
6. **Nueva consulta:** intentar publicar otra combinación aún no publicada. Mostrar el bloqueo por presupuesto y, en la respuesta de la API, **HTTP 409**.
7. **Auditoría:** abrir los eventos de publicación y denegación. Explicar que el registro no debe incluir contraseñas ni mediciones.

Si la interfaz o el servicio fallan, explicar el resultado esperado desde las pruebas y el informe. No presentar capturas antiguas ni afirmar que se ejecutó un paso que no pudo mostrarse.

## Preguntas probables

- **¿Por qué ε = 1 en Fitbit y 0,1 en Gym?** Son mecanismos y unidades protegidas diferentes. Fitbit usa una persona completa y eligió ε = 1 con MAE ≤ 5 min y ≥ 95 % de respuestas en abril. Gym eligió 0,1 únicamente en validación según utilidad y brecha TPR.
- **¿El modelo pierde utilidad?** En la prueba Gym, la exactitud pasó de 68,49 % a 66,21 %, una pérdida descriptiva de 2,28 puntos. El conjunto de prueba ya se había observado antes, así que no confirma generalización independiente.
- **¿Se redujo el riesgo de membresía?** El AUC fue 0,5369 sin ruido y 0,5379 con DP. Este ensayo no demuestra una reducción empírica. La garantía formal declarada corresponde al histograma con ε fijo y vecindad por fila.
- **¿El modelo es equitativo?** En la partición evaluada, TPR privado Female/Male = 0,5905/0,6265 y FPR = 0,3019/0,2586. No atribuimos causalidad ni afirmamos ausencia de sesgo.
- **¿Qué falta para clientes reales?** R9, el retroceso del presupuesto al restaurar, permanece alto; también faltan conservación y eliminación operativas, validación de consentimiento con personas reales y despliegue verificado. La DPIA no aprueba un piloto.
- **¿Qué protege cada técnica?** HMAC seudonimiza IDs Fitbit; AES-256-GCM cifra mediciones almacenadas; la API autoriza cada objeto; DP centralizada limita la influencia de una persona en la estadística publicada. Ninguna sustituye a las demás.
