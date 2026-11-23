"""Pruebas del cliente del ERP con respuestas simuladas (decisión 0010). No usan red ni Frappe.

Correr:  python -m unittest discover -s comunicalo_auth/tests -t .
"""

import unittest

import requests

from comunicalo_auth import erp

BASE = "https://erp.ejemplo/"
PASSWORD = "Secreta-123"
TOKEN = "jwt.de.prueba"


class RespuestaFalsa:
    def __init__(self, status_code, cuerpo=None, json_invalido=False):
        self.status_code = status_code
        self._cuerpo = cuerpo
        self._json_invalido = json_invalido

    def json(self):
        if self._json_invalido:
            raise ValueError("no es JSON")
        return self._cuerpo


class SesionFalsa:
    """Imita requests: guarda la llamada y regresa una respuesta o lanza una excepción."""

    def __init__(self, respuesta=None, excepcion=None):
        self.respuesta = respuesta
        self.excepcion = excepcion
        self.llamadas = []

    def _responder(self, metodo, url, **kwargs):
        self.llamadas.append((metodo, url, kwargs))
        if self.excepcion:
            raise self.excepcion
        return self.respuesta

    def post(self, url, **kwargs):
        return self._responder("POST", url, **kwargs)

    def get(self, url, **kwargs):
        return self._responder("GET", url, **kwargs)


def login_200():
    return RespuestaFalsa(
        200,
        {
            "success": True,
            "message": "Inicio de sesión exitoso",
            "data": {
                "token": TOKEN,
                "empleado": {
                    "id": 15,
                    "numero_empleado": "1234",
                    "nombre_completo": "Ana López Pérez",
                    "roles": ["X"],
                    "permisos": ["ELEARNING_VER", 7],
                },
            },
        },
    )


class PruebasLogin(unittest.TestCase):
    def _login(self, sesion, ip=None):
        return erp.iniciar_sesion(BASE, "1234", PASSWORD, 10, ip_cliente=ip, session=sesion)

    def assertSinSecretos(self, resultado):
        texto = repr(resultado) + resultado.mensaje
        self.assertNotIn(PASSWORD, texto)
        self.assertNotIn(TOKEN, texto)

    def test_200_exitoso(self):
        sesion = SesionFalsa(login_200())
        r = self._login(sesion, ip="201.1.2.3")
        self.assertTrue(r.ok)
        self.assertEqual(r.motivo, "ok")
        self.assertEqual(r.token, TOKEN)
        self.assertEqual(r.numero_empleado, "1234")
        self.assertEqual(r.permisos, ("ELEARNING_VER",))
        self.assertNotIn(TOKEN, repr(r))
        metodo, url, kwargs = sesion.llamadas[0]
        self.assertEqual((metodo, url), ("POST", "https://erp.ejemplo/api/auth/login"))
        self.assertEqual(kwargs["json"], {"numero_empleado": "1234", "password": PASSWORD})
        self.assertEqual(kwargs["timeout"], 10)
        self.assertEqual(kwargs["headers"]["X-Forwarded-For"], "201.1.2.3")

    def test_400_muestra_mensaje_del_erp(self):
        r = self._login(SesionFalsa(RespuestaFalsa(400, {"success": False, "message": "Faltan datos"})))
        self.assertFalse(r.ok)
        self.assertEqual((r.motivo, r.mensaje), ("rechazado", "Faltan datos"))
        self.assertSinSecretos(r)

    def test_401_intentos_restantes(self):
        r = self._login(SesionFalsa(RespuestaFalsa(401, {"success": False, "message": "Credenciales inválidas. Intentos restantes: 2"})))
        self.assertEqual(r.motivo, "rechazado")
        self.assertIn("Intentos restantes: 2", r.mensaje)
        self.assertSinSecretos(r)

    def test_401_sin_mensaje(self):
        r = self._login(SesionFalsa(RespuestaFalsa(401, json_invalido=True)))
        self.assertEqual((r.motivo, r.mensaje), ("rechazado", erp.MENSAJE_RECHAZO_GENERICO))

    def test_403_bloqueado(self):
        r = self._login(SesionFalsa(RespuestaFalsa(403, {"success": False, "message": "Cuenta bloqueada."})))
        self.assertEqual(r.motivo, "bloqueado")
        self.assertEqual(r.mensaje, "Cuenta bloqueada. " + erp.MENSAJE_BLOQUEO)

    def test_500_erp_no_disponible(self):
        r = self._login(SesionFalsa(RespuestaFalsa(500, {"message": "Error interno con datos"})))
        self.assertEqual((r.motivo, r.mensaje), ("erp_no_disponible", erp.MENSAJE_ERP_NO_DISPONIBLE))

    def test_timeout(self):
        r = self._login(SesionFalsa(excepcion=requests.Timeout(f"timeout con {PASSWORD}")))
        self.assertEqual(r.motivo, "erp_no_disponible")
        self.assertSinSecretos(r)

    def test_sin_conexion(self):
        r = self._login(SesionFalsa(excepcion=requests.ConnectionError("sin conexión")))
        self.assertEqual(r.motivo, "erp_no_disponible")

    def test_200_sin_token(self):
        r = self._login(SesionFalsa(RespuestaFalsa(200, {"success": True, "data": {"empleado": {}}})))
        self.assertEqual(r.motivo, "erp_no_disponible")

    def test_200_no_json(self):
        r = self._login(SesionFalsa(RespuestaFalsa(200, json_invalido=True)))
        self.assertEqual(r.motivo, "erp_no_disponible")

    def test_200_cuerpo_lista(self):
        r = self._login(SesionFalsa(RespuestaFalsa(200, ["raro"])))
        self.assertEqual(r.motivo, "erp_no_disponible")

    def test_405_pagina_equivocada(self):
        r = self._login(SesionFalsa(RespuestaFalsa(405, json_invalido=True)))
        self.assertEqual(r.motivo, "erp_no_disponible")

    def test_mensaje_largo_se_recorta(self):
        r = self._login(SesionFalsa(RespuestaFalsa(401, {"message": "x" * 1000})))
        self.assertEqual(len(r.mensaje), erp.LARGO_MAXIMO_MENSAJE)


