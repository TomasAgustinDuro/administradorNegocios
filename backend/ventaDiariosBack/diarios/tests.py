from django.forms import ValidationError
from django.test import TestCase
from .models import DiarioVendido

class DiarioVendidoTest(TestCase):

    def test_nombre_requerido(self):
        diario = DiarioVendido(nombre="", valor=100)
        with self.assertRaises(ValidationError):
            diario.full_clean()

    def test_valor_invalido(self):
        diario = DiarioVendido(nombre="El Diario", valor=-1)  # Valor negativo
        with self.assertRaises(ValidationError):
            diario.full_clean()

    def test_valor_valido(self):
        diario = DiarioVendido(nombre="El Diario", valor=100)
        try:
            diario.full_clean()
        except ValidationError:
            self.fail("El valor debería ser válido")
