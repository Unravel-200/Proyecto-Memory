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

## Edificios del campus (blockouts antiguos, eliminados)

La colocación en rejilla que hubo antes se eliminó por completo junto con los
75 blockouts de una sola habitación que la ocupaban (ver el commit
`blockouts: elimina los 75 blockout...` en Modelos-3D). Lo que sigue describe
la colocación **actual**, hecha a partir de las envolventes completas de los
18 edificios generadas en `Modelos-3D/_PlanosLib`.

## Envolventes del campus: importación y colocación

Los 18 edificios (19 volúmenes: el Gimnasio son dos exentos, Gym y Pool) se
modelaron en Blender directamente desde sus planos — ver
`Modelos-3D/_PlanosLib/README.md`. Un FBX por nivel, 85 en total.

```
campus_terreno.py       inventario de actores, extensión del landscape,
                         trazado del río, rejilla gruesa de alturas (20 m)
malla_alturas.py        rejilla fina de alturas por trazado de rayos (10 m),
                         guardada en malla_alturas.json
importar_edificios.py   importa los 85 FBX a /Game/Modelos3D/<Edificio>/ y
                         crea los 3 materiales del campus por slot
resolver_trazado.py     decide DÓNDE va cada edificio (fuera del editor,
                         python normal) y genera campus_trazado.py
campus_trazado.py       GENERADO — no editar a mano, ver más abajo
colocar_campus.py       coloca las envolventes y su zócalo en el mapa
verificar_campus.py     solapes reales entre bounding boxes ya colocados
verificar_rio.py        distancia real de cada edificio al spline del río
revisar_trazado.py      la misma comprobación que resolver_trazado, pero
                         DESDE el editor, contra el terreno en vivo
diag_solapes.py         vuelca loc/yaw/bbox de un edificio, para depurar
```

### El diseño urbano

El río cruza el mapa en diagonal y lo parte en dos. La campaña ya está
organizada en noches por zona (Definitivo §3), así que el trazado las respeta:

| Zona | Avenida | Edificios | Noche |
|---|---|---|---|
| Sur | Y = −100, este-oeste | Biblioteca, Generales, Educación, Mantenimiento, Ciencias, Medicina, Psicología, Ingeniería, Soda, Residencias, Centro Cultural | 1 y 2 |
| Norte | X = +100, norte-sur | Informática, Artes, Auditorio, Historia, Derecho, Gimnasio, Piscina | 3 |
| Remate norte | — | Rectoría (torre de 40 m) | 4 |

Cada avenida tiene dos hileras enfrentadas. `resolver_trazado.py` no inventa
el urbanismo — las hileras y sus lados son fijos — pero sí decide **dónde**
cae cada edificio dentro de su hilera: desliza cada uno a lo largo del eje y
prueba las permutaciones del orden de la hilera completa, buscando la
posición donde el terreno bajo su huella sea lo más parejo posible, sin pisar
a otro ni acercarse a menos de 55 m del río. Desnivel máximo bajo cualquier
huella: 4.2 m (Gimnasio); 17 de 19 quedan por debajo de 3.5 m.

### El giro del pivote: el exportador invierte Y

**Encontrado verificando bounding boxes, no asumido.** El pivote de cada malla
es la esquina suroeste al nivel del suelo *en Blender*. Pero
`blender_modelo.py` exporta con `axis_forward='-Z', axis_up='Y'` — la
convención estándar Blender→Unreal — y esa conversión invierte el eje Y: el
mesh importado se extiende en Y local de **−H a 0**, no de 0 a H.

Comprobado leyendo `edificios_importados.json` para Medicina (H = 50 m):
`min Y = -5000, max Y ≈ 0`. Confirma la inversión.

Dos consecuencias, no una:

1. **El centro local real de la huella es (W/2, −H/2)**, no (W/2, H/2). Con el
   centro viejo, cada edificio se colocaba desplazado H metros de donde debía,
   lo que producía solapes falsos entre edificios de hileras distintas —
   Medicina y Soda "se solapaban" 41 × 32 m cuando en realidad no se tocaban;
   el zócalo (calculado aparte, en espacio de mundo) se quedaba correctamente
   plantado mientras la envolvente aparecía a 50 m de donde tenía que estar.
2. **La fachada gira con la inversión.** El muro sur del plano (donde está el
   `ACCESO PRINCIPAL`) queda en el extremo alto del rango [−H, 0], no en el
   bajo. Con yaw = 0 la fachada mira a **+Y (norte)**, no a −Y como parece
   intuitivo:

   | yaw | fachada mira a |
   |---:|---|
   | 0 | +Y (norte) |
   | 90 | −X (oeste) |
   | 180 | −Y (sur) |
   | 270 | +X (este) |

`colocar_campus.py` usa el centro corregido; `resolver_trazado.py` ya genera
los yaw de esta tabla, no los "intuitivos". Si se regenera un FBX con otra
convención de ejes, hay que revisar esto de nuevo.

### El zócalo

El terreno es natural y ondulado: casi ninguna huella de 40-85 m de lado cae
sobre algo realmente plano. La cota de planta baja es el punto **más alto**
del terreno bajo la huella (para que ningún promontorio asome dentro del
edificio); el hueco que queda del lado bajo lo cierra un **zócalo
perimetral** — un anillo de 3 m de ancho, no un bloque macizo, porque por
dentro de la huella están los sótanos. Baja hasta 1 m por debajo del punto
más bajo del terreno.

### Verificado

