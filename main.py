import json
from pathlib import Path

ARQUIVO_DADOS = Path(__file__).resolve().parent / "ativos.json"
TIPOS_ATIVOS = ["Notebook", "Roteador", "Servidor Web", "Impressora"]
SEVERIDADES = ["baixa", "média", "alta", "crítica"]
STATUS = ["aberta", "em tratamento", "corrigida", "risco aceito"]


def salvar_ativos(ativos):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(ativos, arquivo, ensure_ascii=False, indent=4)


def carregar_ativos():
    if not ARQUIVO_DADOS.exists():
        salvar_ativos([])
        return []
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        print("JSON vazio ou inválido. Iniciando sem cadastros.")
        salvar_ativos([])
        return []


def buscar_ativo(ativos, busca):
    for ativo in ativos:
        if str(ativo["id"]) == busca or ativo["nome"].lower() == busca.lower():
            return ativo
    return None


def cadastrar_ativo(ativos):
    id_ativo = input("ID numérico do ativo: ")
    for ativo in ativos:
        if ativo["id"] == id_ativo:
            print("Esse ID já está cadastrado.")
            return

    nome = input("Nome/hostname: ").strip()
    responsavel = input("Responsável: ").strip()
    localizacao = input("Setor/localização: ").strip()
    print("Tipos disponíveis:", ", ".join(TIPOS_ATIVOS))
    tipo = input("Tipo do ativo: ").strip()

    if not nome or not responsavel or not localizacao:
        print("Nome, responsável e localização não podem ficar vazios.")
        return
    if tipo not in TIPOS_ATIVOS:
        print("Tipo inválido.")
        return
    

    ativos.append({
        "id": id_ativo, "nome": nome, "responsavel": responsavel,
        "localizacao": localizacao, "tipo": tipo, "vulnerabilidades": []
    })
    salvar_ativos(ativos)
    print("Ativo cadastrado.")


def visualizar_ativos(ativos):
    if not ativos:
        print("Não há ativos cadastrados.")
        return
    for ativo in ativos:
        print("\nID:", ativo["id"], "| Nome:", ativo["nome"], "| Tipo:", ativo["tipo"])
        print("Responsável:", ativo["responsavel"], "| Localização:", ativo["localizacao"])


def editar_remover_ativo(ativos):
    ativo = buscar_ativo(ativos, input("ID ou hostname do ativo: ").strip())
    if ativo is None:
        print("Ativo não encontrado.")
        return

    print("1 - Alterar nome | 2 - Alterar responsável | 3 - Alterar localização")
    print("4 - Alterar tipo | 5 - Remover ativo")
    opcao = input("Escolha: ").strip()

    if opcao in ["1", "2", "3", "4"]:
        novo_valor = input("Novo valor: ").strip()
        if not novo_valor:
            print("O valor não pode ficar vazio.")
            return
        if opcao == "1":
            ativo["nome"] = novo_valor
        elif opcao == "2":
            ativo["responsavel"] = novo_valor
        elif opcao == "3":
            ativo["localizacao"] = novo_valor
        elif opcao == "4":
            if novo_valor not in TIPOS_ATIVOS:
                print("=== TIPO INVÁLIDO ===")
                return
        salvar_ativos(ativos)
        print("Ativo atualizado.")

    elif opcao == "5":
        if input("Confirma a remoção? (s/n): ").strip().lower() == "s":
            ativos.remove(ativo)
            salvar_ativos(ativos)
            print("Ativo e suas vulnerabilidades foram removidos.")
        else:
            print("Remoção cancelada.")
    else:
        print("Opção inválida.")


