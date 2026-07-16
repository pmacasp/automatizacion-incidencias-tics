from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Incidencia:
    """Representa una incidencia tecnológica."""

    codigo: str
    fecha_reporte: str
    area: str
    tipo_incidencia: str
    descripcion: str
    prioridad: str
    estado: str = "Pendiente"
    responsable: str = ""
    fecha_atencion: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convierte la incidencia en un diccionario serializable."""

        return asdict(self)

    @classmethod
    def from_dict(cls, datos: dict[str, Any]) -> "Incidencia":
        """Crea una incidencia a partir de un diccionario."""

        return cls(
            codigo=datos["codigo"],
            fecha_reporte=datos["fecha_reporte"],
            area=datos["area"],
            tipo_incidencia=datos["tipo_incidencia"],
            descripcion=datos["descripcion"],
            prioridad=datos["prioridad"],
            estado=datos.get("estado", "Pendiente"),
            responsable=datos.get("responsable", ""),
            fecha_atencion=datos.get("fecha_atencion"),
        )
