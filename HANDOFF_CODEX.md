# HANDOFF CODEX — Proyecto Memoria

## Identificación de esta entrega

- Versión de trabajo: v0.1.0 — personaje, movimiento y cámaras.
- Fecha local: 2026-07-28 (America/Costa_Rica).
- Última actualización: 2026-07-27 — movimiento diagonal y look con ratÃ³n aprobados: las cuatro
  combinaciones produjeron sus vectores, quedaron alrededor de 300 cm/s sin
  ventaja diagonal observable y se detuvieron.
- Rama: feature/v0.1-player-cameras.
- Motor verificado: Unreal Engine 5.8.
- Plataforma de la base compilada: Windows 64-bit, Development Editor.
- Autoría operativa declarada por el propietario: base inicial y línea de modelado
  3D trabajadas con Claude; rama del Player, QA, compilación reciente e integración
  parcial de Input trabajadas con Codex. Git registra los commits como
  `unknown <jefferson.amador@ucr.ac.cr>`, por lo que esta separación se apoya en la
  confirmación del propietario y en los documentos de trazabilidad, no en el campo
  Author de Git.
- Estado: el C++ vigente, incluido salto y persistencia, ya recibió compilación
  Development Editor completa y exitosa. Unreal Editor 5.8, Enhanced Input y el
  servidor oficial Unreal MCP fueron verificados. Existen las seis Input Actions y
  `IMC_Player` con 16 mappings guardados y verificados. `BP_PlayerController`,
  `BP_PlayerCharacter` y `BP_GameMode_DeveloperTesting` existen, tienen las
  referencias requeridas, Event Graphs vacíos y compilación exitosa.
  `L_Developer_Testing` usa ese GameMode, contiene exactamente un Player Start y
  no contiene Pawn manual ni lógica de Level Blueprint. La geometría funcional
  compacta de 23 cubos está completa y validada. `PLR-PIE-001`,
  `PLR-MOV-001..002` y `EVC-06` están en PASS: PIE creó el Controller y Character
  correctos, aplicó `IMC_Player` y First Person, y las ocho direcciones de teclado
  produjeron sus vectores sin movimiento residual. Las cuatro diagonales midieron
  aproximadamente 300 cm/s, no 424 cm/s. No apareció ninguno de los seis
  diagnósticos prohibidos. Las pruebas desde look en adelante continúan pendientes.
  HWiNFO permaneció activo; durante la sesión se observó CPU (Tctl/Tdie) a
  49.2 °C y un máximo acumulado de 80.6 °C.
- Publicación remota de la rama del Player: `origin/feature/v0.1-player-cameras`
  contiene `336aa91`. Los commits locales posteriores todavía no están
  publicados; no se hizo un nuevo push, merge, rebase ni tag.

Este documento consolida lo realizado con Claude y Codex para facilitar una
transferencia entre computadoras, revisión, continuidad, auditoría y una futura
preparación de publicación. No sustituye la documentación oficial de
Proyecto-Memoria-docs y no establece por sí mismo licencia, titularidad legal ni
obligaciones de atribución.

## Reanudación rápida — próxima sesión

### Punto de control

- Repositorio de código: Proyecto-Memory.
- Rama obligatoria: feature/v0.1-player-cameras.
- HEAD al comenzar la sesión de geometría: `90ef65f`.
- HEAD probado durante la primera sesión PIE: `5e1993f`.
- Commits relevantes de v0.1.0:
  - f8dfb21 — personaje, movimiento y cámaras.
  - e8095b4 — agachado híbrido.
  - 5eccd8e — limpieza de sprint/crouch al perder posesión.
  - 947681f — guía reproducible de integración en Unreal Editor.
  - d82ea86 — punto de reanudación y restricciones de la laptop.
  - efc931c — matriz de evidencia QA del Player.
  - 9132738 — verificador QA de solo lectura para preflight y postflight.
  - 73de57b — endurecimiento de Git/LFS, assets, matriz QA y Output Log.
  - a7236e0 — handoff actualizado con la matriz y el verificador QA.
  - 20e8fd2 — salto seguro, cámara inmediata y persistencia de perspectiva.
  - 59ed2cf — decisiones aprobadas, guía de 27 pasos y matriz de 84 pruebas.
  - e2fbad7 — verificador sincronizado con IA_Jump y las configuraciones aprobadas.
  - a97762a — handoff de salto, persistencia y estado pendiente anterior a Editor.
  - 8e0aaba — documentación de la sesión inicial de Input.
  - d569e31 — 16 mappings de `IMC_Player` configurados y verificados.
  - 81fa688 — `BP_PlayerController` configurado, auditado y guardado.
  - 4efac4c — postflight y documentación final de `BP_PlayerController`.
  - 46b4f25 — `BP_PlayerCharacter` creado, auditado y documentado.
  - d96e173 — postflight y documentación final de `BP_PlayerCharacter`.
  - 6707913 — `BP_GameMode_DeveloperTesting` creado, auditado y documentado.
  - 1629eac — postflight y documentación final de
    `BP_GameMode_DeveloperTesting`.
  - d4d6732 — configuración base de `L_Developer_Testing`, evidencia parcial y
    documentación.
  - 1c42a63 — postflight y documentación final de la configuración base del
    mapa.
  - 90ef65f — layout compacto exacto documentado y auditado.
  - 83644f5 — geometría compacta creada, auditada y documentada.
  - 5e1993f — postflight y documentación final de la geometría.
  - 8def4bb — evidencia y documentación de la primera prueba PIE.
  - c2a61c3 — postflight y documentación final de la primera prueba PIE.
  - 9e46365 — evidencia y documentación del movimiento cardinal W/A/S/D.
  - 352f629 — postflight y documentación final del movimiento cardinal.
  - 39352d1 — evidencia y documentación del movimiento diagonal.
- Checklist oficial actualizado en Proyecto-Memoria-docs, commit 6a270af.
- El propietario autorizó el 2026-07-20 crear el commit de transferencia y hacer
  push de los tres repositorios. La rama `feature/v0.1-player-cameras` se publica
  en `origin`; no se hizo merge, rebase ni tag.
- Proyecto-Memoria-docs queda en `main`, HEAD 7c44472, sincronizado con
  `origin/main` después de publicar 6a270af, 005f910 y 7c44472.
- Modelos-3D queda en `main`, HEAD a1e3952, sincronizado con `origin/main` después
  de publicar el blockout del aula.
- Modelos-3D contiene dos archivos sin seguimiento del propietario que deben
  preservarse: Plaza/SM_Tree_PlazaCentral_A.blend y
  Plaza/SM_Tree_PlazaCentral_A.py.

### Próxima acción recomendada

La base de enfriamiento ya fue usada con éxito en las sesiones controladas.
`IMC_Player`, los tres Blueprints, el mapa y el layout compacto de 23 cubos
quedaron guardados y validados. `LVL-01`, `GEO-01..07` y `EVC-05` están en PASS.
La primera ejecución PIE y el movimiento cardinal y diagonal también están
completos: `PLR-PIE-001`, `PLR-MOV-001..002` y `EVC-06` están en PASS. El próximo
trabajo es `PLR-MOV-003`, sección 12 punto 4 de `EDITOR_SETUP_V0.1.md`: probar
look horizontal y vertical con el ratón, incluido detenerlo. No reconfigurar las
secciones 5 a 10 ni repetir los casos aprobados por costumbre; sí iniciar PIE
para cada prueba funcional.

En una PC adecuada, no repetir las secciones ya completadas por costumbre.
Verificar primero rama, HEAD y archivos transferidos. Abrir Unreal con el MCP
oficial si se desea automatizar el Editor y continuar en `EDITOR_SETUP_V0.1.md`
desde la sección 12 punto 4: `PLR-MOV-003`.
`PLAYER_SETTINGS_V0.1.md`, `QA_PLAYER_V0.1.md` y
`Tools/QA/Invoke-PlayerQACheck.ps1` ya existen; no recrearlos.

Esta entrega incluye `HANDOFF_CODEX.md` y los siete `.uasset` en el mismo commit,
con los binarios gestionados por Git LFS. En el equipo nuevo, el preflight debe
ejecutarse únicamente después de comprobar que el clone/pull está limpio. Si Git
muestra cambios o archivos faltantes, detener el flujo e investigar. No usar
`-AllowDirty` para evitar esta protección.

Nota de precedencia: los estados principales de `PLAYER_SETTINGS_V0.1.md`,
`EDITOR_SETUP_V0.1.md` y `QA_PLAYER_V0.1.md` están sincronizados al 2026-07-27.
Los siete controles de configuración `MAP-01..07` están en PASS; las pruebas
funcionales desde look continúan en `NOT RUN`. `BP-01..06`, `LVL-01`,
`GEO-01..07`, `PLR-PIE-001`, `PLR-MOV-001..002` y `EVC-04..06` están en PASS.
La matriz contiene 28 PASS y 56 IDs `NOT RUN`.

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

