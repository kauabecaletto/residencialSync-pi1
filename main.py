import re 
from data import db_buscar_usuario_por_contato
from database import *

nome_logado = ""
id_logado = None

def cadastrar():   
    chave = True
    while chave:
        nome = input('Nome: ')
        senha = input('Senha: ')
        contato = input('E-mail: ')

        if not contato.strip():
            print("O e-mail é obrigatório!")
            continue

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', contato):
            print("E-mail inválido!")
            continue

        if db_buscar_usuario_por_nome(nome):
            print('Nome já cadastrado; tente novamente!')
        elif db_buscar_usuario_por_contato(contato):
            print('E-mail já cadastrado; tente novamente!')
        else:
            chave = False
            db_cadastrar_usuario(nome, senha, contato)
            print('Cadastro realizado com sucesso!\n')
             
def login():
    contato_tentativa = input("Digite seu e-mail cadastrado: ")
    senha_tentativa = input("\nDigite sua senha cadastrada: ")
    
    usuario = db_buscar_usuario_por_contato(contato_tentativa)
    
    if usuario is None:
        print("Usuário inexistente")
        return False

    # usuario[0] é id, usuario[1] é nome, usuario[2] é senha
    if usuario[2] != senha_tentativa:
        print("Alguma credencial errada")
        return False
    else:
        global nome_logado, id_logado
        id_logado = usuario[0]
        nome_logado = usuario[1]
        print('Login efetuado com sucesso!\n')
        return True
  
def adicionar_solicitacao():
    print("\n--- NOVA SOLICITAÇÃO ---")
    print("1: Hidráulico\n2: Elétrico\n3: Vazamento de gás\n4: Infraestrutura\n5: Outro\n")
    peso_tipo = 0
    chave_tipo = True
    while chave_tipo:
        try:
            tipo_opcao = int(input("Qual o problema?\n"))
        except ValueError:
            print("Digita um número válido aí.")
            continue
            
        if tipo_opcao == 1:
            tipo = "Hidráulico"
            peso_tipo = 4
            chave_tipo = False
        elif tipo_opcao == 2:
            tipo = "Elétrico"
            peso_tipo = 3
            chave_tipo = False
        elif tipo_opcao == 3:
            tipo = "Vazamento de gás"
            peso_tipo = 10
            chave_tipo = False
        elif tipo_opcao == 4:
            tipo = "Infraestrutura"
            peso_tipo = 2
            chave_tipo = False
        elif tipo_opcao == 5:
            tipo = "Outro"
            peso_tipo = 1
            chave_tipo = False
        else:
            print("Opção inválida, tenta de novo.")

    descricao = ""
    while not descricao.strip():
        descricao = input("\nDescreva o problema com mais detalhes:\n")
        if not descricao.strip():
            print("A descrição não pode ficar em branco.")

    print("\nNíveis de impacto:")
    print("1: Leve\n2: Moderada\n3: Preocupante\n4: Grave\n5: Urgente!")
    
    chave_nivel = True
    while chave_nivel:
        try:
            nivel_opcao = int(input('Qual o nível avaliado do problema (1-5)?\n'))
        except ValueError:
            print("Digita um número válido.")
            continue
            
        if nivel_opcao == 1:
            nivel = "Leve"
            chave_nivel = False
        elif nivel_opcao == 2:
            nivel = "Moderada"
            chave_nivel = False
        elif nivel_opcao == 3:
            nivel = "Preocupante"
            chave_nivel = False
        elif nivel_opcao == 4:
            nivel = "Grave"
            chave_nivel = False
        elif nivel_opcao == 5:
            nivel = "Urgente!"
            chave_nivel = False
        else:
            print("Nível inválido, tenta de novo.")

    pontuacao = peso_tipo + nivel_opcao

    if pontuacao >= 10:
        prioridade = "Alta"
    elif pontuacao >= 6:
        prioridade = "Média"
    else:
        prioridade = "Baixa"

    if db_adicionar_solicitacao(id_logado, tipo, descricao, nivel, prioridade):
        print(f'\n[OK] Solicitação criada! A prioridade calculada foi: {prioridade}\n')
    else:
        print('\n[Erro] Erro ao salvar no banco.\n')

