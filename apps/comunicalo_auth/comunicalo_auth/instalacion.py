"""Instalación y migración de comunicalo_auth. Idempotente: corre en after_install y after_migrate."""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

CAMPOS_USUARIO = {
    "User": [
        {
            "fieldname": "numero_empleado",
            "label": "Número de empleado",
            "fieldtype": "Data",
            "insert_after": "username",
            "read_only": 1,
            "no_copy": 1,
            "search_index": 1,
            "description": "Identidad del empleado en el ERP (decisión 0011). Lo llena el login.",
        },
        {
            "fieldname": "empresa_erp",
            "label": "Empresa (ERP)",
            "fieldtype": "Data",
            "insert_after": "numero_empleado",
            "read_only": 1,
            "no_copy": 1,
        },
        {
            "fieldname": "area_erp",
            "label": "Área (ERP)",
            "fieldtype": "Data",
            "insert_after": "empresa_erp",
            "read_only": 1,
            "no_copy": 1,
        },
    ]
}


def after_install():
    create_custom_fields(CAMPOS_USUARIO, update=True)
    # Solo entran empleados validados por el ERP: nadie se registra por su cuenta.
    frappe.db.set_single_value("Website Settings", "disable_signup", 1)