- 0 solapes reales entre bounding boxes (`verificar_campus.py`).
- Ningún edificio a menos de 55 m del río; el más cercano es Informática,
  a 66 m, medido contra el spline real, no contra la copia de puntos
  (`verificar_rio.py`).
- 19 edificios, 85 envolventes + 76 piezas de zócalo, 161 actores en total,
  todos bajo `Campus/<Sur|Norte>/<Edificio>/` en el World Outliner.

### Separación pareja: por qué la primera pasada se sentía "pegada"

La primera versión del solver minimizaba la separación (probaba desde
`SEPARACION` hacia arriba y se quedaba con la primera terreno-válida). Con
edificios de 40-85 m eso da hileras irregulares: separación real medida entre
17 y 122 m sin ningún criterio — pegado en unos tramos, un vacío sin explicar
en otros. Reportado directamente por el usuario ("siento que todos los
edificios estan demasiado pegados y hay partes muy vacias"), y confirmado
midiendo los huecos reales antes de tocar nada.

El arreglo no fue solo subir un parámetro. `resolver_fila` ahora persigue una
**separación objetivo constante** (`GAP_OBJETIVO`, penalizando alejarse en
cualquier sentido, no solo pasarse del mínimo). Eso solo no bastaba: al buscar
terreno sin límite, cada edificio derivaba un poco hacia mejor suelo, la
deriva se acumulaba edificio tras edificio, y el último de una hilera de 5 se
quedaba sin margen antes del río -aunque la suma total sí cabía si cada uno se
hubiera quedado cerca de su hueco. La causa: la ventana de búsqueda de cada
edificio estaba anclada a donde había quedado el ANTERIOR, no a un plan fijo.

`horario_ideal()` calcula, una sola vez por hilera, la posición ideal de cada
edificio con `GAP_OBJETIVO` (o el hueco que quepa, si el objetivo no entra en
el largo disponible). Cada edificio busca su mejor terreno en una ventana
acotada alrededor de SU posición ideal —no de la del vecino—, así que la
deriva de uno no contamina al siguiente. Un `piso` (borde derecho del anterior
+ `SEPARACION`) sigue siendo un límite duro por si el terreno empuja a dos
vecinos a la misma zona.

Resultado de esa pasada: separación real entre 30 y 45 m en las 19
posiciones, sin huecos sueltos por encima de `GAP_PARQUE` (60 m) — el propio
ajuste de huecos parejos hizo innecesarios los parques de relleno del intento
anterior. Costó algo de terreno: el desnivel máximo subió de 4.2 a 5.2 m
(Derecho), resuelto igual que el resto por el zócalo.

### Segundo bug real: el borde del mapa estaba mal medido

`malla_alturas.py` usaba `X0,X1 = -560.0, 440.0` para la rejilla de alturas,
salido de un cálculo de `campus_terreno.py` que combinaba mal `loc + bounds`.
El landscape real, medido directo de los 64 `LandscapeStreamingProxy` con
`diag_tiles.py`, es exactamente **-504..504** en X e Y (8×8 losetas de
126 m). La diferencia -hasta 56 m de más por el lado oeste/sur- dejó a
**Medicina** e **Ingeniería** con la mitad del edificio fuera del landscape
real, cerca del tile `LandscapeStreamingProxy_0_2_0`. Lo reportó el usuario
directamente ("hay edificios que están fuera del mapa").

Corregido: `malla_alturas.py` regenerado con los límites reales.
`verificar_bordes.py` comprueba, sobre el bounding box real de cada actor ya
colocado (no sobre la teoría), que nada se salga de ±504.

### Reticula de 5 avenidas: usar el mapa, no solo el borde del río

El trazado de una sola avenida por lado ocupaba una franja de 600×150 m al
sur y 300×170 m al norte, pegada al río, con el resto del landscape -más de
800.000 m²- vacío. El usuario lo notó ("reordena todos los edificios y los
distribuyes más por todo el mapa, dejando menos espacios vacíos").

El rediseño no añade edificios ni cambia la lógica de noches: reparte los
mismos 19 sobre una **retícula de 5 avenidas** en vez de 2 —tres al sur del
río (`S1` Y=−400, `S2` Y=−250, `S3` Y=−100) y dos al norte (`N1` X=80, `N2`
X=260)—, cada una con sus dos hileras enfrentadas de siempre. La huella total
del campus pasa de dos franjas angostas a un área de ~620×380 m al sur y
~350×330 m al norte.

Esto exigió corregir `horario_ideal()`: con avenidas de 620 m para filas de
apenas 1-2 edificios, perseguir solo `GAP_OBJETIVO` (32 m) dejaba casi toda
la avenida vacía al final, pegado el tramo construido a `desde`. Ahora el
hueco entre edificios **reparte el sobrante de la avenida**, con un tope
(`GAP_MAX`, 85 m) a partir del cual ya no sirve para dar aire y la fila se
**centra** en su avenida en vez de seguir estirando el hueco. Huecos reales
resultantes: 30 a 100 m, la mayoría por encima de `GAP_PARQUE` (60 m) y
marcados como candidatos a parque — la propia dispersión ya funciona como el
"menos vacío sin explicar" que se pedía.

Verificado sobre el resultado real: 0 solapes, 0 actores fuera del landscape,
el edificio más cercano al río queda a 79.7 m (mínimo exigido: 55 m; antes de
este rediseño era 66.4 m). Desnivel máximo bajo una huella: 6.1 m (Derecho).

Los dos cubos `RavineBuffer_*` de la colocación antigua no se tocaron: no son
edificios.

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
