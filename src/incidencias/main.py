from pathlib import Path

from incidencias.consola import (
    AplicacionConsola,
    Entrada,
    Salida,
)
from incidencias.repositorio import RepositorioIncidencias
from incidencias.servicio import ServicioIncidencias


def crear_aplicacion(
    ruta_datos: str | Path = "data/incidencias.json",
    ruta_salida: str | Path = "output",
    input_fn: Entrada = input,
    output_fn: Salida = print,
) -> AplicacionConsola:
    """Construye la aplicación con sus dependencias."""

    repositorio = RepositorioIncidencias(
        ruta_datos
    )
    servicio = ServicioIncidencias(
        repositorio
    )

    return AplicacionConsola(
        servicio=servicio,
        ruta_salida=ruta_salida,
        input_fn=input_fn,
        output_fn=output_fn,
    )


def main() -> None:
    """Inicia la aplicación de consola."""

    aplicacion = crear_aplicacion()
    aplicacion.ejecutar()


if __name__ == "__main__":
    main()
