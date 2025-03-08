import unittest
from entidades.fuente import FuenteMonocromatica
from utilidades.aleatorios import GenerateRandomNormalPosition2D
import numpy as np

class TestFuenteMonocromatica(unittest.TestCase):

  def setUp(self):
    self.frecuencia = 500
    self.origen = 0
    self.fuente = FuenteMonocromatica(self.frecuencia, self.origen)

  def test_constructor(self):
    self.assertEqual(self.fuente.frecuencia, self.frecuencia)
    self.assertEqual(self.fuente.origen, self.origen)
    self.assertEqual(self.fuente.dispersion_pos, GenerateRandomNormalPosition2D)
    self.assertIsNone(self.fuente.dispersion_ang)

  def test_emitir(self):
    foton = self.fuente.emitir(1)
    self.assertEqual(foton.f, self.frecuencia)
    self.assertEqual(foton.pos[1], self.origen)
    self.assertEqual(len(self.fuente.fotones), 1)

  def test_emitirN(self):
    N = 10
    fotones = self.fuente.emitirN(N, 0, 5, np.pi/2, np.pi/4)
    self.assertEqual(len(fotones), N)
    self.assertEqual(len(self.fuente.fotones), N)

if __name__ == '__main__':
  unittest.main()