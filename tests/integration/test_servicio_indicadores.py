import pytest

from incidencias.indicadores import generar_indicadores
from incidencias.repositorio import RepositorioIncidencias
from incidencias.servicio import ServicioIncidencias


@pytest.mark.integration
def test_servicio_genera_datos_para_indicadores(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"

    servicio = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    primera = servicio.registrar(
        fecha_reporte="2026-07-10",
        area="Dirección Financiera",
        tipo_incidencia="Software",
        descripcion="Error al ingresar al sistema",
        prioridad="Alta",
    )

    segunda = servicio.registrar(
        fecha_reporte="2026-07-11",
        area="Catastro",
        tipo_incidencia="Hardware",
        descripcion="El monitor no enciende",
        prioridad="Media",
    )

    tercera = servicio.registrar(
        fecha_reporte="2026-07-12",
        area="Dirección Financiera",
        tipo_incidencia="Software",
        descripcion="Error al generar un reporte",
        prioridad="Alta",
    )

    servicio.cambiar_a_en_proceso(
        codigo=segunda.codigo,
        responsable="Técnico 1",
    )

    servicio.atender(
        codigo=tercera.codigo,
        responsable="Técnico 2",
        fecha_atencion="2026-07-14",
    )

    indicadores = generar_indicadores(
        servicio.listar()
    )

    assert primera.estado == "Pendiente"
    assert indicadores["total"] == 3
    assert indicadores["pendientes"] == 1
    assert indicadores["en_proceso"] == 1
    assert indicadores["atendidas"] == 1
    assert indicadores["porcentaje_atencion"] == 33.33

    assert indicadores["por_prioridad"] == {
        "Alta": 2,
        "Media": 1,
    }

    assert indicadores["por_area"] == {
        "Catastro": 1,
        "Dirección Financiera": 2,
    }

    assert indicadores[
        "alta_prioridad_pendientes"
    ] == 1

    assert indicadores[
        "tiempo_promedio_atencion_dias"
    ] == 2.0