def cadastrar_vulnerabilidade(ativos):
    ativo = buscar_ativo(ativos, input("ID ou hostname do ativo: ").strip())
    if ativo is None:
        print("Ativo não encontrado.")
        return

    descricao = input("Descrição: ").strip()
    categoria = input("Categoria: ").strip()
    severidade = input("Severidade (baixa, média, alta, crítica): ").strip().lower()
    status = input("Status (aberta, em tratamento, corrigida, risco aceito): ").strip().lower()

    if not descricao or not categoria:
        print("Descrição e categoria não podem ficar vazias.")
        return
    if severidade not in SEVERIDADES or status not in STATUS:
        print("Severidade ou status inválido.")
        return

    ativo["vulnerabilidades"].append({
        "descricao": descricao, "categoria": categoria,
        "severidade": severidade, "status": status
    })
    salvar_ativos(ativos)
    print("Vulnerabilidade cadastrada.")


def visualizar_vulnerabilidades(ativos):
    ativo = buscar_ativo(ativos, input("ID ou hostname do ativo: ").strip())
    if ativo is None:
        print("Ativo não encontrado.")
        return
    if not ativo["vulnerabilidades"]:
        print("Este ativo não possui vulnerabilidades.")
        return

    numero = 1
    for vuln in ativo["vulnerabilidades"]:
        print("\nVulnerabilidade", numero, "-", vuln["descricao"])
        print("Categoria:", vuln["categoria"], "| Severidade:", vuln["severidade"], "| Status:", vuln["status"])
        numero += 1


def editar_remover_vulnerabilidade(ativos):
    ativo = buscar_ativo(ativos, input("ID ou hostname do ativo: ").strip())
    if ativo is None:
        print("Ativo não encontrado.")
        return

    vulnerabilidades = ativo["vulnerabilidades"]
    if not vulnerabilidades:
        print("Este ativo não possui vulnerabilidades.")
        return

    numero = 1
    for vuln in vulnerabilidades:
        print(numero, "-", vuln["descricao"])
        numero += 1
    numero = input("Número da vulnerabilidade: ")
    if numero < 1 or numero > len(vulnerabilidades):
        print("Número inválido.")
        return
    vuln = vulnerabilidades[numero - 1]

    print("1 - Alterar descrição | 2 - Alterar categoria")
    print("3 - Alterar severidade | 4 - Alterar status | 5 - Remover")
    opcao = input("Escolha: ").strip()

    if opcao in ["1", "2", "3", "4"]:
        novo_valor = input("Novo valor: ").strip()
        if not novo_valor:
            print("O valor não pode ficar vazio.")
            return
        if opcao == "1":
            vuln["descricao"] = novo_valor
        elif opcao == "2":
            vuln["categoria"] = novo_valor
        elif opcao == "3":
            if novo_valor.lower() not in SEVERIDADES:
                print("Severidade inválida.")
                return
            vuln["severidade"] = novo_valor.lower()
        else:
            if novo_valor.lower() not in STATUS:
                print("Status inválido.")
                return
            vuln["status"] = novo_valor.lower()
        salvar_ativos(ativos)
        print("Vulnerabilidade atualizada.")

    elif opcao == "5":
        if input("Confirma a remoção? (s/n): ").strip().lower() == "s":
            vulnerabilidades.remove(vuln)
            salvar_ativos(ativos)
            print("Vulnerabilidade removida.")
        else:
            print("Remoção cancelada.")
    else:
        print("Opção inválida.")


def interface_menu():
    print("\n--- MENU DE ATIVOS ---")
    print("1 - Cadastrar ativo")
    print("2 - Visualizar ativos")
    print("3 - Editar/remover ativo")
    print("4 - Cadastrar vulnerabilidade")
    print("5 - Visualizar vulnerabilidades")
    print("6 - Editar/remover vulnerabilidade")
    print("0 - Sair")


def menu_interativo():
    ativos = carregar_ativos()
    while True:
        interface_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_ativo(ativos)
        elif opcao == "2":
            visualizar_ativos(ativos)
        elif opcao == "3":
            editar_remover_ativo(ativos)
        elif opcao == "4":
            cadastrar_vulnerabilidade(ativos)
        elif opcao == "5":
            visualizar_vulnerabilidades(ativos)
        elif opcao == "6":
            editar_remover_vulnerabilidade(ativos)
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida. Digite de 0 a 6.")


menu_interativo()
