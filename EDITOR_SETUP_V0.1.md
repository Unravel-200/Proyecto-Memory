# Configuración de Unreal Editor — v0.1.0

## Propósito

Esta guía describe cómo integrar en Unreal Editor 5.8 el código C++ de personaje,
movimiento y cámaras de Proyecto-Memory. El código vigente, incluido el salto y la
persistencia de perspectiva, fue compilado correctamente y revisado
estáticamente. Su comportamiento todavía no ha sido probado en PIE.

Estado de partida verificado:

- Rama de código: feature/v0.1-player-cameras.
- Commit base mínimo verificado: 336aa91; se admite un descendiente limpio.
- Unreal Engine: 5.8.
- Plataforma compilada: Win64 Development Editor.
- Resultado C++ vigente más reciente: Succeeded.
- Salto, `UPMGameUserSettings` y restauración de cámara: compilados; pruebas
  funcionales pendientes.
- Assets existentes: BP_TestActor y L_Developer_Testing.
- Assets de Input: existen las seis Input Actions y `IMC_Player`; este último
  todavía no tiene mappings.
- Assets de Player: todavía no existen.

### Sesión corta preparada para el 2026-07-23

La base de enfriamiento ya está disponible, pero no puede usarse el 2026-07-22;
por eso hoy no se abre Unreal. La primera apertura de mañana se limita a:

1. Encender la base, conectar el cargador si está disponible y abrir HWiNFO en
   modo Sensors-only.
2. Reiniciar los valores mínimo/máximo y anotar la temperatura inicial.
3. Abrir Unreal sin recompilar y completar solamente la sección 5,
   `IMC_Player`.
4. Guardar y validar los assets, anotar la temperatura máxima y cerrar Unreal.

No ejecutar PIE ni continuar a Blueprints en esa misma apertura. Pausar y cerrar
si la temperatura actual llega a 90 °C; detener de inmediato si alcanza 95 °C,
hay olor extraño, congelamiento, stutter severo o apagado.

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

El MCP oficial de Unreal 5.8 puede automatizar esta sección, pero su conversión
completa de `UInputMappingContext` no se ha probado todavía de extremo a extremo.
Usar llamadas en serie y aplicar este control antes de guardar:

1. Leer `defaultKeyMappings` y confirmar que `mappings` está vacío. No escribir en
   la propiedad superior `mappings`, porque está obsoleta desde Unreal 5.7.
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

Usar Shapes > Cube para evitar importar assets. El cubo básico mide 100 cm por
lado; su escala es dimensión deseada / 100.

En World Outliner crear la carpeta PlayerTests.

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

1. Spawn y posesión.
2. Movimiento W/A/S/D.
3. Movimiento diagonal.
4. Look con ratón.
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
