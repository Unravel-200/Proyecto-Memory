# Configuración de Unreal Editor — v0.1.0

## Propósito

Esta guía describe cómo integrar en Unreal Editor 5.8 el código C++ de personaje,
movimiento y cámaras de Proyecto-Memory. El código vigente, incluido el salto y la
persistencia de perspectiva, fue compilado correctamente y revisado
estáticamente. El arranque, la posesión, `IMC_Player` y la perspectiva inicial ya
fueron probados en PIE; las demás pruebas funcionales continúan pendientes.

Estado de partida verificado:

- Rama de código: feature/v0.1-player-cameras.
- Commit base mínimo verificado: 336aa91; se admite un descendiente limpio.
- Unreal Engine: 5.8.
- Plataforma compilada: Win64 Development Editor.
- Resultado C++ vigente más reciente: Succeeded.
- Salto, `UPMGameUserSettings` y restauración de cámara: compilados; pruebas
  funcionales pendientes.
- Assets existentes: BP_TestActor y L_Developer_Testing.
- Assets de Input: existen las seis Input Actions y `IMC_Player` con los 16
  mappings de la sección 5 guardados y verificados.
- Assets de Player: `BP_PlayerController` y `BP_PlayerCharacter` existen, están
  configurados y compilan. `BP_GameMode_DeveloperTesting` también existe, usa esas
  dos clases y compila.
- Mapa base: `L_Developer_Testing` usa `BP_GameMode_DeveloperTesting`, contiene
  exactamente un Player Start y no contiene Pawn manual ni lógica de Level
  Blueprint. La geometría compacta de 23 cubos de la sección 10 existe, está
  guardada y fue auditada fuera de PIE mediante MCP. La primera ejecución PIE de
  la sección 11 también está aprobada mediante `EV-PIE-START-01`.

### Sesión de Input completada el 2026-07-22

La sesión se ejecutó con la base de enfriamiento encendida y HWiNFO en modo
Sensors-only:

1. Preflight 19/19 PASS y worktree limpio sobre `8e0aaba`.
2. Unreal abrió sin recompilar y el mapa informó 0 errores y 0 advertencias.
3. Se completó únicamente la sección 5; MCP leyó las 16 filas antes de guardar.
4. `IMC_Player` se guardó y validó; Unreal cerró de forma ordenada.

No se ejecutó PIE ni se continuó a Blueprints. El máximo térmico reportado durante
la sesión fue 70 °C y la última lectura antes del cierre fue 50 °C actual / 66 °C
máxima. Esa sesión dejó preparada la sección 6 y mantuvo los mismos límites
térmicos.

### Sesión de BP_PlayerController completada el 2026-07-22

1. Preflight 19/19 PASS y worktree limpio sobre `d569e31`.
2. Unreal abrió sin recompilar; Map Check informó 0 errores y 0 advertencias.
3. Se completó únicamente la sección 6, con lectura de vuelta de parent, 12
   propiedades y Event Graph vacío.
4. El Blueprint compiló con warnings-as-errors, se guardó por ruta explícita,
   pasó AssetCheck y Unreal cerró de forma ordenada.
5. Después del commit local `81fa688`, postflight obtuvo 22/24 PASS con worktree
   limpio. Los dos FAIL son pendientes esperados: faltan `BP_PlayerCharacter`,
   `BP_GameMode_DeveloperTesting` y las pruebas QA no ejecutadas; el Output Log no
   contiene diagnósticos propios prohibidos.

No se recompiló C++ ni se ejecutó PIE. Después de reiniciar el máximo de HWiNFO,
la sesión empezó en 37 °C actual / 38 °C máxima, alcanzó 69 °C máxima con el
Editor y terminó con 30 °C actual / 69 °C máxima reportadas. Ese cierre dejó
preparada la sección 7, completada en la sesión siguiente.

### Sesión de BP_PlayerCharacter completada el 2026-07-22

1. Preflight 19/19 PASS y worktree limpio sobre `4efac4c`.
2. La base estaba encendida, HWiNFO activo y Blender cerrado. Antes de continuar
   se reportaron 41,6 °C actuales y 86 °C máximos; el pico estaba por debajo del
   límite de pausa de 90 °C.
3. Unreal abrió sin recompilar; Map Check informó 0 errores y 0 advertencias.
4. Se completó únicamente la sección 7. MCP confirmó parent, ocho componentes,
   jerarquía, movimiento, cápsula, crouch, cámaras y CameraMode; no escribió
   propiedades ni aplicó el valor provisional de 60 cm.
5. El Event Graph quedó vacío. El Blueprint compiló dos veces con
   warnings-as-errors, se guardó por ruta explícita, quedó no sucio y pasó
   AssetCheck.
6. Unreal cerró de forma ordenada. Postflight obtuvo 22/24 PASS; los dos FAIL son
   pendientes esperados: en ese momento faltaba el GameMode y quedaban 72
   resultados QA `NOT RUN`.

No se recompiló C++ ni se ejecutó PIE. Ese cierre dejó preparada la sección 8,
completada el 2026-07-26.

### Sesión de BP_GameMode_DeveloperTesting completada el 2026-07-26

1. El cargador y la base estaban conectados, HWiNFO activo y Blender cerrado. Se
   reportaron 41 °C actuales y 46 °C máximos antes de abrir.
2. Preflight 19/19 PASS y worktree limpio sobre `d96e173`.
3. Unreal abrió sin recompilar; Map Check informó 0 errores y 0 advertencias.
4. Se completó únicamente la sección 8. MCP confirmó las dependencias y la
   ausencia del destino antes de crear.
5. El GameMode quedó como hijo exacto de `GameModeBase`, con
   `BP_PlayerCharacter_C` y `BP_PlayerController_C` asignados y releyéndose una
   referencia por vez.
6. El Event Graph quedó vacío. El Blueprint compiló dos veces con
   warnings-as-errors, se guardó por ruta explícita, quedó no sucio y pasó
   AssetCheck.
7. Unreal cerró de forma ordenada. Postflight obtuvo 23/24 PASS; el único FAIL
   esperado son las 70 pruebas QA todavía `NOT RUN`.

No se tocó `L_Developer_Testing`, no se recompiló C++ y no se ejecutó PIE. La
configuración base de la sección 9 se completó en la sesión siguiente.

### Sesión de L_Developer_Testing completada el 2026-07-26

1. La base de enfriamiento e HWiNFO estaban activos. Durante la sesión se
   reportaron 37 °C actuales y 78 °C máximos, por debajo del límite de pausa.
2. Preflight obtuvo 19/19 PASS y el worktree estaba limpio sobre `1629eac`.
3. Se abrió únicamente `/Game/Maps/L_Developer_Testing`; el mapa estaba vacío de
   contenido jugable y no tenía Player Start.
4. World Settings quedó con
   `BP_GameMode_DeveloperTesting_C` como GameMode Override.
