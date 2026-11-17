<!-- Um pequeno documento explicando o formato exato dos JSONs trocados entre o Python, o Prolog e o Lisp, para o relatório -->

# Contrato de Dados (JSON)
Este documento especifica a estrutura de retorno esperada pelo script Common Lisp (`intersecao.lisp`) quando chamado pelo  Python.

Exemplo de estrutura de saída gerada pelo Lisp:
```json
{
  "usuario_origem": "ana",
  "candidato": "daniela",
  "amigos_em_comum": ["bruno", "eduardo"],
  "total_em_comum": 2,
  "afinidade": 0.50
}