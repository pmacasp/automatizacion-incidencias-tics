import pytest

from incidencias.indicadores import (
    calcular_porcentaje_atencion,
    calcular_tiempo_promedio_atencion,
    generar_indicadores,
)
from incidencias.modelo import Incidencia


def crear_incidencia(
    codigo: str,
    fecha_reporte: str = "2026-07-10",
    area: str = "Financiera",
    tipo_incidencia: str = "Software",
    prioridad: str = "Media",
    estado: str = "Pendiente",
    responsable: str = "",
    fecha_atencion: str | None = None,
) -> Incidencia:
    """Crea una incidencia de ejemplo para las pruebas."""

    return Incidencia(
        codigo=codigo,
        fecha_reporte=fecha_reporte,
        area=area,
        tipo_incidencia=tipo_incidencia,
        descripcion="Incidencia utilizada en una prueba",
        prioridad=prioridad,
        estado=estado,
        responsable=responsable,
        fecha_atencion=fecha_atencion,
    )


@pytest.mark.unit
def test_porcentaje_atencion_sin_incidencias_es_cero():
    resultado = calcular_porcentaje_atencion(
        atendidas=0,
        total=0,
    )

    assert resultado == 0.0


@pytest.mark.unit
def test_porcentaje_atencion_se_redondea_a_dos_decimales():
    resultado = calcular_porcentaje_atencion(
        atendidas=2,
        total=3,
    )

    assert resultado == 66.67


@pytest.mark.unit
def test_tiempo_promedio_sin_incidencias_atendidas_es_cero():
    incidencias = [
        crear_incidencia(
            codigo="INC-001",
            estado="Pendiente",
        ),
        crear_incidencia(
            codigo="INC-002",
            estado="En proceso",
        ),
    ]

    resultado = calcular_tiempo_promedio_atencion(
        incidencias
    )

    assert resultado == 0.0


@pytest.mark.unit
def test_calcular_tiempo_promedio_de_atencion():
    incidencias = [
        crear_incidencia(
            codigo="INC-001",
            fecha_reporte="2026-07-10",
            estado="Atendida",
            responsable="Técnico 1",
            fecha_atencion="2026-07-12",
        ),
        crear_incidencia(
            codigo="INC-002",
            fecha_reporte="2026-07-11",
            estado="Atendida",
            responsable="Técnico 2",
            fecha_atencion="2026-07-14",
        ),
        crear_incidencia(
            codigo="INC-003",
            estado="Pendiente",
        ),
    ]

    resultado = calcular_tiempo_promedio_atencion(
        incidencias
    )

    assert resultado == 2.5


@pytest.mark.unit
def test_generar_indicadores_sin_incidencias():
    resultado = generar_indicadores([])

    assert resultado == {
        "total": 0,
        "pendientes": 0,
        "en_proceso": 0,
        "atendidas": 0,
        "porcentaje_atencion": 0.0,
        "por_prioridad": {},
        "por_area": {},
        "por_tipo": {},
        "alta_prioridad_pendientes": 0,
        "tiempo_promedio_atencion_dias": 0.0,
    }


@pytest.mark.unit
def test_generar_indicadores_con_incidencias():
    incidencias = [
        crear_incidencia(
            codigo="INC-001",
            area="Financiera",
            tipo_incidencia="Software",
            prioridad="Alta",
            estado="Pendiente",
        ),
        crear_incidencia(
            codigo="INC-002",
            area="Catastro",
            tipo_incidencia="Hardware",
            prioridad="Media",
            estado="En proceso",
            responsable="Técnico 1",
        ),
        crear_incidencia(
            codigo="INC-003",
            fecha_reporte="2026-07-10",
            area="Financiera",
            tipo_incidencia="Software",
            prioridad="Alta",
            estado="Atendida",
            responsable="Técnico 2",
            fecha_atencion="2026-07-12",
        ),
    ]

    resultado = generar_indicadores(incidencias)

    assert resultado["total"] == 3
    assert resultado["pendientes"] == 1
    assert resultado["en_proceso"] == 1
    assert resultado["atendidas"] == 1
    assert resultado["porcentaje_atencion"] == 33.33

    assert resultado["por_prioridad"] == {
        "Alta": 2,
        "Media": 1,
    }

    assert resultado["por_area"] == {
        "Catastro": 1,
        "Financiera": 2,
    }

    assert resultado["por_tipo"] == {
        "Hardware": 1,
        "Software": 2,
    }

    assert resultado["alta_prioridad_pendientes"] == 1
    assert resultado["tiempo_promedio_atencion_dias"] == 2.0