5. Se creó exactamente un Player Start en `(0,0,100)`, rotación cero y escala
   uno. MCP confirmó su cápsula de referencia 40/92, cero Pawn manual y cero
   `LevelScriptActor`.
6. Se guardó solo el mapa, se recargó desde disco, Map Check informó 0 errores y
   0 advertencias, AssetCheck inició sin diagnóstico asociado y el asset quedó no
   sucio.
7. El archivo quedó en 11648 bytes con SHA-256
   `08FECC04BD9B391F8C9CEB44CDBB784A95B3994703143C0B4225CF2BB2F822FD`.
   Unreal cerró de forma ordenada con `LogExit: Exiting`.
8. El mapa y los cuatro documentos locales quedaron en el commit `d4d6732`.
   Postflight obtuvo 23/24 PASS con worktree limpio; el único FAIL esperado son
   las 70 filas QA todavía `NOT RUN`.

No se creó geometría, no se ejecutó PIE ni se recompiló C++. El Player Start debe
revisarse otra vez después de crear el suelo. La siguiente sesión empieza en la
sección 10 y debe decidir primero el layout global de la geometría.

### Sesión de geometría completada el 2026-07-27

1. HWiNFO estaba activo y se informó una lectura inicial de 60 °C actual / 67 °C
   máxima. Preflight obtuvo 19/19 PASS sobre `90ef65f`.
2. Se abrió únicamente `/Game/Maps/L_Developer_Testing`. No existía geometría ni
   trabajo ajeno colocado; había un solo Player Start.
3. Se creó primero `GEO01_Floor` en `(0,0,-10)`. MCP confirmó bounds
   `(-1000,-1000,-20)..(1000,1000,0)`, cubo oficial, `BlockAll`,
   `QueryAndPhysics`, `ECC_WorldStatic`, `Static` y física desactivada.
4. El Player Start existente se reutilizó como `PlayerStart_PlayerV01` en
   `(-600,-500,100)`. Después de guardar y recargar, Map Check informó 0 errores
   y 0 advertencias y no apareció `BADsize`. La cápsula real 42/96 deja su base
   en `Z=4` y 83 cm libres a cada lado.
5. Se crearon las otras 22 piezas del layout compacto. MCP auditó las 23 antes
   de guardar y nuevamente después de recargar: nombres, carpetas, transforms,
   bounds, malla, movilidad y colisión coincidieron con esta sección.
6. Los diez escalones apoyan en `Z=0`; la pared de cámara conserva `BlockAll`,
   que bloquea Pawn y Camera. El mapa mantiene el GameMode correcto, un único
   Player Start, cero Pawn manual y cero `LevelScriptActor`.
7. Se guardó solo el mapa, quedó no sucio y la recarga final produjo Map Check
   0/0. El archivo mide 60641 bytes y su SHA-256 es
   `05791E0B54CA19C9BB862E264BD1E4B79BB614133D8C67D4B0C0F03F6DAD81B6`.
   Unreal cerró con `LogExit: Exiting`.
8. El mapa y estos documentos quedaron en `83644f5`. Postflight obtuvo 24/25
   PASS con worktree limpio; el único FAIL esperado eran los 61 IDs QA que en ese
   momento continuaban `NOT RUN`.

No se ejecutó PIE, AssetCheck explícito, Hot Reload ni compilación C++. Los
guardados iniciaron validación automática sin producir un resultado aprobatorio.
Esa sesión dejó preparada la sección 11, completada el mismo 2026-07-27.

### Sesión inicial PIE completada el 2026-07-27

1. Preflight obtuvo 19/19 PASS con worktree limpio sobre `5e1993f`. La base de
   enfriamiento y HWiNFO estaban activos; antes de continuar se informaron 36 °C
   actuales y 68 °C máximos.
2. Se abrió `/Game/Maps/L_Developer_Testing` en UE 5.8 y se realizaron dos
   arranques PIE normales en `PlayMode_InViewPort`, no simulación.
3. MCP confirmó un único `BP_GameMode_DeveloperTesting_C`, un único
   `BP_PlayerController_C` y un único `BP_PlayerCharacter_C`; Controller y
   Character compartían el mismo `PlayerState`.
4. El Controller contenía `EnhancedInputComponent`, `IMC_Player`, las seis Input
   Actions y prioridad 0. Una sonda controlada de `W` durante 0.75 s movió el
   Character de X `-600` a `-384.060176`, demostrando posesión y contexto activo.
   Esta sonda no sustituye la prueba completa `PLR-MOV-001`.
5. La preferencia guardada era First Person y `CameraModeComponent` informó
   `InitialMode=FirstPerson`, `CurrentMode=FirstPerson` y FOV 90°.
6. Los dos PIE cerraron con `bSessionEnded=true`; Unreal cerró después con
   `LogExit: Exiting`. No apareció ninguno de los seis diagnósticos prohibidos
   del Player. Los avisos de introspección MCP y el warning genérico de
   `r.MotionVectorSimulation` no se describen como un log completamente limpio.
7. `PLR-PIE-001` y `EVC-06` quedaron en PASS mediante `EV-PIE-START-01`. No se
   guardó ni modificó ningún asset.
8. Después del commit local `8def4bb`, postflight obtuvo 24/25 PASS con worktree
   limpio. El único FAIL esperado son los 59 IDs QA todavía `NOT RUN`.

### Movimiento cardinal completado el 2026-07-27

1. Preflight obtuvo 19/19 PASS con worktree limpio sobre `c2a61c3`. La base de
   enfriamiento y HWiNFO estaban activos; al finalizar se informaron 36 °C
   actuales y 68 °C máximos.
2. En PIE normal sobre `/Game/Maps/L_Developer_Testing` se activó
   `showdebug enhancedinput` y se probaron W, A, S y D por separado.
3. `IA_Move` mostró W `(0,+1)`, S `(0,-1)`, D `(+1,0)` y A `(-1,0)`. El
   Character avanzó, retrocedió y se desplazó a ambos lados en las direcciones
   esperadas, sin ejes intercambiados.
4. Después de soltar cada tecla, lecturas repetidas de la posición quedaron
   idénticas. La captura liberada de A también mostró `IA_Move=None` y `(0,0)`.
   Intentos duplicados sin foco en el viewport se descartaron y no se usaron como
   evidencia.
5. PIE terminó con `bSessionEnded=true` y Unreal con `LogExit: Exiting`. No se
   modificó ningún asset ni apareció uno de los seis diagnósticos prohibidos.
   Avisos de audio, render y una referencia MCP vencida se registraron como ajenos
   al Player.
6. `PLR-MOV-001` quedó en PASS mediante `EV-MOV-WASD-01`. La evidencia ignorada
   por Git está bajo `UnrealProject/Saved/QA/PlayerV0.1/MOV-20260727/`; el log
   mide 349092 bytes y su SHA-256 es
   `4D5DB3E6A42AE27237F05E9723EBBE5201B2FBE38536292AA4B2818F489106D4`.