> Continúa Proyecto Memoria en esta PC nueva. Trabaja únicamente en
> Proyecto-Memory y lee HANDOFF_CODEX.md, PLAYER_SETTINGS_V0.1.md,
> EDITOR_SETUP_V0.1.md y QA_PLAYER_V0.1.md completos. Verifica que la rama sea
> feature/v0.1-player-cameras y que existan los siete assets bajo
> UnrealProject/Content/Input. No hagas push, merge, rebase ni tag sin mi permiso.
> No edites Proyecto-Memoria-docs y no toques Modelos-3D; preserva especialmente
> Plaza/SM_Tree_PlazaCentral_A.blend y .py. El C++ vigente ya compiló correctamente.
> Las seis Input Actions, los 16 mappings de IMC_Player y los tres Blueprints ya
> están guardados y verificados. L_Developer_Testing ya usa el GameMode y tiene
> un único Player Start definitivo y la pista compacta de 23 cubos validada.
> La primera ejecución PIE ya aprobó spawn, posesión, IMC_Player, primera persona
> y ausencia de los seis diagnósticos prohibidos. PLR-MOV-001 y PLR-MOV-002
> también aprobaron las cuatro direcciones cardinales, las cuatro diagonales,
> estimaciones alrededor de 300 cm/s sin ventaja diagonal observable y detención
> al soltar. Continúa desde
> EDITOR_SETUP_V0.1.md sección 12 punto 4 con PLR-MOV-003; no reconfigures las
> secciones 5 a 10 ni vuelvas a auditar casos aprobados por costumbre. Sí inicia
> PIE para ejecutar las pruebas funcionales. No
> ejecutes herramientas de Unreal en paralelo y no declares pruebas PIE como
> aprobadas hasta ejecutarlas.

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

## Trabajo realizado con Claude

La atribución de esta sección procede de la confirmación del propietario y del
informe `Proyecto-Memoria-docs/Modelos3D/Trazabilidad_Modelos_3D_IA.txt`, que
identifica expresamente una sesión con Claude (Sonnet 5). Todos los commits de los
tres repositorios usan el autor genérico `unknown`; Git por sí solo no distingue a
Claude, Codex o al propietario.

### Base de Proyecto-Memory anterior a la rama de Codex

Según la confirmación del propietario, la base anterior se trabajó con Claude. El
rango termina en `45dcfcb`, padre directo de `f8dfb21`, primer commit documentado
de Codex en la rama del Player.

| Commit | Trabajo registrado |
|---|---|
| 579001e | Importación inicial de documentos, juego, checklist, historia y recomendaciones. |
| 9c253c2 | Estructura base del repositorio, `.gitattributes` con LFS, `.gitignore`, README y `.gitkeep`. |
| 1242222 | Aclaración de que Config, Source y el `.uproject` deben rastrearse. |
| 45dd085 | Scaffold UE 5.8/C++: proyecto, Targets, módulo, configuraciones y `APMTestActor`. |
| 2c49e3e | Actualización del checklist v0.0.1 que entonces vivía dentro del repo. |
| 76b89bf | Retiro de la copia de Docs al migrarla a Proyecto-Memoria-docs. |
| 26a14e7 | Primera compilación exitosa y creación de `L_Developer_Testing.umap`. |
| 9a4fbb6 | Creación de `BP_TestActor.uasset` y comprobación de herencia C++ a Blueprint. |
| 45dcfcb | Corrección del README para apuntar al repositorio hermano de documentación. |

### Línea de modelado 3D de Claude

Claude generó 34 activos mediante scripts Python ejecutados con Blender 5.1 en
modo headless. El propietario abrió y revisó visualmente cada `.blend` y pidió
correcciones por chat. Los materiales son procedurales; el informe no registra
texturas, fuentes ni assets externos descargados. Esto no certifica originalidad,
licencia ni aptitud para publicación.

- Estado Blender: 32 `[X] Listo en Blender` y 2 `[P] Provisional`.
- Estado Unreal: los 34 siguen `[UE] Pendiente`; ninguno fue exportado, importado
  ni validado dentro de Unreal.
- Los primeros 20 activos conservan el `.blend`, pero sus scripts temporales se
  eliminaron y la lógica se reconstruyó desde la conversación.
- Desde `ARC-LIB-005` se conservaron 14 scripts `.py` junto al `.blend`.
- Fuente exhaustiva de prompts, correcciones y decisiones:
  `Proyecto-Memoria-docs/Modelos3D/Trazabilidad_Modelos_3D_IA.txt`.
- Fuente de estado vigente:
  `Proyecto-Memoria-docs/Modelos3D/Registro_Maestro_Activos_Proyecto_Memoria.txt`.
- Infraestructura del repositorio de modelos: `a5980cd` creó el repositorio y
  `3f18671` agregó el README hacia Proyecto-Memoria-docs. Junto con los commits de
  la tabla y `23954c7`, esto cubre los 40 commits actuales de Modelos-3D.

Inventario completo generado y documentado:

| ID | Archivo base dentro de Modelos-3D | Estado | Commit(s) |
|---|---|---|---|
| FUR-LIB-007 | Biblioteca/SM_Bookshelf_Library_A.blend | Listo en Blender | 0bab614 |
| PRP-LIB-006 | Biblioteca/SM_BookRow_Library_A.blend | Listo en Blender | 5d215b3 |
| FUR-LIB-008 | Biblioteca/SM_Bookshelf_Door_A.blend | Listo en Blender | 22fcaeb |
| ARC-LIB-002 | Biblioteca/SM_Hatch_Library_A.blend | Listo en Blender | 00016a6 |
| PRP-LIB-007 | Biblioteca/SM_HangingBulb_Library_A.blend | Listo en Blender | 8a8b2f3 |
| FUR-LIB-009 | Biblioteca/SM_MetalShelf_LibraryBasement_A.blend | Listo en Blender | 2a74c69 |
| DOC-LIB-001 | Biblioteca/SM_Manuscript_ForbiddenHistories_Library.blend | Listo en Blender | 3508618 |
| ARC-LIB-003 | Biblioteca/SM_Door_LibraryBasement_A.blend | Listo en Blender | ee9232a |
| FUR-LIB-001 | Biblioteca/SM_Desk_LibraryLobby_A.blend | Listo en Blender | efc807f |
| FUR-LIB-002 | Biblioteca/SM_Bench_LibraryLobby_A.blend | Listo en Blender | c14c700 |
| PRP-LIB-001 | Biblioteca/SM_DirectorySign_Library_A.blend | Listo en Blender | d5d8713 |
| ARC-LIB-001 | Biblioteca/SM_Door_LibraryMain_A.blend | Listo en Blender | d5d93f4 |
| FUR-LIB-003 | Biblioteca/SM_Desk_LibraryGuard_A.blend | Listo en Blender | 3c09ee9 |
| PRP-LIB-002 | Biblioteca/SM_Phone_LibraryReception_A.blend | Listo en Blender | b35f463 |
| PRP-LIB-003 | Biblioteca/SM_LogBook_LibraryReception_A.blend | Listo en Blender | b619bf0 |
| FUR-LIB-005 | Biblioteca/SM_Desk_LibrarySurveillance_A.blend | Listo en Blender | 98f020f |
| PRP-LIB-004 | Biblioteca/SM_MonitorSet_LibrarySurveillance_A.blend | Listo en Blender | 6ff0e00 |
| PRP-LIB-005 | Biblioteca/SM_Console_LibrarySurveillance_A.blend | Listo en Blender | 697801d |
| ARC-LIB-004 | Biblioteca/SM_Door_LibraryService_A.blend | Listo en Blender | 06eac60 |
| PRP-LIB-008 | Biblioteca/SM_ExitSign_Library_A.blend | Listo en Blender | fcadb6e |
| ARC-LIB-005 | Biblioteca/SM_VestibuloBlockout_Library_A.blend + .py | Listo en Blender | 717d311, bf88451 |
| ARC-LIB-006 | Biblioteca/SM_RecepcionBlockout_Library_A.blend + .py | Listo en Blender | 973060d |
| ARC-LIB-007 | Biblioteca/SM_VigilanciaBlockout_Library_A.blend + .py | Listo en Blender | 7dae03a, def2789 |
| ARC-LIB-008 | Biblioteca/SM_ColeccionRestringidaBlockout_Library_A.blend + .py | Listo en Blender | def2789 |
| ARC-LIB-009 | Biblioteca/SM_Sotano1Blockout_Library_A.blend + .py | Listo en Blender | 3181829 |
| ARC-EXT-001 | Plaza/SM_PlazaFloorBlockout_A.blend + .py | Listo en Blender | dca3df8 |
| ARC-EXT-002 | Plaza/SM_Fountain_PlazaCentral_A.blend + .py | Provisional | c124c80, 9a88a45 |
| FUR-EXT-001 | Plaza/SM_Bench_PlazaCentral_A.blend + .py | Listo en Blender | 87b2169 |
| PRP-EXT-001 | Plaza/SM_Lamppost_PlazaCentral_A.blend + .py | Listo en Blender | d8b8944 |
| ARC-GEN-002 | Generales/SM_VestibuloBlockout_Generales_A.blend + .py | Listo en Blender | 542699e |
| ARC-GEN-003 | Generales/SM_SodaBlockout_Generales_A.blend + .py | Listo en Blender | ca991a7 |
| ARC-GEN-004 | Generales/SM_Stairs_Generales_A.blend + .py | Provisional | cecb76d |
| FUR-GEN-001 | Generales/SM_DiningSet_Soda_A.blend + .py | Listo en Blender | fc5c973 |
| ARC-GEN-005 | Generales/SM_AulaBlockout_Generales_A.blend + .py | Listo en Blender | a1e3952 |

