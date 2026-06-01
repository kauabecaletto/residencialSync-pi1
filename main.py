import re
from database import *

# ==========================================
# VARIÁVEIS GLOBAIS DE SESSÃO
# ==========================================
nome_logado = ""
id_logado = None
is_admin = False

# ==========================================
# LÓGICA DE NEGÓCIO E MENUS (CLI)
# ==========================================
def cadastrar():
    chave = True
    while chave:
        nome = input('Nome: ')
        senha = input('Senha: ')
        contato = input('E-mail cadastral: ')

        if not contato.strip():
            print("O e-mail é obrigatório!")
            continue

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', contato):
            print("Formato de e-mail inválido!")
            continue

        if db_buscar_usuario_por_contato(contato):
            print('Este e-mail já está em uso. Tente fazer login!')
        else:
            chave = False
            db_cadastrar_usuario(nome, senha, contato)
            print('Cadastro realizado com sucesso!\n')

def login():
    global nome_logado, id_logado, is_admin

    contato_tentativa = input("Digite seu e-mail: ")
    senha_tentativa = input("Digite sua senha: ")

    usuario = db_buscar_usuario_por_contato(contato_tentativa)

    if usuario is None:
        print("Usuário inexistente ou e-mail incorreto.")
        return False

    if usuario[2] != senha_tentativa:
        print("Senha incorreta.")
        return False
    else:
        id_logado = usuario[0]
        nome_logado = usuario[1]

        if contato_tentativa == "admin@residencial.com":
            is_admin = True
            nome_logado = "Administração"
            print('\n[LOGADO COMO ADMINISTRAÇÃO]')
        else:
            is_admin = False
            print(f'Login efetuado com sucesso! Bem-vindo, {nome_logado}.\n')

        return True

def adicionar_solicitacao():
    print("\n--- NOVA SOLICITAÇÃO ---")
    print("1: Hidráulico\n2: Elétrico\n3: Vazamento de gás\n4: Infraestrutura\n5: Outro\n")

    chave_tipo = True
    while chave_tipo:
        try:
            tipo_opcao = int(input("Qual a categoria do problema?\n"))
        except ValueError:
            print("Digita um número válido aí.")
            continue

        if tipo_opcao == 1:
            tipo = "Hidráulico"
            chave_tipo = False
        elif tipo_opcao == 2:
            tipo = "Elétrico"
            chave_tipo = False
        elif tipo_opcao == 3:
            tipo = "Vazamento de gás"
            chave_tipo = False
        elif tipo_opcao == 4:
            tipo = "Infraestrutura"
            chave_tipo = False
        elif tipo_opcao == 5:
            tipo = "Outro"
            chave_tipo = False
        else:
            print("Opção inválida, tenta de novo.")

    descricao = ""
    while not descricao.strip():
        descricao = input("\nDescreva o problema com mais detalhes:\n")
        if not descricao.strip():
            print("A descrição não pode ficar em branco.")

    print("\n--- CLASSIFICAÇÃO DE RISCO ---")
    print("FATOR 1 - ALCANCE (Quantas áreas estão sendo afetadas?):")
    print("1: Apenas um cômodo do meu apartamento")
    print("2: Meu apartamento inteiro")
    print("3: Meu andar ou corredor")
    print("4: Um bloco inteiro")
    print("5: O condomínio todo")

    chave_urgencia = True
    while chave_urgencia:
        try:
            urgencia = int(input('Informe o Alcance (1-5): '))
            if 1 <= urgencia <= 5:
                chave_urgencia = False
            else:
                print("Número deve ser entre 1 e 5.")
        except ValueError:
            print("Digita um número válido.")

    print("\nFATOR 2 - TIPO DE RISCO (Qual a consequência do problema?):")
    print("1: Apenas estético (Ex: pintura descascando)")
    print("2: Desconforto rotineiro (Ex: lâmpada queimada, porta rangendo)")
    print("3: Prejuízo material em andamento (Ex: cano vazando, infiltração)")
    print("4: Risco à segurança ou saúde (Ex: fio elétrico exposto)")
    print("5: Risco de vida ou estrutural (Ex: cheiro de gás, rachadura na coluna)")

    chave_gravidade = True
    while chave_gravidade:
        try:
            gravidade = int(input('Informe o Tipo de Risco (1-5): '))
            if 1 <= gravidade <= 5:
                chave_gravidade = False
            else:
                print("Número deve ser entre 1 e 5.")
        except ValueError:
            print("Digita um número válido.")

    pontuacao = urgencia + gravidade

    if tipo == "Vazamento de gás" or pontuacao >= 8:
        prioridade = "Alta"
    elif pontuacao >= 5:
        prioridade = "Média"
    else:
        prioridade = "Baixa"

    nivel_formatado = f"Alcance {urgencia} | Risco {gravidade}"

    id_gerado = db_adicionar_solicitacao(id_logado, tipo, descricao, nivel_formatado, prioridade)
    if id_gerado:
        print(f'\n[OK] Solicitação criada! ID: #{id_gerado} | Pontuação: {pontuacao} | Prioridade: {prioridade}\n')
    else:
        print('\n[Erro] Erro ao salvar no banco.\n')