class PruebasPerfil(unittest.TestCase):
    def _perfil(self, sesion):
        return erp.obtener_perfil(BASE, TOKEN, 10, session=sesion)

    def test_200_solo_campos_necesarios(self):
        datos = {
            "numero_empleado": "1234",
            "nombres": "Ana",
            "apellido_paterno": "López",
            "apellido_materno": "Pérez",
            "correo_corporativo": "ana@grupocomunicalo.mx",
            "empresa_nombre": "Comunicalo",
            "area_nombre": "Ventas",
            "salario": 99999,
            "curp": "XXXX",
            "rfc": "YYYY",
        }
        sesion = SesionFalsa(RespuestaFalsa(200, {"success": True, "data": datos}))
        r = self._perfil(sesion)
        self.assertTrue(r.ok)
        self.assertEqual(set(r.datos), set(erp.CAMPOS_PERFIL))
        self.assertNotIn("salario", r.datos)
        metodo, url, kwargs = sesion.llamadas[0]
        self.assertEqual((metodo, url), ("GET", "https://erp.ejemplo/api/rh/mi-perfil"))
        self.assertEqual(kwargs["headers"]["Authorization"], f"Bearer {TOKEN}")

    def test_503_mantenimiento(self):
        self.assertEqual(self._perfil(SesionFalsa(RespuestaFalsa(503, {}))).motivo, "mantenimiento")

    def test_404_no_encontrado(self):
        self.assertEqual(self._perfil(SesionFalsa(RespuestaFalsa(404, {}))).motivo, "no_encontrado")

    def test_401_no_encontrado(self):
        self.assertEqual(self._perfil(SesionFalsa(RespuestaFalsa(401, {}))).motivo, "no_encontrado")

    def test_timeout(self):
        self.assertEqual(self._perfil(SesionFalsa(excepcion=requests.Timeout())).motivo, "erp_no_disponible")

    def test_500(self):
        self.assertEqual(self._perfil(SesionFalsa(RespuestaFalsa(500, {}))).motivo, "erp_no_disponible")

    def test_200_sin_data(self):
        self.assertEqual(self._perfil(SesionFalsa(RespuestaFalsa(200, {"success": True}))).motivo, "erp_no_disponible")


if __name__ == "__main__":
    unittest.main()
