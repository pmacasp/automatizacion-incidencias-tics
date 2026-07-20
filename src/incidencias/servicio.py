from datetime import date

from incidencias.modelo import Incidencia
from incidencias.repositorio import RepositorioIncidencias
from incidencias.validaciones import (
    validar_area,
    validar_descripcion,
    validar_fecha,
    validar_fecha_atencion,
    validar_prioridad,
    validar_texto_obligatorio,
    validar_tipo_incidencia,
)


class ServicioIncidencias:
    """Gestiona las operaciones y reglas de las incidencias."""

    def __init__(
        self,
        repositorio: RepositorioIncidencias,
    ) -> None:
        self.repositorio = repositorio
        self._incidencias = list(
            repositorio.cargar()
        )

    def listar(self) -> list[Incidencia]:
        """Devuelve una copia de las incidencias registradas."""

        return list(self._incidencias)

    def buscar(
        self,
        codigo: str,
    ) -> Incidencia | None:
        """Busca una incidencia por su código."""

        if not isinstance(codigo, str):
            return None

        codigo_normalizado = codigo.strip().upper()

        for incidencia in self._incidencias:
            if incidencia.codigo.upper() == codigo_normalizado:
                return incidencia

        return None

    def registrar(
        self,
        fecha_reporte: str,
        area: str,
        tipo_incidencia: str,
        descripcion: str,
        prioridad: str,
    ) -> Incidencia:
        """Registra una nueva incidencia."""

        validar_fecha(
            fecha_reporte,
            "fecha_reporte",
        )
        validar_area(area)
        validar_tipo_incidencia(tipo_incidencia)
        validar_descripcion(descripcion)
        validar_prioridad(prioridad)

        incidencia = Incidencia(
            codigo=self._generar_codigo(),
            fecha_reporte=fecha_reporte,
            area=area.strip(),
            tipo_incidencia=tipo_incidencia,
            descripcion=descripcion.strip(),
            prioridad=prioridad,
        )

        self._incidencias.append(incidencia)
        self._guardar()

        return incidencia

    def cambiar_a_en_proceso(
        self,
        codigo: str,
        responsable: str,
    ) -> Incidencia:
        """Cambia una incidencia pendiente a En proceso."""

        validar_texto_obligatorio(
            responsable,
            "responsable",
        )

        incidencia = self._obtener_o_error(codigo)

        if incidencia.estado != "Pendiente":
            raise ValueError(
                "Solo una incidencia pendiente puede pasar "
                "a En proceso."
            )

        incidencia.estado = "En proceso"
        incidencia.responsable = responsable.strip()

        self._guardar()

        return incidencia

    def atender(
        self,
        codigo: str,
        responsable: str,
        fecha_atencion: str | None = None,
    ) -> Incidencia:
        """Marca una incidencia como atendida."""

        validar_texto_obligatorio(
            responsable,
            "responsable",
        )

        incidencia = self._obtener_o_error(codigo)

        if incidencia.estado == "Atendida":
            raise ValueError(
                "La incidencia ya se encuentra atendida."
            )

        fecha_cierre = (
            fecha_atencion
            if fecha_atencion is not None
            else date.today().isoformat()
        )

        validar_fecha_atencion(
            incidencia.fecha_reporte,
            fecha_cierre,
        )

        incidencia.estado = "Atendida"
        incidencia.responsable = responsable.strip()
        incidencia.fecha_atencion = fecha_cierre

        self._guardar()

        return incidencia

    def _generar_codigo(self) -> str:
        """Genera el siguiente código secuencial."""

        mayor_numero = 0

        for incidencia in self._incidencias:
            partes = incidencia.codigo.split("-")

            if (
                len(partes) == 2
                and partes[0].upper() == "INC"
                and partes[1].isdigit()
            ):
                mayor_numero = max(
                    mayor_numero,
                    int(partes[1]),
                )

        return f"INC-{mayor_numero + 1:03d}"

    def _obtener_o_error(
        self,
        codigo: str,
    ) -> Incidencia:
        """Obtiene una incidencia o genera un error."""

        incidencia = self.buscar(codigo)

        if incidencia is None:
            codigo_mostrado = (
                codigo.strip().upper()
                if isinstance(codigo, str)
                else str(codigo)
            )

            raise ValueError(
                f"No existe la incidencia {codigo_mostrado}."
            )

        return incidencia

    def _guardar(self) -> None:
        """Guarda el estado actual de las incidencias."""

        self.repositorio.guardar(
            self._incidencias
        )