7. Después del commit local `9e46365`, postflight obtuvo 24/25 PASS con worktree
   limpio. El único FAIL esperado son los 58 IDs QA todavía `NOT RUN`.

### Movimiento diagonal completado el 2026-07-27

1. Preflight obtuvo 19/19 PASS con worktree limpio sobre `352f629`. La base de
   enfriamiento y HWiNFO estaban activos.
2. Cada combinación inició un PIE limpio en un `startTransform` temporal sobre
   una zona abierta del mismo suelo, sin guardar ni modificar el mapa.
3. `showdebug enhancedinput` mostró W+A `(-1,+1)`, W+D `(+1,+1)`,
   S+A `(-1,-1)` y S+D `(+1,-1)`.
4. Dos capturas temporizadas por combinación midieron aproximadamente
   299.65, 299.83, 300.19 y 299.83 cm/s. Las lecturas visibles están redondeadas;
   runtime confirmó `MaxWalkSpeed=300`, sin la ventaja de velocidad diagonal que
   produciría un vector sin limitar.
5. Al soltar, las cuatro mostraron `IA_Move=None`, `(0,0)` y posiciones idénticas
   en dos lecturas MCP posteriores. Los intentos con foco interceptado o un eje
   bloqueado por el pasillo se descartaron.
6. PIE terminó con `bSessionEnded=true` y Unreal con `LogExit: Exiting`. No
   cambió ningún asset ni apareció uno de los seis diagnósticos prohibidos.
7. `PLR-MOV-002` quedó en PASS mediante `EV-MOV-DIAG-01`. La evidencia ignorada
   por Git está bajo `UnrealProject/Saved/QA/PlayerV0.1/DIAG-20260727/`; el log
   mide 358642 bytes y su SHA-256 es
   `16D19EB3BCB8393D8E4893EA9A9AA90398F87CB0577AE17D68988483B5338324`.
8. Después del commit local `39352d1`, postflight obtuvo 24/25 PASS con worktree
   limpio, Unreal cerrado y el Output Log reconocido. El único FAIL esperado son
   los 57 IDs QA todavía `NOT RUN`.

La siguiente prueba es `PLR-MOV-003`, sección 12 punto 4: look horizontal y
vertical con el ratón, incluido detenerlo y confirmar que no queda movimiento.

Esta guía es operativa y local. No reemplaza el checklist oficial de
Proyecto-Memoria-docs y completar sus casillas no autoriza actualizarlo.

Las decisiones de cámara, salto y controles aprobadas el 2026-07-15 están en
`PLAYER_SETTINGS_V0.1.md`. Ese documento prevalece cuando una instrucción antigua
de esta guía todavía describa una opción que ya fue cerrada.

## Resultado esperado

Al terminar esta guía deben existir:

~~~text
Content/
├── Blueprints/
│   ├── Levels/
│   │   └── BP_GameMode_DeveloperTesting
│   └── Player/
│       ├── BP_PlayerCharacter
│       └── BP_PlayerController
├── Input/
│   ├── Actions/
│   │   ├── IA_Crouch
│   │   ├── IA_Jump
│   │   ├── IA_Look
│   │   ├── IA_Move
│   │   ├── IA_Sprint
│   │   └── IA_ToggleCamera
│   └── Mappings/
│       └── IMC_Player
└── Maps/
    └── L_Developer_Testing
~~~

La documentación oficial ya propone Content/Blueprints/Player para
BP_PlayerCharacter. Las carpetas Input, BP_PlayerController y el GameMode de
prueba son extensiones operativas necesarias para esta implementación; deben
registrarse en la documentación compartida solo cuando el propietario lo autorice.

Los nombres BP_PlayerController y BP_GameMode_DeveloperTesting, así como sus
rutas, son convenciones provisionales de esta guía. La arquitectura oficial aún
no define esos dos assets; no deben presentarse como una decisión aprobada hasta
que se autorice actualizar la documentación compartida.

## Límites de esta sesión de Editor

Esta integración no debe:

- Añadir lógica central a Level Blueprint.
- Duplicar los componentes nativos del Character.
- Crear movimiento o cambio de cámara en Blueprint.
- Usar Hot Reload para cambios UCLASS, UPROPERTY o UFUNCTION.
- Crear tags, hacer merge, push o actualizar el checklist oficial.
- Crear IA_Interact o adelantar el sistema de interacción de v0.2.0.
- Importar una malla sin origen, licencia y escala conocidos.
- Declarar v0.1.0 terminada sin pruebas funcionales.

## 1. Preparar el equipo y el repositorio

Usar la PC adecuada para Unreal Editor. Si el equipo presenta temperatura,
ventiladores o consumo anormales, guardar, cerrar y registrar la prueba como
BLOCKED.

Antes de abrir:

1. Confirmar que Unreal Editor está cerrado.
2. Abrir una terminal en Proyecto-Memory.
3. Confirmar la rama y el estado:

~~~powershell
git status --short --branch
git log -1 --oneline
~~~

Resultado esperado:

~~~text
## feature/v0.1-player-cameras
5eccd8e ... fix(player): limpiar estado al perder posesión
~~~

Un commit posterior es válido si contiene 5eccd8e y el árbol está limpio.

4. Abrir UnrealProject/ProyectoMemoria.uproject con Unreal Engine 5.8.
5. No aceptar una conversión a otra versión del motor.
6. Si Unreal solicita recompilar módulos, cancelar, cerrar y realizar una
   compilación completa desde terminal antes de reabrir.

## 2. Comprobaciones iniciales del proyecto

En Edit > Plugins:

- Confirmar que Enhanced Input está habilitado.
- No habilitar plugins adicionales para esta tarea.
- Reiniciar solo si Unreal lo solicita por un cambio real.

En Project Settings > Engine > Input:

- Default Player Input Class debe ser EnhancedPlayerInput.
- Default Input Component Class debe ser EnhancedInputComponent.

El repositorio ya contiene esos valores en DefaultInput.ini. No editarlos a mano
si el Editor los muestra correctamente.

Abrir Output Log y conservarlo visible durante la configuración.

## 3. Crear las carpetas

En Content Drawer crear:

~~~text
/Game/Input
/Game/Input/Actions
/Game/Input/Mappings
/Game/Blueprints/Player
/Game/Blueprints/Levels
~~~

No mover BP_TestActor ni L_Developer_Testing.

## 4. Crear las Input Actions

En /Game/Input/Actions:

1. Clic derecho.
2. Input > Input Action.
3. Crear los seis assets.
4. Abrir cada asset y configurar Value Type.

| Asset | Value Type | Triggers del asset |
|---|---|---|
| IA_Move | Axis2D | Ninguno |
| IA_Look | Axis2D | Ninguno |
| IA_Sprint | Digital/Bool | Ninguno |
| IA_Crouch | Digital/Bool | Ninguno |
| IA_Jump | Digital/Bool | Ninguno |
| IA_ToggleCamera | Digital/Bool | Ninguno |

