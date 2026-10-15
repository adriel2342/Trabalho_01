import json
from pathlib import Path

ARQUIVOS_DADOS = Path(__file__).resolve().parent /"ativos.json"

TIPOS_ATIVOS = ["Notebook, Roteador, Servidor Web, Impressora"]
SEVERIDADE =["baixa, media, alta, critica"]
STATUS = ["Aberta, Em tratamento, Corrigida, Risco aceito"] 


def salvar_ativo(ativos):
    with open(ARQUIVOS_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(ativos, arquivo, ensure_ascii=False, indent=4)

def carregar_ativos():
    if not ARQUIVOS_DADOS.exists():
        salvar_ativo([])
        return
    with open (ARQUIVOS_DADOS, "r", enconding= "utf-8") as arquivo:
        return json.load(arquivo)
    
# área relacionada a busca de algum ativo   
    
def buscar_ativo(ativos, busca):
    for ativo in ativos:
        if str(ativo["id"]) == busca or ativo["nome"].lower() == busca.lower():
            return ativo
    return None
    
def cadastrar_ativo(ativos):
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
            "id": id_ativo,
            "nome": nome,
            "responsavel" : responsavel,
            "ip" : ip_ativo,
            "tipo" : tipo

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
        print("Responsável:", ativo["responsavel"], "| Localização:", ativo["localizacao"])
        

def editar_remover_ativo(ativos):
    ativo = buscar_ativo(ativos, input("INSIRA O id OU O nome do ativo: " ).strip())
    if ativo is None:
        print("=== ATIVO NAO LOCALIZADO ===")
        return
    
    print("1 - Alterar nome | 2 - Alterar responsável | 3 - Alterar localização")
    print("4 - Alterar tipo | 5 - Remover ativo")
    opcao = input("SELECIONE UM DOS NUMEROS ACIMA: ")
    if opcao in ["1", "2", "3","4"]:
        novo_valor = input("NOVO VALOR: ").strip()
        if not novo_valor:
            print("=== ESSE CAMPO NAO PODE FICAR EM BRANCO ===")
            return
        if opcao == "1":
            ativo ["nome"] = novo_valor
        elif opcao == "2":
            ativo ["responsavel"] = novo_valor
        elif opcao == "3":
            ativo["localizacao"] = novo_valor
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
    ativo = buscar_ativo(ativos,input("id OU nome DO ATIVO: ").strip())
    if ativo is None:
        print("=== ATIVO NAO LOCALIZADO ===")
        return
    descricao = input("=== DESCRIÇA0: ")
    categoria = input("=== CATEGORIA: ")
    severidade = input ("=== SEVERIDADE (baixa, média, altaa, crítica):  ").strip().lower()
    status = input("=== STATUS (aberta, em tratamento, corrigida, risco aceito)").strip().lower()
    if not descricao or not categoria:
        print("=== OS CAMPOS NAO PODEM FICAR VAZIOS ===")
        return
    if severidade not in SEVERIDADE or status not in STATUS:
        print("=== CATEGORIA DE VULNERABILIDADE E STATUS INVÁLIDA ===")
        return 
    ativo["vulnerabilidades"].append({
        "descricao": descricao,
        "categoria": categoria,
        "severidade": severidade,
        "status": status,
    })

    


def visualizar_vuln(ativos):
    pass

def editar_remover_vuln(ativos):
    pass

#opcoes mostradas do que o usuario tera    
def Interface_menu (ativos):
    while True:
        print(" ===            CADASTRAR ATIVO         === (1)")
        print(" ===           VISUALIZAR ATIVOS        === (2)")
        print(" ===        EDITAR / REMOVER ATIVOS     === (3)")
        print(" ===       CADASTRAR VULNERABILIDADES   === (4)")
        print(" ===      VISUALIZAR VULNERABILIDADES   === (5)")
        print(" ===  EDITAR / REMOVER VULNERABILIDADES === (6)")
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
            print("PROGRAMA ENCERRADO")
            break
        else:
            print("opcao invalida selecione de 0 a 6")

ativos = carregar_ativos()
Interface_menu(ativos)


# DISCLAMER: esse código foi feito com o auxílio de inteligencia artificial(gemini, e chatgpt) foram utilizadas como forma de aprendizado e estudo, o código nao foi feito totalmente e nem copiado pela ia, e sim utilizada como auxílio na formaçao do código.

          



