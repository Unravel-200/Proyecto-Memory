# QA Player — v0.1.0

## Propósito y estado

Esta matriz registra la evidencia de integración del personaje, movimiento,
salto, agachado y cámaras descritos en `EDITOR_SETUP_V0.1.md`. Debe ejecutarse
desde la sección 1 de esa guía, con refrigeración y monitoreo adecuados para
Unreal Engine 5.8.

Estado actual: **mappings, `BP_PlayerController` y `BP_PlayerCharacter` auditados;
ninguna prueba PIE ejecutada**. Los 12 PASS de `MAP-01..07` y `BP-01..05`
demuestran configuración guardada, no que la integración sea jugable ni que
v0.1.0 esté terminada.

Referencias y línea base:

- `EDITOR_SETUP_V0.1.md`: procedimiento y criterios operativos.
- `HANDOFF_CODEX.md`: alcance, contratos C++ y restricciones de reanudación.
- Rama requerida: `feature/v0.1-player-cameras`.
- Commit mínimo verificado: `336aa91`; se admite un descendiente con worktree
  limpio.
- Estado al actualizar esta plantilla: seis Input Actions e `IMC_Player` existen;
  los 16 mappings están verificados y `BP_PlayerController` y
  `BP_PlayerCharacter` están listos. Faltan el GameMode, el mapa funcional y las
  pruebas PIE.
- Motor y configuración: Unreal Engine 5.8, Win64 Development Editor.

## Alcance y exclusiones

Incluye Enhanced Input, Blueprints de configuración, spawn y posesión,
movimiento, sprint, salto, crouch híbrido, cámaras 1P/3P, colisión, geometría de
prueba, teclado, ratón, mando físico, rendimiento y persistencia de referencias.

No autoriza:

- abrir Unreal sin la base de enfriamiento activa y monitoreo térmico;
- recompilar sin necesidad o ejecutar PIE antes de completar la integración;
- añadir lógica central al Level Blueprint o a los Event Graphs;
- duplicar componentes nativos o reimplementar movimiento/cámaras en Blueprint;
- usar Hot Reload, habilitar plugins extra o convertir el proyecto;
- crear `IA_Interact`, Gameplay Tags o trabajo de v0.2.0;
- importar mallas sin origen, licencia y escala verificados;
- modificar `Proyecto-Memoria-docs` o `Modelos-3D`;
- hacer push, merge, rebase o tag;
- declarar v0.1.0 completa o cambiar marcas `[~]` a `[X]`.

## Protocolo de resultados

Todas las filas comienzan en `NOT RUN`, que significa que todavía no se han
intentado. Al ejecutar una prueba, sustituirlo por un único resultado:

- `PASS`: se ejecutaron todos los pasos, se cumplió el criterio y hay evidencia.
- `FAIL`: se ejecutó y el resultado difiere de lo esperado; registrar reproducción,
  valor observado y bug asociado.
- `BLOCKED`: no pudo completarse por una condición externa o decisión pendiente;
  registrar causa y condición para reintentar.

No marcar `PASS` por inspección parcial, compilación anterior o por el estado
aparente al cerrar el Editor. Una repetición debe conservar la evidencia anterior
y añadir una ejecución al historial.

La evidencia puede ser captura, video, Output Log, salida de consola, medición o
resultado automatizado. Asignar IDs `EV-001`, `EV-002`, etc. y anotar una ruta o
ubicación reproducible, sin secretos ni datos personales.

## Identificación de la ejecución

| Campo | Valor |
|---|---|
| ID de ejecución | |
| Fecha y zona horaria | |
| Probador | |
| PC / CPU / GPU / RAM | |
| Sistema operativo | |
| Unreal Engine | 5.8 |
| Configuración | Win64 Development Editor |
| Rama | `feature/v0.1-player-cameras` |
| Commit probado | |
| Estado Git inicial | |
| Mapa | `/Game/Maps/L_Developer_Testing` |
| Teclado / ratón | |
| Mando, conexión y firmware | |
| Malla licenciada disponible | Sí / No |
| Resolución y ajustes gráficos | |
| Límites probados | 30 / 60 / 120 FPS / otros |
| Tolerancia aprobada para 300/550 cm/s | |
| Ventana y umbral aprobados de rendimiento | |
| Umbral aprobado para salto de yaw | |
| Criterio visual aprobado de clipping 3P | |
| Ubicación de evidencias | |

## Condiciones de detención