### Contrato obligatorio de IA_Crouch

IA_Crouch debe permanecer activa durante toda la pulsación. El C++ mide la
duración con FInputActionInstance::GetElapsedTime().

No añadir:

- Hold.
- Tap.
- Pressed.
- Released.
- Pulse.

Si más adelante se desea un trigger explícito, usar Down y volver a ejecutar todas
las pruebas de Started, Completed y Canceled.

## 5. Crear IMC_Player

En /Game/Input/Mappings:

1. Clic derecho.
2. Input > Input Mapping Context.
3. Nombrar el asset IMC_Player.
4. Abrirlo y agregar los mappings siguientes.

### IA_Move — teclado

| Tecla | Modificadores, en orden | Valor esperado |
|---|---|---|
| W | Swizzle Input Axis Values = YXZ | X=0, Y=1 |
| S | Negate; Swizzle Input Axis Values = YXZ | X=0, Y=-1 |
| A | Negate | X=-1, Y=0 |
| D | Ninguno | X=1, Y=0 |

Una tecla Digital produce inicialmente el valor en X. Swizzle YXZ mueve ese valor
al eje Y para avanzar o retroceder.

### IA_Move — mando

Agregar:

~~~text
Gamepad Left Thumbstick 2D-Axis
~~~

`DefaultInput.ini` define zona muerta 0 para los cuatro ejes principales del
mando, por decisión del propietario. No añadir un modificador Dead Zone en
Enhanced Input: los movimientos pequeños y cualquier drift real deben permanecer
visibles durante QA.

Si existe drift después de probar, no corregirlo por suposición:

1. Registrar el dispositivo.
2. Registrar el valor y el efecto observado.
3. Mantener la decisión de zona muerta 0 hasta nueva autorización del propietario.

Los nombres de las teclas pueden aparecer traducidos en el Editor. Para los
sticks y el ratón se debe elegir la entrada 2D-Axis, no mapear X e Y como acciones
separadas.

### IA_Look

Agregar:

~~~text
Mouse XY 2D-Axis
Gamepad Right Thumbstick 2D-Axis
~~~

No añadir Negate inicialmente. La preferencia personal de inversión se controla
con bInvertLookY en BP_PlayerController. Si el signo base del dispositivo es
incorrecto para todos los usuarios, corregir el Mapping y documentarlo.

### IA_Sprint

Agregar:

~~~text
Left Shift
Gamepad Left Thumbstick Button
~~~

Sin triggers adicionales.

### IA_Crouch

Agregar:

~~~text
C
Left Control
Gamepad Face Button Right
~~~

Sin triggers ni modificadores. Mantener el contrato descrito en la sección 4.

### IA_Jump

Agregar:

~~~text
Space Bar
Gamepad Face Button Bottom
~~~

Sin triggers ni modificadores. Al presionar desde crouch, el C++ debe intentar
levantar al personaje y saltar solo si recuperó espacio suficiente.

### IA_ToggleCamera

Agregar:

~~~text
V
Gamepad Face Button Top
~~~

Sin triggers adicionales.

Guardar IMC_Player.

### Procedimiento MCP seguro para IMC_Player

El MCP oficial de Unreal 5.8 automatizó la lectura, pero no pudo ampliar de forma
segura el array después del primer elemento; por eso el resto se completó
manualmente. Si alguna vez se reconstruye el asset desde cero, usar llamadas en
serie y aplicar este control antes de guardar:

1. Leer `defaultKeyMappings` y confirmar el estado de `mappings`. En una
   reconstrucción nueva debe estar vacío. No escribir en la propiedad superior
   `mappings`, porque está obsoleta desde Unreal 5.7.
2. Escribir únicamente D → IA_Move, sin modificadores, y leer el resultado.
3. Si acción, tecla y arrays vacíos coinciden, probar W → IA_Move con
   `InputModifierSwizzleAxis` y comprobar que su orden sea `YXZ`.
4. Solo si ambas pruebas coinciden, escribir las 16 filas de esta sección y volver
   a leerlas antes de guardar.
5. Si una lectura difiere, no guardar: configurar el asset manualmente en el
   Editor.

Para `ObjectTools.set_properties`, `values` debe ser un texto que contiene JSON y
la ruta raíz correcta es:

~~~json
{
  "defaultKeyMappings": {
    "mappings": []
  }
}
~~~

Rutas de los modificadores:

~~~text
/Script/EnhancedInput.InputModifierNegate
/Script/EnhancedInput.InputModifierSwizzleAxis
~~~

Sus valores predeterminados ya producen Negate en los tres ejes y Swizzle `YXZ`;
no añadir campos dentro del mismo objeto de referencia porque el convertidor puede
ignorarlos silenciosamente. Nombres internos de las teclas no alfabéticas:

| Control visible | `keyName` interno |
|---|---|
| Espacio | SpaceBar |
| Shift izquierdo | LeftShift |
| Ctrl izquierdo | LeftControl |
| Palanca izquierda 2D | Gamepad_Left2D |
| Palanca derecha 2D | Gamepad_Right2D |
| Botón de palanca izquierda | Gamepad_LeftThumbstick |
| Botón derecho | Gamepad_FaceButton_Right |
| Botón inferior | Gamepad_FaceButton_Bottom |
| Botón superior | Gamepad_FaceButton_Top |
| Mouse XY | Mouse2D |

Después de la lectura final deben existir exactamente 16 filas: Move 5, Look 2,
Sprint 2, Crouch 3, Jump 2 y ToggleCamera 2. Todos los triggers quedan vacíos;
solo W, S y A tienen modificadores, S conserva el orden Negate seguido de Swizzle,
y no existe ningún modificador Dead Zone.

## 6. Crear BP_PlayerController

Estado: **completada el 2026-07-22**. Se verificaron el parent exacto
`/Script/ProyectoMemoria.PMPlayerController`, todos los valores de la tabla, el
Event Graph vacío, dos compilaciones con warnings-as-errors y el guardado
explícito. El archivo resultante mide 22564 bytes y su SHA-256 es
`A9C8D639135632B2FECE4E64922596B1F4146E17E627D2303DD832EC1A5597B1`.

En /Game/Blueprints/Player:

1. Clic derecho > Blueprint Class.
2. All Classes.
3. Buscar PMPlayerController.
4. Seleccionar APMPlayerController.
5. Nombrar BP_PlayerController.
6. En Class Settings confirmar Parent Class = PMPlayerController.

Si PMPlayerController no aparece:

1. Cerrar el Editor.
2. Compilar ProyectoMemoriaEditor de forma completa.
3. Reabrir.
4. No utilizar Hot Reload como solución.

En Class Defaults, categoría ProyectoMemoria > Player > Input, asignar:

