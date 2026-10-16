-- Monta gota.aseprite con las animaciones aprobadas (una etiqueta por animación).
-- Corta los fotogramas de las hojas de revision/sprites según revision/manifest.json.
--
-- Uso: aseprite -b --script-param dir=<carpeta Gota> --script gota_final.lua

local dir = app.params.dir
local fh = assert(io.open(app.fs.joinPath(dir, "revision", "manifest.json")))
local manifiesto = json.decode(fh:read("a"))
fh:close()

local lado = manifiesto.tam * manifiesto.escalaFuente
local spr = Sprite(lado, lado, ColorMode.RGB)
spr.layers[1].name = "Gota"
local f, rangos = 0, {}
for _, anim in ipairs(manifiesto.animaciones) do
  for _, v in ipairs(anim.variantes) do
    local hoja = Image{ fromFile = app.fs.joinPath(dir, "revision", v.hoja) }
    local desde = f + 1
    for i = 0, v.n - 1 do
      f = f + 1
      if f > 1 then spr:newEmptyFrame() end
      local img = Image(hoja, Rectangle((i % v.cols) * lado, (i // v.cols) * lado, lado, lado))
      spr:newCel(spr.layers[1], f, img, Point(0, 0))
      spr.frames[f].duration = v.duraciones[i + 1] / 1000
    end
    rangos[#rangos+1] = { v.id, desde, f }
  end
end
-- Las etiquetas se crean al final: si no, crecen al añadir fotogramas detrás
for _, r in ipairs(rangos) do spr:newTag(r[2], r[3]).name = r[1] end
spr:saveAs(app.fs.joinPath(dir, "gota.aseprite"))
for _, r in ipairs(rangos) do print(r[1]) end
