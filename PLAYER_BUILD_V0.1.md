# Versión jugable v0.1.0

## Abrir el juego

Ejecutar:

`Builds/PlayerV0.1/Windows/ProyectoMemoria.exe`

La carpeta `Builds/` es local y está excluida de Git. Si se mueve el paquete,
debe conservarse la carpeta completa `Windows`, no solo el `.exe`.

## Controles actuales

| Acción | Teclado | Mando |
|---|---|---|
| Moverse | W/A/S/D | Stick izquierdo |
| Mirar | Mouse | Stick derecho |
| Correr | Shift izquierdo | Gatillo superior izquierdo |
| Agacharse | C | Gatillo inferior izquierdo |
| Saltar | Space | A / X |
| Cambiar cámara | V | Y / triángulo |
| Pausa | Esc | — |

Al iniciar aparece el menú principal. `Jugar` entra a la partida; `Esc` abre
la pausa. Si el teclado no responde, hacer clic una vez dentro de la ventana.

## Estado

Esta compilación fue probada fuera del Editor el 2026-07-30. Carga
`/Game/Maps/L_Developer_Testing` y usa `BP_GameMode_DeveloperTesting_C`.
