import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from chatbot.tree import Tree
from database.database import registrar_chat
from nltk.corpus import mac_morpho
from nltk.tag import UnigramTagger


nltk.data.path.append('./database/nltk_data')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('rslp')
nltk.download('stopwords')
nltk.download('mac_morpho')


train_sents = mac_morpho.tagged_sents()
tagger = UnigramTagger(train_sents)

def extract_entities_and_intentions(question, tree):
    """
    Extrai as entidades e intenções de uma pergunta fornecida. A função tokeniza a 
    pergunta, remove palavras irrelevantes (stopwords) e, em seguida, busca as 
    entidades e intenções correspondentes na árvore de conhecimento fornecida.

    Args:
        question (str): A pergunta feita pelo usuário em formato de string.
        tree (Tree): A árvore de conhecimento usada para procurar as entidades e intenções.

    Returns:
        tuple: Uma tupla contendo duas listas:
            - entities (list): Lista de entidades extraídas da pergunta.
            - intentions (list): Lista de intenções extraídas da pergunta.
    """
    stop_words = set(stopwords.words("portuguese"))
    tokens = word_tokenize(question.lower())

    tokens_clean = [word for word in tokens if word not in stop_words and word.isalpha()]

    entities = []
    intentions = []

    for token in tokens_clean:

        if tree.search_in_level(token, 1):
            entities.append(token)

        elif tree.search_in_level(token, 2):
            intentions.append(token)

    return entities, intentions

def find_answer_in_tree(question, tree):
    """
    Encontra uma resposta para a pergunta fornecida, procurando por entidades e intenções 
    na árvore de conhecimento. Se ambas forem encontradas, a função procura a resposta 
    correspondente na árvore.

    Args:
        question (str): A pergunta feita pelo usuário.
        tree (Tree): A árvore de conhecimento usada para encontrar a resposta.

    Returns:
        str: A resposta encontrada na árvore de conhecimento ou uma mensagem padrão 
             caso a resposta não seja encontrada.
    """
    entities, intentions = extract_entities_and_intentions(question, tree)

    if entities and intentions:
        entity = entities[0]
        intention = intentions[0]

        answer = tree.find_answer(entity, intention)

        if answer:
            return answer
        
    return "Desculpe, não consegui entender sua pergunta."

def chatbot(question, usuario_id, tree_instance):
    """
    Função principal do chatbot que processa a pergunta feita pelo usuário, 
    extrai as entidades e intenções usando a árvore de conhecimento fornecida, 
    encontra a resposta e registra a interação no banco de dados.

    Args:
        question (str): A pergunta feita pelo usuário.
        usuario_id (int): O ID do usuário que está interagindo com o chatbot.
        tree_instance (Tree): A instância da árvore de conhecimento usada para 
                               obter as respostas.

    Returns:
        str: A resposta gerada pelo chatbot com base na pergunta, entidades e intenções.
    """
    entidades, intencao = extract_entities_and_intentions(question, tree_instance)
    
    resposta = find_answer_in_tree(question, tree_instance)
    
    registrar_chat(usuario_id, question, resposta, entidades, intencao)
    
    return resposta
