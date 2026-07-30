# Decisiones del Player y controles

## Estado del documento

- Versión objetivo inmediata: v0.1.0 — personaje, movimiento y cámaras.
- Decisiones confirmadas por el propietario: 2026-07-15.
- Fuente de verdad para estas decisiones: este documento.
- Estado técnico: especificación aprobada; el C++ vigente compiló correctamente,
  existen las seis Input Actions y `IMC_Player` con sus 16 mappings verificados, y
  `BP_PlayerController` y `BP_PlayerCharacter` están configurados, compilados y
  guardados. `BP_GameMode_DeveloperTesting` también está configurado, compilado y
  guardado. `L_Developer_Testing` ya usa ese GameMode, conserva un único Player
  Start, no contiene Pawn manual ni lógica de Level Blueprint y tiene la
  geometría funcional compacta. El arranque, la posesión, `IMC_Player`, la
  perspectiva inicial y el movimiento cardinal y diagonal ya pasaron PIE; las
  demás pruebas funcionales continúan pendientes.
- Las sesiones controladas del 2026-07-22, 2026-07-26 y 2026-07-27 usaron la
  base de enfriamiento y HWiNFO. Las sesiones de configuración no recompilaron
  C++; las sesiones PIE de arranque, movimiento cardinal y diagonal se cerraron
  correctamente el 2026-07-27.

Este documento usa nombres sencillos para describir lo que debe experimentar el
jugador. No afirma que las funciones pendientes ya existan.

## Cámara

- La primera vez que se abre el juego, la vista inicial es primera persona.
- Cuando el jugador cambia de vista, el juego recuerda su elección.
- Si el personaje muere o reaparece, conserva la vista con la que murió.
- Si el jugador cierra y vuelve a abrir el juego, conserva la última vista usada.
- El movimiento de cámara responde inmediatamente al mouse o al mando, sin
  suavizado ni retraso artificial.
- La inversión vertical es opcional y está desactivada de forma predeterminada.
- La velocidad del mouse y la velocidad del mando se ajustan por separado.

## Salto

- El personaje puede saltar.
- Si está agachado y se presiona salto, primero intenta levantarse y después salta.
- Si un techo impide levantarse, no atraviesa la geometría y no deja un salto
  pendiente que ocurra inesperadamente más tarde.
- Mantener o soltar el botón respeta el ciclo normal de salto de `ACharacter`.

## Controles predeterminados

El diseño principal es teclado y mouse. El mando es opcional, pero debe quedar
completamente funcional.

### Teclado y mouse

| Acción | Control predeterminado |
|---|---|
| Caminar | W, A, S y D |
| Mover la cámara | Mouse |
| Saltar | Espacio |
| Correr | Shift izquierdo |
| Agacharse | Ctrl izquierdo o C |
| Cambiar primera/tercera persona | V |

### Mando

| Acción | Control predeterminado |
|---|---|
| Caminar | Palanca izquierda |
| Mover la cámara | Palanca derecha |
| Saltar | A en Xbox / X en PlayStation, botón inferior |
| Correr | Presionar la palanca izquierda, L3 |
| Agacharse | B en Xbox / círculo en PlayStation, botón derecho |
| Cambiar primera/tercera persona | Y en Xbox / triángulo en PlayStation, botón superior |

No se añade una zona muerta deliberada para ocultar movimientos pequeños del
mando. Cualquier drift real debe quedar visible durante QA y registrarse con el
modelo de mando utilizado.

## Menú de controles posterior

El menú para personalizar controles es obligatorio antes de finalizar el juego,
pero no bloquea la integración inicial de v0.1.0. Se implementará en la etapa de
menús y ajustes.

El menú debe:

- estar disponible dentro del juego;
- permitir cambiar teclado, mouse y mando;
- ofrecer una asignación principal y otra secundaria por acción;
- rechazar una tecla o botón ya ocupado y mostrar un aviso claro;
- permitir restablecer todos los valores predeterminados;
- guardar los cambios para futuras ejecuciones;
- ofrecer velocidades separadas para mouse y mando;
- permitir activar o desactivar la inversión vertical.

La ausencia temporal de este menú no autoriza olvidar estos requisitos ni marcar
como terminada la etapa futura de ajustes.

## Diferencias con el estado actual

Después de aprobar esta especificación, las siguientes funciones quedaron
implementadas y compiladas. `EV-PIE-START-01` verificó únicamente el arranque
inicial, `EV-MOV-WASD-01` verificó W/A/S/D por separado y `EV-MOV-DIAG-01`
verificó las cuatro diagonales; las pruebas específicas de las demás funciones
siguen pendientes:

