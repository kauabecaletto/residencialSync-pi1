# residencialSync-pi1

Sistema CLI em Python e MySQL para gestão de manutenção condominial. Desenvolvido para o Projeto Integrador I do curso de Sistemas de Informação — PUC-Campinas, 2026.

---

## O que o sistema faz

- Cadastro de moradores com nome, senha e contato
- Login com validação de credenciais
- Abertura de solicitações de manutenção com tipo, descrição e nível de impacto
- Classificação automática de prioridade (Alta, Média ou Baixa)
- Atualização de status (Aberta → Em andamento → Fechada)
- Consultas por status e prioridade
- Estatísticas de solicitações por status e prioridade
- Todos os dados persistidos no MySQL

---

## Regra de prioridade

A prioridade é calculada automaticamente no momento da abertura da solicitação:

| Condição | Prioridade |
|---|---|
| Vazamento de gás (qualquer nível) | Alta |
| Elétrico com nível Grave ou Urgente | Alta |
| Qualquer tipo com nível Grave ou Urgente | Alta |
| Qualquer tipo com nível Preocupante | Média |
| Demais casos | Baixa |

---

## Requisitos

- Python 3.10+
- MySQL 8.x
- Biblioteca: `mysql-connector-python`
- Biblioteca: `python-dotenv`

Instalar dependências:
```bash
pip install mysql-connector-python python-dotenv
```

---

## Como executar

**1. Clone o repositório:**
```bash
git clone https://github.com/kauabecaletto/residencialSync-pi1.git
cd residencialSync-pi1
```

**2. Crie o banco de dados:**

Abra o MySQL Workbench e execute o arquivo `tabelas.sql`.

**3. Crie o arquivo `.env`** na raiz do projeto:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=residencial_sync
```

**4. Rode o sistema:**
```bash
python main.py
```

---

## Estrutura do projeto

```
residencialSync-pi1/
├── main.py          # Interface CLI e menus
├── database.py      # Conexão e operações no banco
├── tabelas.sql      # Script de criação das tabelas
├── .env             # Credenciais do banco (não sobe pro GitHub)
├── .gitignore
└── README.md
```

---

## Integrantes

- Kauã Becaletto
- Eduardo Marçal
- Arthur Almeida
- Lucas Marinho