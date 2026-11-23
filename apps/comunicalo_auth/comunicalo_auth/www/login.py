"""Contexto de la página /login propia (reemplaza la de Frappe sin modificar su código)."""

import frappe
from frappe.www.login import sanitize_redirect

no_cache = 1
sitemap = 0

DESTINO_POR_OMISION = "/lms"


def get_context(context):
    redirect_to = sanitize_redirect(frappe.local.request.args.get("redirect-to"))

    if frappe.session.user != "Guest":
        frappe.local.flags.redirect_location = redirect_to or DESTINO_POR_OMISION
        raise frappe.Redirect

    context.no_header = True
    context.no_breadcrumbs = True
    context.show_sidebar = False
    context.for_test = "login.html"
    context.title = "Iniciar sesión"
    context.hide_login = True
    context.redirect_to = redirect_to or DESTINO_POR_OMISION
    return context
