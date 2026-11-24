# O ponto de entrada único do sistema. É o script que o utilizador executa no terminal para interagir com a aplicação.

from pathlib import Path
import json
from models import RedeSocial
from orchestrator import OrquestradorMultiparadigma


def exibir_menu() -> None:
    
    print("      REDE SOCIAL MULTIPARADIGM - MENU PRINCIPAL")
    print("-" * 55)
    print("1. Listar usuários cadastrados")
    print("2. Consultar perfil de um usuário")
    print("3. Sugerir conexões + Afinidade")
    print("4. Calcular grau de separação / caminho")
    print("5. Comparar afinidade direta entre dois usuários")
    print("0. Sair")
    print("-" * 55)


def main() -> None:
    raiz = Path(__file__).resolve().parent.parent
    rede = RedeSocial(raiz / "dados" / "usuarios.json")
    orquestrador = OrquestradorMultiparadigma(raiz)

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- LISTA DE USUÁRIOS (50 Registros) ---")
            try:
                # Usa diretamente o método da classe RedeSocial para obter a lista de utilizadores
                # (Se o teu método se chamar diferente, adaptamos, mas 'rede.usuarios' ou 'rede.obter_usuarios()' é o padrão)
                usuarios = list(rede.usuarios.values()) if isinstance(rede.usuarios, dict) else rede.usuarios
                
                total = len(usuarios)
                bloco = 15
                
                for i in range(0, total, bloco):
                    sublote = usuarios[i:i + bloco]
                    for idx, u in enumerate(sublote, start=i + 1):
                        # Extrai o nome independentemente de ser objeto ou dicionário
                        nome = getattr(u, 'nome', None) or (u.get('nome') if isinstance(u, dict) else str(u))
                        print(f"{idx}. {nome.capitalize()}")
                    
                    if i + bloco < total:
                        continuar = input("\nPressiona [Enter] para ver mais ou 'q' para voltar ao menu: ").strip().lower()
                        if continuar == 'q':
                            break
            except Exception as e:
                print(f"Erro ao listar utilizadores: {e}")
            
            print("\n----------------------------------------")
        
        elif opcao == "2":
            nome = input("Digite o nome do usuário: ").strip()
            usuario = rede.buscar_usuario(nome)
            if not usuario:
                print("Usuário não encontrado.")
            else:
                print(f"\nPerfil de {usuario.nome.capitalize()} (ID: {usuario.id}):")
                print(f"   Amigos diretos : {', '.join(usuario.amigos) or 'Nenhum'}")
                print(f"   Interesses     : {', '.join(usuario.interesses) or 'Nenhum'}")

        elif opcao == "3":
            nome = input("Gerar recomendações para qual usuário? (ex: ana): ").strip()
            usuario = rede.buscar_usuario(nome)
            if not usuario:
                print("Usuário não encontrado na base JSON.")
                continue

            try:
                # 1. Prolog infere candidatos (amigos de amigos via findall/3)
                sugestoes = orquestrador.consultar_sugestoes_prolog(usuario.nome)
                if not sugestoes:
                    print(f"\nNenhuma sugestão encontrada em Prolog para '{usuario.nome}'.")
                    continue

                print(f"\nSugestões geradas pelo Prolog para {usuario.nome.capitalize()}:")
                resultados_ranqueados = []

                # 2. Common Lisp calcula interseção e coeficiente de Jaccard de cada candidato
                for cand_nome in sugestoes:
                    cand_obj = rede.buscar_usuario(cand_nome)
                    amigos_cand = cand_obj.amigos if cand_obj else []
                    analise = orquestrador.calcular_afinidade_lisp(
                        usuario.nome, cand_nome, usuario.amigos, amigos_cand
                    )
                    resultados_ranqueados.append(analise)

                # Ordena pela maior afinidade calculada pelo Lisp
                resultados_ranqueados.sort(key=lambda x: x["afinidade"], reverse=True)

                for r in resultados_ranqueados:
                    comuns = ", ".join(r["amigos_em_comum"]) or "nenhum"
                    print(
                        f"  -> {r['candidato'].capitalize()} | "
                        f"Afinidade (Jaccard): {r['afinidade']:.2f} | "
                        f"Amigos em comum ({r['total_em_comum']}): {comuns}"
                    )
            except RuntimeError as erro:
                print(f"\n[Erro de Integração] {erro}")

        elif opcao == "4":
            origem = input("Usuário de origem (ex: ana): ").strip()
            destino = input("Usuário de destino (ex: gabriel): ").strip()
            try:
                caminho = orquestrador.consultar_caminho_prolog(origem, destino)
                if caminho:
                    graus = len(caminho) - 1  # Grau de separação (arestas)
                    rota = " -> ".join(p.capitalize() for p in caminho)
                    print(f"\nCaminho encontrado ({graus} grau(s) de separação):")
                    print(f"  {rota}")
                else:
                    print("\nNão existe caminho de amizade entre esses usuários no Prolog.")
            except RuntimeError as erro:
                print(f"\n[Erro de Integração] {erro}")

        elif opcao == "5":
            nome_a = input("Primeiro usuário (ex: ana): ").strip()
            nome_b = input("Segundo usuário (ex: daniela): ").strip()
            user_a = rede.buscar_usuario(nome_a)
            user_b = rede.buscar_usuario(nome_b)

            if not user_a or not user_b:
                print("Um ou ambos os usuários não existem no JSON.")
                continue

            try:
                analise = orquestrador.calcular_afinidade_lisp(
                    user_a.nome, user_b.nome, user_a.amigos, user_b.amigos
                )
                print("\nResultado retornado pelo Common Lisp:")
                print(f"   Amigos em comum : {analise['amigos_em_comum']}")
                print(f"   Total em comum  : {analise['total_em_comum']}")
                print(f"   Afinidade       : {analise['afinidade']:.2f}")
            except RuntimeError as erro:
                print(f"\n[Erro de Integração] {erro}")

        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()