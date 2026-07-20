from datetime import date, datetime


TIPOS_INCIDENCIA_VALIDOS = {
    "Hardware",
    "Software",
    "Red",
    "Acceso",
    "Otro",
}

PRIORIDADES_VALIDAS = {
    "Alta",
    "Media",
    "Baja",
}

ESTADOS_VALIDOS = {
    "Pendiente",
    "En proceso",
    "Atendida",
}


def validar_texto_obligatorio(
    valor: str,
    nombre_campo: str,
) -> None:
    """Comprueba que un campo de texto tenga contenido."""

    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(
            f"El campo {nombre_campo} es obligatorio."
        )


def validar_opcion(
    valor: str,
    opciones_validas: set[str],
    nombre_campo: str,
) -> None:
    """Comprueba que un valor pertenezca a un catálogo permitido."""

    validar_texto_obligatorio(valor, nombre_campo)

    if valor not in opciones_validas:
        raise ValueError(
            f"{nombre_campo} no válido: {valor}."
        )


def validar_area(area: str) -> None:
    """Valida el área que reporta una incidencia."""

    validar_texto_obligatorio(area, "area")


def validar_tipo_incidencia(tipo_incidencia: str) -> None:
    """Valida el tipo de incidencia."""

    validar_opcion(
        tipo_incidencia,
        TIPOS_INCIDENCIA_VALIDOS,
        "Tipo de incidencia",
    )


def validar_descripcion(descripcion: str) -> None:
    """Valida la descripción de una incidencia."""

    validar_texto_obligatorio(
        descripcion,
        "descripcion",
    )


def validar_prioridad(prioridad: str) -> None:
    """Valida la prioridad de una incidencia."""

    validar_texto_obligatorio(
        prioridad,
        "Prioridad",
    )

    if prioridad not in PRIORIDADES_VALIDAS:
        raise ValueError(
            f"Prioridad no válida: {prioridad}."
        )


def validar_estado(estado: str) -> None:
    """Valida el estado de una incidencia."""

    validar_opcion(
        estado,
        ESTADOS_VALIDOS,
        "Estado",
    )


def validar_fecha(
    fecha: str,
    nombre_campo: str,
) -> date:
    """Valida una fecha y devuelve su representación date."""

    validar_texto_obligatorio(fecha, nombre_campo)

    try:
        return datetime.strptime(
            fecha,
            "%Y-%m-%d",
        ).date()
    except ValueError as error:
        raise ValueError(
            f"{nombre_campo} debe usar formato AAAA-MM-DD."
        ) from error


def validar_fecha_atencion(
    fecha_reporte: str,
    fecha_atencion: str,
) -> None:
    """Comprueba la coherencia entre reporte y atención."""

    reporte = validar_fecha(
        fecha_reporte,
        "fecha_reporte",
    )
    atencion = validar_fecha(
        fecha_atencion,
        "fecha_atencion",
    )

    if atencion < reporte:
        raise ValueError(
            "La fecha de atención no puede ser anterior "
            "a la fecha de reporte."
        )
