from nltk.stem import RSLPStemmer

stemmer = RSLPStemmer()

class Node:
    def __init__(self, value):
        """
        Constrói um nó da árvore com o valor fornecido.

        Args:
            value (str): O valor armazenado no nó.
        """
        self.value = value
        self.children = []

class Tree:
    def __init__(self, value):
        """
        Constrói a árvore com a raiz recebendo o valor fornecido.

        Args:
            value (str): O valor da raiz da árvore.
        """
        self.root = Node(value)

    def add_child(self, parent_value, value, stem=False):
        """
        Adiciona um nó filho a um nó pai na árvore.

        Args:
            parent_value (str): O valor do nó pai ao qual o nó filho será adicionado.
            value (str): O valor do nó filho.
            stem (bool, opcional): Se `True`, o valor será "stemado" (radicalizado). O valor padrão é `False`.
        """
        if stem:
            value = stemmer.stem(value)
        parent_node = self.search(parent_value)
        if parent_node:
            parent_node.children.append(Node(value))
        else:
            print(f"Nó pai com valor {parent_value} não encontrado.")

    def search(self, value, node=None):
        """
        Busca por um nó na árvore com o valor correspondente.

        Args:
            value (str): O valor do nó a ser buscado.
            node (Node, opcional): O nó inicial para a busca. Se `None`, começa pela raiz da árvore. O valor padrão é `None`.

        Returns:
            Node ou None: O nó correspondente se encontrado, caso contrário retorna `None`.
        """
        if node is None:
            node = self.root

        if node.value == value or node.value == stemmer.stem(value):
            return node

        for child in node.children:
            result = self.search(value, child)
            if result:
                return result
        return None

    def search_in_level(self, value, level, node=None, current_level=0):
        """
        Busca por um nó com um valor específico em um nível específico da árvore.

        Args:
            value (str): O valor do nó a ser buscado.
            level (int): O nível em que a busca deve ocorrer.
            node (Node, opcional): O nó inicial para a busca. Se `None`, começa pela raiz da árvore. O valor padrão é `None`.
            current_level (int, opcional): O nível atual da árvore durante a busca. O valor padrão é `0`.

        Returns:
            bool: `True` se o nó for encontrado no nível especificado, `False` caso contrário.
        """
        if node is None:
            node = self.root

        if current_level == level:
            if node.value == value or node.value == stemmer.stem(value):
                return True
            return False

        for child in node.children:
            if self.search_in_level(value, level, child, current_level + 1):
                return True
        return False

    def find_answer(self, entity, intent):
        """
        Encontra a resposta associada a uma entidade e intenção na árvore.

        Args:
            entity (str): A entidade para a qual a resposta será procurada.
            intent (str): A intenção relacionada à resposta.

        Returns:
            str ou None: A resposta encontrada ou `None` caso a resposta não seja encontrada.
        """
        entity_stem = stemmer.stem(entity)
        intent_stem = stemmer.stem(intent)

        entity_node = self.search(entity_stem)
        if entity_node:
            for child in entity_node.children:
                if child.value == intent_stem:
                    return child.children[0].value
        return None
