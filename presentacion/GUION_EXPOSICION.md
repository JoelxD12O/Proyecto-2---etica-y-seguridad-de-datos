# Guion de la exposición – Alzace Fitness (DS3031)

**Reparto**
- **Josué**: toda la exposición, diapositivas 1 a 12 y 16 a 17 (unos 13 min).
- **Joel**: la demo en vivo, diapositiva 13 (unos 3 min). Las diapositivas 14 y 15 son el respaldo si la demo falla.

| Diap. | Tema | Quién | Tiempo |
|---|---|---|---|
| 1 | Portada | Josué | 0:40 |
| 2 | Lo que pedía el proyecto | Josué | 0:45 |
| 3 | El problema | Josué | 1:00 |
| 4 | Dos fuentes de datos | Josué | 1:00 |
| 5 | Arquitectura y roles | Josué | 1:00 |
| 6 | Privacidad diferencial | Josué | 1:15 |
| 7 | ¿Por qué ε = 1? | Josué | 1:00 |
| 8 | Utilidad del modelo | Josué | 1:15 |
| 9 | DPIA | Josué | 1:15 |
| 10 | Reflexiones éticas | Josué | 1:00 |
| 11 | Seguridad y verificación | Josué | 1:00 |
| 12 | Cumplimiento y pendientes | Josué | 0:45 |
| 13 | **Demo en vivo** | **Joel** | 3:00 |
| 14–15 | Respaldo (solo si falla la demo) | Joel | 0:40 |
| 16 | Conclusiones | Josué | 1:00 |
| 17 | Referencias (queda puesta en preguntas) | Josué | 0:10 |

---

## JOSUÉ

**1 – Portada**
Buenos días, profesor. Somos Joel Cayllahua y Josué Hernández, y presentamos Alzace Fitness, nuestro proyecto final de Ética y Seguridad de Datos. Es una app de seguimiento de entrenamiento que maneja datos de salud de los clientes de un club. La idea central es que el club pueda publicar estadísticas del grupo con privacidad diferencial sin exponer a nadie. Yo voy a explicar el diseño y los resultados, y al final Joel hace la demo en vivo.

**2 – Lo que pedía el proyecto**
El enunciado pedía tres bloques. Del lado del negocio, evaluar los riesgos de privacidad y éticos sin perder la utilidad de los datos. En privacidad y ética, implementar y evaluar privacidad diferencial, hacer una DPIA del ciclo de vida y discutir sesgo, transparencia y consentimiento. En lo técnico, una base de datos con front y backend, notebooks de análisis y la justificación de la librería y de ε. Al final volvemos a esta lista para mostrar qué cumplimos y qué quedó pendiente.

**3 – Datos de salud en el entrenamiento virtual**
El club pasa a entrenamiento virtual, y el entrenador necesita seguir el progreso de cada cliente a distancia. Eso implica registrar actividad, frecuencia cardíaca, peso y grasa corporal, que son datos de salud y por eso son sensibles según la Ley 29733. Además, el club quiere conocer la tendencia del grupo. La pregunta del proyecto es cómo publicar estadísticas útiles sin que se pueda reconocer a ninguna persona. Para probarlo usamos dos fuentes públicas, 33 participantes de Fitbit y 973 perfiles del dataset Gym.

**4 – Dos fuentes, analizadas por separado**
Las dos fuentes se analizan por separado. Fitbit tiene los minutos activos por día y es la que alimenta la estadística protegida, y su identificador se seudonimiza con HMAC. Gym sirve para el experimento del modelo y el análisis de sesgo. En el parcial propusimos unirlas al azar, pero al implementarlo vimos que no comparten un identificador y que eso inventaría personas que no existen, así que lo descartamos. En el gráfico se ve que hay personas con 4 días y otras con 31, por eso la estadística da un voto a cada persona y no a cada fila.

**5 – Arquitectura y roles**
La arquitectura tiene un front en Next.js con una vista por rol y una API en FastAPI. La API valida el rol y además el dueño de cada registro en cada petición, no solo en la pantalla. Los campos de salud se guardan cifrados con AES-256-GCM, sobre SQLite en la demo y PostgreSQL en modo alojado. Hay tres roles. El cliente ve lo suyo y decide su consentimiento. El entrenador ve solo a sus clientes asignados. Y el administrador publica estadísticas y revisa la auditoría, pero nunca ve historias biométricas.

**6 – Privacidad diferencial: qué publicamos**
Esta es la pregunta que publicamos: cuántos minutos activos por día registró, en promedio, una persona del grupo en el mes. Primero calculamos la media de cada persona, así cada participante tiene un solo voto. Después acotamos su aporte entre 0 y 120 minutos, para limitar cuánto puede mover el resultado una sola persona. Luego aplicamos ruido de Laplace a la suma y al conteo, con ε/2 cada uno, y si el conteo con ruido es menor que 8, no publicamos. La unidad protegida es la persona completa, cada publicación cuesta ε = 1 y el presupuesto total permite dos publicaciones.