def excluir_solicitacao():
    try:
        excluir = int(input("Digite o ID da solicitação que deseja excluir:\n"))
    except ValueError:
        print("ID inválido")
        return
            
    if db_excluir_solicitacao(excluir):
        print("Solicitação excluída com sucesso do banco de dados!")
    else:
        print("Não foi encontrada nenhuma solicitação com esse ID.")

def atualizar_status():
    try:
        id_sol = int(input("Digite o ID da solicitação que deseja atualizar:\n"))
    except ValueError:
        print("ID inválido")
        return

    solicitacao = db_buscar_solicitacao_por_id(id_sol)

    if solicitacao is None:
        print("Nenhuma solicitação encontrada com esse ID.")
        return

    status_atual = solicitacao[1]
    print(f"\nStatus atual: {status_atual}")

    # Regra de integridade: não pode voltar atrás se já estiver Fechada
    if status_atual == "Fechada":
        print("Essa solicitação já está fechada e não pode ser alterada.")
        return

    print("1: Em andamento\n2: Fechada")

    try:
        opcao = int(input("Qual o novo status?\n"))
    except ValueError:
        print("Opção inválida")
        return

    if opcao == 1:
        novo_status = "Em andamento"
    elif opcao == 2:
        novo_status = "Fechada"
    else:
        print("Opção inválida")
        return

    if db_atualizar_status(id_sol, novo_status):
        print(f"Status atualizado para '{novo_status}' com sucesso!")
    else:
        print("Erro ao atualizar o status.")

def consultas_e_estatisticas():
    chave = True
    while chave:
        print("""
        ╔════════════════════════════════════════╗
        ║       CONSULTAS E ESTATÍSTICAS         ║
        ╠════════════════════════════════════════╣
        ║  [1] Filtrar por status                ║
        ║  [2] Filtrar por prioridade            ║
        ║  [3] Estatísticas por status           ║
        ║  [4] Estatísticas por prioridade       ║
        ║  [0] Voltar                            ║
        ╚════════════════════════════════════════╝
        """)
        try:
            opcao = int(input("O que deseja ver? "))
        except ValueError:
            print("Opção inválida")
            continue

        if opcao == 0:
            chave = False

        elif opcao == 1:
            print("1: Aberta\n2: Em andamento\n3: Fechada")
            try:
                s = int(input("Qual status?\n"))
            except ValueError:
                print("Opção inválida")
                continue
            if s == 1: valor = "Aberta"
            elif s == 2: valor = "Em andamento"
            elif s == 3: valor = "Fechada"
            else:
                print("Opção inválida")
                continue
            lista = db_consultar_solicitacoes(filtro_tipo="status", valor_filtro=valor)
            if len(lista) == 0:
                print(f"\nNenhuma solicitação com status '{valor}'.")
            else:
                print(f"\n--- SOLICITAÇÕES: {valor.upper()} ---")
                for sol in lista:
                    print(f"ID: {sol[0]} | Tipo: {sol[2]} | Prioridade: {sol[5]} | Data: {sol[7]}")

        elif opcao == 2:
            print("1: Alta\n2: Média\n3: Baixa")
            try:
                p = int(input("Qual prioridade?\n"))
            except ValueError:
                print("Opção inválida")
                continue
            if p == 1: valor = "Alta"
            elif p == 2: valor = "Média"
            elif p == 3: valor = "Baixa"
            else:
                print("Opção inválida")
                continue
            lista = db_consultar_solicitacoes(filtro_tipo="prioridade", valor_filtro=valor)
            if len(lista) == 0:
                print(f"\nNenhuma solicitação com prioridade '{valor}'.")
            else:
                print(f"\n--- SOLICITAÇÕES: PRIORIDADE {valor.upper()} ---")
                for sol in lista:
                    print(f"ID: {sol[0]} | Tipo: {sol[2]} | Status: {sol[6]} | Data: {sol[7]}")

        elif opcao == 3:
            resultado = db_obter_estatisticas("status")
            if len(resultado) == 0:
                print("\nNenhuma solicitação registrada.")
            else:
                print("\n--- TOTAL POR STATUS ---")
                for linha in resultado:
                    print(f"{linha[0]}: {linha[1]} solicitações)")

        elif opcao == 4:
            resultado = db_obter_estatisticas("prioridade")
            if len(resultado) == 0:
                print("\nNenhuma solicitação registrada.")
            else:
                print("\n--- TOTAL POR PRIORIDADE ---")
                for linha in resultado:
                    print(f"{linha[0]}: {linha[1]} solicitação(ões)")

        else:
            print("Opção inválida")