Detener, guardar lo que sea seguro, cerrar y registrar `BLOCKED` si el equipo se
sobrecalienta, Unreal solicita conversión, aparecen errores C++/Blueprint no
comprendidos, el Editor intenta escribir fuera de `Proyecto-Memory`, el mapa o los
assets parecen dañados, o hace falta una decisión de diseño no aprobada.

## A. Preflight y dependencias

| ID | Comprobación y criterio de aceptación | Estado | Evidencia / observado |
|---|---|---|---|
| PRE-01 | PC apta, con temperatura, ventiladores y consumo normales. Unreal está cerrado antes de revisar Git. | NOT RUN | |
| PRE-02 | `git status --short --branch` muestra la rama requerida y worktree limpio; `git log -1 --oneline` identifica un descendiente de `5eccd8e`. | NOT RUN | |
| PRE-03 | El proyecto abre con UE 5.8 sin conversión. Si solicita recompilar módulos, se cancela y se hace una compilación completa antes de reabrir. | NOT RUN | |
| PRE-04 | Enhanced Input está habilitado y no se habilitaron plugins adicionales. | NOT RUN | |
| PRE-05 | `Default Player Input Class = EnhancedPlayerInput` y `Default Input Component Class = EnhancedInputComponent`. | NOT RUN | |
| PRE-06 | Output Log está visible; todos los Blueprints compilan y `GameMode Override` está confirmado antes de PIE. | NOT RUN | |
| PRE-07 | Hay teclado y ratón funcionales. Se identifica un mando físico; un mapping sin dispositivo no prueba compatibilidad. | NOT RUN | |
| PRE-08 | Para la frontera de crouch existe instrumentación que registra `GetElapsedTime()`; 0.24/0.25/0.26 s no se estiman manualmente. | NOT RUN | |
| PRE-09 | Para evaluar apariencia 3P, la malla tiene origen, licencia y escala verificados. Sin malla, solo esa evaluación queda `BLOCKED`. | NOT RUN | |

### Clasificación de las filas

- Toda fila es obligatoria para aceptar v0.1.0 salvo que se marque aquí como
  condicional.
- `PRE-09` y `PLR-VIS-001` son condicionales a disponer de una malla válida; su
  bloqueo no invalida input, cápsula ni mecánica de cámaras.
- En `PLR-CRO-AUT-001`, los tres tiempos son obligatorios para cerrar el contrato
  del umbral. Repetirlos a 30 y 120 FPS es condicional a que el equipo lo permita;
  60 FPS forma parte del objetivo de aceptación.
- Mando físico y rendimiento son obligatorios para v0.1.0. Sin equipo adecuado se
  registran `BLOCKED`, y la versión no puede cerrarse aunque el setup del Editor
  sí quede preparado.
- Un `BLOCKED` en una fila obligatoria impide aceptar la versión. Un bloqueo
  condicional debe quedar documentado, pero no convierte otros subsistemas en
  fallidos.

## B. Auditoría de assets y configuración

### Carpetas e Input Actions

| ID | Comprobación y criterio de aceptación | Estado | Evidencia / observado |
|---|---|---|---|
| SET-01 | Existen `/Game/Input/Actions`, `/Game/Input/Mappings`, `/Game/Blueprints/Player` y `/Game/Blueprints/Levels`; no se movieron `BP_TestActor` ni `L_Developer_Testing`. | NOT RUN | |
| SET-02 | `IA_Move` e `IA_Look` son Axis2D; `IA_Sprint`, `IA_Crouch`, `IA_Jump` e `IA_ToggleCamera` son Digital/Bool. Move, Look, Sprint, Jump y Toggle no tienen triggers de asset; Crouch usa ninguno por defecto o la excepción Down documentada en `SET-03`. | NOT RUN | |
| SET-03 | `IA_Crouch` permanece activa toda la pulsación y no usa Hold, Tap, Pressed, Released ni Pulse. Si usa la excepción Down, se registra y se repite Started/Completed/Canceled. | NOT RUN | |

### IMC_Player

