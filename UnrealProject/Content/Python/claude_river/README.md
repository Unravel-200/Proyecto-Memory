# Río de L_Campus_Natural

Pipeline reproducible del río `WaterBodyRiver5`, del tile
`LandscapeStreamingProxy_7_0_0` (NO, macizo) al `LandscapeStreamingProxy_2_7_0`
(E, borde del mapa).

## El pincel de agua: se rompe entre sesiones

El pincel puede quedarse en un estado roto dentro de una sesión del editor:
sus render targets se quedan a `None` y el log repite
`Invalid Render Target for Water Brush. Aborting Render`. Cuando eso pasa,
`Affects Landscape` **no talla nada** (comprobado midiendo: 0 de 16.641 celdas
cambian al activarlo y desactivarlo).

**Reiniciar el editor lo arregla.** Tras el reinicio el pincel se inicializa y
talla con normalidad (5 de 7 testigos cambian al conmutar `affects_landscape`,
y los valores con el pincel desactivado coinciden con el muestreo base).

Si vuelve a fallar: reiniciar el editor antes de dar por hecho que hay que
esculpir a mano. `test_brush_now.py` responde a esa pregunta en un minuto.

El cauce **actual es procedural**, tallado por el pincel a partir del spline y
de `curve_settings` / `water_heightmap_settings`. No hay esculpido permanente
del landscape: si se cambia el spline, el cauce sigue.

`apply_river.py` y `refine_river.py` son de la vía alternativa: tallan a mano
con `ALandscape::EditorApplySpline`. Solo sirven si el pincel está roto, y
modifican el terreno de forma **destructiva**.

## Color de las riberas

El material `M_Landscape_Campus_Natural` mezcla dos colores planos por
pendiente: verde (0.12, 0.30, 0.08) y café de tierra (0.26, 0.22, 0.16).

Medido en el mapa: las riberas del río están a 17° de mediana (p75 23°, p90
29°), y el resto del terreno es casi todo llano (mediana 4°, p90 10°, solo un
0,4 % supera 22°). Con el umbral original el café solo entraba a partir de 45°,
así que las riberas salían verdes.

Ahora la mezcla es `alpha = max(pendiente, máscara del río)`:

- **pendiente**: `clamp(17.09 − 17.35·cos(θ), 0, 1)` → café de 10° a 22°.
  Cubre los taludes. Se cambia en `dirt_by_slope.py` (`ANG0`, `ANG1`).
- **máscara**: `T_RiverMask`, 1024², muestreada con la posición del mundo
  (`(XY + 50400) / 100800`). Cubre el lecho plano del cauce, que la pendiente
  no puede coger nunca, más la orilla próxima. Se regenera con
  `make_river_mask.py` (`MARGEN_PLENO`, `MARGEN_FUNDIDO`) y se reimporta con
  `apply_river_mask.py`.

**El `Clamp(0,1)` del alpha no es opcional.** `LinearInterpolate` de Unreal no
acota el alpha: sin él, con umbrales agresivos las pendientes fuertes daban
alpha de hasta 17, el color se extrapolaba mucho más allá del café (verde
negativo, rojo alto) y salían manchas fucsia y moradas.

**La máscara está horneada para el trazado actual.** Si se mueve el río, hay
que regenerarla o el café se quedará donde estaba el cauce viejo.

**La vía de la capa pintada no funcionó** y se dejó deshecha. El pincel de agua
puede pintar weightmaps, pero registrar una capa nueva exige pasar por
`ULandscapeInfo`, que Python no expone: un `LandscapeLayerInfoObject` creado con
`create_asset` sale con `LayerName` vacío (propiedad de solo lectura) y el peso
pintado se queda en 0,00 en todo el recorrido. Duplicar uno de fábrica arregla
el `LayerName` pero no el registro.

## Edificios del campus

Estaban en una rejilla regular a cota fija (1600-2300) y **13 de 19 quedaban
enterrados**, hasta 2.500 uu bajo tierra.

Además **10 de 19 tenían pitch ±90 y quedaban de canto**. Todas las mallas
están authorizadas con la altura en Z, que es siempre su dimensión menor
(340-1020 uu, alturas de planta): la rotación correcta es pitch y roll a cero.
Al enderezarlos la huella cambia mucho — Artes pasa de 420 a 3000 uu de ancho —
así que hay que recalcular la colocación después de enderezar, nunca antes.

Se recolocaron conservando la distribución del usuario: cada edificio va al
emplazamiento válido más cercano a donde él lo puso (terreno llano bajo toda la
huella, fuera del cauce, sin pisar a otro). **12 de 19 conservan su XY exacto**.

```
edificios_muestreo.py    copia de seguridad + rejilla del terreno actual
enderezar_edificios.py   pitch/roll a cero y reexporta las huellas nuevas
    colocar_edificios.py (fuera del editor) decide los emplazamientos
aplicar_edificios.py     mueve los CampusBuilding_*
asentar_edificios.py     afina la cota con 25 trazados por huella
verificar_edificios.py   apoyo, holgura al cauce y solapes
restaurar_edificios.py   deshace todo desde edificios_backup.json
```

Los dos cubos `RavineBuffer_*` no se tocaron: no son edificios.

## No hacer

**Nunca poner `landscape_material` a `None`** para forzar que el landscape
relea sus capas de pintura: tumba el editor. (`refresh_layers.py` hace eso;
está conservado solo como aviso, no ejecutarlo.) La lista de capas se
reconstruye sola al reabrir el proyecto.

## Orden de ejecución

```
py ".../sample_terrain.py"    # rejilla 129x129 de alturas por trazado de rayos
py ".../base_terrain.py"      # idem, con el pincel desactivado (terreno base)
    design_route.py           # se ejecuta FUERA del editor (python normal)
py ".../apply_river.py"       # primera pasada: spline + metadatos + tallado
py ".../refine_river.py"      # ajuste fino sobre el mismo eje (el bueno)
py ".../verify_river.py"      # secciones transversales medidas
py ".../check_containment.py" # 390 estaciones x 2 márgenes: ¿se sale el agua?
py ".../check_flow.py"        # ¿el flujo va siempre aguas abajo?
```

`design_route.py` es el que decide el trazado. Criterio hidrológico:
inundación por prioridad (minimax) desde la desembocadura — la ruta que
minimiza la cota máxima que hay que atravesar, es decir el drenaje natural con
la mínima excavación. Sobre eso: ajuste a vaguada, meandros acotados por el
relieve y perfil de agua estrictamente descendente.

## Restaurar

`restore_river.py` devuelve el actor (transformada, spline y metadatos) al
estado previo, guardado en `river_backup_estado_previo.json`.
**No revierte el tallado del terreno**: se escribió en la capa `Layer` y no hay
copia de las alturas anteriores.

## Resultado medido (recorrido del usuario, cauce del pincel)

| | |
|---|---|
| longitud | 129.726 uu (1,30 km) |
| puntos originales del usuario reutilizados | 32 de 50 |
| sinuosidad | 1,07 |
| desnivel | 4.427 uu (44,3 m) |
| pendiente media | 3,43 % (6,5 % en cabecera → 0,25 % en la boca) |
| anchura | 380 → 2.350 uu |
| profundidad proyectada / medida | 95 → 430 / 0 → 422 uu |
| velocidad | 340 → 103 |
| márgenes con orilla sobre el agua | 649 de 650 (la que falta es el borde del mapa) |
| tramos con cota ascendente | 0 de 201 |
| muestras con flujo contracorriente | 0 de 201 |
