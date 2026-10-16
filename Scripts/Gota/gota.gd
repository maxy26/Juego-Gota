extends CharacterBody2D
## Gota, el personaje principal.
##
## Reposo: reposo -> (quieta mucho tiempo) entrada al reposo prolongado -> bucle
## de reposo prolongado. Si detecta movimiento durante el reposo prolongado,
## reacciona y vuelve al reposo.

## Segundos quieta antes de empezar el reposo prolongado.
@export var segundos_hasta_prolongado := 8.0

@onready var sprite: AnimatedSprite2D = $Sprite

var _tiempo_quieta := 0.0


func _ready() -> void:
	sprite.animation_finished.connect(_al_terminar_animacion)
	sprite.play(&"reposo")


func _process(delta: float) -> void:
	if sprite.animation != &"reposo":
		return
	_tiempo_quieta += delta
	if _tiempo_quieta >= segundos_hasta_prolongado:
		sprite.play(&"reposo_prolongado_entrada")


func _unhandled_input(event: InputEvent) -> void:
	if event.is_pressed() and not event.is_echo():
		detectar_movimiento()


## Llamar cuando Gota detecte movimiento (del jugador o de algo cercano).
func detectar_movimiento() -> void:
	_tiempo_quieta = 0.0
	if sprite.animation in [&"reposo_prolongado_entrada", &"reposo_prolongado"]:
		sprite.play(&"reaccion_movimiento")


func _al_terminar_animacion() -> void:
	match sprite.animation:
		&"reposo_prolongado_entrada":
			sprite.play(&"reposo_prolongado")
		&"reaccion_movimiento":
			_tiempo_quieta = 0.0
			sprite.play(&"reposo")