| ID | Acción | Mapping y criterio de aceptación | Estado | Evidencia / observado |
|---|---|---|---|---|
| MAP-01 | `IA_Move` | W: Swizzle YXZ → `(0,1)`; S: Negate y luego Swizzle YXZ → `(0,-1)`; A: Negate → `(-1,0)`; D: sin modificador → `(1,0)`. | PASS | EV-IMC-01 |
| MAP-02 | `IA_Move` | Gamepad Left Thumbstick 2D-Axis, sin modificador Dead Zone; `DefaultInput.ini` usa zona muerta 0 por decisión aprobada. | PASS | EV-IMC-01 |
| MAP-03 | `IA_Look` | Mouse XY 2D-Axis y Gamepad Right Thumbstick 2D-Axis, sin Negate inicial. | PASS | EV-IMC-01 |
| MAP-04 | `IA_Sprint` | Left Shift y Gamepad Left Thumbstick Button; sin triggers adicionales. | PASS | EV-IMC-01 |
| MAP-05 | `IA_Crouch` | C, Left Control y Gamepad Face Button Right; sin triggers ni modificadores. | PASS | EV-IMC-01 |
| MAP-06 | `IA_ToggleCamera` | V y Gamepad Face Button Top —Y/triángulo—; sin triggers adicionales. | PASS | EV-IMC-01 |
| MAP-07 | `IA_Jump` | Space Bar y Gamepad Face Button Bottom —A/X—; sin triggers ni modificadores. | PASS | EV-IMC-01 |

`EV-IMC-01` — sesión local del 2026-07-22 sobre `8e0aaba`: capturas del Editor,
lectura MCP de `defaultKeyMappings.mappings` con 16 filas antes de guardar, Output
Log `UnrealProject/Saved/Logs/ProyectoMemoria.log`, AssetCheck del recurso y
SHA-256 `6F602EEA54C72BE64FE327DAC86CA7623509F281268BF33574509BAFA13B6C1A`.

### Blueprints y mapa

| ID | Comprobación y criterio de aceptación | Estado | Evidencia / observado |
|---|---|---|---|
| BP-01 | `BP_PlayerController` hereda de `APMPlayerController`; referencia `IMC_Player` y las seis IA; sensibilidad predeterminada de mouse/mando 1.0, inversión Y false, prioridad 0 y umbral 0.25 s; Event Graph vacío; compila y guarda. | PASS | EV-BPC-01 |
| BP-02 | `BP_PlayerCharacter` hereda de `APMPlayerCharacter`; conserva sin duplicados Capsule, Arrow, Mesh, CharacterMovement, cámaras, boom y CameraModeComponent; Event Graph vacío; compila y guarda. | PASS | EV-BPCHAR-01 |
| BP-03 | Character: Walk 300, Sprint 550 y Crouch 180 cm/s; cápsula radio 42 y semialtura 96 cm; Can Crouch true. Crouched Half Height 60 cm se registra como provisional. | PASS | EV-BPCHAR-01 |
| BP-04 | 1P: ubicación `(-10,0,64)`, Use Pawn Control Rotation true. 3P: arm 300 cm, boom usa control rotation, Probe Size 12 cm, canal Camera y cámara no usa control rotation. | PASS | EV-BPCHAR-01 |
| BP-05 | CameraMode: Initial Mode First Person, FOV 1P/3P 90° y Third Person Arm Length 300 cm. | PASS | EV-BPCHAR-01 |
| BP-06 | `BP_GameMode_DeveloperTesting` hereda de GameModeBase, usa `BP_PlayerCharacter` y `BP_PlayerController`, tiene Event Graph vacío, compila y guarda. | NOT RUN | |
| LVL-01 | `L_Developer_Testing` usa ese GameMode; hay un solo Player Start, fuera del suelo, sin `BADsize`, con espacio para cápsula de 84 × 192 cm; no hay Pawn manual ni lógica en Level Blueprint. | NOT RUN | |

`EV-BPC-01` — sesión local del 2026-07-22 sobre `d569e31`: MCP confirmó el
parent exacto `/Script/ProyectoMemoria.PMPlayerController`, leyó de vuelta las 12
propiedades requeridas —`IMC_Player`, seis IA, sensibilidad X/Y 1.0, inversión Y
false, prioridad 0 y umbral 0.25 s— y confirmó el Event Graph vacío. El Blueprint
compiló dos veces con warnings-as-errors, se guardó por ruta explícita, quedó no
sucio y pasó AssetCheck. Archivo de 22564 bytes; SHA-256
`A9C8D639135632B2FECE4E64922596B1F4146E17E627D2303DD832EC1A5597B1`.

