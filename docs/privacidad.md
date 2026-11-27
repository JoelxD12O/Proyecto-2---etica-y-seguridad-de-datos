# Qué publica el club y qué precisión tiene

La pregunta es «¿cuántos minutos activos por día registró, en promedio, una persona del grupo durante el mes?». El entrenador puede consultar la estadística grupal. La ficha personal se protege por separado mediante autenticación, autorización por cliente y cifrado.

## De una persona a una contribución

1. En Fitbit se suman los minutos de actividad moderada e intensa de cada día. Un duplicado idéntico cuenta una vez. Un conflicto detiene la importación.
2. Se calcula una media por participante usando sus días observados. Cada persona pesa lo mismo. Se limita esa media a [0, 120] minutos. El tope se fijó para esta consulta de promedio mensual y puede subestimar a las personas más activas.
3. Dos conjuntos vecinos difieren en **todos** los registros mensuales de una persona. Restar 60 a cada media acotada hace que añadir o quitar una persona cambie la suma centrada a lo sumo en 60 y el conteo en 1.
4. Se protegen ambas cantidades con mecanismos Laplace independientes. Con ε = 1, cada uno recibe 0,5. Las escalas respectivas son 120 minutos y 2 personas. Si el conteo **con ruido** es menor que 8, se omite el valor. En otro caso se calcula 60 + suma protegida / conteo protegido, se acota el resultado y se redondea. La omisión y el redondeo son posprocesamiento. La garantía por publicación es (ε, 0)-DP bajo esta definición de vecindad.
5. La API ofrece fuentes y meses predefinidos. Del programa solo se publican meses cerrados según la hora de Lima: el mes en curso se rechaza con 422 porque una cifra con datos parciales quedaría guardada y gastaría ε. Una transacción guarda el cargo y la publicación juntos, incluso si se omite el valor. El mismo mes y fuente devuelven el resultado guardado. El límite global de ε = 2 admite dos publicaciones distintas de ε = 1 en toda la instalación. Para un servicio continuo habría que acordar presupuesto, horizonte y participación repetida antes de ampliar este alcance.

