import pytest

from incidencias.main import crear_aplicacion
from incidencias.repositorio import RepositorioIncidencias


@pytest.mark.e2e
def test_flujo_completo_desde_registro_hasta_reportes(
    tmp_path,
):
    ruta_datos = tmp_path / "data" / "incidencias.json"
    ruta_salida = tmp_path / "output"

    entradas = iter(
        [
            "1",
            "2026-07-16",
            "Dirección Financiera",
            "Software",
            "No se puede ingresar al sistema",
            "Alta",
            "4",
            "INC-001",
            "Técnico 1",
            "5",
            "INC-001",
            "Técnico 1",
            "2026-07-17",
            "6",
            "7",
            "8",
        ]
    )

    salidas = []

    def entrada_simulada(mensaje):
        salidas.append(mensaje)
        return next(entradas)

    aplicacion = crear_aplicacion(
        ruta_datos=ruta_datos,
        ruta_salida=ruta_salida,
        input_fn=entrada_simulada,
        output_fn=salidas.append,
    )

    aplicacion.ejecutar()

    incidencias = RepositorioIncidencias(
        ruta_datos
    ).cargar()

    assert len(incidencias) == 1
    assert incidencias[0].codigo == "INC-001"
    assert incidencias[0].estado == "Atendida"
    assert incidencias[0].responsable == "Técnico 1"
    assert incidencias[0].fecha_atencion == "2026-07-17"

    assert (
        ruta_salida / "indicadores.json"
    ).exists()

    assert (
        ruta_salida / "indicadores.csv"
    ).exists()

    assert any(
        "INC-001 registrada correctamente" in salida
        for salida in salidas
    )

    assert any(
        "Total de incidencias: 1" in salida
        for salida in salidas
    )

    assert any(
        "Reportes generados correctamente" in salida
        for salida in salidas
    )
