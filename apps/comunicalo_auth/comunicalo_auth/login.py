"""Login de Learning con número de empleado y contraseña del ERP (decisiones 0005, 0010, 0011).

Flujo: la página /login (www/login.html) llama a `entrar`. Se valida contra el ERP, se trae el
perfil, se crea o actualiza el usuario de Frappe y se abre la sesión con LoginManager.login_as.
La contraseña y el token del ERP no se guardan ni se registran en ningún lado.
"""

from __future__ import annotations

import frappe
from frappe.rate_limiter import rate_limit
from frappe.www.login import sanitize_redirect

from comunicalo_auth import erp, identidad

ROL_ESTUDIANTE = "LMS Student"
DESTINO_POR_OMISION = "/lms"
TIMEOUT_POR_OMISION = 10

MENSAJE_FALTAN_DATOS = "Escribe tu número de empleado y tu contraseña."
MENSAJE_PRIMERA_VEZ_SIN_PERFIL = (
    "La intranet está en mantenimiento. Como es tu primera vez en Cursos, intenta de nuevo más tarde."
)
MENSAJE_SIN_REGISTRO = "No se encontró tu registro de empleado activo. Consulta con Recursos Humanos."
MENSAJE_DESACTIVADO = "Tu acceso a Cursos está desactivado. Consulta con Recursos Humanos."
MENSAJE_ADMIN_INCORRECTO = "Usuario o contraseña incorrectos."
MENSAJE_SIN_CONFIGURAR = "El acceso a Cursos no está configurado. Avisa a Desarrollo."


def _config() -> tuple[str | None, float]:
    url = (frappe.conf.get("erp_api_url") or "").strip()
    try:
        timeout = float(frappe.conf.get("erp_timeout_segundos") or TIMEOUT_POR_OMISION)
    except (TypeError, ValueError):
        timeout = TIMEOUT_POR_OMISION
    return (url or None), timeout


def _fallo(mensaje: str) -> dict:
    return {"ok": False, "mensaje": mensaje}


def _exito(redirect_to: str | None) -> dict:
    return {"ok": True, "redirect": sanitize_redirect(redirect_to) or DESTINO_POR_OMISION}


MENSAJE_ERROR_INTERNO = "No se pudo iniciar sesión por un error interno. Intenta de nuevo o avisa a Desarrollo."


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=10, seconds=60)
def entrar(numero_empleado: str | None = None, password: str | None = None, redirect_to: str | None = None):
    try:
        return _entrar(numero_empleado, password, redirect_to)
    except Exception:
        # Sin developer_mode, la traza no incluye variables locales (la contraseña no llega al log).
        # Nunca activar developer_mode en A.
        frappe.db.rollback()
        frappe.clear_messages()
        frappe.log_error(title="comunicalo_auth: error inesperado en el login")
        return _fallo(MENSAJE_ERROR_INTERNO)
    finally:
        frappe.form_dict.pop("password", None)


def _entrar(numero_empleado: str | None, password: str | None, redirect_to: str | None) -> dict:
    numero = identidad.normalizar_numero(numero_empleado)
    if not numero or not password:
        return _fallo(MENSAJE_FALTAN_DATOS)

    # Cuenta local de emergencia (decisión 0005): no pasa por el ERP.
    if numero == "ADMINISTRATOR":
        return _entrar_administrador(password, redirect_to)

    base_url, timeout = _config()
    if not base_url:
        return _fallo(MENSAJE_SIN_CONFIGURAR)

    login = erp.iniciar_sesion(base_url, numero, password, timeout, ip_cliente=frappe.local.request_ip)
    password = None  # noqa: F841  (se descarta; no se vuelve a usar)
    if not login.ok:
        return _fallo(login.mensaje)

    perfil = erp.obtener_perfil(base_url, login.token, timeout)
    login = erp.RespuestaLogin(  # se descarta el token
        True, "ok", numero_empleado=login.numero_empleado, nombre_completo=login.nombre_completo, permisos=login.permisos
    )

    usuario = _buscar_usuario(numero)
    if perfil.ok:
        usuario = _crear_o_actualizar(numero, perfil.datos, login.nombre_completo, usuario)
    elif perfil.motivo == "no_encontrado":
        return _fallo(MENSAJE_SIN_REGISTRO)
    elif not usuario:
        return _fallo(MENSAJE_PRIMERA_VEZ_SIN_PERFIL)
    # Perfil en mantenimiento o ERP sin respuesta: el usuario existente entra con sus datos guardados.

    if not frappe.db.get_value("User", usuario, "enabled"):
        return _fallo(MENSAJE_DESACTIVADO)

    frappe.local.login_manager.login_as(usuario)
    return _exito(redirect_to)


