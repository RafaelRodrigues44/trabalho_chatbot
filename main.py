from auth.user import autenticar_usuario, cadastrar_usuario
from chatbot.chatbot import chatbot, find_answer_in_tree
from chatbot.tree import Tree
from database.database import create_tables, registrar_chat, visualizar_historico

def main():
    """
    Função principal que configura o sistema de chat, registra usuários, 
    processa perguntas e respostas, e exibe o histórico de interações.

    - Cria as tabelas no banco de dados.
    - Configura a árvore de entidades e intenções para o chatbot.
    - Realiza o cadastro e autenticação de um usuário.
    - Processa uma pergunta do usuário e retorna uma resposta do chatbot.
    - Exibe o histórico de chats do usuário.
    """

    create_tables()  

    tree = Tree("aluguel")

    # Entidades e Intenções
    tree.add_child("aluguel", "veículo", True)
    tree.add_child("aluguel", "carro", True)
    tree.add_child("aluguel", "automóvel", True)
    tree.add_child("aluguel", "data", True)
    tree.add_child("aluguel", "localização", True)
    tree.add_child("aluguel", "serviços", True)

    # Intenções para Veículo
    tree.add_child("veículo", "tipo", True)
    tree.add_child("veículo", "modelo", True)
    tree.add_child("veículo", "categoria", True)
    tree.add_child("tipo", "Carros disponíveis: SUV, Sedan, Hatchback, Picape, Cabriolet")
    tree.add_child("tipo", "Quais modelos de carros estão disponíveis?")
    tree.add_child("modelo", "Carros disponíveis: SUV, Sedan, Hatchback, Picape, Cabriolet")
    tree.add_child("modelo", "Quais carros posso alugar?")
    tree.add_child("veículo", "preço", True)
    tree.add_child("veículo", "valor", True)
    tree.add_child("preço", "Preço médio: R$ 150 por dia")
    tree.add_child("preço", "Qual o preço de aluguel de um carro?")
    tree.add_child("preço", "Quanto custa o aluguel de um veículo?")
    tree.add_child("veículo", "disponibilidade", True)
    tree.add_child("disponibilidade", "Disponível a partir de 15 de dezembro")
    tree.add_child("disponibilidade", "Quando estará disponível o veículo?")
    tree.add_child("veículo", "avaliação", True)
    tree.add_child("avaliação", "Avaliação média de 4.7 estrelas")
    tree.add_child("veículo", "características", True)
    tree.add_child("características", "Carro com ar condicionado, direção hidráulica, câmbio automático")

    # Intenções para Data
    tree.add_child("data", "início", True)
    tree.add_child("início", "Data de início: 15 de dezembro de 2024")
    tree.add_child("data", "término", True)
    tree.add_child("término", "Data de término: 22 de dezembro de 2024")
    tree.add_child("data", "duração", True)
    tree.add_child("duração", "Duração do aluguel: 7 dias")
    tree.add_child("data", "disponibilidade", True)
    tree.add_child("disponibilidade", "Datas disponíveis para aluguel")
    tree.add_child("data", "quais datas posso alugar?", True)
    tree.add_child("data", "quando posso pegar o carro?", True)
    tree.add_child("data", "qual a data de início?", True)
    tree.add_child("data", "qual a data de término?", True)

    # Intenções para Localização
    tree.add_child("localização", "retirada", True)
    tree.add_child("retirada", "Local de retirada: Aeroporto de São Paulo")
    tree.add_child("localização", "devolução", True)
    tree.add_child("devolução", "Local de devolução: Centro de São Paulo")
    tree.add_child("localização", "distância", True)
    tree.add_child("distância", "Distância até o destino: 30 km")
    tree.add_child("localização", "endereço", True)  
    tree.add_child("endereço", "Endereço de retirada: Rua Exemplo, 123")  
    tree.add_child("localização", "onde retirar o carro?", True)
    tree.add_child("localização", "onde pegar o veículo?", True)
    tree.add_child("localização", "qual o endereço de retirada?", True)  
    tree.add_child("localização", "onde fica a retirada?", True)
    tree.add_child("localização", "qual o local de retirada?", True)

    # Intenções para Serviços Adicionais
    tree.add_child("serviços", "seguro", True)
    tree.add_child("seguro", "Seguro completo disponível")
    tree.add_child("serviços", "GPS", True)
    tree.add_child("GPS", "GPS incluído por R$ 20 por dia")
    tree.add_child("serviços", "motorista", True)
    tree.add_child("motorista", "Serviço de motorista disponível")
    tree.add_child("serviços", "assistência", True)
    tree.add_child("assistência", "Assistência 24h incluída no pacote")  
    tree.add_child("serviços", "assistência 24h", True)  
    tree.add_child("serviços", "assurance", True)
    tree.add_child("assurance", "Seguro de viagem incluído")

    # Perguntas Comuns
    tree.add_child("aluguel", "como funciona o processo de aluguel?", True)
    tree.add_child("aluguel", "quais são os requisitos para alugar?", True)
    tree.add_child("aluguel", "qual a documentação necessária?", True)
    tree.add_child("aluguel", "quais são as regras para alugar?", True)
    tree.add_child("aluguel", "quais são as condições para alugar?", True)
    tree.add_child("data", "qual a data de início?", True)
    tree.add_child("data", "quando começa o aluguel?", True)
    tree.add_child("data", "qual é o primeiro dia do aluguel?", True)
    tree.add_child("data", "qual a data de término?", True)
    tree.add_child("data", "quanto tempo dura o aluguel?", True)
    tree.add_child("localização", "onde retirar o veículo?", True)
    tree.add_child("localização", "qual o endereço de retirada?", True)
    tree.add_child("localização", "onde pegar o carro?", True)
    tree.add_child("serviços", "quais serviços adicionais estão disponíveis?", True)
    tree.add_child("serviços", "quais são os serviços extras?", True)
    tree.add_child("serviços", "tem seguro incluso?", True)
    tree.add_child("serviços", "o que está incluído no aluguel?", True)
    tree.add_child("serviços", "preciso pagar algo mais além do aluguel?", True)


    nome = "João"
    email = "joao@example.com"
    senha = "senha123"
    
    if cadastrar_usuario(nome, email, senha):
        print("Usuário cadastrado com sucesso.")
    
    usuario_id, nome = autenticar_usuario(email, senha)
    if usuario_id:
        print(f"Bem-vindo, {nome}!")   
        
        # pergunta = "qual é o tipo de veículo disponível?"
        # pergunta = "Qual o preço médio de aluguel de um veículo?"
        pergunta = "Qual a localização de retirada?"
        # pergunta = "Qual é a avaliação média dos veículos?"

        resposta = chatbot(pergunta, usuario_id, tree)  

        print(f"Pergunta de {nome}: {pergunta}")
        print(f"Resposta: {resposta}")
        
        visualizar_historico(usuario_id)
    else:
        print("Erro ao autenticar o usuário.")

if __name__ == "__main__":
    main()