Dimensiones y relaciones arquitectónicas principales registradas por Claude:

- Biblioteca: vestíbulo 12 x 15 m con salida lateral de 1,10 m; recepción 6 x 8 m;
  vigilancia 5 x 7 m con apertura de 1,80 m; colección restringida 10 x 14 m; y
  sótano 45 x 35 m con techo de 3,5 m, conectado únicamente por la compuerta.
- Plaza: piso base 45 x 45 m; fuente de 20 m de diámetro y 0,5 m de profundidad,
  además de banca y farola en L.
- Generales: vestíbulo 14 x 12 m, soda 15 x 12 m, escalera en U que sube 4,5 m,
  set de mesa con cuatro sillas y aula 8 x 10 m del cuarto piso con puerta de
  1,20 m. El aula usa origen local porque los pisos 1-3 y el pasillo del piso 4
  todavía no tienen blockout.

Decisiones, descartes y límites que deben preservarse:

- `FUR-LIB-004` y `FUR-LIB-006`, sillas basadas en referencias fotográficas no
  deseadas, fueron descartadas y eliminadas. No recrearlas sin solicitud.
- Dos archivos de murales decorativos y una estantería con libros procedentes de
  una sesión anterior de Claude Code también fueron excluidos por el propietario;
  no se conservan la sesión ni los scripts para auditarlos.
- `ARC-EXT-002` conserva el centro vacío: se rechazaron cinco conceptos de
  escultura y el detalle queda para arte final.
- `ARC-GEN-004` es provisional porque aún no tiene zancas continuas.
- `ENV-EXT-001` tuvo dos intentos por script rechazados. Los archivos
  `Plaza/SM_Tree_PlazaCentral_A.blend` y `.py` permanecen sin seguimiento y son
  trabajo manual del propietario: no tocarlos ni reintentarlos por script.
- `FUR-GEN-003`, pupitre tipo tablet-arm, tuvo 13 intentos rechazados el
  2026-07-15. El propietario decidió modelarlo a mano; no reintentar sin pedido.
- No intentar por script la fachada `ARC-GEN-001` con el Árbol del Conocimiento
  sin confirmación expresa.
- Siguen planeados `FUR-GEN-002`, `PRP-GEN-001`, `FUR-GEN-004`, `PRP-GEN-002` y
  `VFX-LIB-001`.
- El commit de limpieza `23954c7` retiró activos descartados por decisión del
  propietario.

Documentación local asociada a la última sesión de Claude:

- `005f910`: registra `ARC-GEN-005`, el aula 8 x 10 m con puerta de 1,20 m.
- `7c44472`: registra los 13 intentos fallidos de `FUR-GEN-003` y la decisión de
  modelarlo manualmente.
- `6a270af`, aunque está entre los tres commits locales de docs, corresponde a la
  actualización autorizada del Player realizada por Codex, no a modelado Claude.

## Archivos creados por Codex

Antes del commit de transferencia, el rango `45dcfcb..a97762a` contenía 13 commits
documentados de Codex, 16 archivos afectados, 4008 inserciones y 5 eliminaciones.
La entrega del 2026-07-20 agrega un commit adicional para el handoff y los assets.

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

Assets binarios creados o modificados con el Unreal MCP oficial y gestionados
mediante Git LFS:

| Ruta | Configuración verificada | Tamaño observado |
|---|---|---:|
| UnrealProject/Content/Input/Actions/IA_Move.uasset | Axis2D; sin triggers ni modifiers | 1350 B |
| UnrealProject/Content/Input/Actions/IA_Look.uasset | Axis2D; sin triggers ni modifiers | 1350 B |
| UnrealProject/Content/Input/Actions/IA_Sprint.uasset | Boolean; sin triggers ni modifiers | 1164 B |
| UnrealProject/Content/Input/Actions/IA_Crouch.uasset | Boolean; sin triggers ni modifiers | 1164 B |
| UnrealProject/Content/Input/Actions/IA_Jump.uasset | Boolean; sin triggers ni modifiers | 1154 B |
| UnrealProject/Content/Input/Actions/IA_ToggleCamera.uasset | Boolean; sin triggers ni modifiers | 1194 B |
| UnrealProject/Content/Input/Mappings/IMC_Player.uasset | 16 mappings; conteo 5/2/2/3/2/2; sin triggers ni Dead Zone | 8569 B |
| UnrealProject/Content/Blueprints/Player/BP_PlayerController.uasset | Parent, 12 propiedades, Event Graph vacío, compilación y guardado verificados | 22564 B |
| UnrealProject/Content/Blueprints/Player/BP_PlayerCharacter.uasset | Parent, componentes y defaults de movimiento/cámaras auditados estáticamente; Event Graph vacío | 27020 B |
| UnrealProject/Content/Blueprints/Levels/BP_GameMode_DeveloperTesting.uasset | GameModeBase con Pawn/Controller verificados; Event Graph vacío | 22306 B |
| UnrealProject/Content/Maps/L_Developer_Testing.umap | GameMode, Player Start y layout compacto de 23 cubos auditados fuera de PIE | 60641 B |

`/Game/Blueprints/Player` contiene `BP_PlayerController` y
`BP_PlayerCharacter`; `/Game/Blueprints/Levels` contiene
`BP_GameMode_DeveloperTesting`. `BP_TestActor` no se movió ni modificó.
`L_Developer_Testing` conserva su ruta y fue modificado únicamente para la
configuración base y la geometría registradas en `EV-LVL-SETUP-01` y
`EV-GEO-LVL-01`.

## Archivo existente modificado por Codex

- UnrealProject/Source/ProyectoMemoria/ProyectoMemoria.Build.cs
  - Se agregó EnhancedInput como dependencia pública del módulo.
- UnrealProject/Config/DefaultEngine.ini
  - Se configuró `PMGameUserSettings` como clase persistente de ajustes.
- UnrealProject/Config/DefaultInput.ini
  - Se desactivó mouse smoothing y se fijó zona muerta 0 para los sticks.
- UnrealProject/Content/Maps/L_Developer_Testing.umap
  - Se asignó `BP_GameMode_DeveloperTesting_C` y se añadió un único Player Start
    definitivo, sin Pawn manual ni lógica de Level Blueprint.
  - Se creó el layout compacto de 23 cubos bajo `PlayerTests`, con geometría
    `BlockAll` y `Static`.

El 2026-07-16 se crearon únicamente los siete assets de Input. El 2026-07-22 se
completaron los mappings de `IMC_Player` y después, en sesiones separadas, se
crearon `BP_PlayerController`, `BP_PlayerCharacter` y
`BP_GameMode_DeveloperTesting`. El 2026-07-26 se configuró únicamente
`L_Developer_Testing`: GameMode Override y un Player Start, sin añadir lógica de
Level Blueprint. El 2026-07-27 se creó y validó únicamente su geometría compacta.
No se tocaron los repositorios excluidos. La única edición
autorizada de Codex fuera de Proyecto-Memory continúa siendo `6a270af` del
2026-07-13.

### Guía operativa del Editor

`EDITOR_SETUP_V0.1.md` conserva el procedimiento reproducible. Las secciones 3 y 4
ya se ejecutaron; la sección 5 está completa con los 16 mappings, la sección 6
con `BP_PlayerController`, la sección 7 con `BP_PlayerCharacter` y la sección 8
con `BP_GameMode_DeveloperTesting`. Las secciones 9 y 10 están completas y
revalidadas desde disco. La sección 11 también está completa mediante
`EV-PIE-START-01`. La sección 12 punto 2 también está completa mediante
`EV-MOV-WASD-01` y el punto 3 mediante `EV-MOV-DIAG-01`. La siguiente tarea es
el punto 4, `PLR-MOV-003`; el movimiento aprobado todavía no confirma el resto
de la integración jugable.

### Matriz y verificador QA

`QA_PLAYER_V0.1.md` conserva el entorno de ejecución, precondiciones, configuración
de assets, geometría, las 27 pruebas de la guía desglosadas, regresión, evidencias,
incidencias y trazabilidad de aceptación. Actualmente tiene 27 PASS: 23 de
configuración/geometría, dos de arranque PIE y dos de movimiento; los otros 57
resultados continúan `NOT RUN`.

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

## Unreal MCP y configuración local de Codex

Se usó únicamente el MCP oficial experimental incluido con Unreal Engine 5.8; no
se instaló un plugin de terceros y no se modificó `ProyectoMemoria.uproject` para
habilitarlo permanentemente.

