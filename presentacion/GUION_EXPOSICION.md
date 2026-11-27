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

## Demostración en vivo — Joel (diapositiva «Demostración: el presupuesto se agota», la 14 de la presentación de 15)

### Preparación (30 min antes)

1. Cerrar Docker Desktop, Zoom, Spotify y pestañas que no se usen.
2. En PowerShell, ir a la carpeta del proyecto:
   ```powershell
   cd "C:\Users\Joel\Desktop\2026-2\Etica y seguridad de datos\Proyecto-2---etica-y-seguridad-de-datos"
   ```
3. Si el presupuesto no está en 0 de 2, reiniciar el estado local de la demo (es descartable):
   ```powershell
   Remove-Item .local\demo.sqlite3
   $env:ALZACE_MODE="demo"; $env:ALZACE_STATE="$PWD\.local"; $env:DATABASE_URL=""
   .\.venv\Scripts\python -m backend.cli init
   .\.venv\Scripts\python -m backend.cli import-fitbit data\raw\dailyActivity_merged.csv
   ```
4. Levantar la app y dejar la ventana abierta:
   ```powershell
   .\scripts\iniciar.ps1
   ```
   Si dice que el puerto 3000 está ocupado, la app ya está corriendo.
5. Abrir http://127.0.0.1:3000.
6. F12 → Console → escribir `allow pasting` → Enter → F12 para cerrar.
7. Tener copiada la consulta:
   ```js
   fetch('/api/clients/demo-mateo',{headers:{'x-alzace-request':'web'}}).then(r=>r.status)
   ```
8. No publicar nada para probar.

**Usuarios ficticios**

| Usuario | Rol | Detalle |
|---|---|---|
| Lucía Valle | Clienta | Asignada al entrenador Diego Ríos |
| Mateo Rojas | Cliente | Asignado a la entrenadora Eva Lira |
| Diego Ríos | Entrenador | Solo ve a sus clientes asignados |
| Alex Vega | Administrador | Publica estadísticas y ve la auditoría |

### Guion

**Inicio**
Gracias, Josué. Ahora lo vemos funcionando en la app. Tiene tres roles, cliente, entrenador y administrador, y cada uno ve solo lo que necesita. Usamos usuarios ficticios. Lucía y Mateo son clientes, Diego es entrenador y Alex es el administrador.
*(Alt+Tab al navegador)*

**Rol 1 – Cliente (Lucía)**
*(«Cliente» → «Entrar al panel»)*
Primero entro como Lucía, que es una clienta. Ella tiene dos módulos, Mi actividad y Mi privacidad.
*(Muestra el resumen)*
En Mi actividad ve su ritmo de actividad, su meta y el plan que le dio su entrenador. Solo sus datos, de nadie más.
*(«Registrar medición» → 47 minutos, 4321 pasos → «Guardar»)*
Registro una medición. En la base de datos no queda en texto claro, se cifra con AES-256-GCM y queda amarrada a Lucía y a ese día.
*(«Mi privacidad» → «Permitir uso grupal» → «Retirar permiso»)*
En Mi privacidad, Lucía decide si su actividad cuenta para las estadísticas del club. Es aparte del servicio y empieza apagado. Lo puede activar y retirar igual de fácil, y si no acepta, su entrenador la sigue atendiendo. Lo que ya se publicó no se revierte, y la pantalla lo explica.
*(«Cerrar sesión»)*

**Rol 2 – Entrenador (Diego)**
*(«Entrenador» → «Entrar al panel»)*
Ahora entro como Diego, que es entrenador. Tiene tres módulos, Mis clientes, Seguimiento y Estadísticas.
*(Abre el selector «Cliente asignado»)*
En Mis clientes solo aparecen los clientes que tiene asignados. Mateo no está, porque es cliente de otra entrenadora.
*(Elige «Lucía Valle»)*
Diego sí ve los datos de Lucía, porque los necesita para entrenarla, y desde aquí le asigna sesiones y metas.
Pero ocultar a Mateo en la pantalla no basta. Voy a pedir su ficha directo al servidor, como haría alguien que intenta saltarse la interfaz.
*(F12 → Console → pega la consulta → Enter)*
*(Aparece 403)*
El servidor responde 403, acceso denegado. El permiso se revisa en cada petición, no solo en la pantalla. Esto es lo que mitiga el riesgo R1 de la DPIA, el acceso cruzado.
*(F12 para cerrar → «Seguimiento»)*
En Seguimiento ve las sesiones que sus clientes no marcaron como hechas. Medimos la adherencia por sesiones cumplidas y no por días sin reloj, porque un día sin reloj no significa que la persona no entrenó.
*(«Cerrar sesión»)*

**Rol 3 – Administrador (Alex)**
*(«Administrador» → «Entrar al panel» → «Estadísticas»)*
Por último entro como Alex, el administrador. Piénsenlo como el gerente del gimnasio. No entrena a nadie, así que no ve los datos de ningún cliente, solo cómo va el grupo en general. Tiene tres módulos, Estadísticas, Auditoría y Operaciones.

En Estadísticas el club publica el promedio de minutos activos al día del grupo. Para abril de 2016 este promedio junta a las 33 personas del estudio Fitbit.
El problema es que un número exacto puede delatar a alguien. Por ejemplo, si comparo el promedio con una persona y sin ella, la resta me dice cuánto entrenó. Por eso usamos privacidad diferencial. Al número real le sumamos un poco de ruido al azar.