`EV-BPCHAR-01` — sesión local del 2026-07-22 sobre `4efac4c`: MCP confirmó el
parent exacto `/Script/ProyectoMemoria.PMPlayerCharacter`, ocho componentes
heredados sin duplicados y `ThirdPersonCamera` unido a
`ThirdPersonCameraBoom`. Leyó Walk/Sprint/Crouch 300/550/180, cápsula 42/96,
Can Crouch true, rotación 540, las dos cámaras, boom y CameraMode con los valores
de aceptación. El valor 60 cm continúa provisional y no se aplicó ningún
override. El Event Graph se leyó vacío; compiló dos veces con
warnings-as-errors, se guardó solo su ruta, quedó no sucio y pasó AssetCheck.
Archivo de 27020 bytes; SHA-256
`59555B01BB8D82222207D58D57A444227348D31D98EB2FAED6A8868D2BBA6838`.
No se ejecutó PIE ni se recompiló C++.

### Geometría de prueba

| ID | Elemento y criterio de aceptación | Estado | Evidencia / observado |
|---|---|---|---|
| GEO-01 | Suelo 2000 × 2000 × 20 cm, BlockAll y Static. | NOT RUN | |
| GEO-02 | Pasillo interior 1000 × 250 × 300 cm, paredes de 20 cm. | NOT RUN | |
| GEO-03 | Puerta con hueco libre 120 × 240 cm y pared de 20 cm. | NOT RUN | |
| GEO-04 | Habitación interior 300 × 300 × 300 cm y puerta 120 × 240 cm. | NOT RUN | |
| GEO-05 | Túnel crouch 300 × 120 × 140 cm. | NOT RUN | |
| GEO-06 | Escalera de 10 peldaños, cada uno 17 cm alto × 30 cm profundo × 220 cm ancho; altura total 170 cm; piezas apoyadas y colisión verificable. | NOT RUN | |
| GEO-07 | Pared de cámara 500 × 20 × 300 cm; bloquea Camera y Pawn. | NOT RUN | |

## C. Matriz funcional de PIE

Precondiciones comunes: secciones A y B completadas sin fallos bloqueantes,
Selected Viewport, Output Log abierto, viewport con input capturado y comandos de
diagnóstico disponibles: `showdebug character`, `showdebug enhancedinput`,
`show collision`, `stat fps`, `stat unit` y `stat game`.

### Inicio, movimiento y look

| ID | Guía | Caso y procedimiento | Criterio de aceptación | Estado | Evidencia / observado |
|---|---:|---|---|---|---|
| PLR-PIE-001 | 12.1 | Iniciar PIE en el Player Start. | GameMode crea Controller y Character; Controller posee el Character; BeginPlay añade `IMC_Player`; aplica la perspectiva guardada o solo 1P en un perfil limpio. No aparecen los warnings prohibidos de la sección D. | NOT RUN | |
| PLR-MOV-001 | 12.2 | Pulsar W, A, S y D por separado con `showdebug enhancedinput`. | Cada tecla produce el vector y dirección configurados, sin ejes intercambiados ni movimiento residual al soltar. | NOT RUN | |
| PLR-MOV-002 | 12.3 | Probar las cuatro diagonales con dos teclas simultáneas. | Combina ambos ejes en la diagonal esperada, no supera la velocidad configurada y se detiene al soltar. | NOT RUN | |
| PLR-MOV-003 | 12.4 | Mover y detener el ratón horizontal y verticalmente. | Yaw y pitch responden inmediatamente, en el sentido base esperado, sin suavizado ni movimiento después de detener el ratón. | NOT RUN | |
| PLR-MOV-004 | 12.5 | En suelo plano, mantener avance hasta velocidad estable y medir. | Objetivo 300 cm/s. Registrar valor, resolución de medición y tolerancia previamente aprobada; si falta esa tolerancia, no decidir subjetivamente y usar `BLOCKED`. | NOT RUN | |
| PLR-MOV-005 | 12.6 | Mantener sprint, medir; soltar y volver a medir. | Objetivos 550 cm/s durante sprint y 300 cm/s al soltar; no queda sprint latente. Registrar la tolerancia aprobada o usar `BLOCKED`. | NOT RUN | |
| PLR-MOV-006 | Handoff | Rotar la vista 90° y 180°; en cada orientación pulsar avance y laterales. | El movimiento se calcula respecto del yaw de la vista, no respecto de ejes fijos del mundo, y conserva las direcciones relativas correctas. | NOT RUN | |

### Crouch híbrido