Configuración global aplicada en esta PC, fuera del repositorio:

~~~toml
[mcp_servers.unreal-mcp]
url = "http://127.0.0.1:8000/mcp"

[mcp_servers.unreal-mcp.tools.call_tool]
approval_mode = "approve"
~~~

Comando equivalente:

~~~powershell
codex mcp add unreal-mcp --url http://127.0.0.1:8000/mcp
~~~

Unreal se lanzó para esa sesión con habilitación temporal:

~~~text
-EnablePlugins=ModelContextProtocol,EditorToolset
-ModelContextProtocolStartServer
~~~

Resultados verificados:

- servidor local escuchando solo en `127.0.0.1:8000`;
- protocolo MCP `2025-06-18` negociado correctamente;
- `EditorToolset` registró 19 toolsets descubribles;
- lectura del Output Log, inspección/creación de carpetas, creación/configuración
  de Data Assets y guardado funcionaron desde Codex;
- se habilitó `EditorToolset`, no `AllToolsets`, para reducir consumo;
- las llamadas a herramientas de Unreal deben ejecutarse en serie, nunca en
  paralelo, porque se despachan en el game thread;
- el warning de `LogModelContextProtocol` sobre Licensed Technology y el EULA de
  Unreal es una advertencia del plugin oficial, no un error del proyecto.

Resultado de la sesión del 2026-07-22 para `IMC_Player`:

- en Unreal 5.8 la propiedad vigente es `defaultKeyMappings.mappings`; no usar el
  `mappings` superior, obsoleto desde 5.7;
- `ObjectTools.set_properties` recibe `values` como un texto que contiene JSON;
- la prueba D → IA_Move fue aceptada y leída correctamente sin guardar;
- el intento de ampliar por MCP a W+D fue rechazado por ambigüedad al cambiar
  tamaño y elementos del array; la lectura inmediata confirmó que no hubo cambio
  parcial;
- se aplicó el fallback previsto: los 15 mappings restantes se configuraron
  manualmente en el Editor con capturas de verificación;
- MCP leyó antes de guardar exactamente 16 filas con conteo 5/2/2/3/2/2, triggers
  vacíos y modificadores solo en W, S y A; S conserva Negate seguido de Swizzle;
- `IMC_Player` se guardó, pasó AssetCheck y quedó en 8569 bytes, SHA-256
  `6F602EEA54C72BE64FE327DAC86CA7623509F281268BF33574509BAFA13B6C1A`.

Resultado de la sesión posterior del 2026-07-22 para `BP_PlayerController`:

- antes de crear se confirmó que el asset no existía y que la clase nativa exacta
  era `/Script/ProyectoMemoria.PMPlayerController`;
- se creó únicamente
  `/Game/Blueprints/Player/BP_PlayerController.BP_PlayerController`;
- MCP confirmó el parent exacto y leyó de vuelta las 12 propiedades requeridas:
  `playerMappingContext`, las seis referencias `*Action`, `lookSensitivityX`,
  `lookSensitivityY`, `bInvertLookY`, `mappingPriority` y
  `crouchHoldThreshold`;
- las referencias apuntan a `IMC_Player` y a `IA_Move`, `IA_Look`, `IA_Sprint`,
  `IA_Crouch`, `IA_Jump` e `IA_ToggleCamera`; los escalares quedaron 1.0, 1.0,
  false, 0 y 0.25 respectivamente;
- el Event Graph fue leído vacío; no se añadió lógica Blueprint;
- compiló dos veces con warnings-as-errors, se guardó solo su ruta explícita,
  `is_dirty` devolvió false y AssetCheck lo validó;
- el archivo resultante mide 22564 bytes y tiene SHA-256
  `A9C8D639135632B2FECE4E64922596B1F4146E17E627D2303DD832EC1A5597B1`;
- Unreal cerró mediante `QUIT_EDITOR`/`CloseEditor` y el log terminó en
  `LogExit: Exiting`; no se ejecutó PIE ni se recompiló C++.

Resultado de la sesión posterior del 2026-07-22 para `BP_PlayerCharacter`:

- preflight obtuvo 19/19 PASS sobre `4efac4c`; Unreal abrió con los plugins
  `ModelContextProtocol` y `EditorToolset` habilitados temporalmente, Map Check
  informó 0 errores y 0 advertencias y se registraron 19 toolsets;
- después de abrir, Unreal consumía aproximadamente 2,14 GB y quedaban
  aproximadamente 1,14 GB de RAM física libre. Edge y Claude permanecieron
  abiertos, Blender permaneció cerrado y todas las llamadas MCP fueron seriales;
- antes de crear se confirmó que el asset no existía;
- se creó únicamente
  `/Game/Blueprints/Player/BP_PlayerCharacter.BP_PlayerCharacter`, hijo exacto de
  `/Script/ProyectoMemoria.PMPlayerCharacter`;
- MCP confirmó ocho componentes heredados sin duplicados: cámaras 1P/3P, boom,
  Mesh, cápsula, Arrow, CharacterMovement y CameraModeComponent;
- leyó Walk/Sprint/Crouch 300/550/180, cápsula 42/96, Can Crouch true, rotación
  540, política de rotación del Character y todos los valores aprobados de cámaras
  y CameraMode;
- `ThirdPersonCamera` quedó unida a `ThirdPersonCameraBoom`; no se asignó malla ni
  se aplicó el Crouched Half Height provisional de 60 cm;
- el Event Graph fue leído vacío, compiló dos veces con warnings-as-errors, se
  guardó solo su ruta, `is_dirty` devolvió false y AssetCheck no registró errores;
- el archivo resultante mide 27020 bytes y tiene SHA-256
  `59555B01BB8D82222207D58D57A444227348D31D98EB2FAED6A8868D2BBA6838`;
- el asset y sus cuatro documentos locales se guardaron en el commit local
  `46b4f25`;
- Unreal cerró normalmente y el log terminó en `LogExit: Exiting`; no se ejecutó
  PIE, Hot Reload ni compilación C++;
- postflight sobre `46b4f25`, con worktree limpio, obtuvo 22/24 PASS. Los dos FAIL
  esperados fueron el GameMode ausente y 72 resultados QA todavía `NOT RUN`.

Resultado de la sesión del 2026-07-26 para `BP_GameMode_DeveloperTesting`:

- preflight obtuvo 19/19 PASS sobre `d96e173`; HWiNFO estaba activo, Blender
  cerrado, el cargador y la base conectados, con 41 °C actuales / 46 °C máximos;
- había aproximadamente 5,56 GB de RAM libre antes de abrir, 1,52 GB después del
  arranque y 5,9 GB tras cerrar; Unreal usó aproximadamente 1,9 GB al inicio y
  3,58 GB al terminar;
- Unreal abrió sin recompilar, Map Check informó 0 errores y 0 advertencias y el
  servidor MCP registró 19 toolsets;
- MCP confirmó que Character y Controller existían y que el GameMode no existía;
- se creó únicamente
  `/Game/Blueprints/Levels/BP_GameMode_DeveloperTesting.BP_GameMode_DeveloperTesting`
  con parent exacto `/Script/Engine.GameModeBase`;
- `defaultPawnClass` quedó en `BP_PlayerCharacter_C` y
  `playerControllerClass` en `BP_PlayerController_C`; se asignaron y releyeron una
  por una y volvieron a comprobarse después de compilar;
- el Event Graph fue leído vacío, compiló dos veces con warnings-as-errors, se
  guardó solo su ruta, `is_dirty` devolvió false y AssetCheck no registró errores;
- el archivo resultante mide 22306 bytes y tiene SHA-256
  `A50BD28E0873FF1A7D4CCA60F597ECFEAC667215014100B0E74C8FEC3E1BB7DC`;
- el asset y sus cuatro documentos locales se guardaron en el commit local
  `6707913`;
- Unreal cerró normalmente y el log terminó en `LogExit: Exiting`; no se tocó el
  mapa, no se ejecutó PIE, Hot Reload ni compilación C++;
- postflight sobre `6707913`, con worktree limpio, obtuvo 23/24 PASS. El único
  FAIL esperado son 70 resultados QA todavía `NOT RUN`.

Resultado de la sesión del 2026-07-26 para `L_Developer_Testing`:

- preflight obtuvo 19/19 PASS sobre `1629eac`; la base e HWiNFO estaban activos
  y se reportaron 37 °C actuales / 78 °C máximos durante la sesión;
- Unreal abrió sin recompilar y se cargó exactamente
  `/Game/Maps/L_Developer_Testing`;
- el mapa no tenía Player Start ni contenido jugable colocado;
- `defaultGameMode` quedó en
  `/Game/Blueprints/Levels/BP_GameMode_DeveloperTesting.BP_GameMode_DeveloperTesting_C`;
- se creó exactamente un `PlayerStart` en `(0,0,100)`, rotación cero y escala
  uno; MCP leyó su cápsula de referencia 40/92, confirmó cero Pawn manual y cero
  `LevelScriptActor`;
