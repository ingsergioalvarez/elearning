"""Evita mandar correos a direcciones técnicas .local (decisión 0011).

Se engancha a Email Queue (before_insert): quita esos destinatarios. Si no queda ninguno, el
correo se marca como enviado con una nota, para que no se reintente ni llene la cola de errores.
"""

from comunicalo_auth.identidad import es_correo_local

NOTA_OMITIDO = "Omitido por comunicalo_auth: todos los destinatarios eran direcciones técnicas .local."


def quitar_destinatarios_locales(doc, method=None):
    destinatarios = list(doc.get("recipients") or [])
    restantes = [r for r in destinatarios if not es_correo_local(r.recipient)]
    if len(restantes) == len(destinatarios):
        return

    for i, fila in enumerate(restantes, start=1):
        fila.idx = i
    doc.set("recipients", restantes)

    if not restantes:
        doc.status = "Sent"
        doc.error = NOTA_OMITIDO