Para pruebas manuales usar un toque claramente corto y un hold de al menos 0.5 s.
La frontera exacta se cubre únicamente mediante instrumentación en
`PLR-CRO-AUT-001`.

| ID | Guía | Caso y procedimiento | Criterio de aceptación | Estado | Evidencia / observado |
|---|---:|---|---|---|---|
| PLR-CRO-001 | 12.7 | Desde pie, dar un toque corto a crouch. | Se agacha al iniciar la pulsación y permanece agachado al soltar. | NOT RUN | |
| PLR-CRO-002 | 12.8 | Estando agachado por el caso anterior, dar otro toque corto. | Permanece agachado durante la pulsación y queda de pie al soltar, si hay espacio. | NOT RUN | |
| PLR-CRO-003 | 12.9 | Desde pie, mantener crouch ≥0.5 s y soltar. | Se agacha inmediatamente, permanece así mientras se mantiene y queda de pie al soltar. | NOT RUN | |
| PLR-CRO-004 | 12.10 | Desde agachado, mantener crouch ≥0.5 s y soltar. | Permanece agachado durante la pulsación y queda de pie al soltar, si hay espacio. | NOT RUN | |
| PLR-CRO-005 | 12.11 | Desde pie, provocar `Canceled` mediante un caso reproducible sin cambiar los triggers para forzarlo. | Restaura la postura inicial de pie. Si no puede emitirse determinísticamente, `BLOCKED` y prueba automatizada. | NOT RUN | |
| PLR-CRO-006 | 12.11 | Desde agachado, repetir el caso reproducible de `Canceled`. | Restaura la postura inicial agachada. No inferir el resultado al detener PIE. | NOT RUN | |
| PLR-CRO-007 | 12.12 | Iniciar sprint y activar crouch sin soltar primero el movimiento. | Crouch cancela sprint, usa 180 cm/s agachado y no deja sprint latente. | NOT RUN | |
| PLR-CRO-008 | 12.13 | Entrar agachado al túnel, intentar levantarse bajo el techo y salir. | Entra agachado; UnCrouch conserva la postura bajo techo; puede levantarse al recuperar espacio. | NOT RUN | |
| PLR-CRO-AUT-001 | Sec. 12 | Inyectar o medir 0.24, 0.25 y 0.26 s; repetir a 30, 60 y 120 FPS cuando el equipo lo permita. | 0.24 s sigue el contrato de toque; 0.25 y 0.26 s siguen el contrato de hold. Cada valor tiene tiempo medido y resultado por FPS. | NOT RUN | |
| PLR-CRO-009 | Handoff | Estando ya agachado, intentar iniciar sprint y avanzar sin cambiar de postura. | Sprint no se activa; el Character sigue agachado y conserva la velocidad de crouch. | NOT RUN | |

### Salto

| ID | Guía | Caso y procedimiento | Criterio de aceptación | Estado | Evidencia / observado |
|---|---:|---|---|---|---|
| PLR-JMP-001 | 12.23 | Desde pie y con espacio, saltar con Espacio y después con A/X; soltar el control durante el salto. | Ambos controles inician el salto y al soltarlos termina la orden mediante `StopJumping`; no queda salto latente. | NOT RUN | |
| PLR-JMP-002 | 12.24 | Desde crouch y con espacio libre encima, presionar salto. | Se levanta y salta como una sola intención; no permanece agachado ni requiere una segunda pulsación. | NOT RUN | |
| PLR-JMP-003 | 12.25 | Desde crouch bajo el túnel, presionar salto; después salir sin volver a pulsarlo. | No atraviesa el techo, no salta bajo el obstáculo y tampoco ejecuta un salto pendiente al recuperar espacio. | NOT RUN | |

### Cámaras

