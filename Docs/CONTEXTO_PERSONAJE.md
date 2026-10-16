# CONTEXTO_PERSONAJE: Gota

> Documento de referencia del personaje. Las decisiones escritas aquí son las que definen el diseño. Las imágenes de referencia previas son aproximadas y **no** representan el personaje final.

---

## 1. Resumen

**Gota** es el personaje principal de un videojuego 2D de estilo caricaturesco: una pequeña gota de agua de apariencia frágil, pero seria, misteriosa, solitaria e inquietante.

---

## 2. Diseño visual

### 2.1 Forma y silueta
- Gota de agua clásica, rechoncha y compacta.
- Punta superior definida, que se estrecha gradualmente y termina ligeramente redondeada.
- Base redonda y ancha.
- Vista de **tres cuartos** a **45°**, mirando hacia la derecha. Para mirar a la izquierda se refleja en espejo. La silueta del cuerpo sigue siendo simétrica; el giro se nota en los ojos (desplazados hacia donde mira, el lejano más estrecho) y en las extremidades (la mano y el pie cercanos más adelante y abajo; la mano lejana asoma por detrás del borde).
- El reflejo lateral se mantiene en el lado izquierdo: la luz no gira con el personaje.
- Proporciones pequeñas y cuerpo de apariencia suave.
- Algo más delgada que la gota clásica (90 % del ancho).

### 2.2 Color y material
- Gris casi blanco, semitransparente.
- Más transparente en la parte superior que en la base.
- Matiz gris plateado muy tenue.
- Acabado cristalino, ligeramente brillante.
- Superficie lisa, sin texturas internas ni manchas.
- Doble contorno gris muy claro, uniforme y casi imperceptible.
- Un reflejo pequeño en uno de los laterales.

### 2.3 Rostro y personalidad
- Dos ojos diminutos, negros sólidos, ovalados verticalmente.
- Ojos juntos y situados a media altura.
- Sin pupilas ni reflejos en los ojos.
- **Sin boca durante el juego.**
- Boca fina **únicamente** durante las cinemáticas.
- Expresión seria y misteriosa.
- Personalidad: solitaria e inquietante (por fuera). Ver 2.6 para su personalidad interior.

#### Expresiones (solo con los ojos; negros, sólidos, sin pupilas)
| Expresión | Cuándo se usa |
|---|---|
| Seria con parpadeo | Idle normal. |
| Mira a la cámara → párpados a media altura → ojos cerrados | Secuencia cuando se queda quieta mucho tiempo. |
| Alerta → seria con parpadeo | Cuando detecta movimiento. |
| Alerta | Según la zona en la que se encuentra y su peligrosidad. |
| Determinada | Según el enemigo y la zona, y su peligrosidad. |
| Preocupada | Según el contexto de la historia. |
| Recelosa | Según el contexto de la historia. |
| Ojos cerrados | Final del reposo prolongado; cierre breve al recibir daño; derrota. |

Descartadas: "de reojo" y la seria sin parpadeo como expresión propia.

### 2.4 Extremidades
- **Sin brazos**: solo manos, que flotan junto a los lados del cuerpo.
- **Sin piernas**: solo pies, que flotan bajo el cuerpo.
- Manos y pies pequeños pero visibles, redondos, sin dedos definidos.
- Mismo color gris claro semitransparente que el cuerpo.
- Manos y pies separados del cuerpo, como si flotaran ligeramente.

### 2.5 Sombra
- Sombra ovalada, muy tenue y suave, debajo del personaje.

### 2.6 Personalidad interior (rasgos tomados de Finn el humano)
Gota toma **solo algunos rasgos** de Finn el humano (*Hora de Aventura*). Por fuera sigue siendo seria, misteriosa, solitaria e inquietante; estos rasgos viven por dentro y **se expresan en cómo se mueve y en lo que hace, nunca en la cara**.

| Rasgo | Cómo es en Gota |
|---|---|
| Valiente | Pequeña y frágil, pero no huye: se planta ante el peligro y ante enemigos grandes. |
| Justiciera | Fuerte sentido del bien y del mal; ayuda a quien lo necesita aunque no se lo pidan. |
| Leal y protectora | Defiende por encima de todo a los pocos que le importan (encaja con ser solitaria). |
| Aventurera e impulsiva | Se lanza a explorar y a actuar sin pensarlo demasiado. |
| Sensible | Siente mucho por dentro (tristeza, culpa, empatía) aunque por fuera no lo muestre. |
| Entusiasta | Se emociona, pero de forma **contenida**; nunca cómica ni exagerada. |

- **No** toma de Finn: la alegría expresiva, la inocencia/ingenuidad ni la competitividad.
- La expresión facial sigue siendo seria (ojos sin cambios, sin boca en el juego).
- Los rasgos se notan en:
  - **Las animaciones existentes**: postura firme y decidida en lugar de tímida.
  - **Animaciones nuevas** propias de estos rasgos (ver sección 3.1).

---

## 3. Animaciones