def _entrar_administrador(password: str, redirect_to: str | None) -> dict:
    login_manager = frappe.local.login_manager
    try:
        login_manager.authenticate(user="Administrator", pwd=password)
    except frappe.AuthenticationError:
        frappe.clear_messages()
        return _fallo(MENSAJE_ADMIN_INCORRECTO)
    login_manager.post_login()
    return _exito(redirect_to)


def _buscar_usuario(numero: str) -> str | None:
    encontrados = frappe.get_all("User", filters={"numero_empleado": numero}, pluck="name", limit=2)
    if len(encontrados) > 1:
        frappe.log_error(
            title="comunicalo_auth: número de empleado duplicado",
            message=f"Hay más de un usuario con numero_empleado={numero}: {encontrados}",
        )
    return encontrados[0] if encontrados else None


def _correo_libre(correo: str, usuario_actual: str | None) -> bool:
    otro = frappe.db.get_value("User", correo, ["name", "numero_empleado"], as_dict=True)
    if not otro:
        return True
    if otro.name == usuario_actual:
        return True
    return False


def _crear_o_actualizar(numero: str, perfil: dict, nombre_completo: str | None, usuario: str | None) -> str:
    correo = identidad.correo_para(perfil, numero)
    nombre, apellidos = identidad.nombre_y_apellidos(perfil, nombre_completo)
    empresa = (perfil.get("empresa_nombre") or "").strip()
    area = (perfil.get("area_nombre") or "").strip()

    if not usuario:
        existente = frappe.db.get_value("User", correo, ["name", "numero_empleado"], as_dict=True)
        if existente and (not existente.numero_empleado or existente.numero_empleado == numero):
            # Usuario dado de alta a mano con el mismo correo (por ejemplo, un administrador): se enlaza.
            usuario = existente.name
            frappe.db.set_value("User", usuario, "numero_empleado", numero)
        elif existente:
            correo = identidad.correo_tecnico(numero)

    if not usuario:
        return _crear_usuario(numero, correo, nombre, apellidos, empresa, area)

    # Cambió el correo en el ERP: se renombra el usuario sin perder su avance (decisión 0011).
    if usuario != correo and _correo_libre(correo, usuario):
        frappe.rename_doc("User", usuario, correo, force=True, show_alert=False)
        frappe.db.set_value("User", correo, "email", correo)
        usuario = correo

    doc = frappe.get_doc("User", usuario)
    cambios = {
        "first_name": nombre,
        "last_name": apellidos,
        "empresa_erp": empresa,
        "area_erp": area,
        "numero_empleado": numero,
    }
    if any((doc.get(campo) or "") != valor for campo, valor in cambios.items()) or not doc.has_role(ROL_ESTUDIANTE):
        doc.update(cambios)
        # Etapa 1 de roles (decisión 0011): se asegura el rol de estudiante; nunca se quitan
        # los roles de administrador asignados a mano.
        if ROL_ESTUDIANTE not in [r.role for r in doc.roles]:
            doc.append_roles(ROL_ESTUDIANTE)
        doc.flags.ignore_permissions = True
        doc.save()
    return usuario


def _crear_usuario(numero: str, correo: str, nombre: str, apellidos: str, empresa: str, area: str) -> str:
    doc = frappe.new_doc("User")
    doc.update(
        {
            "email": correo,
            "first_name": nombre,
            "last_name": apellidos,
            "username": identidad.username_para(numero),
            "user_type": "Website User",
            "send_welcome_email": 0,
            "enabled": 1,
            "numero_empleado": numero,
            "empresa_erp": empresa,
            "area_erp": area,
        }
    )
    # Sin contraseña local: el empleado solo puede entrar validando contra el ERP.
    doc.flags.no_welcome_mail = True
    doc.flags.ignore_permissions = True
    doc.append_roles(ROL_ESTUDIANTE)
    doc.insert()
    return doc.name
