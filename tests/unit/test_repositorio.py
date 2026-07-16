import json

import pytest

from incidencias.modelo import Incidencia
from incidencias.repositorio import RepositorioIncidencias


def crear_incidencia_ejemplo() -> Incidencia:
    """Construye una incidencia reutilizable para las pruebas."""

    return Incidencia(
        codigo="INC-001",
        fecha_reporte="2026-07-16",
        area="Tesorería",
        tipo_incidencia="Software",
        descripcion="No se puede ingresar al sistema",
        prioridad="Alta",
    )


@pytest.mark.unit
def test_cargar_archivo_inexistente_retorna_lista_vacia(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"
    repositorio = RepositorioIncidencias(ruta)

    resultado = repositorio.cargar()

    assert resultado == []


@pytest.mark.unit
def test_cargar_archivo_vacio_retorna_lista_vacia(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"
    ruta.write_text("", encoding="utf-8")
    repositorio = RepositorioIncidencias(ruta)

    resultado = repositorio.cargar()

    assert resultado == []


@pytest.mark.unit
def test_guardar_y_cargar_incidencias(
    tmp_path,
):
    ruta = tmp_path / "datos" / "incidencias.json"
    repositorio = RepositorioIncidencias(ruta)
    incidencia = crear_incidencia_ejemplo()

    repositorio.guardar([incidencia])
    resultado = repositorio.cargar()

    assert ruta.exists()
    assert resultado == [incidencia]

    datos_guardados = json.loads(
        ruta.read_text(encoding="utf-8")
    )

    assert datos_guardados[0]["area"] == "Tesorería"


@pytest.mark.unit
def test_cargar_json_invalido_genera_error(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"
    ruta.write_text(
        "{contenido invalido",
        encoding="utf-8",
    )
    repositorio = RepositorioIncidencias(ruta)

    with pytest.raises(
        ValueError,
        match="JSON inválido",
    ):
        repositorio.cargar()


@pytest.mark.unit
def test_cargar_json_que_no_es_lista_genera_error(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"
    ruta.write_text(
        '{"codigo": "INC-001"}',
        encoding="utf-8",
    )
    repositorio = RepositorioIncidencias(ruta)

    with pytest.raises(
        ValueError,
        match="debe contener una lista",
    ):
        repositorio.cargar()


@pytest.mark.unit
def test_cargar_incidencia_incompleta_genera_error(
    tmp_path,
):
    ruta = tmp_path / "incidencias.json"
    ruta.write_text(
        '[{"codigo": "INC-001"}]',
        encoding="utf-8",
    )
    repositorio = RepositorioIncidencias(ruta)

    with pytest.raises(
        ValueError,
        match="incidencia incompleta o inválida",
    ):
        repositorio.cargar()