def excluir_solicitacao():
    try:
        excluir = int(input("Digite o ID da solicitação que deseja excluir:\n"))
    except ValueError:
        print("ID inválido")
        return

    solicitacao = db_buscar_solicitacao_por_id(excluir)
    if solicitacao is None:
        print("Não foi encontrada nenhuma solicitação com esse ID.")
        return

    dono_do_chamado = solicitacao[2]
    if dono_do_chamado != id_logado and not is_admin:
        print("Acesso Negado: Você só pode excluir suas próprias solicitações.")
        return

    if db_excluir_solicitacao(excluir):
        print("Solicitação excluída com sucesso do banco de dados!")
    else:
        print("Erro ao excluir no banco.")

def atualizar_status():
    if not is_admin:
        print("\n[ACESSO NEGADO] Apenas a administração pode alterar o status de um chamado.")
        return

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
        if is_admin:
            print("""
        ╔════════════════════════════════════════╗
        ║       CONSULTAS E ESTATÍSTICAS         ║
        ╠════════════════════════════════════════╣
        ║  [1] Filtrar por status                ║
        ║  [2] Filtrar por prioridade            ║
        ║  [3] Estatísticas por status           ║
        ║  [4] Estatísticas por prioridade       ║
        ║  [5] Filtrar por Usuário Específico    ║
        ║  [0] Voltar                            ║
        ╚════════════════════════════════════════╝
        """)
        else:
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
                    print(f"ID: {sol[0]} | Solicitante: {sol[1]} | Tipo: {sol[2]} | Prioridade: {sol[5]} | Data: {sol[7]}")

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
                    print(f"ID: {sol[0]} | Solicitante: {sol[1]} | Tipo: {sol[2]} | Status: {sol[6]} | Data: {sol[7]}")

        elif opcao == 3:
            resultado = db_obter_estatisticas("status")
            if len(resultado) == 0:
                print("\nNenhuma solicitação registrada.")
            else:
                print("\n--- TOTAL POR STATUS ---")
                for linha in resultado:
                    print(f"{linha[0]}: {linha[1]} solicitações")

        elif opcao == 4:
            resultado = db_obter_estatisticas("prioridade")
            if len(resultado) == 0:
                print("\nNenhuma solicitação registrada.")
            else:
                print("\n--- TOTAL POR PRIORIDADE ---")
                for linha in resultado:
                    print(f"{linha[0]}: {linha[1]} solicitações")

        elif opcao == 5:
            if not is_admin:
                print("\n[ACESSO NEGADO] Apenas a administração pode consultar chamados de outros usuários.")
                continue

            try:
                user_id = int(input("Digite o ID numérico do usuário:\n"))
            except ValueError:
                print("ID inválido")
                continue

            lista = db_consultar_solicitacoes(filtro_tipo="usuario", valor_filtro=user_id)
            if len(lista) == 0:
                print(f"\nNenhuma solicitação encontrada para o Usuário ID {user_id}.")
            else:
                print(f"\n--- SOLICITAÇÕES DO USUÁRIO ID {user_id} ---")
                for sol in lista:
                    print(f"ID Chamado: {sol[0]} | Solicitante: {sol[1]} | Tipo: {sol[2]} | Status: {sol[6]} | Data: {sol[7]}")

        else:
            print("Opção inválida")

def modificar_solicitacoes():
    chave_adicionar_solicitacoes = True
    while chave_adicionar_solicitacoes:
        nome_formatado = nome_logado[:22].ljust(22)

        if is_admin:
            label_opcao2 = "Mostrar TODAS as solicitacoes  "
        else:
            label_opcao2 = "Mostrar MINHAS solicitacoes    "

        print(f"""
        ╔════════════════════════════════════════╗
        ║        A R E A   L O G A D A           ║
        ╠════════════════════════════════════════╣
        ║  Usuário: {nome_formatado}║
        ╠════════════════════════════════════════╣
        ║  [1] Adicionar uma nova solicitacao    ║
        ║  [2] {label_opcao2}║
        ║  [3] Consultas e estatísticas          ║
        ║  [4] Excluir uma solicitacao           ║
        ║  [5] Atualizar status (Apenas Admin)   ║
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
                if is_admin:
                    lista = db_consultar_solicitacoes()
                    cabecalho = "MURAL DE SOLICITAÇÕES (TODAS)"
                else:
                    lista = db_consultar_solicitacoes(filtro_tipo="usuario", valor_filtro=id_logado)
                    cabecalho = "MINHAS SOLICITAÇÕES"

                if len(lista) == 0:
                    print("Não há nenhuma solicitação registrada.")
                else:
                    print(f"\n--- {cabecalho} ---")
                    for sol in lista:
                        print(f"ID: {sol[0]} | Solicitante: {sol[1]} | Tipo: {sol[2]} | Prioridade: {sol[5]} | Status: {sol[6]} | Data: {sol[7]}")

            elif resposta == 3:
                consultas_e_estatisticas()

            elif resposta == 4:
                excluir_solicitacao()

            elif resposta == 5:
                atualizar_status()

            else:
                print("Opção inválida")

# ==========================================
# MENU PRINCIPAL
# ==========================================
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
            print("Programa encerrado.")
        else:
            print("Resposta inválida")