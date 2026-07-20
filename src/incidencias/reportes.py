import csv
import json
from pathlib import Path
from typing import Any


INDICADORES_RESUMEN = (
    "total",
    "pendientes",
    "en_proceso",
    "atendidas",
    "porcentaje_atencion",
    "alta_prioridad_pendientes",
    "tiempo_promedio_atencion_dias",
)

INDICADORES_AGRUPADOS = (
    "por_prioridad",
    "por_area",
    "por_tipo",
)


def exportar_indicadores_json(
    indicadores: dict[str, Any],
    ruta: str | Path,
) -> Path:
    """Exporta los indicadores a un archivo JSON."""

    ruta_destino = Path(ruta)

    ruta_destino.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    contenido = json.dumps(
        indicadores,
        ensure_ascii=False,
        indent=2,
    )

    ruta_destino.write_text(
        contenido + "\n",
        encoding="utf-8",
    )

    return ruta_destino


def exportar_indicadores_csv(
    indicadores: dict[str, Any],
    ruta: str | Path,
) -> Path:
    """Exporta los indicadores a un archivo CSV."""

    ruta_destino = Path(ruta)

    ruta_destino.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    filas = _convertir_indicadores_en_filas(
        indicadores
    )

    with ruta_destino.open(
        mode="w",
        encoding="utf-8-sig",
        newline="",
    ) as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=[
                "categoria",
                "indicador",
                "valor",
            ],
        )

        escritor.writeheader()
        escritor.writerows(filas)

    return ruta_destino


def _convertir_indicadores_en_filas(
    indicadores: dict[str, Any],
) -> list[dict[str, Any]]:
    """Convierte los indicadores en filas para el CSV."""

    filas = []

    for nombre in INDICADORES_RESUMEN:
        if nombre not in indicadores:
            continue

        filas.append(
            {
                "categoria": "resumen",
                "indicador": nombre,
                "valor": indicadores[nombre],
            }
        )

    for categoria in INDICADORES_AGRUPADOS:
        valores = indicadores.get(
            categoria,
            {},
        )

        if not isinstance(valores, dict):
            continue

        for nombre, valor in sorted(
            valores.items()
        ):
            filas.append(
                {
                    "categoria": categoria,
                    "indicador": nombre,
                    "valor": valor,
                }
            )

    return filas
