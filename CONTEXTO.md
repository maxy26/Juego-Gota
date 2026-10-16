# CONTEXTO

> Última actualización: 2026-10-15

## Objetivo

Videojuego 2D en **Godot 4.6** (nombre provisional: **Juego Gota**). La protagonista es **Gota**, una pequeña gota de agua de aspecto frágil pero seria, misteriosa e inquietante, con una personalidad interior valiente y protectora.

El diseño completo del personaje (forma, colores, ojos, expresiones, animaciones y personalidad) está en [Docs/CONTEXTO_PERSONAJE.md](Docs/CONTEXTO_PERSONAJE.md), que es la **fuente de verdad** del personaje.

## Historia del proyecto

1. Los sprites de Gota se diseñaron primero en pixel art (48×48) y se cambiaron después a un estilo dibujado a mano inspirado en *Hollow Knight*.
2. Se probaron vista frontal y tres cuartos: se eligió **tres cuartos a 45°**, mirando a la derecha.
3. Se quitaron brazos y piernas: Gota solo tiene **manos y pies flotantes**.
4. Se definieron las **expresiones** (solo con los ojos) y las animaciones de **reposo**.
5. El 2026-10-15 se creó este proyecto de Godot y se trasladaron aquí todos los archivos de Gota.

## Decisiones

- **Motor:** Godot 4.6, renderizador *GL Compatibility*, ventana de 1280×720 con estiramiento `canvas_items`.
- **Arte vectorial generado por código:** Gota se dibuja con curvas en SVG desde `Arte/Gota/scripts/gota_hk.py` y se convierte a PNG con un navegador en modo headless. Así cada fotograma es coherente y se puede regenerar al cambiar el diseño.
- **Aseprite como montaje:** las hojas aprobadas se juntan en `Arte/Gota/gota.aseprite` (una etiqueta por animación) y desde ahí se exportan al juego.
- **Fotogramas de 512×512** (dibujados a 256×256 y renderizados al doble). En el juego el sprite se escala a 0,4 y su origen está en los pies.
- **~12 fps** en todas las animaciones.
- **Mirar a la izquierda:** se refleja en espejo (`flip_h`).
- **Revisión en el navegador:** cada animación nueva se enseña en una página local con varias propuestas antes de darla por buena.
- **Estructura de carpetas** como el resto de proyectos de Godot del usuario (`Assets/`, `Scenes/`, `Scripts/`, `Resources/`).

## Arquitectura

```
Juego Gota/
├── project.godot
├── Assets/Sprites/Gota/      Hojas de sprites exportadas (PNG + JSON), una por animación
├── Resources/Gota/           gota_frames.tres (SpriteFrames de todas las animaciones)
├── Scenes/
│   ├── principal.tscn        Escena principal (de prueba por ahora)
│   └── Gota/gota.tscn        CharacterBody2D + AnimatedSprite2D + colisión
├── Scripts/Gota/gota.gd      Estados de reposo de Gota
├── Docs/CONTEXTO_PERSONAJE.md   Diseño del personaje (fuente de verdad)
└── Arte/ (.gdignore)         Fuentes del arte; Godot no las importa
    └── Gota/
        ├── gota.aseprite     Animaciones aprobadas (etiquetas)
        ├── scripts/          gota_hk.py · gota_final.lua · exportar_godot.py
        ├── revision/         Página de revisión (index.html + servidor.py)
        └── fuentes/          SVG generados (no se suben a git)
```

## Animaciones de Gota

| Etiqueta | Bucle | Uso |
|---|---|---|
| `reposo` | Sí | Idle normal: seria con parpadeo. |
| `reposo_prolongado_entrada` | No | Quieta mucho tiempo: mira a la cámara → párpados a media altura → ojos cerrados. |
| `reposo_prolongado` | Sí | Ojos cerrados y pulso de transparencia. |
| `reaccion_movimiento` | No | Detecta movimiento: alerta → seria con parpadeo. |
| `reposo_alerta` | Sí | Zona peligrosa o tras un golpe; ojos de alerta. |
| `reposo_determinada` | Sí | Enemigo o zona muy peligrosa; mirada determinada. |
| `reposo_preocupada` | Sí | Según la historia. |
| `reposo_recelosa` | Sí | Según la historia. |

## Entorno

Windows 11, Godot 4.6.3, Aseprite compilado desde el código fuente (`C:\Users\Usuario\Documents\aseprite\build\bin\aseprite.exe`), Python 3.14 y Brave (para convertir SVG a PNG). Equipo con 8 GB de RAM y gráfica integrada.