| Propiedad | Valor |
|---|---|
| Player Mapping Context | IMC_Player |
| Move Action | IA_Move |
| Look Action | IA_Look |
| Sprint Action | IA_Sprint |
| Crouch Action | IA_Crouch |
| Jump Action | IA_Jump |
| Toggle Camera Action | IA_ToggleCamera |
| Look Sensitivity X | 1.0 |
| Look Sensitivity Y | 1.0 |
| Invert Look Y | false |
| Mapping Priority | 0 |
| Crouch Hold Threshold | 0.25 s |

Event Graph debe permanecer vacío.

Compilar y guardar el Blueprint.

## 7. Crear BP_PlayerCharacter

**Estado: completada y auditada el 2026-07-22. No repetir si el asset y su hash
coinciden con `EV-BPCHAR-01` de `QA_PLAYER_V0.1.md`.**

En /Game/Blueprints/Player:

1. Clic derecho > Blueprint Class.
2. All Classes.
3. Buscar PMPlayerCharacter.
4. Seleccionar APMPlayerCharacter.
5. Nombrar BP_PlayerCharacter.
6. Confirmar Parent Class = PMPlayerCharacter.

No duplicar componentes. La jerarquía heredada debe incluir:

~~~text
BP_PlayerCharacter
├── CapsuleComponent
├── ArrowComponent
├── Mesh
├── CharacterMovement
├── FirstPersonCamera
├── ThirdPersonCameraBoom
│   └── ThirdPersonCamera
└── CameraModeComponent
~~~

### Valores de movimiento

| Propiedad | Valor inicial |
|---|---|
| Walk Speed | 300 cm/s |
| Sprint Speed | 550 cm/s |
| Crouch Speed | 180 cm/s |

### Cápsula y crouch

Confirmar:

| Propiedad | Valor |
|---|---|
| Capsule Radius | 42 cm |
| Capsule Half Height | 96 cm |
| CharacterMovement: Can Crouch | true |

Crouched Half Height = 60 cm es una propuesta provisional para la primera prueba,
no un valor aprobado. Debe validarse con malla, animación y túnel bajo.

### Cámara de primera persona

Confirmar:

| Propiedad | Valor |
|---|---|
| Relative Location | X=-10, Y=0, Z=64 |
| Use Pawn Control Rotation | true |

### Cámara de tercera persona

Confirmar:

| Componente/propiedad | Valor |
|---|---|
| ThirdPersonCameraBoom: Target Arm Length | 300 cm |
| ThirdPersonCameraBoom: Use Pawn Control Rotation | true |
| ThirdPersonCameraBoom: Probe Size | 12 cm |
| ThirdPersonCameraBoom: Probe Channel | Camera |
| ThirdPersonCamera: Use Pawn Control Rotation | false |

### CameraModeComponent

| Propiedad | Valor |
|---|---|
| Initial Mode | First Person |
| First Person Field Of View | 90 |
| Third Person Field Of View | 90 |
| Third Person Arm Length | 300 cm |

### Malla

Si no existe una malla esquelética con licencia y escala verificadas, dejar Mesh
vacío. Movimiento y cámaras pueden probarse sin representación visual; la prueba
de apariencia en tercera persona quedará BLOCKED.

No añadir lógica al Event Graph.

Compilar y guardar el Blueprint.

## 8. Crear BP_GameMode_DeveloperTesting

**Estado: completada y auditada el 2026-07-26. No repetir si el asset y su hash
coinciden con `EV-BPGM-01` de `QA_PLAYER_V0.1.md`.**

La documentación oficial no define todavía una convención de GameMode. Para esta
guía se propone un Blueprint de configuración de pruebas:

~~~text
/Game/Blueprints/Levels/BP_GameMode_DeveloperTesting
~~~

1. Clic derecho > Blueprint Class.
2. Seleccionar GameModeBase.
3. Nombrar BP_GameMode_DeveloperTesting.
4. En Class Defaults configurar:

| Propiedad | Clase |
|---|---|
| Default Pawn Class | BP_PlayerCharacter |
| Player Controller Class | BP_PlayerController |

Conservar vacío el Event Graph. Compilar y guardar.

## 9. Configurar L_Developer_Testing

**Estado: completado y revalidado el 2026-07-27. `LVL-01` está en PASS mediante
`EV-LVL-SETUP-01` y `EV-GEO-LVL-01`. No repetir la asignación del GameMode ni
crear otro Player Start.**

Abrir /Game/Maps/L_Developer_Testing.

En World Settings:

~~~text
GameMode Override = BP_GameMode_DeveloperTesting
~~~

Agregar un Player Start:

- No debe estar dentro del suelo.
- Debe tener espacio para una cápsula de 84 cm de diámetro y 192 cm de altura.
- La flecha debe señalar la orientación inicial.
- No debe mostrar BADsize.

No colocar manualmente BP_PlayerCharacter si el GameMode ya lo genera.

No añadir lógica al Level Blueprint.

## 10. Crear geometría de prueba

**Estado: completado y revalidado desde disco el 2026-07-27 mediante
`EV-GEO-LVL-01`. No recrear ni duplicar estas piezas. La primera ejecución PIE de
la sección 11 y el movimiento cardinal y diagonal también están completados; la
siguiente tarea es `PLR-MOV-003`.**

Usar Shapes > Cube para evitar importar assets. El cubo básico mide 100 cm por
lado; su escala es dimensión deseada / 100.

En World Outliner crear la carpeta PlayerTests.

### Layout compacto reproducible

El 2026-07-26 se eligió este layout técnico para la pista de pruebas. Completa
coordenadas que la especificación dimensional no definía; no representa el diseño
visual final del juego.

Convenciones:

- todas las medidas y ubicaciones están en centímetros;
- todos los cubos usan `/Engine/BasicShapes/Cube`, rotación `(0,0,0)`,
  `Collision Preset = BlockAll` y `Mobility = Static`;
- la superficie superior del suelo queda en `Z=0`;
- los actores se organizan bajo las subcarpetas indicadas de `PlayerTests`;
- el Player Start existente se mueve y se reutiliza; no crear un segundo;
- pasillo y habitación quedan sin techo;
- la pared con puerta también es la pared oeste de la habitación;
- las paredes y el techo del túnel adoptan 20 cm de grosor operativo;
- no se añade el descanso opcional de la escalera.

Mover el único Player Start a:

| Actor | Carpeta | Ubicación | Rotación |
|---|---|---:|---:|
| `PlayerStart_PlayerV01` | `PlayerTests/Spawn` | `(-600,-500,100)` | `(0,0,0)` |

Con la cápsula real 42/96, la base queda en `Z=4`. Después de crear el suelo hay
que recargar el mapa y confirmar Map Check 0/0, ausencia de `BADsize` y espacio
libre antes de cambiar `LVL-01` a PASS.

Crear estas 23 piezas:

