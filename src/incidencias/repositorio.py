import json
from json import JSONDecodeError
from pathlib import Path

from incidencias.modelo import Incidencia


class RepositorioIncidencias:
    """Administra la persistencia local de incidencias en JSON."""

    def __init__(
        self,
        ruta: str | Path,
    ) -> None:
        self.ruta = Path(ruta)

    def cargar(self) -> list[Incidencia]:
        """Carga las incidencias almacenadas en el archivo JSON."""

        if not self.ruta.exists():
            return []

        contenido = self.ruta.read_text(
            encoding="utf-8-sig"
        )

        if not contenido.strip():
            return []

        try:
            datos = json.loads(contenido)
        except JSONDecodeError as error:
            raise ValueError(
                "El archivo de incidencias contiene JSON inválido."
            ) from error

        if not isinstance(datos, list):
            raise ValueError(
                "El archivo JSON debe contener una lista "
                "de incidencias."
            )

        try:
            return [
                Incidencia.from_dict(elemento)
                for elemento in datos
            ]
        except (KeyError, TypeError) as error:
            raise ValueError(
                "El archivo contiene una incidencia "
                "incompleta o inválida."
            ) from error

    def guardar(
        self,
        incidencias: list[Incidencia],
    ) -> None:
        """Guarda una lista de incidencias en formato JSON."""

        self.ruta.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        datos = [
            incidencia.to_dict()
            for incidencia in incidencias
        ]

        contenido = json.dumps(
            datos,
            ensure_ascii=False,
            indent=2,
        )

        self.ruta.write_text(
            contenido + "\n",
            encoding="utf-8",
        )