- se guardó únicamente el mapa y se recargó desde disco; conservó GameMode y
  Player Start, `is_dirty` devolvió false y Map Check informó 0 errores y 0
  advertencias;
- AssetCheck inició la validación sin registrar un diagnóstico asociado antes del
  cierre;
- el archivo resultante mide 11648 bytes y tiene SHA-256
  `08FECC04BD9B391F8C9CEB44CDBB784A95B3994703143C0B4225CF2BB2F822FD`;
- el mapa y sus cuatro documentos locales se guardaron en el commit
  `d4d6732`;
- Unreal cerró normalmente y el log terminó en `LogExit: Exiting`; no se creó
  geometría, no se ejecutó PIE, Hot Reload ni compilación C++;
- `LVL-01` continúa `NOT RUN`: después de crear el suelo debe repetirse la
  comprobación de `BADsize` y despeje usando la cápsula real 42/96. Si el suelo
  queda centrado en `Z=-10`, su superficie superior será `Z=0` y el Player Start
  provisional en `Z=100` dejará 4 cm bajo la cápsula real;
- postflight sobre `d4d6732`, con worktree limpio, obtuvo 23/24 PASS. El único
  FAIL esperado son las 70 filas QA todavía `NOT RUN`.

Resultado de la sesión del 2026-07-27 para la geometría:

- preflight obtuvo 19/19 PASS sobre `90ef65f`; HWiNFO estaba activo y se
  reportaron inicialmente 60 °C actuales / 67 °C máximos;
- se abrió únicamente `/Game/Maps/L_Developer_Testing`; no había geometría ni
  actores de trabajo ajeno y se conservó un solo Player Start;
- se creó primero `GEO01_Floor` con superficie superior en `Z=0`; se auditó como
  cubo oficial, `BlockAll`, `QueryAndPhysics`, `ECC_WorldStatic`, `Static` y sin
  física;
- el Player Start existente se reutilizó como `PlayerStart_PlayerV01` en
  `(-600,-500,100)`. La cápsula real 42/96 deja su base en `Z=4` y 83 cm libres
  a cada lado; tras guardar y recargar, Map Check dio 0/0 y no apareció
  `BADsize`;
- se crearon las otras 22 piezas. MCP verificó las 23 antes de guardar y otra
  vez después de recargar: nombres únicos, carpetas, transforms, bounds, cubo
  oficial, `Static` y `BlockAll` sin overrides;
- los conteos por carpeta son 1/2/3/3/3/10/1 más un Player Start. Las dimensiones
  interiores, los diez escalones apoyados en `Z=0` y el bloqueo Pawn/Camera de la
  pared coinciden con `EDITOR_SETUP_V0.1.md`;
- la lectura final confirmó GameMode correcto, un Player Start, cero Pawn manual,
  cero `LevelScriptActor`, mapa no sucio y Map Check 0/0;
- se guardó únicamente el mapa. Quedó en 60641 bytes con SHA-256
  `05791E0B54CA19C9BB862E264BD1E4B79BB614133D8C67D4B0C0F03F6DAD81B6`;
- Unreal cerró normalmente y el log terminó en `LogExit: Exiting`; no se ejecutó
  PIE, AssetCheck explícito, Hot Reload ni compilación C++. Los guardados
  iniciaron validación automática sin producir un resultado aprobatorio.
- el mapa y sus tres documentos locales quedaron en `83644f5`; postflight sobre
  ese commit obtuvo 24/25 PASS con worktree limpio. El único FAIL eran los 61 IDs
  QA que en ese momento continuaban `NOT RUN`.

Resultado de la primera sesión PIE del 2026-07-27:

- preflight obtuvo 19/19 PASS sobre `5e1993f`; la rama estaba 13 commits delante
  de origin y el worktree estaba limpio. La base de enfriamiento y HWiNFO estaban
  activos; se informaron 36 °C actuales y 68 °C máximos antes de continuar;
- se cargó `/Game/Maps/L_Developer_Testing` y se realizaron dos arranques PIE
  normales en `PlayMode_InViewPort`, no simulación. El mundo de juego fue
  `/Game/Maps/UEDPIE_0_L_Developer_Testing`;
- MCP confirmó exactamente un `BP_GameMode_DeveloperTesting_C`, un
  `BP_PlayerController_C` y un `BP_PlayerCharacter_C`. Character y Controller
  compartían el mismo `PlayerState`;
- el Controller contenía `EnhancedInputComponent`, `IMC_Player`, las seis Input
  Actions y prioridad 0. Una sonda controlada envió `W` durante 0.75 s al
  viewport: el Character pasó de X `-600` a `-384.060176`, con Y `-500` y Z
  `98.15` sin cambios. Esto demostró posesión y contexto activo, pero no ejecutó
  el caso completo `PLR-MOV-001`;
- `UnrealProject/Saved/Config/WindowsEditor/GameUserSettings.ini` contenía
  `PreferredCameraMode=FirstPerson`; en runtime `InitialMode` y `CurrentMode`
  fueron First Person, con FOV 90°;
- el Output Log registró ambos inicios y cierres PIE con `bSessionEnded=true`.
  No apareció ninguno de los seis diagnósticos prohibidos del Player. Sí quedaron
  avisos de introspección MCP, un warning genérico de
  `r.MotionVectorSimulation` y un error de sesión MCP vencida recuperado al
  reinicializar; no debe describirse el log completo como libre de warnings o
  errores;
- Unreal cerró normalmente con `LogExit: Exiting`. El log final mide 332942 bytes
  y tiene SHA-256
  `DE80BE804F6F173ED1B6F4C288A64402706ABD0D4182823EA85303CA8ABC777C`;
- antes de otra apertura se copió el log sin modificar a
  `UnrealProject/Saved/QA/PlayerV0.1/PIE-START-20260727/ProyectoMemoria.log`;
- no se modificó ni guardó ningún asset. `PLR-PIE-001` y `EVC-06` quedaron en
  PASS mediante `EV-PIE-START-01`; la matriz pasó a 25 PASS y 59 `NOT RUN`.
  Movimiento completo, look, sprint, crouch, salto, cámaras, espacios, mando,
  respawn, persistencia entre ejecuciones y rendimiento siguen sin probar.
- después del commit local `8def4bb`, postflight obtuvo 24/25 PASS con worktree
  limpio, assets LFS hidratados, Unreal cerrado y la copia preservada del log
  reconocida. El único FAIL esperado son los 59 IDs QA todavía `NOT RUN`.

Resultado de la sesión de movimiento cardinal del 2026-07-27:

- preflight obtuvo 19/19 PASS sobre `c2a61c3`, con worktree limpio, base de
  enfriamiento y HWiNFO activos;
- en PIE normal sobre `/Game/Maps/L_Developer_Testing` se activó
  `showdebug enhancedinput`. Las capturas válidas mostraron W `(0,+1)`,
  S `(0,-1)`, D `(+1,0)` y A `(-1,0)`, cada una por separado;
- con yaw inicial 0°, W cambió X de `-600` a `-434.034`, S devolvió X a
  `-599.998`, D cambió Y de `-500` a `-417.101` y A, en un PIE limpio, cambió Y
  de `-500` a `-582.899`. Después de soltar cada tecla, dos lecturas MCP
  separadas conservaron exactamente la posición; A además mostró
  `IA_Move=None` y `(0,0)` en la captura liberada;
- los intentos duplicados en que el viewport había perdido el foco se descartaron
  y no se usaron como evidencia;
- no apareció ninguno de los seis diagnósticos prohibidos. El log sí contiene
  avisos ajenos al Player sobre audio de un `Wireless Controller`,
  `r.MotionVectorSimulation` y una consulta MCP a una referencia PIE vencida. La
  presencia del dispositivo de audio no constituye una prueba funcional de mando;
- PIE terminó con `bSessionEnded=true`, Unreal cerró con `LogExit: Exiting` y no
  se modificó ningún asset. La copia preservada está bajo
  `UnrealProject/Saved/QA/PlayerV0.1/MOV-20260727/ProyectoMemoria.log`, mide
  349092 bytes y tiene SHA-256
  `4D5DB3E6A42AE27237F05E9723EBBE5201B2FBE38536292AA4B2818F489106D4`;
- `PLR-MOV-001` quedó en PASS mediante `EV-MOV-WASD-01`. La matriz pasó a 26 PASS
  y 58 `NOT RUN`; la siguiente prueba es `PLR-MOV-002`.
- después del commit local `9e46365`, postflight obtuvo 24/25 PASS con worktree
  limpio, Unreal cerrado, estructura de 84 IDs válida y Output Log reconocido.
  El único FAIL esperado son los 58 IDs QA todavía `NOT RUN`.

Resultado de la sesión de movimiento diagonal del 2026-07-27:

- preflight obtuvo 19/19 PASS sobre `352f629`, con worktree limpio, base de
  enfriamiento y HWiNFO activos;
