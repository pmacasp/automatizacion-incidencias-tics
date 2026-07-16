import pytest

from incidencias.validaciones import (
    validar_area,
    validar_descripcion,
    validar_estado,
    validar_fecha,
    validar_fecha_atencion,
    validar_prioridad,
    validar_tipo_incidencia,
)


@pytest.mark.unit
def test_datos_validos_no_generan_error():
    validar_area("Dirección Financiera")
    validar_tipo_incidencia("Software")
    validar_descripcion("No se puede acceder al sistema")
    validar_prioridad("Alta")
    validar_estado("Pendiente")
    validar_fecha("2026-07-16", "fecha_reporte")
    validar_fecha_atencion("2026-07-16", "2026-07-16")


@pytest.mark.unit
@pytest.mark.parametrize("valor", ["", "   ", None])
def test_area_vacia_genera_error(valor):
    with pytest.raises(
        ValueError,
        match="El campo area es obligatorio",
    ):
        validar_area(valor)


@pytest.mark.unit
def test_tipo_incidencia_invalido_genera_error():
    with pytest.raises(
        ValueError,
        match="Tipo de incidencia no válido",
    ):
        validar_tipo_incidencia("Telefonía")


@pytest.mark.unit
def test_prioridad_invalida_genera_error():
    with pytest.raises(
        ValueError,
        match="Prioridad no válida",
    ):
        validar_prioridad("Urgente")


@pytest.mark.unit
def test_estado_invalido_genera_error():
    with pytest.raises(
        ValueError,
        match="Estado no válido",
    ):
        validar_estado("Cerrada")


@pytest.mark.unit
def test_fecha_con_formato_invalido_genera_error():
    with pytest.raises(
        ValueError,
        match="fecha_reporte debe usar formato AAAA-MM-DD",
    ):
        validar_fecha("16/07/2026", "fecha_reporte")


@pytest.mark.unit
def test_fecha_atencion_anterior_al_reporte_genera_error():
    with pytest.raises(
        ValueError,
        match="La fecha de atención no puede ser anterior",
    ):
        validar_fecha_atencion(
            fecha_reporte="2026-07-16",
            fecha_atencion="2026-07-15",
        )
