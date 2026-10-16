# INSTRUCCIONES

> Última actualización: 2026-10-15

## Abrir y probar el juego

1. Abre Godot 4.6 → **Importar** → elige `project.godot` de esta carpeta.
2. Pulsa **F5**. La escena principal muestra a Gota en reposo:
   - Tras 8 s quieta entra en reposo prolongado (mira a la cámara, cierra los ojos y pulsa su transparencia).
   - Pulsa cualquier tecla para que reaccione y vuelva al reposo.

## Usar a Gota en otras escenas

- Instancia `Scenes/Gota/gota.tscn`. Su origen está en los pies.
- Cambiar de animación: `$Sprite.play(&"reposo_alerta")` (ver la tabla de animaciones en [CONTEXTO.md](CONTEXTO.md)).
- Avisar de movimiento cercano: `gota.detectar_movimiento()`.
- Mirar a la izquierda: `$Sprite.flip_h = true`.

## Crear o cambiar animaciones de Gota

Requisitos: Python 3, Brave y el Aseprite compilado (`C:\Users\Usuario\Documents\aseprite\build\bin\aseprite.exe`). Las rutas son relativas a la carpeta del proyecto.

1. **Dibujar:** añade o edita la animación en `PROPUESTAS` de `Arte/Gota/scripts/gota_hk.py` (`ciclo` en ms, `respiraciones`, `ojos` u `ojos_t`, `postura`, `pulso`, `bucle`…) y genera las propuestas:
   ```
   python -I Arte\Gota\scripts\gota_hk.py "Arte\Gota"
   ```
2. **Revisar:** arranca la página y ábrela en el navegador:
   ```
   python -I Arte\Gota\revision\servidor.py
   ```
   http://127.0.0.1:8765 — se puede votar, elegir favorita y comentar cada propuesta (se guarda en `Arte/Gota/revision/opiniones.json`).
3. **Montar en Aseprite** las animaciones aprobadas:
   ```
   aseprite -b --script-param dir="Arte\Gota" --script Arte\Gota\scripts\gota_final.lua
   ```
4. **Exportar al juego** (hojas en `Assets/Sprites/Gota/` y `Resources/Gota/gota_frames.tres`):
   ```
   python -I Arte\Gota\scripts\exportar_godot.py
   ```
5. Abre Godot para que reimporte las hojas.

El diseño del personaje manda: cualquier animación debe respetar [Docs/CONTEXTO_PERSONAJE.md](Docs/CONTEXTO_PERSONAJE.md), y las decisiones cerradas de su sección 7 no se cambian sin que lo pida el usuario.

## Git y GitHub

- Mensajes de commit **en español**, cortos y descriptivos.
- Los commits los firma el usuario. **No se añaden coautores, firmas ni menciones a herramientas** en commits, ramas, pull requests ni archivos del proyecto.
- No se suben: `.godot/`, `Arte/*/fuentes/`, `Arte/*/revision/sprites/` ni `opiniones.json` (se regeneran).

## Flujo de cada sesión

1. Leer [PENDIENTES.md](PENDIENTES.md) y [CONTEXTO.md](CONTEXTO.md).
2. Proponer las animaciones o cambios en la página de revisión y esperar la aprobación del usuario.
3. Montar, exportar y probar en Godot (que la escena cargue sin errores).
4. Actualizar PENDIENTES, CONTEXTO si cambia algo importante, y añadir una entrada en [AUDITORIA.md](AUDITORIA.md).
5. Commit y subida a GitHub.