**7 – ¿Por qué ε = 1?**
Para elegir ε simulamos 300 publicaciones por cada valor. Antes del experimento fijamos el criterio: un error medio de 5 minutos como máximo y al menos 95 % de resultados devueltos. ε = 1 es el menor valor que cumple ambos, con 4,7 minutos de error sobre una referencia de 34,05 y el 100 % de respuestas. Esa corrida usaba una semilla fija, así que la repetimos con 30 semillas independientes, y el error esperado con ε = 1 es de unos 4,2 minutos, así que la elección se sostiene. En términos de privacidad, ε = 1 significa que incluir o excluir a una persona cambia la probabilidad de cualquier resultado como máximo unas 2,7 veces. Usamos IBM diffprivlib por su muestreo seguro de Laplace y seguimos la guía NIST SP 800-226.

**8 – Utilidad del modelo con y sin privacidad**
Para medir el costo en un modelo entrenamos un clasificador sobre Gym que predice si una sesión dura 75 minutos o más. Aquí la unidad protegida es la fila y no la persona, porque Gym no tiene un identificador de persona en el tiempo. Con ε = 1 la exactitud baja 2,5 puntos en la corrida principal, o 1,8 con 30 semillas, y el ataque de membresía da un AUC de 0,49, que es azar, con o sin ruido. El eje empieza en 60 %, así que las barras exageran la diferencia. La brecha entre grupos pasa de 0,4 puntos a favor del grupo femenino a 0,7 a favor del masculino. Va en la dirección que describe Bagdasaryan, pero con 128 y 164 personas no es significativa, así que la tomamos como algo a vigilar.

**9 – DPIA**
Hicimos la DPIA recorriendo el ciclo de vida del dato con LINDDUN. En el informe hay nueve riesgos y aquí mostramos los seis principales. La segunda columna dice la etapa y la categoría LINDDUN. Por ejemplo, que un usuario vea la ficha de otro es divulgación, y se mitiga con autorización por registro. Después de las medidas ningún riesgo queda en alto, y tres quedan en medio, el acceso a la ficha de otro, la reidentificación por promedios y el robo de la base o de un respaldo. La decisión es pilotar con condiciones, que son TLS, plazo de conservación, un responsable de los derechos ARCO y el registro ante la ANPD.

**10 – Reflexiones éticas**
Tres reflexiones éticas. Sesgo: el ruido no afecta igual a todos los grupos, y un día sin reloj no es un día inactivo, por eso la adherencia se mide con sesiones cumplidas. Transparencia: publicamos el método, la unidad protegida, ε y el error esperado, y también los costos, como que el tope baja la media de 34,69 a 34,05. Consentimiento: está separado del servicio, empieza apagado y se puede retirar, y la pantalla explica que retirarlo no borra lo ya publicado. Y dos puntos legales. La Ley 29733 exige consentimiento por escrito para datos de salud, y si alojamos en Supabase y Render los datos salen del Perú, que es una transferencia internacional, por eso se cifran antes de enviarse.

**11 – Seguridad y verificación**
Estas son las medidas de seguridad: cifrado por campo, contraseñas con bcrypt, cookie HttpOnly y SameSite estricta, autorización por rol y por registro, auditoría de solo inserción y respaldo cifrado. Diecisiete pruebas automáticas pasan, doce del backend y cinco que simulan a un usuario en el navegador, y una se omite porque necesita una base PostgreSQL externa. También comprobamos que pedir la ficha de otro cliente da 403, que republicar el mismo mes no gasta ε y que el escaneo pasivo de ZAP dejó solo tres alertas informativas.

**12 – Cumplimiento y pendientes**
Volviendo al enunciado, cubrimos los requerimientos dentro del alcance de una demo local, y los notebooks se reproducen de principio a fin. No todo está terminado. Falta validar el despliegue con TLS, correr ZAP activo sobre un entorno autorizado y la prueba en PostgreSQL. También falta fijar el plazo de conservación, permitir que el cliente exporte o borre sus datos, que hoy sería manual, y definir cómo se renueva el presupuesto ε. Por eso la DPIA los pone como condición antes de un piloto real. Ahora Joel les muestra todo esto funcionando.

---

## JOEL – Demo en vivo (diapositiva 13)

