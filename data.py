import mysql.connector

from dotenv import load_dotenv
import os

load_dotenv()

def obter_conexao():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conexao
    except mysql.connector.Error as erro:
        print(f"[Erro de Conexão] Não foi possível conectar ao banco: {erro}")
        return None

def db_cadastrar_usuario(nome, senha, contato):
    conexao = obter_conexao()
    if conexao is None: return False

    cursor = conexao.cursor()
    comando = "INSERT INTO moradores (nome, senha, contato) VALUES (%s, %s, %s)"
    valores = (nome, senha, contato)

    try:
        cursor.execute(comando, valores)
        conexao.commit()
        return True
    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar no banco: {erro}")
        return False
    finally:
        cursor.close()
        conexao.close()

def db_buscar_usuario_por_contato(contato):
    conexao = obter_conexao()
    if conexao is None: return None

    cursor = conexao.cursor()
    comando = "SELECT id, nome, senha FROM moradores WHERE contato = %s"
    cursor.execute(comando, (contato,))
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()
    return usuario

# OPERAÇÕES DE SOLICITAÇÕES (CRUD)

def db_adicionar_solicitacao(morador_id, tipo, descricao, nivel, prioridade):
    conexao = obter_conexao()
    if conexao is None: return False

    cursor = conexao.cursor()
    comando = """
        INSERT INTO solicitacoes (morador_id, tipo, descricao, nivel, prioridade, status)
        VALUES (%s, %s, %s, %s, %s, 'Aberta')
    """
    valores = (morador_id, tipo, descricao, nivel, prioridade)

    try:
        cursor.execute(comando, valores)
        conexao.commit()
        return True
    except mysql.connector.Error as erro:
        print(f"Erro ao salvar solicitação: {erro}")
        return False
    finally:
        cursor.close()
        conexao.close()

def db_excluir_solicitacao(id_solicitacao):
    conexao = obter_conexao()
    if conexao is None: return False

    cursor = conexao.cursor()
    comando = "DELETE FROM solicitacoes WHERE id = %s"

    try:
        cursor.execute(comando, (id_solicitacao,))
        conexao.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print(f"Erro ao excluir: {erro}")
        return False
    finally:
        cursor.close()
        conexao.close()

def db_buscar_solicitacao_por_id(id_solicitacao):
    conexao = obter_conexao()
    if conexao is None: return None

    cursor = conexao.cursor()
    comando = "SELECT id, status FROM solicitacoes WHERE id = %s"
    cursor.execute(comando, (id_solicitacao,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()
    return resultado

def db_atualizar_status(id_solicitacao, novo_status):
    conexao = obter_conexao()
    if conexao is None: return False

    cursor = conexao.cursor()
    comando = "UPDATE solicitacoes SET status = %s WHERE id = %s"

    try:
        cursor.execute(comando, (novo_status, id_solicitacao))
        conexao.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as erro:
        print(f"Erro ao atualizar status: {erro}")
        return False
    finally:
        cursor.close()
        conexao.close()

# CONSULTAS COM FILTROS E ESTATÍSTICAS

def db_consultar_solicitacoes(filtro_tipo=None, valor_filtro=None):
    conexao = obter_conexao()
    if conexao is None: return []

    cursor = conexao.cursor()
    comando = "SELECT id, morador_id, tipo, descricao, nivel, prioridade, status, data_hora FROM solicitacoes"

    if filtro_tipo == "status":
        comando += " WHERE status = %s"
        cursor.execute(comando, (valor_filtro,))
    elif filtro_tipo == "prioridade":
        comando += " WHERE prioridade = %s"
        cursor.execute(comando, (valor_filtro,))
    elif filtro_tipo == "usuario":
        comando += " WHERE morador_id = %s"
        cursor.execute(comando, (valor_filtro,))
    else:
        cursor.execute(comando)

    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado

def db_obter_estatisticas(agrupar_por):
    conexao = obter_conexao()
    if conexao is None: return []

    cursor = conexao.cursor()

    if agrupar_por in ["status", "prioridade"]:
        comando = f"SELECT {agrupar_por}, COUNT(*) FROM solicitacoes GROUP BY {agrupar_por}"
        cursor.execute(comando)
        resultado = cursor.fetchall()
    else:
        resultado = []

    cursor.close()
    conexao.close()
    return resultado
    