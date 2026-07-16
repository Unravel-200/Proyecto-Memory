# Decisiones del Player y controles

## Estado del documento

- Versión objetivo inmediata: v0.1.0 — personaje, movimiento y cámaras.
- Decisiones confirmadas por el propietario: 2026-07-15.
- Fuente de verdad para estas decisiones: este documento.
- Estado técnico: especificación aprobada; C++ y configuración preparados;
  compilación, Input Assets y pruebas todavía pendientes.
- Restricción actual: no abrir Unreal, compilar, ejecutar PIE ni generar shaders en
  esta laptop.

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

Después de aprobar esta especificación quedaron preparados, pero todavía sin
compilar ni probar:

- binding C++ de salto y levantado inmediato con comprobación de techo;
- memoria de perspectiva para respawn y futuras ejecuciones mediante
  `UPMGameUserSettings`;
- protección para que `BeginPlay` no reemplace una perspectiva ya restaurada;
- suavizado de mouse desactivado y camera lag desactivado;
- zona muerta 0 para las cuatro direcciones de los sticks;
- guía, matriz QA y layout del mando actualizados a A/X y Y/triángulo.

Los Input Assets, el menú y sus widgets todavía no existen. El C++ actual conserva
una sensibilidad compartida para mouse y mando; separarlas dinámicamente pertenece
a la etapa de ajustes.

Estas diferencias son trabajo pendiente, no fallos observados en PIE. Todavía no
se ha abierto ni probado Unreal para implementar esta especificación.

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