| ID | Guía | Caso y procedimiento | Criterio de aceptación | Estado | Evidencia / observado |
|---|---:|---|---|---|---|
| PLR-CAM-001 | 12.14 | Desde 1P, activar Toggle Camera y luego avanzar/girar. | Queda activa solo 3P, FOV 90°, arm 300 cm, colisión del boom activa y Character orientado hacia movimiento. | NOT RUN | |
| PLR-CAM-002 | 12.15 | Con una orientación reconocible, volver de 3P a 1P. | Queda activa solo 1P y usa yaw del Controller, sin salto brusco visible. Guardar video; si es ambiguo por falta de umbral, `BLOCKED` hasta definirlo. | NOT RUN | |
| PLR-CAM-003 | 12.16 | Alternar varias veces quieto, caminando, corriendo y agachado. | Cada pulsación produce un cambio; los estados siguen coherentes; nunca hay dos cámaras activas ni ninguna activa. | NOT RUN | |
| PLR-CAM-004 | 12.17 | En 3P, acercarse y girar junto a la pared de cámara. | El boom retrae la cámara sin atravesar la pared y recupera su longitud al alejarse. | NOT RUN | |
| PLR-CAM-007 | 12.26 | Cambiar de perspectiva y reemplazar el Pawn con un arnés controlado de respawn, documentado y sin lógica central en Level Blueprint; no volver a pulsar Toggle Camera. | El nuevo Character usa la misma perspectiva del anterior, equivalente a conservar la vista al morir y reaparecer. | NOT RUN | |
| PLR-VIS-001 | Alcance 3P | Evaluar encuadre y apariencia del Character en 3P. | La malla tiene licencia/escala registradas y cumple el criterio visual de clipping anotado para la ejecución. Sin malla o criterio aprobado, solo esta fila queda `BLOCKED`. | NOT RUN | |

### Espacios y colisión

| ID | Guía | Caso y procedimiento | Criterio de aceptación | Estado | Evidencia / observado |
|---|---:|---|---|---|---|
| PLR-ENV-001 | 12.18 | Recorrer el pasillo de 250 cm, rozar ambas paredes y girar. | Avanza y gira sin atascarse ni atravesar colisión. | NOT RUN | |
| PLR-ENV-002 | 12.18 | Atravesar la puerta de 120 × 240 cm en ambos sentidos. | La cápsula atraviesa el hueco sin atascarse ni atravesar paredes. | NOT RUN | |
| PLR-ENV-003 | 12.18 | Entrar, maniobrar y salir de la habitación 300 × 300 cm. | Movimiento y cámaras siguen utilizables; no hay atascos ni clipping del Pawn. | NOT RUN | |
| PLR-ENV-004 | 12.18 | Subir y bajar los 10 escalones, recto y cerca de los bordes. | Recorre la escalera sin atravesarla, atascarse o caer entre piezas; registrar cualquier ajuste necesario. | NOT RUN | |

### Mando, preferencias, rendimiento y persistencia

| ID | Guía | Caso y procedimiento | Criterio de aceptación | Estado | Evidencia / observado |
|---|---:|---|---|---|---|
| PLR-PAD-001 | 12.19 | Con mando físico identificado, probar movimiento/look, L3 sprint, B/círculo crouch, A/X salto y Y/triángulo cámara. | Todas las acciones responden; los sticks alcanzan rango útil y vuelven al centro. Registrar modelo, conexión y FPS. | NOT RUN | |
| PLR-PAD-002 | 12.19 | Dejar sticks en reposo, observar input/Pawn/cámara y recorrer el rango completo. | Se confirma zona muerta configurada en 0 y se registra todo drift real, dispositivo y efecto observado; no se oculta con otra capa sin nueva autorización. | NOT RUN | |
| PLR-CAM-005 | 12.20 | Cambiar sensibilidad X/Y desde defaults y comparar con 1.0 usando mouse y mando. | El ajuste compartido actual cambia ambos dispositivos de forma proporcional y no acepta valores negativos. La separación por dispositivo pertenece al menú posterior. | NOT RUN | |
| PLR-CAM-006 | 12.20 | Alternar Invert Look Y y repetir el movimiento vertical. | Solo Y invierte su sentido; X no cambia. | NOT RUN | |
| PLR-PERF-001 | 12.21 | Recorrer toda la geometría usando movimiento, crouch y cámaras con `stat fps`, `stat unit` y `stat game`. | Se documentan hardware, resolución, ajustes, ruta, duración y Game/Draw/GPU. Se evalúa el objetivo de 60 FPS con la ventana/umbral aprobados; sin criterio o hardware representativo, `BLOCKED`. | NOT RUN | |
| PLR-REG-003 | 12.22 | Detener PIE, compilar Blueprints, Save All, cerrar y reabrir UE 5.8. | Persisten IA/IMC, clases, defaults, GameMode y mapa; los Blueprints compilan y se aplica la vista guardada o 1P en un perfil limpio. | NOT RUN | |
| PLR-REG-005 | 12.27 / checklist oficial | Cambiar a 3P, cerrar completamente el juego y volver a iniciarlo con el mismo perfil; repetir sin preferencia guardada. | Restaura 3P con el perfil existente; una primera ejecución sin preferencia guardada inicia en 1P. | NOT RUN | |

