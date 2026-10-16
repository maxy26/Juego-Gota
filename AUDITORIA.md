# AUDITORÍA

> Registro de revisiones, pruebas y decisiones. Entrada nueva arriba.

## Plantilla

```
## AUD-XXX — AAAA-MM-DD — Título
**Alcance:** · **Hallazgos:** · **Riesgos:** · **Acciones:** · **Estado:**
```

---

## AUD-001 — 2026-10-15 — Creación del proyecto y animaciones de reposo

**Alcance:** creación del proyecto de Godot, traslado del arte de Gota y primeras animaciones en el juego.

**Decisiones:**
- Estilo dibujado a mano inspirado en *Hollow Knight*, acabado "Limpio", vista de tres cuartos a 45°, sin brazos ni piernas (manos y pies flotantes), cuerpo al 90 % del ancho de la gota clásica.
- Expresiones solo con los ojos y su uso definido por el usuario (tabla en `Docs/CONTEXTO_PERSONAJE.md`, sección 2.3). Descartadas: "de reojo" y la seria sin parpadeo como expresión propia.
- 8 animaciones de reposo aprobadas: `reposo`, `reposo_prolongado_entrada`, `reposo_prolongado`, `reaccion_movimiento`, `reposo_alerta`, `reposo_determinada`, `reposo_preocupada`, `reposo_recelosa`.
- El arte fuente vive en `Arte/` con `.gdignore` para que Godot no importe las hojas de revisión ni los SVG.
- `gota_frames.tres` se genera desde las exportaciones de Aseprite (no se edita a mano).

**Pruebas:**
- Importación del proyecto con Godot 4.6.3 en modo consola: sin errores.
- Prueba automática de la escena principal: las 8 animaciones cargan con su número de fotogramas, ~12 fps y el bucle correcto; la cadena reposo → entrada → reposo prolongado → reacción → reposo funciona.
- Las 8 etiquetas de `gota.aseprite` (271 fotogramas de 512×512) cubren sus fotogramas sin solaparse.

**Riesgos y límites:**
- Escala del sprite (0,4) y colisión aproximadas: revisar cuando haya escenario.
- Las hojas de 512×512 por fotograma pesan (~7 MB en total). Si el juego crece, valorar bajar a 256×256.
- El escenario del juego sigue sin definir (afecta a fondos y a la legibilidad de una protagonista semitransparente).

**Estado:** cerrada.
