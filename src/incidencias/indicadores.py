from collections import Counter
from datetime import date
from typing import Any

from incidencias.modelo import Incidencia


def calcular_porcentaje_atencion(
    atendidas: int,
    total: int,
) -> float:
    """Calcula el porcentaje de incidencias atendidas."""

    if total == 0:
        return 0.0

    porcentaje = atendidas / total * 100

    return round(porcentaje, 2)


def calcular_tiempo_promedio_atencion(
    incidencias: list[Incidencia],
) -> float:
    """Calcula el promedio de días de atención."""

    tiempos_atencion = []

    for incidencia in incidencias:
        if (
            incidencia.estado != "Atendida"
            or incidencia.fecha_atencion is None
        ):
            continue

        fecha_reporte = date.fromisoformat(
            incidencia.fecha_reporte
        )
        fecha_atencion = date.fromisoformat(
            incidencia.fecha_atencion
        )

        dias = (
            fecha_atencion - fecha_reporte
        ).days

        tiempos_atencion.append(dias)

    if not tiempos_atencion:
        return 0.0

    promedio = (
        sum(tiempos_atencion)
        / len(tiempos_atencion)
    )

    return round(promedio, 2)


def generar_indicadores(
    incidencias: list[Incidencia],
) -> dict[str, Any]:
    """Genera el resumen de indicadores de atención."""

    total = len(incidencias)

    pendientes = sum(
        incidencia.estado == "Pendiente"
        for incidencia in incidencias
    )

    en_proceso = sum(
        incidencia.estado == "En proceso"
        for incidencia in incidencias
    )

    atendidas = sum(
        incidencia.estado == "Atendida"
        for incidencia in incidencias
    )

    altas_pendientes = sum(
        incidencia.prioridad == "Alta"
        and incidencia.estado == "Pendiente"
        for incidencia in incidencias
    )

    return {
        "total": total,
        "pendientes": pendientes,
        "en_proceso": en_proceso,
        "atendidas": atendidas,
        "porcentaje_atencion": (
            calcular_porcentaje_atencion(
                atendidas=atendidas,
                total=total,
            )
        ),
        "por_prioridad": _contar_por_atributo(
            incidencias,
            "prioridad",
        ),
        "por_area": _contar_por_atributo(
            incidencias,
            "area",
        ),
        "por_tipo": _contar_por_atributo(
            incidencias,
            "tipo_incidencia",
        ),
        "alta_prioridad_pendientes": (
            altas_pendientes
        ),
        "tiempo_promedio_atencion_dias": (
            calcular_tiempo_promedio_atencion(
                incidencias
            )
        ),
    }


def _contar_por_atributo(
    incidencias: list[Incidencia],
    atributo: str,
) -> dict[str, int]:
    """Cuenta incidencias agrupándolas por un atributo."""

    valores = [
        getattr(incidencia, atributo)
        for incidencia in incidencias
    ]

    conteos = Counter(valores)

    return dict(
        sorted(conteos.items())
    )