| Actor | Carpeta | Ubicación | Dimensiones |
|---|---|---:|---:|
| `GEO01_Floor` | `PlayerTests/GEO01_Floor` | `(0,0,-10)` | `2000×2000×20` |
| `GEO02_Corridor_Wall_South` | `PlayerTests/GEO02_Corridor` | `(-300,-635,150)` | `1000×20×300` |
| `GEO02_Corridor_Wall_North` | `PlayerTests/GEO02_Corridor` | `(-300,-365,150)` | `1000×20×300` |
| `GEO03_DoorWall_SouthPier` | `PlayerTests/GEO03_DoorWall` | `(210,-615,150)` | `20×110×300` |
| `GEO03_DoorWall_NorthPier` | `PlayerTests/GEO03_DoorWall` | `(210,-385,150)` | `20×110×300` |
| `GEO03_DoorWall_Lintel` | `PlayerTests/GEO03_DoorWall` | `(210,-500,270)` | `20×120×60` |
| `GEO04_Room_Wall_South` | `PlayerTests/GEO04_Room` | `(370,-660,150)` | `300×20×300` |
| `GEO04_Room_Wall_North` | `PlayerTests/GEO04_Room` | `(370,-340,150)` | `300×20×300` |
| `GEO04_Room_Wall_East` | `PlayerTests/GEO04_Room` | `(530,-500,150)` | `20×340×300` |
| `GEO05_Tunnel_Wall_South` | `PlayerTests/GEO05_Tunnel` | `(-550,30,80)` | `300×20×160` |
| `GEO05_Tunnel_Wall_North` | `PlayerTests/GEO05_Tunnel` | `(-550,170,80)` | `300×20×160` |
| `GEO05_Tunnel_Roof` | `PlayerTests/GEO05_Tunnel` | `(-550,100,150)` | `300×160×20` |
| `GEO06_Stair_01` | `PlayerTests/GEO06_Stairs` | `(-285,100,8.5)` | `30×220×17` |
| `GEO06_Stair_02` | `PlayerTests/GEO06_Stairs` | `(-255,100,17)` | `30×220×34` |
| `GEO06_Stair_03` | `PlayerTests/GEO06_Stairs` | `(-225,100,25.5)` | `30×220×51` |
| `GEO06_Stair_04` | `PlayerTests/GEO06_Stairs` | `(-195,100,34)` | `30×220×68` |
| `GEO06_Stair_05` | `PlayerTests/GEO06_Stairs` | `(-165,100,42.5)` | `30×220×85` |
| `GEO06_Stair_06` | `PlayerTests/GEO06_Stairs` | `(-135,100,51)` | `30×220×102` |
| `GEO06_Stair_07` | `PlayerTests/GEO06_Stairs` | `(-105,100,59.5)` | `30×220×119` |
| `GEO06_Stair_08` | `PlayerTests/GEO06_Stairs` | `(-75,100,68)` | `30×220×136` |
| `GEO06_Stair_09` | `PlayerTests/GEO06_Stairs` | `(-45,100,76.5)` | `30×220×153` |
| `GEO06_Stair_10` | `PlayerTests/GEO06_Stairs` | `(-15,100,85)` | `30×220×170` |
| `GEO07_CameraWall` | `PlayerTests/GEO07_CameraWall` | `(250,600,150)` | `500×20×300` |

Dimensiones interiores resultantes:

- pasillo: `X=-800..200`, `Y=-625..-375`, 1000 × 250 × 300;
- puerta: `Y=-560..-440`, `Z=0..240`, hueco libre 120 × 240;
- habitación: `X=220..520`, `Y=-650..-350`, 300 × 300 × 300;
- túnel: `X=-700..-400`, `Y=40..160`, `Z=0..140`,
  300 × 120 × 140;
- escalera: `X=-300..0`, `Y=-10..210`, diez niveles de 17 cm hasta
  `Z=170`;
- pared de cámara: `X=0..500`, `Y=590..610`, `Z=0..300`.

El circuito comienza dentro del pasillo mirando hacia `+X`. Tras probar la
habitación, se regresa por el pasillo, se rodea su extremo oeste, se atraviesa el
túnel, se sube y baja la escalera y finalmente se prueba la pared de cámara.

### Suelo

~~~text
Dimensiones de prueba: 2000 × 2000 × 20 cm
Collision Preset: BlockAll
Mobility: Static
~~~

### Pasillo

~~~text
Largo interior: 1000 cm
Ancho interior: 250 cm
Altura: 300 cm
Grosor de pared: 20 cm
~~~

### Puerta

Construir la abertura con cubos, sin booleanos:

~~~text
Ancho libre: 120 cm
Alto libre: 240 cm
Grosor de pared: 20 cm
~~~

El ancho y alto recomendados proceden de la guía oficial de dimensiones. En esta
versión solo se prueba la abertura y su colisión; no se crea todavía una puerta
interactiva.

### Habitación pequeña

~~~text
Interior: 300 × 300 cm
Altura: 300 cm
Puerta: 120 × 240 cm
~~~

### Túnel de crouch

~~~text
Largo: 300 cm
Ancho: 120 cm
Altura interior: 140 cm
~~~

La altura supone Crouched Half Height provisional de 60 cm. La prueba debe
confirmar que el Character entra agachado y no puede levantarse dentro.

### Escaleras

Crear 10 escalones:

~~~text
Altura por escalón: 17 cm
Profundidad por escalón: 30 cm
Ancho: 220 cm
Altura total: 170 cm
~~~

Los valores corresponden a la escalera principal recomendada. Si se añade un
descanso, usar 220 × 220 cm.

Para construirla con cubos sin dejar piezas flotantes, numerar los escalones de
1 a 10 y usar columnas apoyadas en el suelo:

~~~text
Profundidad de cada columna: 30 cm
Ancho de cada columna: 220 cm
Altura de la columna n: n × 17 cm
Centro longitudinal de la columna n: (n - 0.5) × 30 cm
Centro vertical de la columna n: (n × 17 cm) / 2
~~~

También se puede usar una escalera de Modeling Mode si está disponible, siempre
que el resultado final conserve esas dimensiones y tenga colisión verificable.

### Pared de cámara

~~~text
Dimensiones: 500 × 20 × 300 cm
Collision: debe bloquear Camera y Pawn
~~~

Guardar L_Developer_Testing.

## 11. Primera ejecución PIE

**Estado: completado el 2026-07-27 mediante `EV-PIE-START-01`; no repetir por
costumbre la auditoría de arranque. Sí iniciar PIE de nuevo para cada prueba
funcional. `PLR-MOV-001..002` también están completadas; continuar en la sección
12, punto 4, con `PLR-MOV-003`.**

Antes de Play:

- Abrir Output Log.
- Seleccionar Selected Viewport.
- Confirmar el GameMode Override.
- Confirmar que todos los Blueprints compilan.

Al iniciar, el flujo esperado es:

