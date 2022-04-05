#  Test Coverage
import unittest


def dividir(a, b):
    if b == 0:
        return None
    return a // b


class TestDividir(unittest.TestCase):
    def test_divisao_por_1_retorna_o_proprio_numero(self):
        self.assertEqual(dividir(10, 1), 10)
        self.assertEqual(dividir(1, 1), 1)

    def test_divisao_por_zero_retorna_none(self):
        self.assertEqual(dividir(10, 0), None)

    def test_divisao_nao_inteira(self):
        self.assertEqual(dividir(5, 2), 2.5)


if __name__ == "__main__":
    unittest.main()