def modificar_solicitacoes(): 
    chave_adicionar_solicitacoes = True
    while chave_adicionar_solicitacoes:
        nome_formatado = nome_logado[:22].ljust(22)
        
        print(f"""
        ╔════════════════════════════════════════╗
        ║        A R E A   L O G A D A           ║
        ╠════════════════════════════════════════╣
        ║  Usuário logado: {nome_formatado}║
        ╠════════════════════════════════════════╣
        ║  [1] Adicionar uma nova solicitacao    ║
        ║  [2] Excluir uma solicitacao           ║
        ║  [3] Mostrar solicitacoes em aberto    ║
        ║  [4] Atualizar status                  ║
        ║  [5] Consultas e estatísticas          ║
        ║  [0] Sair                              ║
        ╚════════════════════════════════════════╝
        """)
        try:
            resposta = int(input("O que deseja fazer? "))
        except ValueError:
            print("Opção inválida")
        else:
            if resposta == 0:
                chave_adicionar_solicitacoes = False
                print("Saindo da conta...")
                 
            elif resposta == 1:
                adicionar_solicitacao() 
                 
            elif resposta == 2:
                lista = db_consultar_solicitacoes(filtro_tipo="usuario", valor_filtro=id_logado)
                if len(lista) == 0:
                    print("Você não tem nenhuma solicitação registrada.")
                else:
                    excluir_solicitacao()

            elif resposta == 3:
                lista = db_consultar_solicitacoes(filtro_tipo="usuario", valor_filtro=id_logado)
                if len(lista) == 0:
                    print("Você não tem nenhuma solicitação registrada.")
                else:
                    print("\n--- SUAS SOLICITAÇÕES REGISTRADAS ---")
                    for sol in lista:
                        print(f"ID: {sol[0]} | Tipo: {sol[2]} | Prioridade: {sol[5]} | Status: {sol[6]} | Data: {sol[7]}")

            elif resposta == 4:
                lista = db_consultar_solicitacoes(filtro_tipo="usuario", valor_filtro=id_logado)
                if len(lista) == 0:
                    print("Você não tem nenhuma solicitação registrada.")
                else:
                    atualizar_status()

            elif resposta == 5:
                lista = db_consultar_solicitacoes(filtro_tipo="usuario", valor_filtro=id_logado)
                if len(lista) == 0:
                    print("Você não tem nenhuma solicitação registrada.")
                else:
                    consultas_e_estatisticas()

            else:
                print("Opção inválida")
            
chave_para_Menu = True
while chave_para_Menu: 
    print("""
    ╔════════════════════════════╗
    ║     SISTEMA DE ACESSO      ║
    ╠════════════════════════════╣
    ║  [1] Cadastrar             ║
    ║  [2] Login                 ║
    ║  [0] Sair                  ║
    ╚════════════════════════════╝
    """)
    try:
        menu_resposta = int(input("\nDigite a opção desejada: "))
    except ValueError:
        print("Opção inválida")
    else:
        if menu_resposta == 1:
            cadastrar()
        
        elif menu_resposta == 2:
            if login():
                modificar_solicitacoes()
        
        elif menu_resposta == 0:
            chave_para_Menu = False
            print("Programa encerrado")
        else:
            print("Resposta inválida")