~~~text
GameMode
├── crea BP_PlayerController
└── crea BP_PlayerCharacter en Player Start
        ↓
Controller posee Character
        ↓
BeginPlay añade IMC_Player
        ↓
CameraMode aplica la vista guardada o First Person en la primera ejecución
~~~

Hacer clic dentro del viewport para capturar input.

No deben aparecer:

~~~text
has no IMC_Player assigned
has one or more unassigned IA_* assets
has an incomplete camera setup
APMPlayerController requires EnhancedInputComponent
PMGameUserSettings is not active
Could not persist the preferred camera mode
~~~

## 12. Orden de pruebas

Registrar cada prueba como PASS, FAIL o BLOCKED.

1. Spawn y posesión. **Completado: `PLR-PIE-001`.**
2. Movimiento W/A/S/D. **Completado: `PLR-MOV-001`.**
3. Movimiento diagonal. **Completado: `PLR-MOV-002`.**
4. Look con ratón. **Siguiente: `PLR-MOV-003`.**
5. Caminar a aproximadamente 300 cm/s.
6. Sprint a aproximadamente 550 cm/s y retorno a 300.
7. Toque corto de crouch desde pie.
8. Segundo toque corto para levantarse.
9. Mantener crouch al menos 0.25 s y soltar.
10. Mantener crouch cuando ya estaba agachado y soltar.
11. Intentar cancelar la acción desde pie y desde agachado mediante un escenario
    reproducible: debe restaurar la postura inicial. Si Enhanced Input no emite
    Canceled de forma determinista, registrar BLOCKED y cubrirlo después con una
    prueba automatizada; no alterar los triggers de IA_Crouch para forzarlo.
12. Crouch mientras se corre: sprint debe cancelarse.
13. Intentar levantarse bajo techo bajo: UnCrouch debe conservar la postura si no
    hay espacio.
14. Cambio First Person a Third Person.
15. Cambio Third Person a First Person sin salto brusco de yaw.
16. Alternar cámara mientras se camina, corre y está agachado.
17. Colisión de cámara contra pared.
18. Pasillo, puerta, habitación y escaleras.
19. Mando físico y drift; un mapping por sí solo no prueba compatibilidad.
20. Sensibilidad compartida actual e inversión Y. La separación mouse/mando se
    valida después con el menú de ajustes.
21. Rendimiento.
22. Cerrar y reabrir el Editor para confirmar que las referencias persisten.
23. Salto normal con Espacio y con A/X; soltar el botón detiene la orden de salto.
24. Saltar desde crouch con espacio: primero se levanta y después salta.
25. Saltar agachado bajo techo: no atraviesa el techo ni salta inesperadamente al
    salir más tarde.
26. Cambiar de perspectiva y sustituir el Pawn mediante un arnés controlado de
    respawn, sin lógica central en Level Blueprint; confirmar que el nuevo Pawn
    conserva la vista del anterior.
27. Cambiar de perspectiva, cerrar completamente el juego y volver a abrirlo:
    conserva la última vista; una instalación sin preferencia inicia en 1P.

### Preparación reproducible de las pruebas 26 y 27

La versión actual no incluye todavía un sistema de muerte. Para la prueba 26 se
necesita un arnés que destruya el Pawn y haga que el mismo PlayerController reciba
otro mediante `AGameModeBase::RestartPlayer`. Si ese arnés C++ o automatizado no
existe, registrar `PLR-CAM-007` como `BLOCKED`; no improvisar lógica central en el
Level Blueprint ni confundir reiniciar PIE con un respawn.

Para la prueba 27:

1. Probar primero el perfil existente: cambiar a 3P, cerrar el juego normalmente
   y volver a abrirlo.
2. Para simular la primera ejecución, usar preferentemente un usuario nuevo de
   Windows en la PC de QA.
3. Si no es posible, cerrar Unreal, respaldar fuera del repositorio el
   `GameUserSettings.ini` generado bajo `UnrealProject/Saved/Config`, apartarlo
   temporalmente y restaurarlo al terminar.
4. Nunca borrar una preferencia del propietario sin respaldo ni marcar 1P como
   primera ejecución si aún se cargó una configuración previa.

Comandos útiles en la consola:

~~~text
showdebug character
showdebug enhancedinput
show collision
stat fps
stat unit
stat game
~~~

DefaultInput.ini permite abrir consola con Tilde y con la tecla |.

En la prueba manual, comparar un toque claramente corto con una pulsación de al
menos 0.5 s. Una persona no puede validar de forma fiable diferencias de 0.01 s.

Los límites siguientes requieren una prueba automatizada o instrumentación
temporal que registre GetElapsedTime():

~~~text
0.24 s
0.25 s
0.26 s
~~~

Repetir a 30, 60 y 120 FPS si el equipo lo permite.

Detener PIE también permite comprobar que EndPlay limpia órdenes transitorias.
OnUnPossess y Canceled necesitan un caso controlado propio; no deben marcarse PASS
solo porque el estado parezca correcto al cerrar el Editor.

## 13. Guardar y revisar cambios

1. Detener PIE.
2. Resolver errores antes de continuar.
3. Compilar cada Blueprint.
4. Save All.
5. Cerrar Unreal Editor.
6. Comprobar Git desde Proyecto-Memory.

Cambios esperados:

