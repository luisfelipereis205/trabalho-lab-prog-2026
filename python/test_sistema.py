# Arquivo de testes automatizados usando unittest ou pytest (exigido no edital).
import unittest
from pathlib import Path
from models import Usuario, RedeSocial
from orchestrator import OrquestradorMultiparadigma


class TestRedeSocialMultiparadigma(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raiz = Path(__file__).resolve().parent.parent
        cls.rede = RedeSocial(cls.raiz / "dados" / "usuarios.json")
        cls.orquestrador = OrquestradorMultiparadigma(cls.raiz)

    def test_carregamento_minimo_50_usuarios(self):
        usuarios = self.rede.listar_todos()
        self.assertGreaterEqual(len(usuarios), 50, "A base JSON deve conter pelo menos 50 usuários.")

    def test_modelo_usuario_encapsulamento(self):
        u = Usuario(99, "Teste", ["ana"], ["linux"])
        self.assertEqual(u.nome, "teste")
        self.assertTrue(u.adicionar_amigo("bruno"))
        self.assertFalse(u.adicionar_amigo("ana"))  # Evita duplicata
        self.assertFalse(u.adicionar_amigo("teste"))  # Evita auto-amizade

    def test_integracao_prolog_sugestoes(self):
        sugestoes = self.orquestrador.consultar_sugestoes_prolog("ana")
        self.assertIn("daniela", sugestoes)
        self.assertIn("fernanda", sugestoes)
        self.assertIn("eduardo", sugestoes)

    def test_integracao_prolog_caminho(self):
        caminho = self.orquestrador.consultar_caminho_prolog("ana", "gabriel")
        self.assertEqual(caminho, ["ana", "bruno", "daniela", "gabriel"])

    def test_integracao_lisp_afinidade(self):
        resultado = self.orquestrador.calcular_afinidade_lisp(
            "ana", "daniela", ["bruno", "carlos", "eduardo"], ["bruno", "gabriel", "eduardo"]
        )
        self.assertEqual(resultado["total_em_comum"], 2)
        self.assertEqual(resultado["amigos_em_comum"], ["bruno", "eduardo"])
        self.assertAlmostEqual(resultado["afinidade"], 0.50, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)