| Situación | Comportamiento definido |
|---|---|
| Reposo | Idle normal: respiración tranquila (dos respiraciones cada 3,2 s), postura firme, seria con un parpadeo por ciclo. Variantes de historia: preocupada y recelosa. |
| Reposo en alerta | Al recuperarse de un golpe o al entrar en una zona peligrosa: respiración corta, manos más altas y pies más abiertos, lista para actuar. Ojos de alerta o determinados según la peligrosidad. |
| Reposo prolongado | Entrada (una vez, 4 s): mira a la cámara, baja los párpados a media altura y cierra los ojos. Bucle: ojos cerrados y ligero pulso de transparencia (el cuerpo baja al 75 % de opacidad, ciclo de 2 s); los ojos no se desvanecen. |
| Reacción al movimiento | Al detectar movimiento (una vez, 1,8 s): abre los ojos en alerta con un pequeño sobresalto, se relaja y parpadea hasta la expresión seria. |
| Caminar | Pasitos cortos. |
| Saltar | Salto suave, con ligera inclinación y aterrizaje blando. |
| Recibir daño | Pequeño temblor y cierre breve de los ojos. |
| Derrota | Se aplana suavemente y después se desvanece. |
| Aparición | Cae desde arriba y aterriza con un rebote mínimo. |
| Ganar una ronda | Breve brillo plateado, sin cambiar su expresión seria. |
| Movimiento rápido | Algunas gotas diminutas se desprenden y desaparecen rápidamente. |

Todas las animaciones deben transmitir la personalidad interior de 2.6 (decisión, firmeza, valentía contenida) sin romper la expresión seria.

### 3.1 Animaciones nuevas por personalidad
Expresión facial siempre seria; el rasgo se transmite con el cuerpo.

| Animación | Rasgo | Comportamiento definido |
|---|---|---|
| En guardia | Valiente | Ante un enemigo, baja un poco el cuerpo, adelanta las manos y se queda firme, sin retroceder. |
| Proteger | Leal y protectora | Se interpone con los brazos abiertos, cubriendo a alguien detrás de ella. |
| Ayudar | Justiciera | Tiende la mano hacia abajo/adelante para levantar o ayudar a alguien. |
| Impulso | Aventurera e impulsiva | Se agacha un instante y sale disparada hacia delante sin dudar. |
| Explorar | Aventurera | Se inclina para mirar a un lado y al otro, curiosa, antes de avanzar. |
| Determinación | Valiente / sensible | Tras recibir daño o caer, se recompone y se endereza con firmeza. Puede encadenarse con "Recibir daño". |

Descartadas por el usuario: tristeza contenida y emoción contenida.

---

## 4. Sonido

- Al aterrizar tras caer desde arriba (animación de aparición): sonido húmedo y sutil, casi imperceptible.

---

## 5. Dirección artística y ambiente

- **Estilo:** caricaturesco 2D, pensado para un videojuego.
- **Acabado:** limpio, delicado, cristalino y ligeramente brillante.
- **Expresión:** seria, misteriosa y solitaria.
- **Sensación:** un personaje pequeño que parece frágil, pero resulta inquietante.
- **Evitar:** exageraciones, expresiones cómicas y deformaciones fuertes.

---

## 6. Pendiente

- **Tipo de escenario del juego:** aún no confirmado. La última pregunta sobre el ambiente quedó sin responder. No asumir un escenario; preguntar al usuario antes de tomar decisiones que dependan de él.

---

## 7. Decisiones cerradas (NO volver a preguntar)

- Forma y proporciones de la gota.
- Color, transparencia y matiz.
- Textura, brillo y contorno.
- Reflejo lateral.
- Ojos, boca y expresión.
- Brazos, piernas, manos y pies.
- Vista de tres cuartos a 45° (cambiada por el usuario: antes era vista frontal simétrica).
- Sin brazos ni piernas: solo manos y pies flotantes; cuerpo al 90 % del ancho.
- Expresiones y su uso (tabla de 2.3).
- Sombra.
- Animaciones de reposo, movimiento, salto, daño, derrota, aparición y victoria.
- Animaciones de personalidad (3.1): en guardia, proteger, ayudar, impulso, explorar y determinación.
- Efecto de transparencia durante el reposo prolongado.
- Sonido al aterrizar.
- Personalidad solitaria e inquietante.
- Personalidad interior con rasgos de Finn el humano: valiente, justiciera, leal y protectora, aventurera e impulsiva, sensible y entusiasta contenida (2.6). Se expresa en animaciones, no en la cara.
- **Estilo gráfico:** dibujo 2D suave inspirado en Hollow Knight (no pixel art), acabado **"A · Limpio"**: curvas suaves y degradado cristalino, sin halo ni sombreado extra. Contorno gris claro del documento (no el contorno negro de Hollow Knight).
- **Formato:** fotogramas de 256×256 renderizados a 512×512; animaciones fluidas (~16 fotogramas por ciclo).

---

## 8. Instrucciones de trabajo

- Tratar este documento como fuente de verdad del personaje.
- No modificar ni reinterpretar las decisiones de la sección 7.
- Mantener la consistencia visual y de animación en cualquier asset, sprite o código que se genere.
- Ante cualquier duda sobre el escenario (sección 6), consultar al usuario.