*(Señala el cuadro de arriba, «0 / 2 ε»)*
Aquí arriba está el presupuesto de privacidad. ε mide cuánta privacidad gasta cada publicación. Con ε chico hay más ruido y más privacidad, y con ε grande, menos ruido y menos privacidad. Para Fitbit elegimos ε igual a 1, que deja un error de unos 4 a 5 minutos sobre una media de unos 34. Cada publicación nueva suma 1, y el límite es 2.

*(Fuente «Estudio Fitbit», Periodo «2016-04» → «Publicar estimación · ε = 1»)*
Publico abril. La referencia sin ruido es 34,05 minutos y la app publica un número cercano, pero no el exacto. Sirve para estimar la media del grupo, pero ya no se puede saber si una persona concreta estaba o no. El contador sube a 1 de 2.

*(F5 → «Estudio Fitbit», «2016-04»)*
Si vuelvo a pedir el mismo mes, me da exactamente el número guardado y el contador no sube. Si recalculara cada vez, alguien podría pedirlo muchas veces, promediar los resultados y quitar el ruido.

*(Periodo «2016-05» → «Publicar estimación · ε = 1»)*
Ahora publico mayo y el contador llega a 2 de 2.
*(Fuente «Programa de entrenamiento»)*
El botón dice Presupuesto agotado. Ya no se puede publicar nada más, y si alguien se salta la pantalla, el servidor responde 409.
Hay un límite porque cada publicación filtra un poco de información y eso se acumula. Si se pudiera publicar infinitas veces, alguien juntaría los resultados y llegaría al dato real. En la demo el límite es fijo, 2 en total.

*(«Auditoría»)*
En Auditoría queda registrado lo que pasa en el sistema. Aquí están las dos publicaciones, y aquí el intento de Diego de ver a Mateo, marcado como Denegado. El registro es de solo inserción, no se puede modificar, y no guarda mediciones ni contraseñas, solo quién hizo qué y cuándo.

*(«Operaciones»)*
Y en Operaciones el administrador asigna qué entrenador atiende a qué cliente, que es lo que decide quién puede ver a quién. También registra incidentes de seguridad y gestiona las copias de seguridad cifradas.

**Cierre**
*(Alt+Tab al PowerPoint → Conclusiones)*
Eso es la demo. Cada rol ve solo lo que necesita, los datos de cada persona están cifrados y protegidos por permisos, y lo que se publica del grupo lleva ruido con un presupuesto limitado. Es una demostración académica local, no un piloto con clientes reales. Josué cierra con las conclusiones.

**Si algo falla:** explicar el resultado esperado según las pruebas y el informe. No presentar capturas antiguas ni afirmar que se ejecutó un paso que no pudo mostrarse.

### Preguntas que responde Joel

- **¿Por qué no publicar el número exacto?** Porque con números exactos se puede deducir a una persona, por ejemplo comparando el promedio con ella y sin ella. El ruido hace que el resultado sea casi igual esté o no esté.
- **¿A cuántas personas promedian?** A las 33 del estudio Fitbit en abril de 2016. Cada persona cuenta una vez, con su propio promedio acotado a 0–120 minutos.
- **¿Por qué solo 2?** Cada publicación filtra un poco y eso se suma. Con 2 cubrimos abril y mayo, los meses del estudio, y lo que se puede saber de cualquier persona queda acotado.
- **¿Son 2 por año?** En la demo son 2 en total. Renovarlo por periodo sería una decisión de producción y la privacidad perdida se acumularía; no está implementado.
- **¿Cómo evitan que alguien vea datos de otro?** El servidor revisa el rol y el titular de cada dato en cada petición. Lo vieron con el 403 de Mateo.
- **¿Dónde se cifran los datos?** Cada medición se cifra con AES-256-GCM antes de guardarse, con datos asociados que la amarran a su tabla, titular, fecha y versión de clave.


## Preguntas probables

- **¿Por qué ε = 1 en Fitbit y 0,1 en Gym?** Son mecanismos y unidades protegidas diferentes. Fitbit usa una persona completa y eligió ε = 1 con MAE ≤ 5 min y ≥ 95 % de respuestas en abril. Gym eligió 0,1 únicamente en validación según utilidad y brecha TPR.
- **¿El modelo pierde utilidad?** En la prueba Gym, la exactitud pasó de 68,49 % a 66,21 %, una pérdida descriptiva de 2,28 puntos. El conjunto de prueba ya se había observado antes, así que no confirma generalización independiente.
- **¿Se redujo el riesgo de membresía?** El AUC fue 0,5369 sin ruido y 0,5379 con DP. Este ensayo no demuestra una reducción empírica. La garantía formal declarada corresponde al histograma con ε fijo y vecindad por fila.
- **¿El modelo es equitativo?** En la partición evaluada, TPR privado Female/Male = 0,5905/0,6265 y FPR = 0,3019/0,2586. No atribuimos causalidad ni afirmamos ausencia de sesgo.
- **¿Qué falta para clientes reales?** R9, el retroceso del presupuesto al restaurar, permanece alto; también faltan conservación y eliminación operativas, validación de consentimiento con personas reales y despliegue verificado. La DPIA no aprueba un piloto.
- **¿Qué protege cada técnica?** HMAC seudonimiza IDs Fitbit; AES-256-GCM cifra mediciones almacenadas; la API autoriza cada objeto; DP centralizada limita la influencia de una persona en la estadística publicada. Ninguna sustituye a las demás.