- cada combinación válida inició en un `startTransform` PIE temporal
  `(500,0,100)`, yaw 0°, dentro de una zona abierta del mismo mapa. No se guardó
  ni modificó el mapa;
- `showdebug enhancedinput` mostró W+A `(-1,+1)`, W+D `(+1,+1)`,
  S+A `(-1,-1)` y S+D `(+1,-1)`. Dos capturas temporizadas por combinación
  derivaron 299.65, 299.83, 300.19 y 299.83 cm/s a partir de valores visibles
  redondeados; runtime confirmó `MaxWalkSpeed=300`;
- las cuatro capturas liberadas mostraron `IA_Move=None` y `(0,0)`. Para cada
  diagonal, dos lecturas MCP posteriores conservaron exactamente la posición;
- los intentos donde HWiNFO interceptó el foco o la pared del pasillo bloqueó un
  eje se descartaron. HWiNFO siguió monitoreando y su ventana se restauró al
  cerrar Unreal;
- no apareció ninguno de los seis diagnósticos prohibidos ni errores
  Blueprint/runtime del Player. El log conserva avisos internos del motor,
  audio, layout, render, MCP/HTTP y una sonda de propiedades no legibles;
- PIE terminó con `bSessionEnded=true`, Unreal cerró con `LogExit: Exiting` y no
  cambió ningún asset. La copia preservada está en
  `UnrealProject/Saved/QA/PlayerV0.1/DIAG-20260727/ProyectoMemoria.log`, mide
  358642 bytes y tiene SHA-256
  `16D19EB3BCB8393D8E4893EA9A9AA90398F87CB0577AE17D68988483B5338324`;
- `PLR-MOV-002` quedó en PASS mediante `EV-MOV-DIAG-01`. La matriz pasó a 27 PASS
  y 57 `NOT RUN`; la siguiente prueba es `PLR-MOV-003`.
- después del commit local `39352d1`, postflight obtuvo 24/25 PASS con worktree
  limpio, Unreal cerrado, estructura de 84 IDs válida y Output Log reconocido.
  El único FAIL esperado son los 57 IDs QA todavía `NOT RUN`.

Referencia operativa conservada de las sesiones de Blueprints:

- `BlueprintTools` expone `create`, `compile_blueprint` y `get_parent`;
  `ObjectTools` expone `search_subclasses`, `list_properties`, `get_properties` y
  `set_properties`; `AssetTools` expone `exists`, `load_asset`, `save_assets` e
  `is_dirty`;
- antes de crear un Blueprint, usar `exists`; intentar crear un duplicado puede
  fallar y abrir un diálogo modal;
- padres nativos exactos: `/Script/ProyectoMemoria.PMPlayerController`,
  `/Script/ProyectoMemoria.PMPlayerCharacter` y `/Script/Engine.GameModeBase`;
- crear, compilar con warnings-as-errors, comprobar el padre y modificar valores
  en grupos pequeños con lectura de vuelta. `set_properties` puede aplicar una
  parte antes de devolver error;
- en `BP_PlayerController` ya se demostró que el orden seguro es probar primero
  los escalares, después una referencia y finalmente las seis Input Actions; no
  repetir esa configuración si el hash y la lectura del asset coinciden;
- el formato canónico aceptado fue
  `InputMappingContext'/Game/Input/Mappings/IMC_Player.IMC_Player'` para el
  contexto y `InputAction'/Game/Input/Actions/IA_Move.IA_Move'` para cada acción,
  cambiando el nombre;
- `BP_PlayerCharacter` debe heredar los componentes y valores que ya fija el
  constructor C++; no reescribir subobjetos por MCP ni fijar todavía el valor
  provisional de Crouched Half Height;
- para GameMode, las clases generadas esperadas terminan en
  `BP_PlayerCharacter_C` y `BP_PlayerController_C`; asignarlas de una en una y
  releer cada propiedad. Usar el formato canónico
  `BlueprintGeneratedClass'/Game/.../BP_Name.BP_Name_C'`;
- guardar rutas explícitas. Una lista vacía en `save_assets` guarda todos los
  paquetes sucios y no debe usarse. Mantener los Event Graphs vacíos.

Esta configuración global no viaja con Git ni con la conversación. En otra PC se
debe repetir el alta del servidor, reiniciar Codex, lanzar Unreal con los flags y
verificar el puerto. El 2026-07-20 también se agregó globalmente
`openaiDeveloperDocs` con URL `https://developers.openai.com/mcp`; tampoco forma
parte del repositorio. Fue agregado correctamente, pero esta sesión todavía no lo
descubrió porque Codex requiere reinicio; no se ha probado después de reiniciar.
La configuración global ya contenía Blender MCP, pero la línea de trabajo de
Codex no debe usarlo ni tocar Modelos-3D.

## Hardware, memoria y límite térmico de la laptop actual

Equipo inspeccionado:

- Lenovo IdeaPad 5 2-in-1 16AHP9, modelo de sistema 83DS.
- AMD Ryzen 7 8845HS, 8 núcleos / 16 hilos.
- Radeon 780M integrada.
- 16 GB LPDDR5-6400 soldados; alrededor de 13,77 GB utilizables por Windows.
- HWiNFO 64 portable v8.50-6020 utilizado en modo Sensors-only; consumo observado
  cercano a 90 MB. AMD Adrenalin solo mostraba temperatura GPU, no CPU.

Preparación realizada antes de Unreal:

- se cerraron Edge, Widgets, Phone Link, Settings, la interfaz de AMD y Card
  Middleware; cerrar Card Middleware no eliminó datos y puede abrirse cuando haga
  falta;
- no se deshabilitaron servicios esenciales ni se instaló un monitor residente;
- durante la sesión sin cargador se observaron 48 % de batería, aproximadamente
  3,7 GB de RAM libre en una comprobación y cerca de 2,54 GB libres con Unreal en
  ejecución.

Registro térmico observado:

| Momento | Temperatura CPU |
|---|---:|
| Reposo inicial | aproximadamente 35 °C |
| Compilación completa | máximo 68,1 °C |
| Primera apertura controlada del Editor | máximo 52,1 °C |
| Trabajo posterior con Unreal MCP/Input | 66 °C actual y máximo 99,2 °C |
| Después de cerrar Unreal y enfriar | 44 °C |
| Sesión con base, inicio | 40 °C actual y 52 °C máxima |
| Sesión con base, máximo reportado | 70 °C |
| Sesión con base, antes de cerrar | 50 °C actual y 66 °C máxima |
| Sesión de Controller tras reiniciar máximo | 37 °C actual y 38 °C máxima |
| Controller con Editor abierto | 49 °C actual y 69 °C máxima |
| Controller antes de cerrar | 30 °C actual y 69 °C máxima |
| Character antes de abrir, máximo acumulado sin reiniciar | 41,6 °C actual y 86 °C máxima |
| GameMode antes de abrir, con cargador y base | 41 °C actual y 46 °C máxima |
| Mapa con base e HWiNFO activos | 37 °C actual y 78 °C máxima |
| Geometría con base e HWiNFO activos | 60 °C actual y 67 °C máxima |
| Primera sesión PIE, antes de continuar | 36 °C actual y 68 °C máxima |

En la primera apertura, los siete assets se guardaron mediante MCP antes de
cerrar. El cierre requirió solicitudes repetidas, pero el log final registra
`QUIT_EDITOR`, `CloseEditor` y una secuencia ordenada de apagado del Editor;
después se confirmó que Unreal ya no estaba ejecutándose. Esa primera apertura no
tuvo postflight.

Regla vigente para esta laptop: no reabrir Unreal sin la base encendida y
condiciones seguras confirmadas. Pausar y cerrar si la temperatura actual llega a
90 °C; detener de inmediato si alcanza 95 °C, hay olor extraño, congelamiento,
stutter severo o apagado. El propietario confirmó que ya tiene una base de
enfriamiento; su modelo no fue reconfirmado y se usó con éxito el 2026-07-22.

La sesión de mappings se completó el 2026-07-22 con base encendida, HWiNFO en modo
Sensors-only y sin recompilar ni ejecutar PIE. RAM libre observada: 4,38 GB antes
de abrir, 1,82 GB después de la apertura, mínimo puntual de 1,59 GB y 3,54 GB al
terminar. Unreal cerró ordenadamente y el log registra `QUIT_EDITOR`,
`CloseEditor` y `LogExit: Exiting`.

Postflight de la sesión de mappings: el log fue reconocido y no contiene
diagnósticos propios prohibidos; el control terminó FAIL únicamente porque en ese
momento faltaban los tres Blueprints requeridos y la matriz completa conservaba
pruebas `NOT RUN`. No fue un fallo de guardado de `IMC_Player`.

La sesión posterior de `BP_PlayerController` mantuvo Edge abierto por decisión del
propietario. Se observaron aproximadamente 5,7 GB de RAM libre antes de abrir,
2,05 GB con Unreal abierto y 5,79 GB después del cierre. El preflight obtuvo 19/19
PASS. Unreal consumía aproximadamente 1,69 GB al terminar la configuración y
respondía normalmente. El cierre fue ordenado. Después del commit local `81fa688`,
el postflight obtuvo 22/24 PASS con worktree limpio: en ese momento faltaban los
dos assets `BP_PlayerCharacter`/`BP_GameMode_DeveloperTesting` y 76 filas QA
seguían sin ejecutarse. El Output Log no contiene diagnósticos propios prohibidos.

