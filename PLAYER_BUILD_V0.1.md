# Versión jugable v0.1.0

## Abrir el juego

Para la build Development de pruebas, ejecutar:

`Builds/PlayerV0.1/Windows/ProyectoMemoria.exe`

También se puede usar el lanzador, que abre el binario interno correcto:

`powershell -ExecutionPolicy Bypass -File Tools/Launch-PlayerV0.1.ps1`

Para la build Shipping de distribución privada:

`powershell -ExecutionPolicy Bypass -File Tools/Launch-PlayerV0.1.ps1 -Shipping`

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

La build Development fue regenerada con `BuildCookRun` y la build Shipping se
generó el 2026-08-04 con `-clientconfig=Shipping`; ambas cargan
`/Game/Maps/L_Developer_Testing` y usan `BP_GameMode_DeveloperTesting_C`.

La Shipping se copió a una carpeta temporal limpia y su binario interno se
mantuvo activo durante 10 segundos con `-nullrhi -nosound`, sin error de carga.
El ejecutable Shipping principal tiene SHA-256
`203FDF32530AC28F7604F8BE02B205B960DBD13FA5828925A7DFAF0C7ABD247C`.

La distribución debe conservar completa la carpeta `Windows` y cumplir la
auditoría de [CREDITS_AND_LICENSES.md](CREDITS_AND_LICENSES.md).

## Verificación reproducible

Para comprobar una copia antes de entregarla:

`powershell -ExecutionPolicy Bypass -File Tools/QA/Verify-PlayerPackage.ps1 -Shipping -LaunchSmoke`

El verificador valida el ejecutable, los contenedores de contenido y sus
SHA-256, y mantiene la build activa durante un smoke test sin Unreal Editor.
