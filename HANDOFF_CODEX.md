# HANDOFF CODEX — Proyecto Memoria

## Identificación de esta entrega

- Versión de trabajo: v0.1.0 — personaje, movimiento y cámaras.
- Fecha local: 2026-07-12 (America/Costa_Rica).
- Última actualización: 2026-07-13 — agachado híbrido solicitado por el propietario.
- Rama: feature/v0.1-player-cameras.
- Motor verificado: Unreal Engine 5.8.
- Plataforma compilada: Windows 64-bit, Development Editor.
- Trabajo técnico generado por: Codex, bajo dirección y revisión del propietario del proyecto.
- Estado: código C++ compilado y carga headless verificada; integración jugable en Unreal Editor pendiente.
- Publicación remota: ninguna. No se hizo push, merge ni tag.

Este documento registra lo realizado por Codex para facilitar revisión, continuidad,
auditoría y una futura preparación de publicación. No sustituye la documentación
oficial de Proyecto-Memoria-docs y no establece por sí mismo licencia, titularidad
legal ni obligaciones de atribución.

## Alcance autorizado y respetado

Se trabajó únicamente en Proyecto-Memory. Proyecto-Memoria-docs se consultó en
modo de solo lectura y Modelos-3D no se modificó. Tampoco se cambió el checklist
compartido.

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
- HANDOFF_CODEX.md

## Archivo existente modificado por Codex

- UnrealProject/Source/ProyectoMemoria/ProyectoMemoria.Build.cs
  - Se agregó EnhancedInput como dependencia pública del módulo.

No se crearon ni editaron assets binarios, Blueprints, mapas, archivos de
configuración, Level Blueprints ni contenido de los repositorios excluidos.

## Arquitectura implementada

Flujo de responsabilidades:

APMPlayerController
  -> traduce Enhanced Input a órdenes
APMPlayerCharacter
  -> posee movimiento, cápsula y componentes de cámara
UPMCameraModeComponent
  -> aplica el estado de perspectiva 1P/3P

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
- Propiedad del UPMCameraModeComponent.

API pública:

| Método | Entrada | Retorno | Contrato |
|---|---|---|---|
| SetSprinting | bool bEnabled | void | Activa sprint solo si el personaje no está agachado. |
| SetCrouching | bool bEnabled | void | Solicita Crouch o UnCrouch y cancela sprint al agacharse. |
| ToggleCrouch | ninguna | void | Alterna Crouch/UnCrouch y cancela sprint al agacharse. |
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
- Agachado híbrido con una acción Digital: toque corto alterna; mantener presionado
  agacha inmediatamente y levanta al soltar.
- Umbral de mantener presionado editable, 0,25 s por defecto.
- Restauración de la postura inicial si Enhanced Input cancela IA_Crouch.
- Recuperación ante un Started duplicado y limpieza al terminar o cambiar el Pawn.
- Cambio de cámara mediante una acción Digital.
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

Comando final:

    Build.bat ProyectoMemoriaEditor Win64 Development
      -Project=<ruta>/ProyectoMemoria.uproject
      -WaitMutex -NoHotReloadFromIDE -MaxParallelActions=1

Resultado final: Succeeded. UHT, compilación y enlace de
UnrealEditor-ProyectoMemoria.dll completados.

Avisos externos observados:

- Visual Studio MSVC 14.51 es más nuevo que la versión preferida 14.50 de UE 5.8.
- Character.h de UE 5.8 emite C4996 por APawn::GetMovementBase. La advertencia
  procede del motor, no de llamadas escritas en este cambio.

## Pruebas ejecutadas

- Compilación Development Editor para Win64 con Unreal Engine 5.8: exitosa.
- Recompilación incremental del agachado híbrido con una acción paralela:
  exitosa en el primer intento.
- Matriz estática del agachado híbrido: PASS para toque desde pie, segundo toque,
  mantener desde pie y mantener desde agachado.
- CompileAllBlueprints en UnrealEditor-Cmd con NullRHI y modo unattended:
  0 errores, 0 warnings y 0 Blueprints que no pudieron cargar.
- BP_TestActor existente: compilación exitosa dentro del commandlet.
- Inspección estática de macros UHT, firmas de Enhanced Input y API UE 5.8.
- git diff --check: sin errores de whitespace; Git solo avisa la política local
  futura LF a CRLF de Build.cs.
