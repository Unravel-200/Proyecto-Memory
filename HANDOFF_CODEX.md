# HANDOFF CODEX — Proyecto Memoria

## Identificación de esta entrega

- Versión de trabajo: v0.1.0 — personaje, movimiento y cámaras.
- Fecha local: 2026-07-16 (America/Costa_Rica).
- Última actualización: 2026-07-16 — decisiones del Player, salto y persistencia preparados.
- Rama: feature/v0.1-player-cameras.
- Motor verificado: Unreal Engine 5.8.
- Plataforma de la base compilada: Windows 64-bit, Development Editor.
- Trabajo técnico generado por: Codex, bajo dirección y revisión del propietario del proyecto.
- Estado: base C++ anterior compilada y carga headless verificada; delta de salto,
  cámara inmediata y persistencia revisado estáticamente pero todavía no
  compilado; integración jugable en Unreal Editor pendiente.
- Publicación remota: ninguna. No se hizo push, merge ni tag.

Este documento registra lo realizado por Codex para facilitar revisión, continuidad,
auditoría y una futura preparación de publicación. No sustituye la documentación
oficial de Proyecto-Memoria-docs y no establece por sí mismo licencia, titularidad
legal ni obligaciones de atribución.

## Reanudación rápida — próxima sesión

### Punto de control

- Repositorio de código: Proyecto-Memory.
- Rama obligatoria: feature/v0.1-player-cameras.
- Commits relevantes de v0.1.0:
  - f8dfb21 — personaje, movimiento y cámaras.
  - e8095b4 — agachado híbrido.
  - 5eccd8e — limpieza de sprint/crouch al perder posesión.
  - 947681f — guía reproducible de integración en Unreal Editor.
  - d82ea86 — punto de reanudación y restricciones de la laptop.
  - efc931c — matriz de evidencia QA del Player.
  - 9132738 — verificador QA de solo lectura para preflight y postflight.
  - 73de57b — endurecimiento de Git/LFS, assets, matriz QA y Output Log.
  - 20e8fd2 — salto seguro, cámara inmediata y persistencia de perspectiva.
  - 59ed2cf — decisiones aprobadas, guía de 27 pasos y matriz de 84 pruebas.
  - e2fbad7 — verificador sincronizado con IA_Jump y las configuraciones aprobadas.
- Checklist oficial actualizado en Proyecto-Memoria-docs, commit 6a270af.
- No existe push, merge, rebase ni tag de esta rama.
- Modelos-3D contiene dos archivos sin seguimiento del propietario que deben
  preservarse: Plaza/SM_Tree_PlazaCentral_A.blend y
  Plaza/SM_Tree_PlazaCentral_A.py.

### Próxima acción recomendada

En la laptop actual no abrir Unreal, compilar, ejecutar PIE ni generar shaders.
`PLAYER_SETTINGS_V0.1.md`, `QA_PLAYER_V0.1.md` y
`Tools/QA/Invoke-PlayerQACheck.ps1` ya están preparados; no volver a crearlos. Las
decisiones de perspectiva, Jump, respuesta inmediata, teclado/mouse, mando y menú
posterior están cerradas. Siguen abiertos los valores finales de crouch y las
tolerancias cuantitativas.

Cuando exista acceso a una PC adecuada, ejecutar primero el preflight con
confirmación humana del hardware. Solo si no hay FAIL, hacer una compilación
completa Development Editor del delta `20e8fd2`, sin Hot Reload. Si compila,
repetir el preflight, continuar con `EDITOR_SETUP_V0.1.md` desde la sección 1 y
registrar cada prueba como PASS, FAIL o BLOCKED. Al cerrar Unreal, ejecutar el
postflight con la ruta al Output Log.

~~~powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  .\Tools\QA\Invoke-PlayerQACheck.ps1 -Phase Preflight -ConfirmHardwareReady

powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  .\Tools\QA\Invoke-PlayerQACheck.ps1 -Phase Postflight `
  -LogPath .\UnrealProject\Saved\Logs\ProyectoMemoria.log
~~~

No usar `-AllowDirty` para una sesión real; existe únicamente para desarrollar el
script. `-AsJson` permite capturar la salida mediante redirección sin que el script
escriba archivos por sí mismo.

No comenzar v0.2.0, fusionar la rama ni crear v0.1.0_player hasta completar los
Blueprints, Input Assets, PIE, geometría, mando, rendimiento y regresión.

### Prompt para copiar mañana

> Continúa Proyecto Memoria. Trabaja únicamente en Proyecto-Memory y lee primero
> HANDOFF_CODEX.md, PLAYER_SETTINGS_V0.1.md y EDITOR_SETUP_V0.1.md completos.
> Verifica en solo lectura que
> la rama sea feature/v0.1-player-cameras, muestra los últimos commits y confirma
> que el worktree esté limpio. No abras Unreal, no compiles y no ejecutes PIE en
> esta laptop. No hagas push, merge, rebase ni tag. No toques Modelos-3D y preserva
> sus archivos sin seguimiento. Mantén Proyecto-Memoria-docs en solo lectura hasta
> que yo autorice otra actualización. QA_PLAYER_V0.1.md y el verificador QA ya
> existen desde los commits efc931c y 9132738; el verificador vigente incluye
> 73de57b y e2fbad7. No los recrees. El delta 20e8fd2 no se ha compilado. En una
> PC adecuada, ejecuta el preflight, compila completamente y después sigue
> EDITOR_SETUP_V0.1.md desde la sección 1.

## Alcance autorizado y respetado

La implementación C++ y sus documentos se realizaron únicamente en
Proyecto-Memory. El 2026-07-13 el propietario autorizó expresamente actualizar el
checklist compartido; se modificó solo
Produccion/Checklist_Versiones_CPP_Blueprints_Actualizado.txt en
Proyecto-Memoria-docs y se creó el commit local 6a270af. Modelos-3D no se modificó.

El trabajo siguió este orden solicitado:

1. APMPlayerCharacter.
2. APMPlayerController.
3. UPMCameraModeComponent.
4. Movimiento.
5. Primera persona.
6. Tercera persona.
7. Cambio de cámara.

## Archivos creados por Codex

- UnrealProject/Source/ProyectoMemoria/Player/PMPlayerCharacter.h
- UnrealProject/Source/ProyectoMemoria/Player/PMPlayerCharacter.cpp
- UnrealProject/Source/ProyectoMemoria/Player/PMPlayerController.h
- UnrealProject/Source/ProyectoMemoria/Player/PMPlayerController.cpp
- UnrealProject/Source/ProyectoMemoria/Player/PMCameraModeComponent.h
- UnrealProject/Source/ProyectoMemoria/Player/PMCameraModeComponent.cpp
- UnrealProject/Source/ProyectoMemoria/Player/PMGameUserSettings.h
- UnrealProject/Source/ProyectoMemoria/Player/PMGameUserSettings.cpp
- EDITOR_SETUP_V0.1.md
- HANDOFF_CODEX.md
- PLAYER_SETTINGS_V0.1.md
- QA_PLAYER_V0.1.md
- Tools/QA/Invoke-PlayerQACheck.ps1

## Archivo existente modificado por Codex

- UnrealProject/Source/ProyectoMemoria/ProyectoMemoria.Build.cs
  - Se agregó EnhancedInput como dependencia pública del módulo.
- UnrealProject/Config/DefaultEngine.ini
  - Se configuró `PMGameUserSettings` como clase persistente de ajustes.
- UnrealProject/Config/DefaultInput.ini
  - Se desactivó mouse smoothing y se fijó zona muerta 0 para los sticks.

Durante el trabajo local del 2026-07-15 y 2026-07-16 no se crearon ni editaron
assets binarios, Blueprints, mapas, Level Blueprints ni contenido de los
repositorios excluidos. La única excepción histórica es la actualización
autorizada `6a270af` del 2026-07-13 ya descrita arriba.

### Guía operativa del Editor

EDITOR_SETUP_V0.1.md conserva el procedimiento reproducible para crear Input
Actions, IMC_Player, Blueprints, GameMode, geometría de prueba y ejecutar PIE
cuando exista acceso a una PC adecuada. Su creación no abrió Unreal Editor ni
confirma que la integración jugable haya sido realizada.

### Matriz y verificador QA

`QA_PLAYER_V0.1.md` conserva el entorno de ejecución, precondiciones, configuración
de assets, geometría, las 27 pruebas de la guía desglosadas, regresión, evidencias,
incidencias y trazabilidad de aceptación. Sus 84 IDs comienzan en NOT RUN; ninguna
prueba de Editor o PIE fue aprobada al preparar la plantilla.

`Tools/QA/Invoke-PlayerQACheck.ps1` es un script PowerShell 5.1 de solo lectura:

- Preflight valida rama, commit mínimo, worktree, instalación UE 5.8, hidratación
  de los assets LFS base, Enhanced Input, respuesta directa, preferencias
  persistentes, fuentes y ausencia de procesos Unreal.
- Postflight rechaza conflictos, renombres, copias, eliminaciones, assets ignorados
  y rutas fuera de la allowlist; comprueba 84 IDs/estados/evidencias QA y exige un
  Output Log reconocible de ProyectoMemoria.
- Devuelve exit 1 ante FAIL y puede emitir JSON con `-AsJson`.
- No abre Unreal, no compila, no cambia Git y no crea evidencias.

El operador debe pasar el Output Log de la sesión recién cerrada. El verificador
registra tamaño y fecha y valida marcadores del proyecto, pero no puede demostrar
por sí solo que un log válido corresponda a esa ejecución concreta.

## Arquitectura implementada

Flujo de responsabilidades:

APMPlayerController
  -> traduce Enhanced Input a órdenes
APMPlayerCharacter
  -> posee movimiento, cápsula y componentes de cámara
UPMCameraModeComponent
  -> aplica el estado de perspectiva 1P/3P
UPMGameUserSettings
  -> conserva la perspectiva entre ejecuciones

Las cámaras son propiedad del Character. El componente de cámara no recibe input
directamente y el Controller no contiene reglas internas de activación de cámaras.
Esta separación permite sustituir presentación en Blueprint sin mover la lógica
central fuera de C++.

### APMPlayerCharacter

Hereda de ACharacter. No usa Tick.

Responsabilidades implementadas:

- Cápsula provisional de radio 42 cm y semialtura 96 cm.
- Velocidad de caminar: 300 cm/s.
- Velocidad de correr: 550 cm/s.
- Velocidad agachado: 180 cm/s.
- Soporte de crouch habilitado en las propiedades públicas del agente de navegación.
- Sincronización del sprint al agacharse, incluso si Crouch se invoca desde un
  Blueprint o un sistema futuro.
- Orden explícita SetCrouching(bool) para separar la postura física de cómo se
  interpreta una pulsación en el Controller.
- Cámara de primera persona unida a la cápsula.
- Spring Arm y cámara de tercera persona.
- Camera lag desactivado en el Spring Arm para respuesta inmediata.
- Mouse smoothing desactivado por `DefaultInput.ini`.
- Propiedad del UPMCameraModeComponent.
- Salto normal y salto desde crouch con comprobación inmediata de espacio; bajo
  techo no se establece `bPressedJump`.

API pública:

| Método | Entrada | Retorno | Contrato |
|---|---|---|---|
| SetSprinting | bool bEnabled | void | Activa sprint solo si el personaje no está agachado. |
| SetCrouching | bool bEnabled | void | Solicita Crouch o UnCrouch y cancela sprint al agacharse. |
| ToggleCrouch | ninguna | void | Alterna Crouch/UnCrouch y cancela sprint al agacharse. |
| TryJumpFromCurrentPosture | ninguna | bool | Se levanta y salta si cabe; false sin salto latente si el techo bloquea. |
| IsSprinting | ninguna | bool | Devuelve el estado lógico de sprint. |
| GetCameraModeComponent | ninguna | UPMCameraModeComponent* | Devuelve el componente propiedad del Character. |
| GetFirstPersonCamera | ninguna | UCameraComponent* | Devuelve la cámara 1P. |
| GetThirdPersonCamera | ninguna | UCameraComponent* | Devuelve la cámara 3P. |

### APMPlayerController

Hereda de APlayerController y usa Enhanced Input.

Responsabilidades implementadas:

- Añadir IMC_Player al subsistema del LocalPlayer al comenzar.
- Retirar ese contexto al terminar la vida del Controller.
- Movimiento relativo al yaw de la vista.
- Look horizontal y vertical.
- Sensibilidad X/Y editable.
- Inversión opcional del eje Y.
- Sprint al mantener una acción; se cancela en Completed y Canceled.
- Sprint, salto y gesto de crouch se limpian también en EndPlay y OnUnPossess para
  que el Pawn anterior no conserve órdenes si se pierde la posesión.
- Agachado híbrido con una acción Digital: toque corto alterna; mantener presionado
  agacha inmediatamente y levanta al soltar.
- Umbral de mantener presionado editable, 0,25 s por defecto.
- Restauración de la postura inicial si Enhanced Input cancela IA_Crouch.
- Recuperación ante un Started duplicado y limpieza al terminar o cambiar el Pawn.
- Salto mediante una acción Digital; Completed/Canceled ejecutan StopJumping.
- Cambio de cámara mediante una acción Digital y guardado inmediato de la
  preferencia.
- Aplicación de la perspectiva guardada cada vez que SetPawn recibe un Character
  nuevo, de modo que un respawn conserve la vista.
- Diagnóstico en log cuando faltan el Mapping Context o Input Actions.
- Comportamiento seguro si todavía no hay assets asignados.

Contrato de assets:

| Propiedad C++ | Asset esperado | Value Type |
|---|---|---|
| PlayerMappingContext | IMC_Player | Input Mapping Context |
| MoveAction | IA_Move | Axis2D |
| LookAction | IA_Look | Axis2D |
| SprintAction | IA_Sprint | Digital |
| CrouchAction | IA_Crouch | Digital, trigger predeterminado o Down |
| JumpAction | IA_Jump | Digital |
| ToggleCameraAction | IA_ToggleCamera | Digital |

API pública:

| Método | Entrada | Retorno | Contrato |
|---|---|---|---|
| GetPMPlayerCharacter | ninguna | APMPlayerCharacter* | Devuelve el Pawn si es del tipo esperado; en otro caso nullptr. |
| SetLookSensitivity | float horizontal, float vertical | void | Guarda valores no negativos. |
| SetInvertLookY | bool bShouldInvert | void | Activa o desactiva la inversión vertical. |

### UPMCameraModeComponent

Hereda de UActorComponent. No usa Tick y se crea de forma nativa dentro de
APMPlayerCharacter; no se ofrece como componente agregable manualmente desde
Blueprint porque sus tres referencias deben configurarse durante construcción.

EPMCameraMode es un enum uint8 expuesto a Blueprint:

- FirstPerson.
- ThirdPerson.

Responsabilidades implementadas:

- Validar que el owner sea ACharacter y que cámaras/boom pertenezcan al mismo actor.
- Activar una sola cámara.
- Aplicar FOV independiente por perspectiva.
- Aplicar longitud del Spring Arm.
- Ejecutar prueba de colisión del Spring Arm solo en tercera persona.
- En 1P, rotar el Character con el Controller.
- En 3P, orientar el Character hacia el movimiento.
- Respetar un modo restaurado antes de BeginPlay, sin reemplazarlo por InitialMode.
- Emitir OnCameraModeChanged cuando el modo realmente cambia.

API pública:

| Método | Entrada | Retorno | Contrato |
|---|---|---|---|
| ConfigureCameras | dos UCameraComponent* y un USpringArmComponent* | void | Se llama durante construcción con componentes del mismo Character. |
| SetCameraMode | EPMCameraMode | bool | true si el modo era válido y pudo aplicarse. |
| ToggleCameraMode | ninguna | EPMCameraMode | Devuelve el modo resultante; conserva el actual si falla la configuración. |
| GetCameraMode | ninguna | EPMCameraMode | Devuelve el estado actual. |
| IsFirstPerson | ninguna | bool | Indica si el modo actual es FirstPerson. |
| GetActiveCamera | ninguna | UCameraComponent* | Devuelve la cámara activa o nullptr si el setup es inválido. |
| HasValidCameraSetup | ninguna | bool | Valida owner, referencias y propiedad de componentes. |

### UPMGameUserSettings

Hereda de UGameUserSettings y usa la infraestructura `GameUserSettings.ini` de
UE 5.8. Primera ejecución usa FirstPerson; cada cambio válido se guarda y la
preferencia se vuelve a aplicar al iniciar o reemplazar el Pawn. Esta preferencia
es local a la instalación y al alcance single-player actual.

El menú posterior podrá reutilizar esta clase, pero la reasignación de teclas,
slots principal/secundario y sensibilidad separada todavía no están implementados.

Valores editables desde defaults de Blueprint:

| Valor | Tipo | Predeterminado |
|---|---|---|
| WalkSpeed | float, cm/s | 300 |
| SprintSpeed | float, cm/s | 550 |
| CrouchSpeed | float, cm/s | 180 |
| CrouchHoldThreshold | float, segundos | 0.25 |
| LookSensitivityX | float | 1.0 |
| LookSensitivityY | float | 1.0 |
| bInvertLookY | bool | false |
| MappingPriority | int32 | 0 |
| InitialMode | EPMCameraMode | FirstPerson |
| FirstPersonFieldOfView | float, grados | 90 |
| ThirdPersonFieldOfView | float, grados | 90 |
| ThirdPersonArmLength | float, cm | 300 |

## Historial de compilación y correcciones

1. Primera compilación: UHT pasó, pero los tres .cpp no resolvieron includes con
   el prefijo Player/ en la estructura actual del módulo. Se cambiaron por includes
   locales autocontenidos.
2. Segunda compilación: Character y CameraMode compilaron. El compilador estricto
   detectó variables locales que ocultaban miembros heredados de AController.
   Se renombraron a PMCharacter y ControllerRotation.
3. Tercera compilación: resultado exitoso.
4. Revisión independiente: se añadió Engine/LocalPlayer.h explícito, limpieza del
   Mapping Context, validaciones de cámara, diagnósticos y sincronización
   sprint/crouch.
5. Compilación final incremental, limitada a una acción paralela: exitosa.
6. Agachado híbrido añadido el 2026-07-13; UHT, PMPlayerCharacter,
   PMPlayerController y enlace recompilados con resultado exitoso.
7. Auditoría de memoria/ciclo de vida: no requiere destructores personalizados;
   se añadió limpieza de sprint al terminar o perder la posesión.
8. El 2026-07-16 se prepararon salto, `UPMGameUserSettings`, restauración en
   `SetPawn` y respuesta inmediata. Sus firmas y flujo se revisaron contra el
   source local de UE 5.8, pero no se ejecutó UHT, compilación ni enlace.

Comando final:

    Build.bat ProyectoMemoriaEditor Win64 Development
      -Project=<ruta>/ProyectoMemoria.uproject
      -WaitMutex -NoHotReloadFromIDE -MaxParallelActions=1

Resultado de la base anterior: Succeeded. UHT, compilación y enlace de
UnrealEditor-ProyectoMemoria.dll completados antes del delta `20e8fd2`.

El estado “Succeeded” no cubre `20e8fd2`. Ese commit debe recibir una compilación
Development Editor completa en una PC adecuada antes de abrir el Editor.

Avisos externos observados:

- Visual Studio MSVC 14.51 es más nuevo que la versión preferida 14.50 de UE 5.8.
- Character.h de UE 5.8 emite C4996 por APawn::GetMovementBase. La advertencia
  procede del motor, no de llamadas escritas en este cambio.

## Pruebas ejecutadas

- Compilación Development Editor para Win64 con Unreal Engine 5.8 de la base
  anterior: exitosa.
- Recompilación incremental del agachado híbrido con una acción paralela:
  exitosa en el primer intento.
- Recompilación de la limpieza sprint/crouch en EndPlay y OnUnPossess: exitosa.
- Matriz estática del agachado híbrido: PASS para toque desde pie, segundo toque,
  mantener desde pie y mantener desde agachado.
- Inspección de ownership: sin new/delete, timers, handles o recursos nativos
  manuales; default subobjects, TObjectPtr y TWeakObjectPtr correctamente usados.
- CompileAllBlueprints en UnrealEditor-Cmd con NullRHI y modo unattended:
  0 errores, 0 warnings y 0 Blueprints que no pudieron cargar.
- BP_TestActor existente: compilación exitosa dentro del commandlet.
- Inspección estática de macros UHT, firmas de Enhanced Input y API UE 5.8.
- Revisión estática independiente del delta `20e8fd2`: firmas `SetPawn`,
  `SetToDefaults`, `ValidateSettings` y `UnCrouch` compatibles con UE 5.8; sin
  bloqueantes encontrados para el alcance single-player.
- Matriz QA validada en UTF-8: 84 IDs únicos, tablas consistentes, cobertura de
  los 27 puntos de EDITOR_SETUP y trazabilidad de requisitos.
- `Invoke-PlayerQACheck.ps1` analizado con el parser de Windows PowerShell 5.1;
  salida humana y JSON válidas.
- Preflight estricto sobre worktree limpio: 0 FAIL y 1 WARN esperado porque esta
  laptop no se confirmó como hardware apto; Unreal permaneció cerrado.
- Casos negativos del verificador: worktree sucio, commit mínimo inválido, assets
  ausentes, filas NOT RUN y diagnósticos prohibidos producen FAIL y exit 1 sin
  abortar la salida estructurada.
- git diff --check: sin errores de whitespace; Git solo avisa la política local
  futura LF a CRLF de Build.cs.
- Auditoría de alcance: el C++ y sus documentos permanecen dentro de
  Proyecto-Memory. La única edición autorizada fuera fue el checklist del commit
  6a270af. Los dos archivos de árbol sin seguimiento en Modelos-3D pertenecen al
  propietario y se preservaron sin modificación.

Los artefactos de build y logs quedaron en carpetas ignoradas por Git:
Binaries, Intermediate y Saved.

## Integración pendiente en Unreal Editor

La base anterior compila, pero el delta `20e8fd2` y el contenido jugable siguen
pendientes. En una PC adecuada se debe:

1. Ejecutar preflight y compilar completamente `ProyectoMemoriaEditor`.
2. Crear BP_PlayerCharacter hijo de APMPlayerCharacter.
3. Asignar malla provisional y revisar cápsula/cámaras/valores.
4. Crear BP_PlayerController hijo de APMPlayerController para asignar IMC_Player
   y las seis IA.
5. Crear IA_Move, IA_Look, IA_Sprint, IA_Crouch, IA_Jump, IA_ToggleCamera e
   IMC_Player.
6. Mantener IA_Crouch como Digital con comportamiento predeterminado o trigger
   Down. No usar Hold, Tap, Pressed, Released ni Pulse porque C++ mide la duración.
   Asignar CrouchHoldThreshold (0,25 s por defecto).
7. Mapear teclado, ratón y mando según `PLAYER_SETTINGS_V0.1.md`: Espacio/A-X para
   salto y V/Y-triángulo para perspectiva.
8. Configurar un GameMode/World Settings de prueba con Pawn y Controller correctos.
9. Probar en L_Developer_Testing sin agregar lógica central al Level Blueprint.
10. Verificar por separado toque corto, segundo toque, mantener/soltar y cancelación
    de IA_Crouch.
    En manual, comparar un toque claramente corto con una pulsación de al menos
    0,5 s. Los límites 0,24/0,25/0,26 s requieren instrumentación o automatización;
    no deben validarse por estimación humana. Repetir a 30, 60 y 120 FPS cuando el
    hardware lo permita.
11. Validar pasillo 2,50 m, puerta 1,20 m, escaleras y habitación pequeña.
12. Probar salto normal/bajo techo, 1P/3P, respawn, persistencia entre ejecuciones,
    paredes, sensibilidad, inversión y objetivo de 60 FPS.

## Decisiones y deudas abiertas de v0.1.0

- Enhanced Input aparece aún como decisión pendiente en el control maestro, aunque
  la decisión local aprobada y la implementación ya lo adoptan.
- El delta `20e8fd2` no está compilado ni probado.
- IA_Jump, IMC_Player y los demás Input Assets todavía no existen.
- La persistencia de perspectiva está implementada en C++, pero no verificada en
  respawn ni entre ejecuciones.
- El menú de controles, bindings principal/secundario, conflictos, restauración y
  sensibilidad separada se implementarán en la etapa posterior de menús.
- No se creó una acción Interact; el sistema de interacción pertenece a v0.2.0.
- No hay replicación de sprint o modo de cámara; esta base asume el alcance
  single-player actual.
- El cambio 3P a 1P debe probarse visualmente para descartar un salto de yaw.
- No hay todavía pruebas funcionales de colisión, escaleras, espacios o mando.
- El agachado híbrido está compilado y revisado por matriz de estados, pero su
  temporización de 0,25 s debe ajustarse mediante prueba de usuario en PIE.
- Crouched Half Height y tolerancias medibles de velocidad/yaw siguen abiertos.
- Un futuro cambio a contexto UI o pausa debe cancelar explícitamente el gesto de
  crouch antes de deshabilitar el input, igual que ya hacen EndPlay y OnUnPossess.

## Preparación futura para publicación

Antes de publicar el juego se deberá mantener este registro y resolver, como mínimo:

- Titularidad, licencia del código y avisos de copyright del proyecto.
- Licencias y créditos de todos los assets, plugins, música, fuentes y librerías.
- Versiones exactas de Unreal, toolchain, SDK de cada plataforma y build reproducible.
- Política de privacidad/telemetría y permisos de plataforma si llegan a aplicar.
- Configuración Shipping, símbolos de depuración, crash reporting y firma.
- QA funcional, rendimiento, accesibilidad, localización, guardado y regresión.
- Clasificación por edades, requisitos y materiales de cada tienda/plataforma.

No se inventó ni añadió una licencia o aviso legal porque esa decisión corresponde
al propietario del proyecto.

## Actualización aplicada al checklist oficial

El propietario autorizó la actualización el 2026-07-13. Se registró en
Proyecto-Memoria-docs mediante el commit local 6a270af. Los avances siguientes
quedaron como [~] y no como [X], porque todavía falta validación manual:

Esta lista refleja únicamente lo registrado por ese commit. El trabajo local del
2026-07-15 y 2026-07-16 no se aplicó a Proyecto-Memoria-docs porque no hubo una
nueva autorización para editarlo.

- Crear APMPlayerCharacter en C++.
- Crear APMPlayerController en C++.
- Crear UPMCameraModeComponent en C++.
- Base C++ de movimiento, caminar, correr y agacharse.
- Agachado híbrido configurable: toque para alternar y mantener para soltar.
- Configuración nativa de cápsula.
- Base C++ de primera persona, tercera persona y cambio de cámara.
- Configuración de colisión de cámara implementada para tercera persona.
- Sensibilidad e inversión opcional expuestas.
- Lógica central en C++.
- Valores de diseño ajustables desde defaults de Blueprint.
- Sin lógica principal nueva en Level Blueprint.

Debe continuar pendiente hasta completar Editor y pruebas:

- BP_PlayerCharacter y BP_PlayerController.
- Malla, Input Actions, Mapping Context y GameMode.
- Teclado, ratón y mando realmente configurados.
- Movimiento y cámaras verificados en PIE.
- Pruebas dimensionales, colisión, escaleras, atasco y 60 FPS.
- Compilación Development Editor completa del delta local `20e8fd2`.
- IA_Jump y pruebas de salto normal, desde crouch y bajo techo.
- Persistencia de perspectiva: C++ local preparado, pendiente de compilación,
  respawn y prueba entre ejecuciones.
- Sincronizar, cuando el propietario lo autorice, las decisiones ya cerradas de
  salto y respuesta inmediata de cámara con el checklist oficial.
- Tag v0.1.0_player, merge y cualquier declaración de versión estable.

## Revisión pedagógica realizada sobre la base

El propietario revisó con Codex los archivos en este orden:

1. PMCameraModeComponent.h: tipos, retornos y contrato público.
2. PMCameraModeComponent.cpp: aplicación del modo y política de rotación.
3. PMPlayerCharacter.h/.cpp: composición, velocidades, crouch y cámaras.
4. PMPlayerController.h: contrato de cada Input Asset.
5. PMPlayerController.cpp: ciclo de vida del Mapping Context y bindings.
6. ProyectoMemoria.Build.cs: por qué EnhancedInput es una dependencia.

Cada archivo .h documenta responsabilidades, tipos y retornos; los .cpp explican
las decisiones que no son evidentes solo por leer la instrucción de código.
No es necesario repetir esta revisión de la base al reanudar, salvo que el
propietario lo solicite o aparezca una duda concreta. El delta `20e8fd2` recibió
revisión técnica estática, pero PMGameUserSettings y el nuevo flujo de salto aún
no han recibido una revisión pedagógica completa con el propietario.
