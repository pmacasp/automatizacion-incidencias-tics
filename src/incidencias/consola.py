from pathlib import Path
from typing import Callable

from incidencias.indicadores import generar_indicadores
from incidencias.modelo import Incidencia
from incidencias.reportes import (
    exportar_indicadores_csv,
    exportar_indicadores_json,
)
from incidencias.servicio import ServicioIncidencias


Entrada = Callable[[str], str]
Salida = Callable[[str], None]


class AplicacionConsola:
    """Interfaz de consola para gestionar incidencias."""

    def __init__(
        self,
        servicio: ServicioIncidencias,
        ruta_salida: str | Path = "output",
        input_fn: Entrada = input,
        output_fn: Salida = print,
    ) -> None:
        self.servicio = servicio
        self.ruta_salida = Path(ruta_salida)
        self.input_fn = input_fn
        self.output_fn = output_fn

    def ejecutar(self) -> None:
        """Ejecuta el menú principal hasta seleccionar Salir."""

        while True:
            self._mostrar_menu()

            try:
                opcion = self.input_fn(
                    "Seleccione una opción: "
                ).strip()

                if opcion == "1":
                    self._registrar()
                elif opcion == "2":
                    self._listar()
                elif opcion == "3":
                    self._buscar()
                elif opcion == "4":
                    self._cambiar_a_en_proceso()
                elif opcion == "5":
                    self._atender()
                elif opcion == "6":
                    self._mostrar_indicadores()
                elif opcion == "7":
                    self._exportar_reportes()
                elif opcion == "8":
                    self.output_fn(
                        "Aplicación finalizada."
                    )
                    break
                else:
                    self.output_fn(
                        "Opción no válida."
                    )

            except ValueError as error:
                self.output_fn(
                    f"Error: {error}"
                )
            except (EOFError, KeyboardInterrupt):
                self.output_fn(
                    "Aplicación finalizada."
                )
                break

    def _mostrar_menu(self) -> None:
        """Muestra las opciones disponibles."""

        self.output_fn(
            "\n"
            "========================================\n"
            " SISTEMA DE INCIDENCIAS TECNOLÓGICAS\n"
            "========================================\n"
            "1. Registrar incidencia\n"
            "2. Listar incidencias\n"
            "3. Buscar incidencia\n"
            "4. Cambiar incidencia a En proceso\n"
            "5. Marcar incidencia como Atendida\n"
            "6. Mostrar indicadores\n"
            "7. Exportar reportes\n"
            "8. Salir"
        )

    def _registrar(self) -> None:
        """Solicita los datos y registra una incidencia."""

        incidencia = self.servicio.registrar(
            fecha_reporte=self.input_fn(
                "Fecha de reporte (AAAA-MM-DD): "
            ),
            area=self.input_fn(
                "Área solicitante: "
            ),
            tipo_incidencia=self.input_fn(
                "Tipo de incidencia: "
            ),
            descripcion=self.input_fn(
                "Descripción: "
            ),
            prioridad=self.input_fn(
                "Prioridad (Alta, Media o Baja): "
            ),
        )

        self.output_fn(
            f"Incidencia {incidencia.codigo} "
            "registrada correctamente."
        )

    def _listar(self) -> None:
        """Muestra todas las incidencias."""

        incidencias = self.servicio.listar()

        if not incidencias:
            self.output_fn(
                "No existen incidencias registradas."
            )
            return

        for incidencia in incidencias:
            self._mostrar_incidencia(incidencia)

    def _buscar(self) -> None:
        """Busca y muestra una incidencia."""

        codigo = self.input_fn(
            "Código de la incidencia: "
        )

        incidencia = self.servicio.buscar(codigo)

        if incidencia is None:
            self.output_fn(
                "No se encontró la incidencia."
            )
            return

        self._mostrar_incidencia(incidencia)

    def _cambiar_a_en_proceso(self) -> None:
        """Cambia una incidencia a estado En proceso."""

        incidencia = (
            self.servicio.cambiar_a_en_proceso(
                codigo=self.input_fn(
                    "Código de la incidencia: "
                ),
                responsable=self.input_fn(
                    "Responsable: "
                ),
            )
        )

        self.output_fn(
            f"Incidencia {incidencia.codigo} "
            "actualizada a En proceso."
        )

    def _atender(self) -> None:
        """Marca una incidencia como atendida."""

        codigo = self.input_fn(
            "Código de la incidencia: "
        )
        responsable = self.input_fn(
            "Responsable: "
        )
        fecha_atencion = self.input_fn(
            "Fecha de atención "
            "(AAAA-MM-DD, vacío para hoy): "
        ).strip()

        incidencia = self.servicio.atender(
            codigo=codigo,
            responsable=responsable,
            fecha_atencion=(
                fecha_atencion or None
            ),
        )

        self.output_fn(
            f"Incidencia {incidencia.codigo} "
            "marcada como Atendida."
        )

    def _mostrar_indicadores(self) -> None:
        """Calcula y presenta los indicadores."""

        indicadores = generar_indicadores(
            self.servicio.listar()
        )

        self.output_fn(
            f"Total de incidencias: "
            f"{indicadores['total']}"
        )
        self.output_fn(
            f"Pendientes: "
            f"{indicadores['pendientes']}"
        )
        self.output_fn(
            f"En proceso: "
            f"{indicadores['en_proceso']}"
        )
        self.output_fn(
            f"Atendidas: "
            f"{indicadores['atendidas']}"
        )
        self.output_fn(
            f"Porcentaje de atención: "
            f"{indicadores['porcentaje_atencion']} %"
        )
        self.output_fn(
            "Tiempo promedio de atención: "
            f"{indicadores[
                'tiempo_promedio_atencion_dias'
            ]} días"
        )

    def _exportar_reportes(self) -> None:
        """Genera los archivos JSON y CSV."""

        indicadores = generar_indicadores(
            self.servicio.listar()
        )

        exportar_indicadores_json(
            indicadores,
            self.ruta_salida / "indicadores.json",
        )

        exportar_indicadores_csv(
            indicadores,
            self.ruta_salida / "indicadores.csv",
        )

        self.output_fn(
            "Reportes generados correctamente."
        )

    def _mostrar_incidencia(
        self,
        incidencia: Incidencia,
    ) -> None:
        """Presenta los datos de una incidencia."""

        self.output_fn(
            "\n"
            f"Código: {incidencia.codigo}\n"
            f"Fecha de reporte: "
            f"{incidencia.fecha_reporte}\n"
            f"Área: {incidencia.area}\n"
            f"Tipo: {incidencia.tipo_incidencia}\n"
            f"Descripción: {incidencia.descripcion}\n"
            f"Prioridad: {incidencia.prioridad}\n"
            f"Estado: {incidencia.estado}\n"
            f"Responsable: "
            f"{incidencia.responsable or 'Sin asignar'}\n"
            f"Fecha de atención: "
            f"{incidencia.fecha_atencion or 'Sin registrar'}"
        )