- Auditoría de alcance: los cambios persistentes están dentro de Proyecto-Memory;
  Proyecto-Memoria-docs y Modelos-3D permanecen limpios.

Los artefactos de build y logs quedaron en carpetas ignoradas por Git:
Binaries, Intermediate y Saved.

## Integración pendiente en Unreal Editor

El código compila, pero aún no existe contenido que lo convierta en un personaje
jugable. En una PC adecuada se debe:

1. Confirmar formalmente la decisión de usar Enhanced Input.
2. Crear BP_PlayerCharacter hijo de APMPlayerCharacter.
3. Asignar malla provisional y revisar cápsula/cámaras/valores.
4. Decidir y crear BP_PlayerController hijo de APMPlayerController para asignar
   IMC_Player y las cinco IA.
5. Crear IA_Move, IA_Look, IA_Sprint, IA_Crouch, IA_ToggleCamera e IMC_Player.
6. Mantener IA_Crouch como Digital con comportamiento predeterminado o trigger
   Down. No usar Hold, Tap, Pressed, Released ni Pulse porque C++ mide la duración.
   Asignar CrouchHoldThreshold (0,25 s por defecto).
7. Mapear teclado, ratón y mando.
8. Configurar un GameMode/World Settings de prueba con Pawn y Controller correctos.
9. Probar en L_Developer_Testing sin agregar lógica central al Level Blueprint.
10. Verificar por separado toque corto, segundo toque, mantener/soltar y cancelación
    de IA_Crouch.
    Probar alrededor de 0,24/0,25/0,26 s a 30, 60 y 120 FPS.
11. Validar pasillo 2,50 m, puerta 1,20 m, escaleras y habitación pequeña.
12. Probar 1P/3P, paredes, sensibilidad, inversión y objetivo de 60 FPS.

## Decisiones y deudas abiertas de v0.1.0

- Enhanced Input aparece aún como decisión pendiente en el control maestro, aunque
  la implementación ya lo adopta.
- No se guarda la preferencia de perspectiva entre sesiones.
- No se implementó movimiento reducido de cámara opcional.
- No se desactivó Jump de forma absoluta; el checklist dice hacerlo solo si se
  decide que no es necesario.
- No se creó una acción Interact; el sistema de interacción pertenece a v0.2.0.
- No hay replicación de sprint o modo de cámara; esta base asume el alcance
  single-player actual.
- El cambio 3P a 1P debe probarse visualmente para descartar un salto de yaw.
- No hay todavía pruebas funcionales de colisión, escaleras, espacios o mando.
- El agachado híbrido está compilado y revisado por matriz de estados, pero su
  temporización de 0,25 s debe ajustarse mediante prueba de usuario en PIE.
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

## Delta acumulado del checklist — NO APLICAR SIN PERMISO

La documentación oficial debe permanecer sin cambios hasta autorización explícita.
Este es el registro local para una actualización futura:

Listo en código y compilado, pero todavía no debe cerrarse oficialmente:

- Crear APMPlayerCharacter en C++.
- Crear APMPlayerController en C++.
- Crear UPMCameraModeComponent en C++.
- Base C++ de movimiento, caminar, correr y agacharse.
- Agachado híbrido configurable: toque para alternar y mantener para soltar.
- Configuración nativa de cápsula.
- Base C++ de primera persona, tercera persona y cambio de cámara.
- Prueba de colisión de cámara implementada para tercera persona.
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
- Persistencia de perspectiva.
- Decisión sobre salto y movimiento reducido de cámara.
- Tag v0.1.0_player, merge y cualquier declaración de versión estable.

## Guía de revisión pedagógica

Orden recomendado para que el propietario revise y aprenda el código:

1. PMCameraModeComponent.h: tipos, retornos y contrato público.
2. PMCameraModeComponent.cpp: aplicación del modo y política de rotación.
3. PMPlayerCharacter.h/.cpp: composición, velocidades, crouch y cámaras.
4. PMPlayerController.h: contrato de cada Input Asset.
5. PMPlayerController.cpp: ciclo de vida del Mapping Context y bindings.
6. ProyectoMemoria.Build.cs: por qué EnhancedInput es una dependencia.

Cada archivo .h documenta responsabilidades, tipos y retornos; los .cpp explican
las decisiones que no son evidentes solo por leer la instrucción de código.
