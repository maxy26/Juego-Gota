"""Exporta las animaciones de gota.aseprite al proyecto de Godot.

1. Una hoja de sprites por etiqueta en Assets/Sprites/Gota/ (PNG + JSON).
2. Resources/Gota/gota_frames.tres: SpriteFrames con todas las animaciones,
   su velocidad y si van en bucle (según Arte/Gota/revision/manifest.json).

Uso: python -I Arte/Gota/scripts/exportar_godot.py
     (variable ASEPRITE para indicar otro ejecutable de Aseprite)
"""
import json
import os
import subprocess

ARTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROYECTO = os.path.dirname(os.path.dirname(ARTE))
ASEPRITE = os.environ.get("ASEPRITE", r"C:\Herramientas\Aseprite\aseprite.exe")
SPRITES = os.path.join(PROYECTO, "Assets", "Sprites", "Gota")
RECURSO = os.path.join(PROYECTO, "Resources", "Gota", "gota_frames.tres")
COLUMNAS = 8


def res(ruta):
    return "res://" + os.path.relpath(ruta, PROYECTO).replace("\\", "/")


def main():
    with open(os.path.join(ARTE, "revision", "manifest.json"), encoding="utf-8") as f:
        manifiesto = json.load(f)
    animaciones = [v for a in manifiesto["animaciones"] for v in a["variantes"] if v.get("aprobada", True)]
    os.makedirs(SPRITES, exist_ok=True)
    os.makedirs(os.path.dirname(RECURSO), exist_ok=True)

    externos, atlas, lista = [], [], []
    for i, v in enumerate(animaciones, 1):
        png = os.path.join(SPRITES, f"gota_{v['id']}.png")
        datos = os.path.join(SPRITES, f"gota_{v['id']}.json")
        subprocess.run([ASEPRITE, "-b", "--tag", v["id"], os.path.join(ARTE, "gota.aseprite"),
                        "--sheet", png, "--data", datos, "--format", "json-array",
                        "--sheet-type", "rows", "--sheet-columns", str(COLUMNAS), "--list-tags"],
                       check=True, capture_output=True)
        with open(datos, encoding="utf-8") as f:
            fotogramas = json.load(f)["frames"]
        externos.append(f'[ext_resource type="Texture2D" path="{res(png)}" id="{i}_hoja"]')
        media = sum(fr["duration"] for fr in fotogramas) / len(fotogramas)
        entradas = []
        for k, fr in enumerate(fotogramas):
            r = fr["frame"]
            sub = f"Atlas_{v['id']}_{k}"
            atlas.append(f'[sub_resource type="AtlasTexture" id="{sub}"]\n'
                         f'atlas = ExtResource("{i}_hoja")\n'
                         f'region = Rect2({r["x"]}, {r["y"]}, {r["w"]}, {r["h"]})\n')
            entradas.append(f'{{\n"duration": {fr["duration"] / media:.3f},\n'
                            f'"texture": SubResource("{sub}")\n}}')
        lista.append(f'{{\n"frames": [{", ".join(entradas)}],\n'
                     f'"loop": {"true" if v.get("bucle", True) else "false"},\n'
                     f'"name": &"{v["id"]}",\n"speed": {1000 / media:.3f}\n}}')
        print(f"{v['id']}: {len(fotogramas)} fotogramas")

    total = len(externos) + len(atlas) + 1
    with open(RECURSO, "w", encoding="utf-8", newline="\n") as f:
        f.write(f'[gd_resource type="SpriteFrames" load_steps={total} format=3]\n\n')
        f.write("\n".join(externos) + "\n\n")
        f.write("\n".join(atlas) + "\n")
        f.write("[resource]\nanimations = [" + ", ".join(lista) + "]\n")
    print("recurso:", res(RECURSO))


if __name__ == "__main__":
    main()
