# Créditos y licencias — Proyecto Memoria

Este archivo es el inventario de distribución de la primera versión. No se
declara una licencia que el propietario no haya confirmado; los elementos sin
confirmación quedan explícitamente marcados para revisión antes de publicar.

## Código del proyecto

- Proyecto Memoria: código original del propietario del proyecto.
- Rama de trabajo: `feature/v0.1-player-cameras`.
- Licencia de distribución: **pendiente de decisión del propietario**.

## Motor y runtime

- Unreal Engine 5.8 — Epic Games. La distribución debe cumplir el acuerdo de
  licencia de Unreal Engine aplicable a la cuenta y plataforma del propietario.
- Enhanced Input — plugin oficial incluido con Unreal Engine; no se añadió un
  plugin externo obligatorio al runtime.

## Personaje y animaciones

- Mannequin estándar de Unreal Engine 5.8 y sus animaciones de agachado:
  `UnrealProject/Content/Mannequin/`.
- Origen: contenido incluido con Unreal Engine.
- Licencia/condiciones de redistribución: verificar contra la licencia vigente
  de Unreal antes de publicar fuera del entorno del propietario.

## Assets externos

- `Modelos-3D/`: inventario externo del propietario. Se conserva sin cambios y
  no se incorpora a esta build hasta que cada asset tenga origen, licencia,
  autor y permiso de redistribución registrados.
- Música, fuentes, efectos de sonido y plugins externos: no identificados en
  el runtime actual; deben permanecer vacíos o registrarse aquí antes de añadir
  contenido.

## Revisión antes de publicar

- [ ] Confirmar titularidad/licencia del código del proyecto.
- [ ] Confirmar condiciones de redistribución del Mannequin de Unreal.
- [ ] Auditar cada asset que se vaya a copiar desde `Modelos-3D/`.
- [ ] Añadir autores, URLs, versiones y textos de atribución de terceros.
- [ ] Revisar avisos legales y requisitos de la plataforma de distribución.

La build Shipping generada mientras estos puntos estén pendientes es solo para
pruebas privadas y no constituye una publicación comercial.
