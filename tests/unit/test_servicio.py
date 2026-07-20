from unittest.mock import Mock

import pytest

from incidencias.modelo import Incidencia
from incidencias.repositorio import RepositorioIncidencias
from incidencias.servicio import ServicioIncidencias


def crear_repositorio_simulado(
    incidencias: list[Incidencia] | None = None,
) -> Mock:
    """Crea un repositorio simulado para las pruebas unitarias."""

    repositorio = Mock(spec=RepositorioIncidencias)
    repositorio.cargar.return_value = list(incidencias or [])
    return repositorio


def crear_incidencia(
    codigo: str = "INC-001",
    estado: str = "Pendiente",
) -> Incidencia:
    """Crea una incidencia de ejemplo."""

    return Incidencia(
        codigo=codigo,
        fecha_reporte="2026-07-16",
        area="Dirección Financiera",
        tipo_incidencia="Software",
        descripcion="No se puede ingresar al sistema",
        prioridad="Alta",
        estado=estado,
    )


@pytest.mark.unit
def test_registrar_incidencia_genera_codigo_y_guarda():
    repositorio = crear_repositorio_simulado()
    servicio = ServicioIncidencias(repositorio)

    incidencia = servicio.registrar(
        fecha_reporte="2026-07-16",
        area="Dirección Financiera",
        tipo_incidencia="Software",
        descripcion="No se puede ingresar al sistema",
        prioridad="Alta",
    )

    assert incidencia.codigo == "INC-001"
    assert incidencia.estado == "Pendiente"
    assert incidencia.responsable == ""
    assert incidencia.fecha_atencion is None

    repositorio.guardar.assert_called_once_with(
        [incidencia]
    )


@pytest.mark.unit
def test_registrar_genera_codigo_secuencial():
    existente = crear_incidencia(codigo="INC-007")
    repositorio = crear_repositorio_simulado([existente])
    servicio = ServicioIncidencias(repositorio)

    incidencia = servicio.registrar(
        fecha_reporte="2026-07-17",
        area="Catastro",
        tipo_incidencia="Hardware",
        descripcion="El monitor no enciende",
        prioridad="Media",
    )

    assert incidencia.codigo == "INC-008"


@pytest.mark.unit
def test_registrar_prioridad_invalida_no_guarda():
    repositorio = crear_repositorio_simulado()
    servicio = ServicioIncidencias(repositorio)

    with pytest.raises(
        ValueError,
        match="Prioridad no válida",
    ):
        servicio.registrar(
            fecha_reporte="2026-07-16",
            area="Tesorería",
            tipo_incidencia="Software",
            descripcion="Error en el sistema",
            prioridad="Urgente",
        )

    repositorio.guardar.assert_not_called()


@pytest.mark.unit
def test_listar_retorna_copia_de_las_incidencias():
    incidencia = crear_incidencia()
    repositorio = crear_repositorio_simulado([incidencia])
    servicio = ServicioIncidencias(repositorio)

    resultado = servicio.listar()
    resultado.clear()

    assert len(servicio.listar()) == 1


@pytest.mark.unit
def test_buscar_incidencia_por_codigo():
    incidencia = crear_incidencia()
    repositorio = crear_repositorio_simulado([incidencia])
    servicio = ServicioIncidencias(repositorio)

    resultado = servicio.buscar(" inc-001 ")

    assert resultado is incidencia


@pytest.mark.unit
def test_buscar_incidencia_inexistente_retorna_none():
    repositorio = crear_repositorio_simulado()
    servicio = ServicioIncidencias(repositorio)

    resultado = servicio.buscar("INC-999")

    assert resultado is None


@pytest.mark.unit
def test_cambiar_pendiente_a_en_proceso():
    incidencia = crear_incidencia()
    repositorio = crear_repositorio_simulado([incidencia])
    servicio = ServicioIncidencias(repositorio)

    resultado = servicio.cambiar_a_en_proceso(
        codigo="INC-001",
        responsable="Técnico 1",
    )

    assert resultado.estado == "En proceso"
    assert resultado.responsable == "Técnico 1"
    assert resultado.fecha_atencion is None

    repositorio.guardar.assert_called_once()


@pytest.mark.unit
def test_no_permite_cambiar_atendida_a_en_proceso():
    incidencia = crear_incidencia(
        estado="Atendida",
    )
    repositorio = crear_repositorio_simulado([incidencia])
    servicio = ServicioIncidencias(repositorio)

    with pytest.raises(
        ValueError,
        match="Solo una incidencia pendiente",
    ):
        servicio.cambiar_a_en_proceso(
            codigo="INC-001",
            responsable="Técnico 1",
        )

    repositorio.guardar.assert_not_called()


@pytest.mark.unit
def test_atender_incidencia_pendiente():
    incidencia = crear_incidencia()
    repositorio = crear_repositorio_simulado([incidencia])
    servicio = ServicioIncidencias(repositorio)

    resultado = servicio.atender(
        codigo="INC-001",
        responsable="Técnico 2",
        fecha_atencion="2026-07-17",
    )

    assert resultado.estado == "Atendida"
    assert resultado.responsable == "Técnico 2"
    assert resultado.fecha_atencion == "2026-07-17"

    repositorio.guardar.assert_called_once()


@pytest.mark.unit
def test_fecha_atencion_anterior_no_modifica_incidencia():
    incidencia = crear_incidencia()
    repositorio = crear_repositorio_simulado([incidencia])
    servicio = ServicioIncidencias(repositorio)

    with pytest.raises(
        ValueError,
        match="La fecha de atención no puede ser anterior",
    ):
        servicio.atender(
            codigo="INC-001",
            responsable="Técnico 1",
            fecha_atencion="2026-07-15",
        )

    assert incidencia.estado == "Pendiente"
    assert incidencia.responsable == ""
    assert incidencia.fecha_atencion is None
    repositorio.guardar.assert_not_called()


@pytest.mark.unit
def test_atender_incidencia_inexistente_genera_error():
    repositorio = crear_repositorio_simulado()
    servicio = ServicioIncidencias(repositorio)

    with pytest.raises(
        ValueError,
        match="No existe la incidencia INC-999",
    ):
        servicio.atender(
            codigo="INC-999",
            responsable="Técnico 1",
            fecha_atencion="2026-07-17",
        )
