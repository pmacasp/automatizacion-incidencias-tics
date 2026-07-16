import pytest

from incidencias.modelo import Incidencia


@pytest.mark.unit
def test_crear_incidencia_con_estado_pendiente_por_defecto():
    incidencia = Incidencia(
        codigo="INC-001",
        fecha_reporte="2026-07-16",
        area="Financiera",
        tipo_incidencia="Software",
        descripcion="No se puede ingresar al sistema",
        prioridad="Alta",
    )

    assert incidencia.codigo == "INC-001"
    assert incidencia.estado == "Pendiente"
    assert incidencia.responsable == ""
    assert incidencia.fecha_atencion is None


@pytest.mark.unit
def test_convertir_incidencia_a_diccionario():
    incidencia = Incidencia(
        codigo="INC-002",
        fecha_reporte="2026-07-16",
        area="Catastro",
        tipo_incidencia="Hardware",
        descripcion="El monitor no enciende",
        prioridad="Media",
    )

    resultado = incidencia.to_dict()

    assert resultado == {
        "codigo": "INC-002",
        "fecha_reporte": "2026-07-16",
        "area": "Catastro",
        "tipo_incidencia": "Hardware",
        "descripcion": "El monitor no enciende",
        "prioridad": "Media",
        "estado": "Pendiente",
        "responsable": "",
        "fecha_atencion": None,
    }


@pytest.mark.unit
def test_crear_incidencia_desde_diccionario():
    datos = {
        "codigo": "INC-003",
        "fecha_reporte": "2026-07-15",
        "area": "Tesorería",
        "tipo_incidencia": "Red",
        "descripcion": "No existe conexión a internet",
        "prioridad": "Alta",
        "estado": "En proceso",
        "responsable": "Técnico 1",
        "fecha_atencion": None,
    }

    incidencia = Incidencia.from_dict(datos)

    assert incidencia.codigo == "INC-003"
    assert incidencia.area == "Tesorería"
    assert incidencia.estado == "En proceso"
    assert incidencia.responsable == "Técnico 1"