~~~text
UnrealProject/Content/Input/Actions/*.uasset
UnrealProject/Content/Input/Mappings/IMC_Player.uasset
UnrealProject/Content/Blueprints/Player/BP_PlayerCharacter.uasset
UnrealProject/Content/Blueprints/Player/BP_PlayerController.uasset
UnrealProject/Content/Blueprints/Levels/BP_GameMode_DeveloperTesting.uasset
UnrealProject/Content/Maps/L_Developer_Testing.umap
~~~

No usar git add .; preparar rutas exactas después de revisar el estado.

No hacer push, merge o tag hasta autorización.

## 14. Diagnóstico rápido

### La clase C++ no aparece al crear Blueprint

- Cerrar el Editor.
- Compilar ProyectoMemoriaEditor.
- Reabrir.
- Confirmar UE 5.8 y la rama correcta.
- No depender de Hot Reload.

### El jugador no aparece

- Confirmar Player Start.
- Confirmar GameMode Override.
- Confirmar Default Pawn Class.
- Buscar BADsize.

### El jugador aparece pero no responde

- Hacer clic dentro del viewport.
- Confirmar Player Controller Class.
- Confirmar IMC_Player y las seis IA en BP_PlayerController.
- Revisar LogPMPlayerController.
- Confirmar las clases Enhanced en Project Settings.

### Aparece `requires EnhancedInputComponent`

- Confirmar Default Input Component Class = EnhancedInputComponent.
- Confirmar Default Player Input Class = EnhancedPlayerInput.
- Confirmar que Enhanced Input está habilitado.
- Reiniciar el Editor después de corregir la configuración.

### Aparecen dos jugadores

- Eliminar el Pawn colocado manualmente o quitarle Auto Possess.
- Conservar un solo Player Start.
- Permitir que BP_GameMode_DeveloperTesting cree el Pawn y el Controller.

### W/S se mueven lateralmente

- Revisar Swizzle YXZ.
- Revisar que IA_Move sea Axis2D.

### Crouch siempre se levanta inmediatamente

- Eliminar triggers Pressed, Tap, Hold, Released o Pulse.
- Confirmar que IA_Crouch permanece activa mientras la tecla está abajo.
- Confirmar Crouch Hold Threshold = 0.25 s.

### El Character no puede levantarse

- Comprobar si hay techo u overlap sobre la cápsula.
- Bajo el túnel de prueba es el comportamiento correcto de UnCrouch.
- Fuera del túnel, revisar colisión y Crouched Half Height.

### La cámara no cambia

- Confirmar IA_ToggleCamera en BP_PlayerController.
- Confirmar V en IMC_Player.
- Confirmar CameraModeComponent en BP_PlayerCharacter.

### La cámara atraviesa paredes

- Confirmar tercera persona.
- Confirmar que la pared bloquea Camera.
- Confirmar Probe Channel = Camera y Probe Size = 12 cm.

### El Character es invisible

Es esperado si Mesh permanece vacío. No bloquea pruebas de input, cápsula o
cámara; sí bloquea evaluación visual de tercera persona.

## 15. Condiciones para detener la sesión

Detener, guardar y registrar BLOCKED si:

- El equipo se sobrecalienta.
- Unreal solicita convertir el proyecto a otra versión.
- Aparecen errores C++ o Blueprint que no se comprenden.
- El Editor intenta modificar archivos fuera de Proyecto-Memory.
- El mapa o los assets existentes parecen dañados.
- Se requiere una decisión de diseño pendiente.

## 16. Decisiones que esta guía no cierra

- Malla y Animation Blueprint definitivos.
- Valor final de Crouched Half Height.
- Valor final de Crouch Hold Threshold.
- Convención oficial para BP_PlayerController y GameMode.

Jump, persistencia de perspectiva, cámara inmediata, layout de mando y zona muerta
0 ya están decididos en `PLAYER_SETTINGS_V0.1.md`. Su C++ y configuración están
compilados, pero siguen pendientes de prueba funcional, no de decisión.

La reasignación de controles en tiempo de ejecución es obligatoria en la etapa
posterior de menús y ajustes. No bloquea v0.1.0 y esta guía todavía no crea su UI.

## 17. Deudas y contradicciones documentales conocidas

Estas observaciones se registran aquí para no perderlas. No autorizan editar la
documentación oficial:

- Enhanced Input figura como decisión pendiente en el control maestro, aunque
  Build.cs, DefaultInput.ini y el C++ actual ya lo adoptan.
- El estado oficial no presenta todavía v0.0.1 como una versión formalmente
  cerrada, mientras este trabajo de v0.1.0 permanece aislado en
  feature/v0.1-player-cameras. No hacer merge ni crear tags saltando esa revisión
  secuencial.
- El propietario aprobó guardar la perspectiva. La implementación usa
  `UPMGameUserSettings`, pero debe compilarse y validarse antes de ejecutar las
  pruebas 26 y 27.
- El checklist menciona interacción básica, pero la interfaz y el componente de
  interacción pertenecen a v0.2.0. Por eso esta guía no crea IA_Interact.
- El mapa de arquitectura indica Gameplay Tags desde v0.1.0, pero el checklist
  puntual no define su integración y el código actual no los registra.
- BP_PlayerController y BP_GameMode_DeveloperTesting son assets de configuración
  necesarios, aunque todavía no figuran en la arquitectura oficial.
- El crouch híbrido y su umbral de 0.25 s fueron implementados después de la
  documentación oficial y requieren prueba de usuario antes de registrarlos como
  decisión definitiva.
- L_Developer_Testing ya existe desde v0.0.1; se reutiliza en vez de crear otro
  mapa solo para satisfacer literalmente el texto del checklist.
- La arquitectura atribuye sensibilidad al componente de cámara, mientras que el
  código la ubica en APMPlayerController, que es quien traduce el input.
- La descripción oficial llama Actor a APMPlayerCharacter; la herencia real y más
  precisa es ACharacter.

## 18. Criterio de finalización de la integración

La integración del Editor puede considerarse preparada cuando:

- Todos los assets esperados existen y compilan.
- No hay warnings propios en Output Log.
- Pawn y Controller correctos se crean y poseen.
- Teclado, ratón y mando están configurados.
- La matriz funcional está ejecutada y documentada.
- Los criterios de cámara, colisión, espacios y rendimiento tienen evidencia.
- Git contiene únicamente cambios esperados.

Esto todavía no autoriza marcar v0.1.0 como completa. La aprobación del
propietario, el registro QA y el permiso para actualizar el checklist oficial
siguen siendo necesarios.

### Sesión de look con ratón completada el 2026-07-28

`PLR-MOV-003` quedó aprobado en PIE normal sobre `/Game/Maps/L_Developer_Testing`, con el visor enfocado y entrada física del propietario. Desde pitch/yaw `0/0`, un movimiento pequeño hacia arriba produjo pitch `-43.2250006°` y yaw `0°`; la lectura MCP permaneció idéntica tras 1.2 s, por lo que no se observó movimiento residual. El log final está en `UnrealProject/Saved/QA/PlayerV0.1/LOOK-20260728/ProyectoMemoria.log` (304299 bytes, SHA-256 `B02C3D092FB4B995FBECF74FC99E21A85C14D031587D7A7C62D6673F12C7A5D4`). Unreal se cerró sin guardar assets. La siguiente tarea es `PLR-MOV-004`, velocidad de avance.
### Sesión de velocidad completada el 2026-07-28

`PLR-MOV-004` confirmó `walkSpeed/maxWalkSpeed=300 cm/s` en PIE. El avance recto sin sprint no produjo deriva lateral y la velocidad quedó en cero al soltar. La siguiente tarea es `PLR-MOV-005`, sprint.
### Sesión de sprint completada el 2026-07-28

`PLR-MOV-005` confirmó el sprint configurado en 550 cm/s y el retorno a 300 cm/s al soltar; `bIsSprinting` y velocity quedaron en falso/cero. La siguiente tarea es `PLR-MOV-006`, movimiento relativo al yaw.
### Sesión de movimiento relativo completada el 2026-07-28

`PLR-MOV-006` confirmó que W sigue el yaw de la cámara (yaw ~92.6°, desplazamiento principalmente en Y). La siguiente tarea es `PLR-CRO-001`, crouch híbrido.
### Sesión de crouch inicial completada el 2026-07-28

`PLR-CRO-001..003` confirmaron toque corto persistente, segundo toque para levantarse y hold básico sin estado residual. La siguiente tarea es `PLR-CRO-004`, hold partiendo de agachado.