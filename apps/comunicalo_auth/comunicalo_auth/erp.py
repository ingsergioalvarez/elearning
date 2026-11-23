"""Cliente HTTP del ERP para el login de Learning (decisiones 0005, 0010 y 0011).

No importa Frappe para poder probarlo aislado con respuestas simuladas.
Reglas:
- La contraseña solo se reenvía al ERP. Nunca se guarda, se registra ni se devuelve.
- El token del ERP solo vive en memoria durante el login (repr oculto) y se descarta después.
- Del perfil solo se conservan los campos que Learning necesita; el resto se descarta.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import requests

RUTA_LOGIN = "/api/auth/login"
RUTA_PERFIL = "/api/rh/mi-perfil"

MENSAJE_ERP_NO_DISPONIBLE = "No se pudo validar con la intranet, intenta más tarde."
MENSAJE_BLOQUEO = "Desbloquéala desde la intranet."
MENSAJE_RECHAZO_GENERICO = "Número de empleado o contraseña incorrectos."

# Únicos campos del perfil que se conservan (el ERP regresa el registro completo del empleado).
CAMPOS_PERFIL = (
    "numero_empleado",
    "nombres",
    "apellido_paterno",
    "apellido_materno",
    "correo_corporativo",
    "empresa_nombre",
    "area_nombre",
)

LARGO_MAXIMO_MENSAJE = 300


@dataclass(frozen=True)
class RespuestaLogin:
    """motivo: ok | rechazado | bloqueado | erp_no_disponible."""

    ok: bool
    motivo: str
    mensaje: str = ""
    token: str | None = field(default=None, repr=False)
    numero_empleado: str | None = None
    nombre_completo: str | None = None
    permisos: tuple[str, ...] = ()


@dataclass(frozen=True)
class RespuestaPerfil:
    """motivo: ok | mantenimiento | no_encontrado | erp_no_disponible."""

    ok: bool
    motivo: str
    datos: dict = field(default_factory=dict)


def _url(base_url: str, ruta: str) -> str:
    return base_url.rstrip("/") + ruta


def _mensaje_del_erp(respuesta) -> str:
    try:
        cuerpo = respuesta.json()
    except ValueError:
        return ""
    if not isinstance(cuerpo, dict):
        return ""
    mensaje = cuerpo.get("message")
    if not isinstance(mensaje, str):
        return ""
    return mensaje.strip()[:LARGO_MAXIMO_MENSAJE]


def iniciar_sesion(
    base_url: str,
    numero_empleado: str,
    password: str,
    timeout: float,
    ip_cliente: str | None = None,
    session=requests,
) -> RespuestaLogin:
    """Valida número de empleado y contraseña con POST {base_url}/api/auth/login."""
    encabezados = {"Accept": "application/json"}
    if ip_cliente:
        encabezados["X-Forwarded-For"] = ip_cliente
    try:
        respuesta = session.post(
            _url(base_url, RUTA_LOGIN),
            json={"numero_empleado": numero_empleado, "password": password},
            headers=encabezados,
            timeout=timeout,
        )
    except requests.RequestException:
        # No se incluye la excepción: su texto podría arrastrar datos de la petición.
        return RespuestaLogin(False, "erp_no_disponible", MENSAJE_ERP_NO_DISPONIBLE)

    codigo = respuesta.status_code
    if codigo == 200:
        try:
            cuerpo = respuesta.json()
        except ValueError:
            return RespuestaLogin(False, "erp_no_disponible", MENSAJE_ERP_NO_DISPONIBLE)
        if not isinstance(cuerpo, dict) or not cuerpo.get("success"):
            return RespuestaLogin(False, "erp_no_disponible", MENSAJE_ERP_NO_DISPONIBLE)
        datos = cuerpo.get("data")
        token = datos.get("token") if isinstance(datos, dict) else None
        empleado = datos.get("empleado") if isinstance(datos, dict) else None
        if not isinstance(token, str) or not token or not isinstance(empleado, dict):
            return RespuestaLogin(False, "erp_no_disponible", MENSAJE_ERP_NO_DISPONIBLE)
        permisos = empleado.get("permisos") or []
        return RespuestaLogin(
            True,
            "ok",
            token=token,
            numero_empleado=str(empleado.get("numero_empleado") or "") or None,
            nombre_completo=str(empleado.get("nombre_completo") or "") or None,
            permisos=tuple(p for p in permisos if isinstance(p, str)),
        )
    if codigo in (400, 401):
        return RespuestaLogin(False, "rechazado", _mensaje_del_erp(respuesta) or MENSAJE_RECHAZO_GENERICO)
    if codigo == 403:
        mensaje = _mensaje_del_erp(respuesta) or "Tu cuenta está bloqueada."
        return RespuestaLogin(False, "bloqueado", f"{mensaje} {MENSAJE_BLOQUEO}")
    return RespuestaLogin(False, "erp_no_disponible", MENSAJE_ERP_NO_DISPONIBLE)


def obtener_perfil(base_url: str, token: str, timeout: float, session=requests) -> RespuestaPerfil:
    """Trae nombre, correo, empresa y área con GET {base_url}/api/rh/mi-perfil."""
    try:
        respuesta = session.get(
            _url(base_url, RUTA_PERFIL),
            headers={"Accept": "application/json", "Authorization": f"Bearer {token}"},
            timeout=timeout,
        )
    except requests.RequestException:
        return RespuestaPerfil(False, "erp_no_disponible")

    codigo = respuesta.status_code
    if codigo == 200:
        try:
            cuerpo = respuesta.json()
        except ValueError:
            return RespuestaPerfil(False, "erp_no_disponible")
        datos = cuerpo.get("data") if isinstance(cuerpo, dict) else None
        if not isinstance(datos, dict):
            return RespuestaPerfil(False, "erp_no_disponible")
        limpios = {c: datos.get(c) for c in CAMPOS_PERFIL}
        return RespuestaPerfil(True, "ok", limpios)
    if codigo == 503:
        return RespuestaPerfil(False, "mantenimiento")
    if codigo in (401, 403, 404):
        return RespuestaPerfil(False, "no_encontrado")
    return RespuestaPerfil(False, "erp_no_disponible")