La sesión posterior de `BP_PlayerCharacter` también mantuvo Edge y Claude abiertos,
pero dejó Blender cerrado. Se observaron aproximadamente 1,14 GB de RAM física
libre con Unreal abierto y unos 2,14 GB usados por el Editor. La base permaneció
encendida y todas las llamadas MCP se ejecutaron en serie. Después del commit local
`46b4f25`, el postflight obtuvo 22/24 PASS con worktree limpio: en ese momento
faltaba `BP_GameMode_DeveloperTesting` como asset y 72 filas QA seguían sin
ejecutarse.

La sesión de `BP_GameMode_DeveloperTesting` del 2026-07-26 empezó con 5,56 GB de
RAM libre, bajó a 1,52 GB después del arranque y terminó con 5,9 GB después del
cierre. Unreal alcanzó aproximadamente 3,58 GB. El cargador y la base estaban
conectados, HWiNFO activo y Blender cerrado. El postflight obtuvo 23/24 PASS; el
único FAIL son 70 filas QA pendientes.

## Transferencia segura a otra PC

No depender únicamente de que esta conversación aparezca en el otro equipo. La
otra sesión debe recibir este handoff y los archivos locales reales.

Opciones seguras, con Unreal cerrado:

1. Copiar la carpeta completa `C:\Users\jeffa\Desktop\Proyecto` mediante una
   unidad externa o red local, conservando las carpetas `.git`; o
2. usar el commit y la rama remota publicados el 2026-07-20. Esta fue la opción
   autorizada y ejecutada para la transferencia inicial. Los commits locales
   posteriores todavía requieren un push expresamente autorizado antes de poder
   recuperarse con `pull` en otra PC.

En el equipo destino se debe instalar Git LFS antes de hidratar los binarios y
usar el HEAD más reciente de `origin/feature/v0.1-player-cameras`. En el estado
actual, origin termina en `336aa91` y todavía no contiene `8e0aaba`, `d569e31` ni
`81fa688`; un `pull` por sí solo no transfiere aún esas partes.
`Blueprints/Player` existe localmente gracias al Controller.
`Blueprints/Levels` debe recrearse si continúa vacío en una clonación.

SHA-256 de los assets para comprobar una copia directa:

~~~text
IA_Crouch.uasset       CF45D82FA8ADFA12DD62E0630807C8FF954B79077E028D62C3C7F304788D35F4
IA_Jump.uasset         D42596F590C5071BC57B6515F517172BE7B71A0BE8A54A945147E4088A59D46E
IA_Look.uasset         E93A45E67A2228BC71F59E752799CFBE92E3AE3689FD0DABCD5FA53BEC2074E0
IA_Move.uasset         04096D4C59781FAF5132CFE25B1B1871C871B92CFF095674D6E306D713C9E9AE
IA_Sprint.uasset       917FC61CCBA1A1437DB4FFA511F22B3731A440A38FC1EC264A73EB7C9806B9B1
IA_ToggleCamera.uasset C564D0CE3A39881067D049E34A9E18E3DC690C11FAA64A52951E933C3ACE490E
IMC_Player.uasset      6F602EEA54C72BE64FE327DAC86CA7623509F281268BF33574509BAFA13B6C1A
BP_PlayerController.uasset A9C8D639135632B2FECE4E64922596B1F4146E17E627D2303DD832EC1A5597B1
~~~

Después de copiar, abrir Codex en la raíz `Proyecto`, pegar el prompt de
reanudación de este documento y dejar que lea primero los archivos indicados. La
configuración MCP global debe repetirse en el equipo nuevo; no copiar directorios
internos de sesiones de Codex como sustituto de este handoff.

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
   source local de UE 5.8 antes de compilar.
9. El 2026-07-16 se ejecutó una compilación Development Editor completa del HEAD
   vigente: UHT, cinco fuentes C++ y enlace de DLL/lib terminaron en `Succeeded`
   en aproximadamente 68 segundos.
10. Después del build se abrió el Editor 5.8, se cargó el proyecto y se verificó
    el Map Check antes de la integración parcial de Input.

Comando final:

    Build.bat ProyectoMemoriaEditor Win64 Development
      -Project=<ruta>/ProyectoMemoria.uproject
      -WaitMutex -NoHotReloadFromIDE -MaxParallelActions=1

Resultado vigente: `Succeeded`. La compilación sí cubre `20e8fd2`,
`UPMGameUserSettings`, IA_Jump, la restauración de cámara y el HEAD `a97762a`.
`UnrealEditor-ProyectoMemoria.dll` quedó con fecha 2026-07-16 22:17:04 local.

Avisos externos observados:

- Visual Studio MSVC 14.51 es más nuevo que la versión preferida 14.50 de UE 5.8.
- Character.h de UE 5.8 emite C4996 por APawn::GetMovementBase. La advertencia
  procede del motor, no de llamadas escritas en este cambio.

## Pruebas ejecutadas

- Compilación Development Editor completa para Win64 con Unreal Engine 5.8 del
  estado vigente: UHT + cinco fuentes + enlace DLL/lib, exitosa en ~68 s.
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
- Preflight histórico sin confirmación humana del hardware: 0 FAIL y 1 WARN
  esperado; Unreal permaneció cerrado.
- Preflight con hardware confirmado inmediatamente antes del build completo:
  19/19 PASS, 0 FAIL y 0 WARN.
- El mismo preflight se repitió después del build: 19/19 PASS, 0 FAIL y 0 WARN.
- Unreal Editor 5.8 inicializó el proyecto; Enhanced Input quedó montado y las
  clases predeterminadas `EnhancedPlayerInput` y `EnhancedInputComponent` fueron
  confirmadas.
- Map Check de la sesión: 0 errores y 0 advertencias.
- El servidor Unreal MCP oficial inició, Codex negoció la conexión y se verificó
  la configuración de las seis Input Actions. Los siete assets se guardaron y
  Content Validation no registró errores de esos assets.
- En una segunda sesión corta, MCP creó y auditó `BP_PlayerController`: parent
  exacto, 12 propiedades, Event Graph vacío, dos compilaciones con
  warnings-as-errors, guardado explícito, AssetCheck y estado no sucio.
- En una tercera sesión corta, MCP creó y auditó `BP_PlayerCharacter`: parent
  exacto, ocho componentes, valores heredados, Event Graph vacío, dos
  compilaciones con warnings-as-errors, guardado explícito, AssetCheck y estado no
  sucio.
- En una cuarta sesión corta, MCP creó y auditó
  `BP_GameMode_DeveloperTesting`: parent exacto, Pawn/Controller correctos, Event
  Graph vacío, dos compilaciones con warnings-as-errors, guardado explícito,
  AssetCheck y estado no sucio.
- En una quinta sesión corta, MCP configuró `L_Developer_Testing`: GameMode
  Override, un único Player Start, cero Pawn manual y cero `LevelScriptActor`;
  guardó y recargó el mapa, que pasó Map Check 0/0 y quedó no sucio. Esta evidencia
  fue parcial hasta la sesión de geometría.
- En una sexta sesión, MCP creó y auditó la pista compacta de 23 cubos, revalidó
  el Player Start y volvió a comprobar todo después de guardar y recargar.
- En una séptima sesión se realizaron dos arranques PIE normales. MCP confirmó un
  GameMode, Controller y Character correctos; una sonda `W` movió el Character
  215.939824 cm y demostró posesión más `IMC_Player` activo. La preferencia y el
  modo runtime coincidieron en First Person y no apareció ninguno de los seis
  diagnósticos prohibidos.
- En una octava sesión se probó W/A/S/D por separado con
  `showdebug enhancedinput`. Los cuatro vectores, las direcciones del Character y
  la detención al soltar coincidieron con la configuración; `PLR-MOV-001` pasó.
- En una novena sesión se probaron W+A, W+D, S+A y S+D con
  `showdebug enhancedinput` desde una zona abierta. Las cuatro combinaciones
  produjeron el vector esperado, quedaron alrededor de 300 cm/s sin la ventaja
  diagonal de aproximadamente 424 cm/s y se detuvieron al soltar;
  `PLR-MOV-002` pasó.
- Postflight de la sesión diagonal sobre `39352d1`: 24/25 PASS, con worktree
  limpio, Output Log preservado y Unreal cerrado. El único FAIL esperado son los
  57 IDs QA todavía `NOT RUN`.
- Postflight de la sesión de movimiento sobre `9e46365`: 24/25 PASS, con
  worktree limpio, Output Log preservado y Unreal cerrado. El único FAIL esperado
  son los 58 IDs QA todavía `NOT RUN`.