- binding C++ de salto y levantado inmediato con comprobación de techo;
- memoria de perspectiva para respawn y futuras ejecuciones mediante
  `UPMGameUserSettings`;
- protección para que `BeginPlay` no reemplace una perspectiva ya restaurada;
- suavizado de mouse desactivado y camera lag desactivado;
- zona muerta 0 para las cuatro direcciones de los sticks;
- guía, matriz QA y layout del mando actualizados a A/X y Y/triángulo.

Las seis Input Actions y el contenedor `IMC_Player` ya existen. Sus 16 mappings de
teclado, mouse y mando fueron guardados y verificados el 2026-07-22.
`BP_PlayerController` también existe como hijo de `APMPlayerController`: referencia
el contexto y las seis acciones, conserva sensibilidad X/Y en 1.0, inversión Y
desactivada, prioridad 0 y umbral de crouch en 0.25 s. `BP_PlayerCharacter` existe
como hijo puramente heredado de `APMPlayerCharacter`; conserva las velocidades,
cápsula, crouch, cámaras y CameraMode aprobados. Ambos Event Graphs están vacíos y
los dos assets fueron compilados, validados y guardados.
`BP_GameMode_DeveloperTesting` ya usa esas dos clases, conserva su Event Graph
vacío y también fue compilado, validado y guardado. El mapa de pruebas ya lo usa,
tiene un único Player Start y no tiene Pawn manual ni lógica de Level Blueprint.
La geometría funcional compacta también está guardada y validada. Todavía faltan
el menú, sus widgets y las pruebas PIE posteriores a `PLR-MOV-002`. El C++ actual
conserva una sensibilidad compartida para mouse y mando; separarlas dinámicamente
pertenece a la etapa de ajustes.

Estas diferencias son trabajo pendiente, no fallos observados en PIE. La primera
sesión PIE confirmó GameMode, spawn, posesión, `IMC_Player` y primera persona. Una
sesión posterior confirmó W/A/S/D por separado, sus cuatro vectores cardinales y
la detención al soltar; otra confirmó las cuatro diagonales alrededor de
300 cm/s, sin ventaja diagonal observable, y la detención. Esto no sustituye las
pruebas de look, velocidad recta, cámaras, mando, respawn o rendimiento.

## Separación de alcance

### Debe resolverse en v0.1.0

- salto y comportamiento al saltar desde agachado;
- persistencia de perspectiva al reaparecer y entre ejecuciones;
- cámara sin suavizado;
- controles predeterminados de teclado, mouse y mando;
- inversión vertical preparada y valor predeterminado desactivado;
- validación de los controles en PIE con teclado y mando.

### Se resuelve en la etapa posterior de menús y ajustes

- pantalla de controles;
- reasignación principal y secundaria;
- detección y aviso de conflictos;
- restauración de valores predeterminados;
- guardado de bindings personalizados;
- velocidades separadas para mouse y mando;
- controles visuales para sensibilidad e inversión vertical.

## Regla de aceptación

Una decisión solo pasa de “especificada” a “implementada” cuando existe código o
asset trazable. Solo pasa a “verificada” cuando se ejecutan las pruebas pertinentes
en una PC adecuada y se adjunta evidencia en la matriz QA.

## Validación funcional reciente

El 2026-07-28 `PLR-MOV-003` confirmó entrada física de mouse: movimiento vertical pequeño desde pitch/yaw `0/0` produjo pitch `-43.2250006°`, yaw `0°`, y permaneció estable tras 1.2 s. Sensibilidades X/Y siguen en `1.0` e inversión Y desactivada. Próxima validación: `PLR-CAM-001` (cambio a tercera persona).
### Corrección aplicada el 2026-07-29

La dirección vertical predeterminada del mouse quedó corregida: moverlo hacia arriba hace que la cámara mire hacia arriba. `bInvertLookY` continúa disponible para invertirla voluntariamente.
### Validación de cámara (2026-07-29)

V alternó correctamente FirstPerson/ThirdPerson y regresó a FirstPerson. La configuración 3P observada fue FOV 90°, brazo 300 cm y colisión activa. La malla del Character sigue sin asignarse; validar apariencia por separado cuando exista un asset autorizado. Siguiente: PLR-CAM-002 (continuidad de yaw).



La continuidad de orientaciÃ³n al regresar de 3P a 1P quedÃ³ confirmada en PIE (PLR-CAM-002).


MenÃº de controles inicial (2026-07-29): se aÃ±adiÃ³ un menÃº principal, pausa con Esc y pantalla de configuraciÃ³n Slate con sensibilidad X/Y, inversiÃ³n vertical y restaurar valores. Queda preparado para separar configuraciÃ³n de mando y teclado en la siguiente iteraciÃ³n.

