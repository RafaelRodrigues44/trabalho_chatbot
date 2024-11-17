import sqlite3
from hashlib import sha256

DATABASE = 'database.db'

def conectar():
    """
    Estabelece uma conexão com o banco de dados SQLite.

    Returns:
        sqlite3.Connection: A conexão com o banco de dados.
    """
    return sqlite3.connect(DATABASE)

def cadastrar_usuario(nome, email, senha):
    """
    Cadastra um novo usuário no banco de dados, realizando a verificação 
    se o email já está em uso. A senha do usuário é armazenada de forma 
    segura, utilizando hash SHA-256.

    Args:
        nome (str): Nome do usuário.
        email (str): Email do usuário, utilizado como identificador único.
        senha (str): Senha do usuário, que será criptografada.

    Returns:
        bool: Retorna True se o usuário foi cadastrado com sucesso, 
              ou False se o email já estiver registrado no banco de dados.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    if cursor.fetchone():
        print("Email já cadastrado.")
        conn.close()
        return False
    
    senha_hash = sha256(senha.encode()).hexdigest()
    
    cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
    conn.commit()
    conn.close()
    return True

def autenticar_usuario(email, senha):
    """
    Autentica um usuário com base no email e na senha fornecidos. 
    A senha é comparada com a versão armazenada no banco de dados, 
    que está criptografada com SHA-256.

    Args:
        email (str): Email do usuário a ser autenticado.
        senha (str): Senha do usuário para verificação.

    Returns:
        tuple or None: Retorna uma tupla (usuario_id, nome) se a autenticação for bem-sucedida, 
                        ou None se o email ou senha estiverem incorretos.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    
    if usuario:
        usuario_id, nome, _, senha_hash = usuario

        if sha256(senha.encode()).hexdigest() == senha_hash:
            conn.close()
            return usuario_id, nome
    
    conn.close()
    return None