- Postflight de la primera sesión PIE sobre `8def4bb`: 24/25 PASS, con worktree
  limpio, Output Log preservado y Unreal cerrado. El único FAIL esperado son los
  59 IDs QA todavía `NOT RUN`.
- Postflight de la sesión de geometría sobre `83644f5`: 24/25 PASS, con worktree
  limpio, objetos LFS hidratados, Output Log válido y Unreal cerrado. El único
  FAIL eran los 61 IDs QA pendientes en ese momento.
- Postflight de la sesión del mapa sobre `d4d6732`: 23/24 PASS, con worktree
  limpio, objetos LFS hidratados, Output Log válido y Unreal cerrado. El único
  FAIL son las mismas 70 filas QA pendientes.
- Postflight de la sesión del GameMode: 23/24 PASS, sin procesos Unreal y Output
  Log válido sin diagnósticos propios prohibidos. El único FAIL son 70 resultados
  QA pendientes.
- No se ejecutaron todavía look, velocidad recta, sprint, crouch, salto, cambio
  de cámara, espacios, mando, respawn, persistencia entre ejecuciones ni
  rendimiento. La matriz tiene 28 PASS y 56 IDs que continúan `NOT RUN`.
- El arranque contiene mensajes internos `LogAutomationTest: Error: Condition
  failed` del motor. Ya se identificaron como pruebas internas de UE, pero por ello
  no debe describirse el Output Log completo como “sin ningún error”.
- Casos negativos del verificador: worktree sucio, commit mínimo inválido, assets
  ausentes, filas NOT RUN y diagnósticos prohibidos producen FAIL y exit 1 sin
  abortar la salida estructurada.
- git diff --check: sin errores de whitespace; Git puede avisar la política local
  futura LF a CRLF en documentos de texto modificados.
- Auditoría de alcance: el C++ y sus documentos permanecen dentro de
  Proyecto-Memory. La única edición autorizada fuera fue el checklist del commit
  6a270af. Los dos archivos de árbol sin seguimiento en Modelos-3D pertenecen al
  propietario y se preservaron sin modificación.

Los artefactos de build y logs quedaron en carpetas ignoradas por Git:
Binaries, Intermediate y Saved.

## Integración pendiente en Unreal Editor

El C++ vigente compila y el setup —Input, Blueprints, mapa y geometría— está
completo. El arranque funcional inicial ya fue validado en PIE, pero el resto del
comportamiento jugable continúa pendiente. Estado y orden restante:

1. Verificar que la transferencia conserva los siete `.uasset`, Git LFS, rama y
   HEAD. No borrar los assets por aparecer sin seguimiento.
2. **Completado; no repetir.** Conservar `IMC_Player` según la sección 5 de
   `EDITOR_SETUP_V0.1.md`:
   - Move: W con Swizzle YXZ; S con Negate y luego Swizzle YXZ; A con Negate; D sin
     modificador; Gamepad Left Thumbstick 2D-Axis.
   - Look: Mouse XY 2D-Axis y Gamepad Right Thumbstick 2D-Axis.
   - Sprint: Left Shift y Gamepad Left Thumbstick Button.
   - Crouch: C, Left Control y Gamepad Face Button Right.
   - Jump: Space Bar y Gamepad Face Button Bottom.
   - ToggleCamera: V y Gamepad Face Button Top.
   Estos 16 mappings están guardados y verificados. No añadir Dead Zone; la
   decisión aprobada es zona muerta 0 para QA.
3. **Completado; no repetir.** IA_Crouch es Digital, sin Hold, Tap, Pressed,
   Released ni Pulse, porque C++ mide la duración; el umbral del Controller quedó
   en 0,25 s.
4. **Completado; no repetir.** `BP_PlayerController` es hijo de
   APMPlayerController, referencia `IMC_Player` y las seis IA, compila, está
   guardado y no contiene lógica en Event Graph.
5. **Completado; no repetir.** `BP_PlayerCharacter` es hijo de
   APMPlayerCharacter, conserva componentes, cápsula, movimiento y cámaras
   heredados, compila, está guardado y no contiene lógica en Event Graph. Mesh
   continúa vacío y el valor de 60 cm no fue aplicado.
6. **Completado; no repetir.** `BP_GameMode_DeveloperTesting` hereda de
   GameModeBase, usa `BP_PlayerCharacter_C` y `BP_PlayerController_C`, compila,
   está guardado y no contiene lógica en Event Graph.
7. **Completado; no repetir.** `L_Developer_Testing` usa
   `BP_GameMode_DeveloperTesting_C`, contiene un único Player Start definitivo y
   no contiene Pawn manual ni lógica de Level Blueprint. `LVL-01` está en PASS.
8. **Completado; no repetir.** El layout compacto de 23 cubos de la sección 10
   está guardado y validado; `GEO-01..07` y `EVC-05` están en PASS.
9. **Completado; no repetir.** La sección 11 y `PLR-PIE-001` confirmaron spawn,
   posesión, `IMC_Player`, perspectiva inicial y ausencia de los seis mensajes
   prohibidos.
10. **Completado; no repetir.** `PLR-MOV-001`, sección 12 punto 2: W, A, S y D
    por separado produjeron los vectores configurados y se detuvieron al soltar.
11. **Completado; no repetir.** `PLR-MOV-002`, sección 12 punto 3: las cuatro
    diagonales produjeron los vectores esperados, no mostraron ventaja diagonal
    de velocidad y se detuvieron al soltar.
12. **Siguiente tarea.** Ejecutar `PLR-MOV-003`, sección 12 punto 4: probar look
    horizontal y vertical con el ratón, incluido detenerlo y confirmar que no
    queda movimiento.
13. Verificar por separado toque corto, segundo toque, mantener/soltar y cancelación
    de IA_Crouch.
    En manual, comparar un toque claramente corto con una pulsación de al menos
    0,5 s. Los límites 0,24/0,25/0,26 s requieren instrumentación o automatización;
    no deben validarse por estimación humana. Repetir a 30, 60 y 120 FPS cuando el
    hardware lo permita.
14. Validar en PIE pasillo 2,50 m, puerta 1,20 m, escaleras y habitación pequeña.
15. Probar salto normal/bajo techo, 1P/3P, respawn, persistencia entre ejecuciones,
    paredes, sensibilidad, inversión y objetivo de 60 FPS.

## Decisiones y deudas abiertas de v0.1.0

- Enhanced Input aparece aún como decisión pendiente en el control maestro, aunque
  la decisión local aprobada y la implementación ya lo adoptan.
- El delta `20e8fd2` está compilado, pero no tiene pruebas funcionales PIE.
- Las seis Input Actions están publicadas. `IMC_Player` tiene sus 16 mappings en
  el commit local `d569e31`; `BP_PlayerController` forma parte de esta entrega.
  Ambos avances posteriores a `336aa91` siguen pendientes de push mediante Git
  LFS.
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

Esta lista refleja únicamente lo registrado por ese commit. El trabajo posterior
del Player del 2026-07-15 y 2026-07-16 no se aplicó a
Proyecto-Memoria-docs porque no hubo una nueva autorización para editar sus
secciones del Player. Claude sí actualizó por separado las secciones de modelos en
005f910 y 7c44472.

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

- Malla visual. El mapa de prueba, las Input Actions y los mappings de
  `IMC_Player` ya están preparados; Character y GameMode ya están creados y
  auditados.
- Teclado, ratón y mando configurados en assets. Una sonda `W` ya confirmó el
  contexto en PIE, pero faltan las pruebas completas de teclado/ratón y no se ha
  probado un mando físico.
- Verificación completa de movimiento y cámaras en PIE.
- Pruebas dimensionales, colisión, escaleras, atasco y 60 FPS.
- IA_Jump ya existe; siguen pendientes las pruebas de salto normal, desde crouch
  y bajo techo.
- Persistencia de perspectiva: C++ compilado, pendiente de respawn y prueba entre
  ejecuciones.
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
revisión técnica estática y compilación completa, pero PMGameUserSettings y el
nuevo flujo de salto aún no han recibido una revisión pedagógica completa con el
propietario.

## Sesión más reciente: PLR-MOV-003 (2026-07-28)

Se ejecutó PIE normal en `/Game/Maps/L_Developer_Testing` con la base de enfriamiento y HWiNFO activos. El propietario realizó un movimiento físico pequeño del mouse hacia arriba. `PlayerCameraManager_0` pasó de pitch/yaw `0/0` a pitch `-43.2250006°` y yaw `0°`; una lectura posterior a 1.2 s fue idéntica. Esto aprueba `PLR-MOV-003` mediante `EV-MOV-LOOK-01` y deja 28 PASS / 56 NOT RUN. El log final se preservó en `UnrealProject/Saved/QA/PlayerV0.1/LOOK-20260728/ProyectoMemoria.log` (304299 bytes, SHA-256 `B02C3D092FB4B995FBECF74FC99E21A85C14D031587D7A7C62D6673F12C7A5D4`). Unreal está cerrado y no se modificaron assets. La siguiente tarea es `PLR-MOV-004`, medir velocidad de avance.