**Al empezar (con la diapositiva 13 en pantalla)**
Gracias, Josué. Ahora lo vemos en la app real, en cuatro pasos, cliente, entrenador, administrador y auditoría.
*(Alt+Tab al navegador en http://127.0.0.1:3000)*

**Paso 1 – Cliente**
*(Elegir «Cliente» → «Entrar al panel»)*
Entro como Lucía, que es una clienta. Ella solo ve su propia actividad.
*(«Registrar medición» → 47 minutos, 4321 pasos → «Guardar»)*
Registro una medición. En la base de datos esto no queda en claro, queda cifrado con AES-256-GCM y amarrado a Lucía y a ese día.
*(Ir a «Mi privacidad» → «Permitir uso grupal», luego «Retirar permiso»)*
Aquí está el consentimiento. Es aparte del servicio, empieza apagado, lo activo y lo puedo retirar igual de fácil. Si Lucía no acepta, su entrenador la sigue atendiendo, solo que no entra a las estadísticas.
*(«Cerrar sesión»)*

**Paso 2 – Entrenador**
*(Elegir «Entrenador» → «Entrar al panel» → abrir el selector de clientes)*
Ahora entro como entrenador. En la lista solo aparecen sus clientes asignados. Mateo no está, porque es de otra entrenadora.
*(F12 → Consola → pegar la consulta y Enter)*
Si intento pedir la ficha de Mateo directo a la API, aunque me salte la pantalla…
*(muestra 403)*
…el servidor responde 403. La autorización se revisa en cada petición, eso es lo que mitiga el riesgo R1 de la DPIA.
*(Cerrar la consola → «Cerrar sesión»)*

**Paso 3 – Administrador y privacidad diferencial**
*(Elegir «Administrador» → «Entrar al panel» → Estadísticas)*
Entro como administrador. Arriba está el presupuesto de privacidad, en 0 de 2.
*(Fuente «Estudio Fitbit», periodo 2016-04 → «Publicar estimación»)*
Publico abril de 2016. El valor sin ruido es 34,05 minutos y la app publica una cifra cercana, pero no exacta. Ese ruido es el que impide saber si una persona estaba o no en el grupo. El presupuesto sube a 1 de 2.
*(Recargar la página, volver a elegir 2016-04)*
Si vuelvo a pedir el mismo mes, sale exactamente el mismo número y el presupuesto sigue en 1. Si se recalculara, alguien podría pedirlo muchas veces y promediar el ruido.
*(Periodo 2016-05 → «Publicar estimación»)*
Ahora publico mayo. El presupuesto llega a 2 de 2 y el botón queda en «Presupuesto agotado». Ya no se puede publicar nada nuevo, ni siquiera saltándose la pantalla, porque el servidor también lo bloquea.

**Paso 4 – Auditoría**
*(Ir a «Auditoría»)*
Por último, la auditoría. Aquí están las dos publicaciones y también los accesos denegados de hace un momento, el del entrenador pidiendo a Mateo, con el titular y el motivo. No guarda mediciones ni contraseñas, y la tabla no se puede modificar.

**Para cerrar**
*(Alt+Tab al PowerPoint, avanzar a la diapositiva 16)*
Eso es la demo. Josué cierra con las conclusiones.

**Si algo falla**
Tranquilo, pasar a la diapositiva 14 y decir:
Tenemos capturas de la app real por si acaso. Aquí se ve el 403 al pedir la ficha de otro cliente y que republicar el mismo mes devuelve el resultado guardado sin gastar presupuesto.
*(diapositiva 15)*
Y aquí el rechazo cuando el presupuesto ya está agotado, y la auditoría con los accesos denegados.

**Consulta para la consola (tenerla copiada)**
```js
fetch('/api/clients/demo-mateo',{headers:{'x-alzace-request':'web'}}).then(r=>r.status)
```

---

## JOSUÉ – Cierre

**16 – Conclusiones**
Cerramos con cuatro ideas. Con ε = 1 la estadística sirve para ver tendencias, con unos 4,2 a 4,7 minutos de error sobre 34. El costo para el modelo es bajo, entre 1,8 y 2,5 puntos, pero no es neutral entre grupos y hay que vigilarlo. Lo que más protege son decisiones de diseño: proteger a la persona completa, limitar el presupuesto y pedir el consentimiento aparte. Y falta lo operativo, por eso decidimos pilotar con condiciones. Gracias, quedamos atentos a sus preguntas.

**17 – Referencias**
*(Dejarla en pantalla durante las preguntas)*

---

## Preguntas probables y quién responde

- **¿Qué significa ε = 1?** (Josué) – Que incluir o excluir a una persona cambia la probabilidad de cualquier resultado como máximo unas 2,7 veces. Con el presupuesto total de 2, como máximo unas 7,4 veces.
- **¿Por qué no un ε más chico?** (Josué) – Con 0,5 el error sube a unos 9,5 minutos y ya no sirve para ver tendencias. Elegimos el menor ε que cumplía el criterio fijado antes.
- **¿Qué pasa cuando se acaba el presupuesto?** (Josué) – En la demo es fijo a propósito para mostrar el límite. En un piloto se renovaría por periodo, por ejemplo cada año, declarando que la pérdida total de privacidad crece con cada periodo.
- **¿Por qué la semilla fija y luego 30 semillas?** (Josué) – La corrida principal es reproducible con los notebooks. La de 30 semillas muestra que el resultado no depende de la suerte, y da un error algo menor.
- **¿Cómo evitan que alguien vea datos de otro?** (Joel) – La API revisa el rol y el dueño de cada registro en cada petición. Lo vieron en la demo con el 403.
- **¿Dónde están cifrados los datos?** (Joel) – Cada medición se cifra con AES-256-GCM antes de guardarse, con datos asociados que la amarran al dueño y al día.
- **¿El modelo es justo?** (Josué) – La brecha cambia muy poco y no es significativa con nuestros tamaños de grupo, pero la dejamos como algo a monitorear.
- **¿Qué falta para usarlo con clientes reales?** (Josué) – TLS, plazo de conservación, exportar o borrar datos y la renovación del presupuesto. Están como condiciones en la DPIA.
