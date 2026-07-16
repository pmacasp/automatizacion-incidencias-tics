import pytest

from incidencias.repositorio import RepositorioIncidencias
from incidencias.servicio import ServicioIncidencias


@pytest.mark.integration
def test_registrar_incidencia_y_recuperarla_desde_json(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"

    repositorio = RepositorioIncidencias(ruta)
    servicio = ServicioIncidencias(repositorio)

    registrada = servicio.registrar(
        fecha_reporte="2026-07-16",
        area="Dirección Financiera",
        tipo_incidencia="Software",
        descripcion="No se puede ingresar al sistema",
        prioridad="Alta",
    )

    nuevo_repositorio = RepositorioIncidencias(ruta)
    nuevo_servicio = ServicioIncidencias(
        nuevo_repositorio
    )

    recuperada = nuevo_servicio.buscar(
        registrada.codigo
    )

    assert ruta.exists()
    assert recuperada is not None
    assert recuperada.codigo == "INC-001"
    assert recuperada.area == "Dirección Financiera"
    assert recuperada.estado == "Pendiente"


@pytest.mark.integration
def test_cambio_a_en_proceso_persiste_en_json(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"

    servicio = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    registrada = servicio.registrar(
        fecha_reporte="2026-07-16",
        area="Catastro",
        tipo_incidencia="Hardware",
        descripcion="El monitor no enciende",
        prioridad="Media",
    )

    servicio.cambiar_a_en_proceso(
        codigo=registrada.codigo,
        responsable="Técnico 1",
    )

    servicio_recargado = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    recuperada = servicio_recargado.buscar(
        registrada.codigo
    )

    assert recuperada is not None
    assert recuperada.estado == "En proceso"
    assert recuperada.responsable == "Técnico 1"
    assert recuperada.fecha_atencion is None


@pytest.mark.integration
def test_atender_incidencia_persiste_en_json(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"

    servicio = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    registrada = servicio.registrar(
        fecha_reporte="2026-07-16",
        area="Tesorería",
        tipo_incidencia="Red",
        descripcion="No existe conexión de red",
        prioridad="Alta",
    )

    servicio.atender(
        codigo=registrada.codigo,
        responsable="Técnico 2",
        fecha_atencion="2026-07-18",
    )

    servicio_recargado = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    recuperada = servicio_recargado.buscar(
        registrada.codigo
    )

    assert recuperada is not None
    assert recuperada.estado == "Atendida"
    assert recuperada.responsable == "Técnico 2"
    assert recuperada.fecha_atencion == "2026-07-18"
