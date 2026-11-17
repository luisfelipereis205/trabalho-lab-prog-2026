# O módulo responsável por ler os dados, empacotar em JSON, chamar os processos externos do Prolog e do Lisp, e tratar os erros de fronteira

import json
import subprocess
from pathlib import Path


class OrquestradorMultiparadigma:
    # A classe OrquestradorMultiparadigma é responsável por orquestrar a integração entre o Python, Prolog e Lisp. Ela fornece métodos para consultar sugestões de conexões e caminhos entre usuários usando Prolog, bem como calcular afinidade entre usuários usando Lisp. A classe também lida com erros de fronteira, como a ausência dos interpretadores necessários no PATH do sistema.

    def __init__(self, raiz_projeto: str | Path):
        self.raiz = Path(raiz_projeto).resolve()
        self.arquivo_prolog = self.raiz / "prolog" / "rede_social.pl"
        self.arquivo_lisp = self.raiz / "lisp" / "intersecao.lisp"

    def consultar_sugestoes_prolog(self, usuario: str) -> list[str]:
        # Executa sugestoes_conexao(Usuario, L) no SWI-Prolog e retorna a lista de sugestões de conexões.
        usuario = usuario.lower().strip()
        goal = (
            f"sugestoes_conexao({usuario}, L), "
            f"atomic_list_concat(L, ',', Out), "
            f"writeln(Out), halt."
        )
        cmd = ["swipl", "-q", "-s", str(self.arquivo_prolog), "-g", goal]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            saida = res.stdout.strip()
            return [item for item in saida.split(",") if item]
        except FileNotFoundError:
            raise RuntimeError("SWI-Prolog ('swipl') não encontrado no PATH do sistema.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erro ao executar Prolog: {e.stderr}")

    def consultar_caminho_prolog(self, origem: str, destino: str) -> list[str]:
        # Executa caminho(Origem, Destino, Caminho) no SWI-Prolog.
        origem = origem.lower().strip()
        destino = destino.lower().strip()
        goal = (
            f"(caminho({origem}, {destino}, C) -> "
            f"atomic_list_concat(C, ',', Out), writeln(Out) ; writeln('')), halt."
        )
        cmd = ["swipl", "-q", "-s", str(self.arquivo_prolog), "-g", goal]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            saida = res.stdout.strip()
            return [item for item in saida.split(",") if item]
        except FileNotFoundError:
            raise RuntimeError("SWI-Prolog ('swipl') não encontrado no PATH do sistema.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erro ao executar Prolog: {e.stderr}")

    def calcular_afinidade_lisp(
        self, origem: str, candidato: str, amigos_a: list[str], amigos_b: list[str]
    ) -> dict:
        # Executa o módulo funcional Common Lisp (SBCL) e retorna o JSON parseado.
        str_amigos_a = ",".join(amigos_a)
        str_amigos_b = ",".join(amigos_b)

        cmd = [
            "sbcl",
            "--script",
            str(self.arquivo_lisp),
            origem.lower().strip(),
            candidato.lower().strip(),
            str_amigos_a,
            str_amigos_b,
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            # Pega a última linha não vazia (onde o JSON é impresso)
            linhas = [l.strip() for l in res.stdout.splitlines() if l.strip()]
            if not linhas:
                raise RuntimeError("O script Lisp não retornou saída.")
            return json.loads(linhas[-1])
        except FileNotFoundError:
            raise RuntimeError("SBCL ('sbcl') não encontrado no PATH do sistema.")
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Erro ao integrar com Common Lisp: {e}")