### Ciclo de vida y regresión controlada

| ID | Fuente | Caso y procedimiento | Criterio de aceptación | Estado | Evidencia / observado |
|---|---|---|---|---|---|
| PLR-REG-001 | Handoff / sec. 12 | Detener PIE con sprint, salto o gesto de crouch activo, usando instrumentación que permita verificar `EndPlay`. | Limpia sprint, `bPressedJump` y gesto transitorio; retirar `IMC_Player` no deja órdenes. No aprobar solo porque el actor desapareció. | NOT RUN | |
| PLR-REG-002 | Handoff / sec. 12 | Provocar `OnUnPossess` durante sprint, salto y, por separado, durante un gesto de crouch activo, sin lógica central en Level Blueprint. | El Pawn anterior no conserva sprint ni salto; el gesto de crouch se cancela y restaura su postura inicial. Si no es observable, `BLOCKED` y automatizar. | NOT RUN | |
| PLR-REG-004 | Handoff | Repetir spawn, movimiento, salto, crouch y cámaras después de reiniciar PIE. | No hay input/Mapping Context duplicado, estado transitorio heredado ni regresión respecto de los casos aprobados. | NOT RUN | |

## D. Logs y evidencia obligatoria

En la primera ejecución y antes del cierre, buscar y registrar la ausencia o
presencia de warnings propios. No deben aparecer:

~~~text
has no IMC_Player assigned
has one or more unassigned IA_* assets
has an incomplete camera setup
APMPlayerController requires EnhancedInputComponent
PMGameUserSettings is not active
Could not persist the preferred camera mode
~~~

| ID | Evidencia mínima | Estado | Referencia |
|---|---|---|---|
| EVC-01 | Salida inicial de `git status --short --branch` y `git log -1 --oneline`. | NOT RUN | |
| EVC-02 | UE 5.8, plugin Enhanced Input y clases Input configuradas. | NOT RUN | |
| EVC-03 | Content Drawer, tipos de las seis IA y mappings completos de `IMC_Player`. | NOT RUN | |
| EVC-04 | Parent classes, jerarquía, defaults, Event Graphs vacíos y compilación de los tres Blueprints. | NOT RUN | |
| EVC-05 | World Settings, Player Start, dimensiones y colisiones de geometría. | NOT RUN | |
| EVC-06 | Output Log al iniciar y durante PIE; búsqueda de los seis mensajes prohibidos. | NOT RUN | |
| EVC-07 | Videos/mediciones de movimiento, salto, crouch, cámaras, espacios y ciclo de vida. | NOT RUN | |
| EVC-08 | Mando identificado, valores analógicos, drift observado y zona muerta 0 confirmada. | NOT RUN | |
| EVC-09 | Tiempos instrumentados 0.24/0.25/0.26 s y FPS de cada repetición. | NOT RUN | |
| EVC-10 | `stat fps`, `stat unit` y `stat game`, con ruta y condiciones de rendimiento. | NOT RUN | |
| EVC-11 | Estado final de Git después de Save All y cerrar Unreal. | NOT RUN | |

### Evidencia heredada no funcional

`HANDOFF_CODEX.md` registra compilaciones C++ exitosas, revisión estática, una
matriz estática de crouch y `CompileAllBlueprints` sin errores sobre el contenido
que existía entonces. Esta evidencia puede citarse como contexto, pero no cambia
a `PASS` ninguna fila de configuración, PIE, mando, geometría o rendimiento de
este documento.

## E. Trazabilidad de aceptación v0.1.0

| Criterio | Casos que aportan evidencia | Resultado |
|---|---|---|
| Cambio estable 1P/3P | `PLR-CAM-001..003`, `PLR-CAM-007`, `PLR-REG-004` | NOT RUN |
| La cámara no atraviesa paredes | `PLR-CAM-004` | NOT RUN |
| El personaje no queda atascado | `PLR-CRO-008`, `PLR-ENV-001..004` | NOT RUN |
| Escaleras transitables | `PLR-ENV-004` | NOT RUN |
| Movimiento estable al objetivo de 60 FPS | `PLR-MOV-001..006`, `PLR-PERF-001` | NOT RUN |
| Salto normal y desde crouch | `MAP-07`, `BP-01`, `PLR-JMP-001..003` | NOT RUN |
| Inputs configurables en assets/defaults | `SET-02..03`, `MAP-01..07`, `BP-01`, `PLR-CAM-005..006`, `PLR-PAD-001..002` | NOT RUN |
| Lógica central permanece en C++ | Auditoría heredada, `BP-01..02`, `LVL-01` | NOT RUN |
| Valores de diseño ajustables en Blueprint | `BP-01`, `BP-03..05`, `PLR-CAM-005..006` | NOT RUN |
| Sin lógica principal en Level Blueprint | `LVL-01` | NOT RUN |
| Guardar la perspectiva elegida | `PLR-CAM-007`, `PLR-REG-005` | NOT RUN — implementación sin verificar |

