"""Pruebas de las reglas de identidad (decisión 0011). No usan red ni Frappe."""

import unittest

from comunicalo_auth import identidad


class PruebasIdentidad(unittest.TestCase):
    def test_normalizar_como_el_erp(self):
        self.assertEqual(identidad.normalizar_numero(" ab 12\t3 "), "AB123")
        self.assertEqual(identidad.normalizar_numero(None), "")

    def test_correo_tecnico(self):
        self.assertEqual(identidad.correo_tecnico("1234"), "1234@empleados.grupocomunicalo.local")
        self.assertEqual(identidad.correo_tecnico("ab/12"), "ab-12@empleados.grupocomunicalo.local")

    def test_correo_corporativo_si_existe(self):
        perfil = {"correo_corporativo": "  Ana@GrupoComunicalo.mx "}
        self.assertEqual(identidad.correo_para(perfil, "1234"), "ana@grupocomunicalo.mx")

    def test_correo_tecnico_si_no_hay_o_es_invalido(self):
        for valor in (None, "", "sin-arroba", "x@y.local"):
            self.assertEqual(identidad.correo_para({"correo_corporativo": valor}, "77"), "77@empleados.grupocomunicalo.local")

    def test_es_correo_local(self):
        self.assertTrue(identidad.es_correo_local("1@empleados.grupocomunicalo.LOCAL"))
        self.assertFalse(identidad.es_correo_local("ana@grupocomunicalo.mx"))
        self.assertFalse(identidad.es_correo_local(None))

    def test_nombre_y_apellidos(self):
        perfil = {"nombres": "Ana María", "apellido_paterno": "López", "apellido_materno": ""}
        self.assertEqual(identidad.nombre_y_apellidos(perfil), ("Ana María", "López"))
        self.assertEqual(identidad.nombre_y_apellidos({}, "Luis Pérez Gómez"), ("Luis", "Pérez Gómez"))
        self.assertEqual(identidad.nombre_y_apellidos({}), ("Empleado", ""))

    def test_username(self):
        self.assertEqual(identidad.username_para("12345"), "12345")
        self.assertEqual(identidad.username_para("15"), "emp15")


if __name__ == "__main__":
    unittest.main()
