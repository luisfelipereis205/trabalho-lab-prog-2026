# Onde ficam as classes exigidas pelo tema de Redes Sociais: Usuario e Conexao.

import json
from pathlib import Path


class Usuario: # Aqui é a classe que representa um usuário na rede social. Ela possui atributos como id, nome, amigos e interesses, além de métodos para acessar esses atributos e adicionar amigos.

    def __init__(self, user_id: int, nome: str, amigos: list[str], interesses: list[str]):
        self._id = user_id
        self._nome = nome.lower().strip()
        self._amigos = list(amigos)
        self._interesses = list(interesses)

    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def amigos(self) -> list[str]:
        return list(self._amigos)

    @property
    def interesses(self) -> list[str]:
        return list(self._interesses)

    def adicionar_amigo(self, nome_amigo: str) -> bool:
        nome_amigo = nome_amigo.lower().strip()
        if nome_amigo != self._nome and nome_amigo not in self._amigos:
            self._amigos.append(nome_amigo)
            return True
        return False
    def para_dicionario(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "amigos": self._amigos,
            "interesses": self._interesses,
        }

    def __repr__(self) -> str:
        return f"Usuario(id={self._id}, nome='{self._nome}', amigos={len(self._amigos)})"


class RedeSocial:
    # A classe RedeSocial é responsável por gerenciar os usuários da rede social. Ela carrega os dados de um arquivo JSON, permite buscar usuários por nome, listar todos os usuários e salvar os dados de volta no arquivo JSON.

    def __init__(self, caminho_json: str | Path):
        self.caminho_json = Path(caminho_json)
        self.usuarios: dict[str, Usuario] = {}
        self.carregar_dados()

    def carregar_dados(self) -> None:
        if not self.caminho_json.exists():
            raise FileNotFoundError(f"Arquivo de dados não encontrado: {self.caminho_json}")

        with open(self.caminho_json, "r", encoding="utf-8") as f:
            conteudo = json.load(f)

        self.usuarios.clear()
        for item in conteudo.get("usuarios", []):
            usuario = Usuario(
                user_id=item["id"],
                nome=item["nome"],
                amigos=item.get("amigos", []),
                interesses=item.get("interesses", []),
            )
            self.usuarios[usuario.nome] = usuario

    def buscar_usuario(self, nome: str) -> Usuario | None:
        return self.usuarios.get(nome.lower().strip())

    def listar_todos(self) -> list[Usuario]:
        return list(self.usuarios.values())

    def salvar_dados(self) -> None:
        dados = {"usuarios": [u.para_dicionario() for u in self.usuarios.values()]}
        with open(self.caminho_json, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)