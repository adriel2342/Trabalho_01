def Interface_menu (ativos):
    while True:
        ativos = carregar_ativos
        print ("=== CADASTRAR ATIVO === (1)")
        print ("=== VISUALIZAR ATIVOS === (2)")
        print(" === EDITAR / REMOVER ATIVOS === (3)")
        print(" === CADASTRAR VULNERABILIDADES === (4)")
        print(" === VISUALIZAR VULNERABILIDADES === (5)")
        print(" === EDITAR / REMOVER VULNERABILIDADES === (6)")
        print(" === SAIR === (0)")
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
        else:
            print("opcao invalida selecione de 0 a 6")
            break    