Elegimos **IBM diffprivlib 0.6.6** porque permite declarar la sensibilidad, dividir explícitamente el presupuesto y usar las mismas operaciones en la API y el experimento. El mecanismo Laplace incorpora un método de muestreo estudiado para reducir riesgos de precisión finita. Dejamos las semillas reproducibles para el laboratorio y usamos azar seguro en el servicio. La unidad protegida, los límites y la composición siguen siendo responsabilidad del equipo. [Holohan et al., Diffprivlib](https://arxiv.org/abs/1907.02444) · [Holohan y Braghin, Secure Random Sampling](https://arxiv.org/abs/2107.10138) · [NIST SP 800-226](https://csrc.nist.gov/pubs/sp/800/226/final).

### Limitaciones conocidas

- **Precisión finita.** El mecanismo Laplace se ejecuta en coma flotante. La prueba matemática ideal supone aritmética real; el muestreo usado reduce una vulnerabilidad concreta, sin demostrar ausencia de todos los canales laterales. El redondeo de la salida es posprocesamiento y no sustituye la revisión de implementación.
- **Claves de la demo.** En el prototipo local, `.local/keys.json` y `demo.sqlite3` quedan en el mismo entorno. Quien copie ambos obtiene datos y claves. En el modo alojado propuesto, el llavero llegaría como secreto de entorno y no se guardaría junto a la base.
- **Retención operativa.** El panel de administración muestra la retención mensual exacta, sin ruido. Se suprime cuando la cohorte inicial tiene menos de ocho membresías. Esta métrica no hereda la garantía de privacidad diferencial de la media grupal.

## Experimento de utilidad en Fitbit

Se eligió la exportación del 12 de abril al 12 de mayo de 2016. En abril hay 33 participantes, 611 días-persona y entre 4 y 19 días observados por participante. La media ponderada por filas sería 35,49 min/día. Dando un voto a cada persona resulta 34,69. Después de acotar una contribución, la referencia queda en **34,05 min/día**. Esta exportación solo cubre parte de abril.

| ε por consulta | Simulaciones | Resultados devueltos | Error absoluto medio | Percentil 90 del error absoluto |
|---:|---:|---:|---:|---:|
| 0,1 | 300 | 83,7 % | 30,34 min | 67,85 min |
| 0,5 | 300 | 99,7 % | 9,50 min | 19,63 min |
| 1 | 300 | 100 % | 4,72 min | 9,69 min |
| 2 | 300 | 100 % | 2,32 min | 4,75 min |

Los errores se calculan sobre las estimaciones devueltas, frente a la media acotada. La diferencia con la media original es otro coste. Como objetivo académico propusimos error medio ≤ 5 minutos y al menos 95 % de respuestas. **ε = 1 es el menor valor ensayado que satisface ambos en este periodo.** Una publicación individual puede desviarse más. Para otro mes, población o tope conviene volver a evaluar la decisión con datos de estudio independientes.

Las semillas de evaluación y referencias exactas pertenecen al laboratorio offline de estos archivos de estudio. Divulgar una comparación exacta con datos operativos eludiría el presupuesto. La API guarda únicamente los resultados protegidos en su historial de publicaciones.

## Modelo y sesgo en Gym Members

Un clasificador predice si una sesión dura al menos 75 minutos, a partir de experiencia y frecuencia semanal. Esta etiqueta aproxima sesiones prolongadas que podrían motivar una conversación con el entrenador, sin ser una meta clínica. El umbral es una elección académica; no se dedujo de una guía de salud. Se separan 510 filas para entrenamiento, 171 para validación y 292 para prueba, con estratificación por clase. El histograma tiene 21 combinaciones de variables y dos clases. La versión privada añade Laplace al vector completo de conteos, de sensibilidad L1 = 1 porque una fila modifica una sola celda. Cada celda recibe ruido de escala 1/ε; el recorte de negativos, suavizado y clasificación son posprocesamiento. La unidad protegida es **una fila de entrenamiento**, no la persona. Gym carece de identificador longitudinal verificable.

| Resultado en prueba | Referencia | Privado ε = 0,1, media de 30 entrenamientos |
|---|---:|---:|
| Exactitud | 68,49 % | 66,21 % |
| Exactitud balanceada | 68,07 % | 66,44 % |
| AUC del ataque de membresía por confianza | 0,5369 | 0,5379 |
| Ventaja máxima del ataque (TPR − FPR) | 0,0756 | 0,0738 |
| Exactitud en el grupo Female (144) | Ver JSON | 64,28 % |
| Exactitud en el grupo Male (148) | Ver JSON | 68,09 % |

La regla declarada para Gym elige el menor ε cuya exactitud y exactitud balanceada medias en validación pierden como máximo 5 puntos porcentuales respecto del histograma sin ruido y cuya brecha TPR entre Female y Male no supera 0,15. Son tolerancias académicas, no estándares externos de equidad; el tamaño de los grupos impide una garantía de equidad. Con 30 semillas independientes por valor, los cuatro ε ensayados cumplen; por ello se elige **ε = 0,1 en validación**, sin mirar la prueba durante la selección. El histograma final se ajusta en entrenamiento más validación y se evalúa en prueba. La referencia trivial de clase mayoritaria obtiene 52,05 %. La precisión, exhaustividad y F1 privados promedian 72,66 %, 60,90 % y 64,19 %. El archivo JSON conserva matrices de confusión, desviación entre semillas y métricas por grupo. El ataque de membresía por confianza tiene AUC similar en ambas versiones; no demuestra una reducción empírica del riesgo. **Limitación importante:** la prueba de este mismo dataset ya fue observada en versiones anteriores. Aunque el procedimiento nuevo no la usa para seleccionar ε, su evaluación no es una confirmación independiente. Haría falta otro conjunto no observado para tal afirmación.

| ε en validación | Accuracy | Balanced accuracy | Brecha TPR | Cumple |
|---:|---:|---:|---:|:---:|
| 0,1 | 0,6472 | 0,6496 | 0,0301 | Sí |
| 0,5 | 0,6421 | 0,6424 | 0,0485 | Sí |
| 1 | 0,6398 | 0,6408 | 0,0563 | Sí |
| 2 | 0,6374 | 0,6392 | 0,0640 | Sí |

La referencia sin ruido en validación es 0,6374 de accuracy y 0,6392 balanceada. La tolerancia de cinco puntos preserva utilidad exploratoria del clasificador y la brecha TPR de 0,15 filtra disparidades grandes en esta muestra; ninguna certifica rendimiento o equidad para clientes reales. La garantía de privacidad diferencial de Gym se refiere al histograma perturbado con un ε fijo y vecindad por fila de entrenamiento. La selección por métricas exactas de validación y la publicación de métricas exactas del laboratorio no reciben automáticamente esa garantía.

ε de Gym se selecciona independientemente de Fitbit. La brecha TPR privada en prueba es 0,0360 y la brecha FPR 0,0433; no se les atribuye causalidad ni se concluye ausencia de sesgo. Tampoco se infieren tendencias mensuales a partir de una sola publicación de abril: se estimó únicamente una media grupal de ese periodo.

La exploración de robustez en `evidence/robustez.json` repite el mecanismo Fitbit con semillas independientes para abril, mayo y topes de 90, 120 y 150 minutos. Para ε = 1, el MAE medio fue 4,131, 4,632, 2,902 y 5,424 minutos, respectivamente. Por tanto el criterio de cinco minutos deja de cumplirse con el tope 150 en abril: ε = 1 no es una elección universal. Las bandas de confianza del archivo reflejan variación entre semillas de simulación con el mismo dataset, no incertidumbre por muestreo de personas. La comparación Gym en ese archivo también se limita a validación.

[Resultados reproducibles](../evidence/experimentos.json) · [Experimento Fitbit](../notebooks/02_privacidad_diferencial.ipynb) · [Modelo y ética](../notebooks/03_modelo_y_etica.ipynb).
