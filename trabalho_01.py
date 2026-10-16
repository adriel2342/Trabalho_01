import json
from pathlib import Path

ARQUIVOS_DADOS = Path(__file__).resolve().parent /"ativos.json"

TIPOS_ATIVOS = ["notebook" , "roteador", "servidor Web", "impressora"]
SEVERIDADE =["baixa", "media", "alta", "critica"]
STATUS = ["aberta", "em tratamento", "corrigida", "risco aceito"]
CATEGORIAS_VULN = ["rede","software","hardware", "CONFIGURACAO  "] 


def salvar_ativo(ativos):
    with open(ARQUIVOS_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(ativos, arquivo, ensure_ascii=False, indent=4)

def carregar_ativos():
    if not ARQUIVOS_DADOS.exists():
        salvar_ativo([])
        return
    with open (ARQUIVOS_DADOS, "r", encoding= "utf-8") as arquivo:
        return json.load(arquivo)
    
# área relacionada a busca de algum ativo   
    

def buscar_ativo(ativos, busca):
    for ativo in ativos:
        if str(ativo["id"]) == busca or ativo["nome"].lower() == busca.lower():
            return ativo

    print("=== ATIVO NAO ENCONTRADO ===")
    return None

def id_ativo_mostrar(ativos):
    for ativo in ativos:
        print("ID", ativo ["id"], "NOME", ativo["nome"])

    
def cadastrar_ativo(ativos):
    print("=== ESSES SAO OS IDS CADASTRADOS ===")
    id_ativo_mostrar(ativos)
    id_ativo = input("ADICIONE UM ID PARA O ATIVO: ").strip()
    for ativo in ativos:
        if ativo ["id"] == id_ativo:
            print("=== ID PREVIAMENTE CADASTRADO ===")
            return

    nome = input("CADASTRE O HOSTNAME DO ATIVO: ").strip()
    responsavel = input ("CADASTRE O RESPONSAVEL PELO ATIVO: ")
    ip_ativo = input("CADASTRE O IP DO ATIVO: ")

    print("tipos disponiveis:", ", ".join(TIPOS_ATIVOS))
    tipo = input("TIPO DO ATIVO: ").strip()
    if not nome or not responsavel or not ip_ativo:
            print("=== OS CAMPOS ACIMA NÃO DEVEM FICAR EM BRANCO ===")
            return
    if tipo not in TIPOS_ATIVOS:
            print("=== TIPO INVÁLIDO === ")
            return

    print("=== CONFIRMAÇÃO ATIVOS ===")
    print(f"ESSE E O: {id_ativo}?" )
    print(f"ESSE É O {nome}?")
    print(f"ESSE É O {responsavel}?")
    print(f"ESSE É O {ip_ativo}")
    print(f"ESSE É O {tipo}?")

    confirmacao = input("PREENCHA COM sim OU nao:").strip().lower()

    if confirmacao == "sim" or confirmacao == "s":
        #parte para salvar no arquivo json
        ativo ={
            "ativo": [],
            "id": id_ativo,
            "nome": nome,
            "responsavel" : responsavel,
            "ip" : ip_ativo,
            "tipo" : tipo,
            "vulnerabilidades": []

        }
        ativos.append(ativo) 

        salvar_ativo(ativos) 

        print("=== CADASTRO CONCLUÍDO ===")

    elif confirmacao == "nao" or confirmacao == "n":
        print("=== REALIZE NOVAMENTE O CADASTRO ===")
        return
    
    else:
        print("=== RESPONDA COM SIM OU NAO ===")
        return


def visualizar_ativo(ativos):
    if not ativos:
        print("=== NAO HA ATIVOS CADASTRADOS ===")
    for ativo in ativos:
        print("\nID:", ativo["id"], "| Nome:", ativo["nome"], "| Tipo:", ativo["tipo"])
        print("Responsável:", ativo["responsavel"], "| ip:", ativo["ip"])
        

def editar_remover_ativo(ativos):
    print("=== ESSES SAO OS IDS CADASTRADOS ===")
    id_ativo_mostrar(ativos)
    ativo = buscar_ativo(ativos, input("INSIRA O id OU O nome do ativo: " ).strip())
    if ativo is None:
        print("=== ATIVO NAO LOCALIZADO ===")
        return
    
    print("1 - Alterar nome | 2 - Alterar responsável | 3 - Alterar ip")
    print("4 - Alterar tipo | 5 - Remover ativo")
    opcao = input("SELECIONE UM DOS NUMEROS ACIMA: ")
    if opcao in ["1", "2", "3","4"]:
        novo_valor = input("NOVO VALOR: ").strip()
        if not novo_valor:
            print("=== ESSE CAMPO NAO PODE FICAR EM BRANCO ===")
            return
        if opcao == "1":
            if novo_valor == ativo["nome"]:
                print("=== VALOR JÁ PREVIAMENTE CADASTRADO ===")
            else:
                ativo ["nome"] = novo_valor
        
        elif opcao == "2":
            if novo_valor == ativo["responsavel"]:
                print("=== VALOR JÁ PREVIAMENTE CADASTRADO ===")
            else:
                ativo ["responsavel"] = novo_valor
        elif opcao == "3":
            if novo_valor == ativo["ip"]:
                print("=== VALOR JÁ PREVIAMENTE CADASTRADO ===")
            else:
                ativo["id"] = novo_valor
        elif opcao == "4":
           if novo_valor not in TIPOS_ATIVOS:
                print("=== TIPO INVÁLIDO ===")
                return
           ativo["tipo"] = novo_valor
        
        salvar_ativo(ativos)
        print("=== ATIVO ATUALIZADO ===")
    elif opcao == "5":
        if input("CONFIRMAR REMOÇAO DO ATIVO? (s/n): ").strip().lower() == "s":
            ativos.remove(ativo)
            salvar_ativo(ativos)
            print("Ativo e suas vulnerabilidades foram removidos.")
        else:
            print("Remoção cancelada.")
    else:
        print("Opção inválida.")
        
        
def cadastrar_vuln(ativos):
    print("=== ESSES SÃO OS IDS CADASTRADOS ===")
    id_ativo_mostrar(ativos)
    ativo = buscar_ativo(ativos, input("ID ou hostname do ativo: ").strip())
    if ativo is None:
        print("Ativo não encontrado.")
        return

    descricao = input("Descrição: ").strip()
    categoria = input("Categoria: ").strip()
    if categoria not in CATEGORIAS_VULN:
        print("=== CATEGORIA ERRADA ===")
        return
    severidade = input("Severidade (baixa, média, alta, crítica): ").strip().lower()
    status = input("Status (aberta, em tratamento, corrigida, risco aceito): ").strip().lower()

    if not descricao or not categoria:
        print("Descrição e categoria não podem ficar vazias.")
        return
    if severidade not in SEVERIDADE or status not in STATUS:
        print("Severidade ou status inválido.")
        return
    
    print("=== CONFIRMACAO ===")
    print(f"A descricao: {descricao} esta correta?")
    print(f"A categoria: {categoria} esta correta?")
    print(f"A severidade: {severidade} esta correta?")
    print(f"O status: {status} esta correto?")
    confirmacao = input("=== RESPONDA COM s/n: ").strip().lower()
    
    if confirmacao == "s" or confirmacao ==  "sim":

        ativo  ["vulnerabilidades"].append({
            "descricao": descricao, 
            "categoria": categoria,
            "severidade": severidade, 
            "status": status

        })
        salvar_ativo(ativos)
        print("=== VULNERABILIDADE CADASTRADA ===.")

    elif confirmacao == "n" or confirmacao == "nao":
        print("=== CADASTRE NOVAMENTE ===")
        return
    else:
        print("=== RESPONDA COM s/n ===")

def visualizar_vuln(ativos):
    print("=== ESSES SAO OS IDS CADASTRADOS ===")
    id_ativo_mostrar(ativos)
    ativo = buscar_ativo(ativos, input("=== DIGITE O ID DO ATIVO:  ").strip())
    if buscar_ativo is None:
        print("=== ATIVO NAO ENCONTRADO ===")
        return
    if not ativo["vulnerabilidades"]:
        print("=== ESSE ATIVO NÃO POSSUI VULNERABILIDADES ===")
        return
    numero = 1
    for vuln in ativo["vulnerabilidades"]:
        print("Vulnerabilidade", numero, "-", vuln["descricao"])
        print("Categoria:", vuln["categoria"], "| Severidade:", vuln["severidade"], "| Status:", vuln["status"])
        numero += 1

def editar_remover_vuln(ativos):
    print("=== ESSES SAO OS IDS CADASTRADO===")
    id_ativo_mostrar(ativos)
    ativo = buscar_ativo( ativos, input("=== DIGITE O ID DO ATIVO: ").strip())
    if buscar_ativo is None:
        print("ATIVO NAO ENCONTRADO")
        return
    if ativo is None:
        return
    vulnerabilidades = ativo["vulnerabilidades"]
    if not vulnerabilidades:
        print("=== NAO HA VULNERABILIDADES REFERENTES A ESSE ATIVO ===")
        return
    numero = 1
    for vuln in vulnerabilidades:
        print(numero, "-", vuln["descricao"])
        numero += 1
        numero = int(input("Número da vulnerabilidade: ").strip())
    if numero < 1 or numero > len(vulnerabilidades):
        print("Número inválido.")
        return
    vuln = vulnerabilidades[numero - 1] 

    print("1 - Alterar descrição | 2 - Alterar categoria")
    print("3 - Alterar severidade | 4 - Alterar status | 5 - Remover")
    opcao = input("Escolha: ").strip()

    if opcao in ["1", "2", "3", "4"]: 
        novo_valor = input("=== NOVO VALOR: ").strip()
        if not novo_valor:
            print("=== O VALOR NAO PODE FICAR EM BRANCO ===")
            return
        if opcao == "1":
            if novo_valor == vuln["descricao"]:
                print("=== VAL0R JÁ PREVIAMENTE CADASTRADO ===")
                return
            else:
                vuln ["descricao"] = novo_valor

        elif opcao == "2":
            if novo_valor .lower() not in CATEGORIAS_VULN:
                print("=== CATEGORIA INVÁLIDA ===")
                return
            if novo_valor ==  vuln["categoria"]:
                print("=== VAL0R JÁ PREVIAMENTE CADASTRADO ===")
            else:
                vuln ["categoria"] = novo_valor

        elif opcao == "3":
            
            if novo_valor .lower() not in SEVERIDADE:
                print("=== SEVERIDADE INVALIDA ===")
                return
            vuln["severidade"] = novo_valor

        elif opcao == "4":
            
            if novo_valor .lower() not in STATUS:
                print("=== STATUS INVALIDO ===")
                return
            vuln ["status"] = novo_valor
        salvar_ativo(ativos)
        print ("=== VULNERABILIDADE MODIFICADA ===")

    elif opcao == "5":
        if input("=== CONFIRMA A REMOCAO? (s/n): ").strip().lower() == "s":
            vulnerabilidades.remove(vuln)
            print("=== VULNERABILIDADE REMOVIDA ===")
        else:
            print("=== REMOCAO CANCELADA ===")
    else: 
        print("=== OPCAO INVALIDA ===")
            

#opcoes mostradas do que o usuario tera    
def Interface_menu (ativos):
    while True:
        print(" ===            CADASTRAR ATIVO         === (1)")
        print(" ===           VISUALIZAR ATIVOS        === (2)")
        print(" ===        EDITAR / REMOVER ATIVOS     === (3)")
        print(" ===       CADASTRAR VULNERABILIDADES   === (4)")
        print(" ===      VISUALIZAR VULNERABILIDADES   === (5)")
        print(" ===    EDITAR/REMOVER VULNERABILIDADES === (6)")
        print(" ===                  SAIR              === (0)")

        #parte relacionada ao menu interativo que o usuário terá 
        escolha_usuario = input("Selecione uma das opções acima: ")
        if escolha_usuario == "1":
            cadastrar_ativo(ativos)
        elif escolha_usuario == "2":
            visualizar_ativo(ativos)
        elif escolha_usuario == "3":
            editar_remover_ativo(ativos)
        elif escolha_usuario == "4":
            cadastrar_vuln(ativos)
        elif escolha_usuario == "5":
            visualizar_vuln(ativos)
        elif escolha_usuario == "6":
            editar_remover_vuln (ativos)
        elif escolha_usuario == "0":
            print("=== PROGRAMA ENCERRADO ===")
            break
        else:
            print("opcao invalida selecione de 0 a 6")

ativos = carregar_ativos()
Interface_menu(ativos)
# DISCLAMER: esse código foi feito com o auxílio de inteligencia artificial(gemini, e chatgpt) foram utilizadas como forma de aprendizado e estudo, o código nao foi feito totalmente e nem copiado pela ia, e sim utilizada como auxílio na formaçao do código.