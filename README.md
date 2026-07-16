# Automatización de incidencias TICS

Aplicación de consola desarrollada en Python para registrar, consultar,
actualizar y analizar incidencias tecnológicas reportadas por las diferentes
áreas de un GAD Municipal.

## Problemática

Actualmente, las incidencias tecnológicas de las diferentes áreas municipales
son reportadas principalmente mediante WhatsApp. Esto ocasiona que la
información quede dispersa en distintas conversaciones y no exista un registro
centralizado para realizar seguimiento de las solicitudes.

Como consecuencia, resulta difícil conocer cuántas incidencias fueron
reportadas, cuáles están pendientes, cuáles están siendo atendidas y qué áreas
presentan una mayor cantidad de requerimientos. Tampoco se dispone de
indicadores confiables para evaluar la atención brindada por el área de TICS.

## Solución propuesta

Desarrollar una aplicación de consola en Python que permita registrar y
gestionar incidencias tecnológicas, almacenar la información localmente en un
archivo JSON y generar indicadores automáticos de atención.

## Objetivo general

Desarrollar una aplicación en Python que permita registrar, consultar,
actualizar y analizar incidencias tecnológicas, con la finalidad de mejorar
su seguimiento y generar indicadores para apoyar la toma de decisiones.

## Funcionalidades

La aplicación permitirá:

1. Registrar una incidencia.
2. Listar todas las incidencias.
3. Buscar una incidencia por código.
4. Cambiar una incidencia a estado En proceso.
5. Marcar una incidencia como Atendida.
6. Mostrar indicadores de atención.
7. Salir de la aplicación.

## Datos de una incidencia

Cada incidencia tendrá los siguientes campos:

| Campo | Descripción |
|---|---|
| codigo | Identificador único generado automáticamente |
| fecha_reporte | Fecha en que se registra la incidencia |
| area | Área municipal que reporta el problema |
| tipo_incidencia | Hardware, Software, Red, Acceso u Otro |
| descripcion | Detalle del problema reportado |
| prioridad | Alta, Media o Baja |
| estado | Pendiente, En proceso o Atendida |
| responsable | Técnico responsable de la atención |
| fecha_atencion | Fecha en que se atendió la incidencia |

## Reglas funcionales

- El código de la incidencia debe ser único.
- El código será generado automáticamente.
- Una incidencia nueva debe iniciar en estado `Pendiente`.
- El área solicitante es obligatoria.
- El tipo de incidencia debe ser válido.
- La descripción es obligatoria.
- La prioridad debe ser `Alta`, `Media` o `Baja`.
- Una incidencia pendiente puede cambiar a `En proceso`.
- Una incidencia pendiente o en proceso puede marcarse como `Atendida`.
- Para atender una incidencia se debe registrar un responsable.
- Al atender una incidencia se debe registrar la fecha de atención.
- La fecha de atención no puede ser anterior a la fecha de reporte.
- Una incidencia atendida no podrá regresar a un estado anterior.
- La información debe conservarse al cerrar la aplicación.

## Indicadores

La aplicación calculará:

- Total de incidencias.
- Total de incidencias pendientes.
- Total de incidencias en proceso.
- Total de incidencias atendidas.
- Porcentaje de atención.
- Incidencias por prioridad.
- Incidencias por área.
- Incidencias por tipo.
- Incidencias de prioridad alta pendientes.
- Tiempo promedio de atención.

## Persistencia

La información se almacenará en:

```text
data/incidencias.json