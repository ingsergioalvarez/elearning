app_name = "comunicalo_auth"
app_title = "Comunicalo Auth"
app_publisher = "Grupo Comunicalo - Desarrollo"
app_description = "Login de Comunicalo Learning con número de empleado y contraseña del ERP"
app_email = ""
app_license = "Propietaria"

after_install = "comunicalo_auth.instalacion.after_install"
after_migrate = "comunicalo_auth.instalacion.after_install"

doc_events = {
    "Email Queue": {
        "before_insert": "comunicalo_auth.correo.quitar_destinatarios_locales",
    },
}
