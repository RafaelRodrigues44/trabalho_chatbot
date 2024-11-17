import sqlite3

DATABASE = 'database.db'

def conectar():
    """
    Estabelece uma conexão com o banco de dados SQLite.

    Returns:
        sqlite3.Connection: A conexão com o banco de dados.
    """
    return sqlite3.connect(DATABASE)

def create_tables():
    """
    Cria as tabelas necessárias no banco de dados, se não existirem: `usuarios` e `chats`.

    A tabela `usuarios` armazena informações sobre os usuários, como `nome`, `email` e `senha`.
    A tabela `chats` armazena o histórico de perguntas e respostas, incluindo as `entidades` e `intenções` associadas.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        pergunta TEXT NOT NULL,
        resposta TEXT NOT NULL,
        entidades TEXT,  
        intenções TEXT,  
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )''')
    
    conn.commit()
    conn.close()

def registrar_chat(usuario_id, pergunta, resposta, entidades, intencao):
    """
    Registra uma nova interação de chat no banco de dados.

    Args:
        usuario_id (int): O ID do usuário que fez a pergunta.
        pergunta (str): A pergunta feita pelo usuário.
        resposta (str): A resposta gerada para a pergunta.
        entidades (list): Lista das entidades extraídas da pergunta.
        intencao (list): Lista das intenções extraídas da pergunta.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO chats (usuario_id, pergunta, resposta, entidades, intenções)
                      VALUES (?, ?, ?, ?, ?)''', 
                   (usuario_id, pergunta, resposta, ', '.join(entidades), ', '.join(intencao)))
    
    conn.commit()
    conn.close()

def visualizar_historico(usuario_id):
    """
    Exibe o histórico de chats de um usuário, mostrando as perguntas, respostas,
    entidades e intenções associadas.

    Args:
        usuario_id (int): O ID do usuário cujo histórico será visualizado.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT pergunta, resposta, entidades, intenções FROM chats WHERE usuario_id = ?", (usuario_id,))
    historico = cursor.fetchall()

    print("\n" + "="*50)
    print("Histórico de Chats:")
    print("="*50)

    if historico:
        pergunta_atual, resposta_atual, entidades_atual, intencao_atual = historico[-1]
        print(f"Pergunta atual: {pergunta_atual}")
        print(f"Resposta atual: {resposta_atual}")
        print(f"Entidades atuais: {entidades_atual}")
        print(f"Intenções atuais: {intencao_atual}")
        print("-"*50)

        print("Histórico de perguntas anteriores:")
        for pergunta, resposta, entidades, intencao in historico[:-1]:
            print(f"Pergunta: {pergunta}")
            print(f"Resposta: {resposta}")
            print(f"Entidades: {entidades}")
            print(f"Intenções: {intencao}")
            print("-"*50)
    else:
        print("Nenhum histórico encontrado.")
    
    print("="*50 + "\n")
    conn.close()
