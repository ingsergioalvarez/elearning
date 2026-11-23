"""Reglas de identidad del empleado en Learning (decisión 0011). Sin dependencias de Frappe."""

from __future__ import annotations

import re

DOMINIO_CORREO_TECNICO = "empleados.grupocomunicalo.local"

_PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_NO_PERMITIDO_EN_CORREO = re.compile(r"[^a-z0-9._-]")


def normalizar_numero(numero) -> str:
    """Igual que el ERP: sin espacios y en mayúsculas."""
    return re.sub(r"\s", "", str(numero or "")).upper()


def correo_tecnico(numero: str, dominio: str = DOMINIO_CORREO_TECNICO) -> str:
    local = _NO_PERMITIDO_EN_CORREO.sub("-", normalizar_numero(numero).lower()) or "sin-numero"
    return f"{local}@{dominio}"


def es_correo_local(correo) -> bool:
    return str(correo or "").strip().lower().endswith(".local")


def correo_corporativo_valido(correo) -> str | None:
    correo = str(correo or "").strip().lower()
    if not correo or es_correo_local(correo) or not _PATRON_CORREO.match(correo):
        return None
    return correo


def correo_para(perfil: dict, numero: str, dominio: str = DOMINIO_CORREO_TECNICO) -> str:
    """Correo corporativo del ERP si es válido; si no, el técnico .local."""
    return correo_corporativo_valido(perfil.get("correo_corporativo")) or correo_tecnico(numero, dominio)


def nombre_y_apellidos(perfil: dict, nombre_completo: str | None = None) -> tuple[str, str]:
    nombres = str(perfil.get("nombres") or "").strip()
    apellidos = " ".join(
        p for p in (str(perfil.get("apellido_paterno") or "").strip(), str(perfil.get("apellido_materno") or "").strip()) if p
    )
    if nombres:
        return nombres, apellidos
    completo = str(nombre_completo or "").strip()
    if completo:
        partes = completo.split(" ", 1)
        return partes[0], (partes[1] if len(partes) > 1 else "")
    return "Empleado", ""


def username_para(numero: str) -> str:
    """username = número de empleado (decisión 0011). lms reemplaza los username de menos de
    4 caracteres, así que a esos se les antepone «emp». La identidad real es el campo
    numero_empleado del usuario, no el username."""
    numero = normalizar_numero(numero)
    return numero if len(numero) >= 4 else f"emp{numero}"