“Inputs configurables” cubre assets y defaults del Editor. La reasignación de
controles en tiempo de ejecución todavía no existe y no debe afirmarse como
implementada.

## F. Cierre y aceptación de la integración

Después de probar:

1. Detener PIE y resolver o registrar cada error.
2. Compilar cada Blueprint, ejecutar Save All y cerrar Unreal Editor.
3. Revisar Git sin usar `git add .`.
4. Confirmar que solo existen cambios esperados bajo estas rutas:

~~~text
UnrealProject/Content/Input/Actions/*.uasset
UnrealProject/Content/Input/Mappings/IMC_Player.uasset
UnrealProject/Content/Blueprints/Player/BP_PlayerCharacter.uasset
UnrealProject/Content/Blueprints/Player/BP_PlayerController.uasset
UnrealProject/Content/Blueprints/Levels/BP_GameMode_DeveloperTesting.uasset
UnrealProject/Content/Maps/L_Developer_Testing.umap
QA_PLAYER_V0.1.md
~~~

Guardar capturas, videos y mediciones fuera del árbol versionado o bajo una ruta
ignorada como `UnrealProject/Saved/QA/PlayerV0.1/<RunID>/`, y referenciarlos desde
esta matriz. Si se decide versionar evidencias, sus rutas deben autorizarse y
añadirse explícitamente a la lista anterior antes de preparar cambios.

La integración puede considerarse preparada solo cuando:

- todos los assets esperados existen y compilan;
- no hay warnings propios en Output Log;
- Pawn y Controller correctos se crean y poseen;
- teclado, ratón y mando físico están configurados y probados;
- no queda ninguna prueba obligatoria en `NOT RUN`; las condicionales siguen las
  excepciones declaradas en la sección A;
- todo `FAIL` está resuelto y todo `BLOCKED` que afecte aceptación está levantado;
- cámaras, colisión, espacios y rendimiento tienen evidencia;
- Git contiene únicamente cambios esperados.

Aunque todo resulte `PASS`, todavía se requiere aprobación del propietario,
registro QA y autorización expresa antes de actualizar el checklist oficial,
fusionar la rama o crear `v0.1.0_player`.

En particular, `PLR-REG-005` representa un requisito oficial cuyo C++ está
compilado, pero todavía no verificado en PIE. Mientras no esté en `PASS`, la
configuración del Editor puede documentarse, pero v0.1.0 no puede aceptarse como
versión completa.

## G. Incidencias, bloqueos y decisiones pendientes

| ID | Tipo | Prueba | Descripción / reproducción | Evidencia | Siguiente acción | Estado |
|---|---|---|---|---|---|---|
| | FAIL / BLOCKED / decisión | | | | | Abierto / resuelto |

Registrar aquí, sin resolver por suposición:

- malla y Animation Blueprint definitivos;
- valores finales de Crouched Half Height y Crouch Hold Threshold;
- convención oficial para Controller y GameMode;
- criterio cuantitativo final de rendimiento;
- tolerancia aprobada para velocidades y umbral medible de salto de yaw;
- implementación posterior del menú de controles y Gameplay Tags.

`IA_Interact` y el sistema de interacción pertenecen a v0.2.0 y no son un bloqueo
de esta matriz.

## Historial de ejecuciones

| ID | Fecha | Commit | PC / dispositivo | PASS / FAIL / BLOCKED | Evidencias | Aprobación |
|---|---|---|---|---|---|---|
| SETUP-IMC-20260722 | 2026-07-22 | `8e0aaba` + cambio local IMC | Lenovo 83DS, teclado/ratón; mando no probado | 7 PASS / 0 FAIL / 0 BLOCKED; PIE NOT RUN | EV-IMC-01 | Pendiente |
| | | | | | | |
