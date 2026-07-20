import pytest

from incidencias.modelo import Incidencia
from incidencias.repositorio import RepositorioIncidencias
from incidencias.servicio import ServicioIncidencias


@pytest.mark.regression
def test_prioridad_invalida_no_crea_registro_persistente(
    tmp_path,
):
    """Evita guardar incidencias con prioridades no permitidas."""

    ruta = tmp_path / "incidencias.json"
    servicio = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    with pytest.raises(
        ValueError,
        match="Prioridad no válida",
    ):
        servicio.registrar(
            fecha_reporte="2026-07-16",
            area="Dirección Financiera",
            tipo_incidencia="Software",
            descripcion="Error al ingresar al sistema",
            prioridad="Urgente",
        )

    assert servicio.listar() == []
    assert not ruta.exists()


@pytest.mark.regression
def test_fecha_atencion_invalida_no_altera_datos_guardados(
    tmp_path,
):
    """Evita modificar datos cuando la fecha de atención es inválida."""

    ruta = tmp_path / "incidencias.json"

    servicio = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    registrada = servicio.registrar(
        fecha_reporte="2026-07-16",
        area="Tesorería",
        tipo_incidencia="Software",
        descripcion="No se puede abrir el sistema",
        prioridad="Alta",
    )

    with pytest.raises(
        ValueError,
        match="La fecha de atención no puede ser anterior",
    ):
        servicio.atender(
            codigo=registrada.codigo,
            responsable="Técnico 1",
            fecha_atencion="2026-07-15",
        )

    servicio_recargado = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    recuperada = servicio_recargado.buscar(
        registrada.codigo
    )

    assert recuperada is not None
    assert recuperada.estado == "Pendiente"
    assert recuperada.responsable == ""
    assert recuperada.fecha_atencion is None


@pytest.mark.regression
def test_codigo_nuevo_continua_desde_el_mayor_existente(
    tmp_path,
):
    """Evita repetir códigos cuando existen saltos en la numeración."""

    ruta = tmp_path / "incidencias.json"
    repositorio = RepositorioIncidencias(ruta)

    incidencias_existentes = [
        Incidencia(
            codigo="INC-001",
            fecha_reporte="2026-07-10",
            area="Catastro",
            tipo_incidencia="Hardware",
            descripcion="El monitor no enciende",
            prioridad="Media",
        ),
        Incidencia(
            codigo="INC-010",
            fecha_reporte="2026-07-11",
            area="Dirección Financiera",
            tipo_incidencia="Software",
            descripcion="Error al generar reporte",
            prioridad="Alta",
        ),
    ]

    repositorio.guardar(
        incidencias_existentes
    )

    servicio = ServicioIncidencias(
        RepositorioIncidencias(ruta)
    )

    nueva = servicio.registrar(
        fecha_reporte="2026-07-16",
        area="Talento Humano",
        tipo_incidencia="Acceso",
        descripcion="Usuario sin acceso al sistema",
        prioridad="Baja",
    )

    assert nueva.codigo == "INC-011"
