import csv
import json

import pytest

from incidencias.reportes import (
    exportar_indicadores_csv,
    exportar_indicadores_json,
)


def crear_indicadores_ejemplo() -> dict:
    """Retorna indicadores reutilizables para las pruebas."""

    return {
        "total": 3,
        "pendientes": 1,
        "en_proceso": 1,
        "atendidas": 1,
        "porcentaje_atencion": 33.33,
        "por_prioridad": {
            "Alta": 2,
            "Media": 1,
        },
        "por_area": {
            "Catastro": 1,
            "Dirección Financiera": 2,
        },
        "por_tipo": {
            "Hardware": 1,
            "Software": 2,
        },
        "alta_prioridad_pendientes": 1,
        "tiempo_promedio_atencion_dias": 2.0,
    }


@pytest.mark.unit
def test_exportar_json_crea_archivo_y_conserva_datos(
    tmp_path,
):
    indicadores = crear_indicadores_ejemplo()
    ruta = tmp_path / "salida" / "indicadores.json"

    resultado = exportar_indicadores_json(
        indicadores,
        ruta,
    )

    assert resultado == ruta
    assert ruta.exists()

    datos_guardados = json.loads(
        ruta.read_text(encoding="utf-8")
    )

    assert datos_guardados == indicadores
    assert datos_guardados["por_area"][
        "Dirección Financiera"
    ] == 2


@pytest.mark.unit
def test_exportar_csv_crea_encabezado_y_resumen(
    tmp_path,
):
    indicadores = crear_indicadores_ejemplo()
    ruta = tmp_path / "salida" / "indicadores.csv"

    resultado = exportar_indicadores_csv(
        indicadores,
        ruta,
    )

    assert resultado == ruta
    assert ruta.exists()

    with ruta.open(
        encoding="utf-8-sig",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)
        filas = list(lector)

    assert lector.fieldnames == [
        "categoria",
        "indicador",
        "valor",
    ]

    assert {
        "categoria": "resumen",
        "indicador": "total",
        "valor": "3",
    } in filas

    assert {
        "categoria": "resumen",
        "indicador": "porcentaje_atencion",
        "valor": "33.33",
    } in filas


@pytest.mark.unit
def test_exportar_csv_incluye_agrupaciones(
    tmp_path,
):
    indicadores = crear_indicadores_ejemplo()
    ruta = tmp_path / "indicadores.csv"

    exportar_indicadores_csv(
        indicadores,
        ruta,
    )

    with ruta.open(
        encoding="utf-8-sig",
        newline="",
    ) as archivo:
        filas = list(
            csv.DictReader(archivo)
        )

    assert {
        "categoria": "por_prioridad",
        "indicador": "Alta",
        "valor": "2",
    } in filas

    assert {
        "categoria": "por_area",
        "indicador": "Dirección Financiera",
        "valor": "2",
    } in filas

    assert {
        "categoria": "por_tipo",
        "indicador": "Software",
        "valor": "2",
    } in filas


@pytest.mark.unit
def test_exportar_csv_sin_indicadores_solo_crea_encabezado(
    tmp_path,
):
    ruta = tmp_path / "indicadores.csv"

    exportar_indicadores_csv(
        {},
        ruta,
    )

    with ruta.open(
        encoding="utf-8-sig",
        newline="",
    ) as archivo:
        lector = csv.DictReader(archivo)
        filas = list(lector)

    assert lector.fieldnames == [
        "categoria",
        "indicador",
        "valor",
    ]
    assert filas == []
