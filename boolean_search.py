# coding=utf-8
from nltk import word_tokenize

"""
L'idée ici est de représenter la query par un arbre
où les noeuds sont soit des opérateurs booléens (NOT, AND, OR) soit des mots
Par exemple: NOT A OR (B AND C) serait représenté par:

               OR
               /\
              /  \
            NOT  AND
            /    / \
           /    /   \
          A    B     C

On pourra ensuite évaluer les resultats de la recherche en parcourant l'arbre en profondeur
"""


class Node:
    """
    Noeud de l'arbre
    """

    def __init__(self, *children):
        self.children = children

    def search(self):
        '''
        Retourne le résultat de la recherche associé
        '''
        raise NotImplementedError


class AndNode(Node):
    """
    Noeud représentant un AND. Possède deux enfants
    """

    def search(self):
        '''
        Pour un AND, le resulat de la recherche est l'intersection de ceux des enfants
        '''
        return self.children[0].search() & self.children[1].search()


class OrNode(Node):
    """
    Noeud représentant un OR. Possède deux enfants
    """

    def search(self):
        '''
        Pour un OR, le resultat de la recherche est l'union de ceux des enfants
        '''
        return self.children[0].search() | self.children[1].search()


class NotNode(Node):
    """
    Noeud représentant un NOT. Possède un enfant.

    Le noeud doit etre instancier avec un index
    """

    def __init__(self, child, index):
        self.children = (child, )
        self.index = index

    def search(self):
        '''
        Pour un NOT, le résultat de la recherche est le complémentaire des résultats de l'enfant
        '''
        return set(self.index.documents_ids) - self.children[0].search()


class WordNode(Node):
    """
    Noeud représentant un mot. Ne possède pas d'enfant.

    Le noeud doit être instancier avec un index et un mot
    """

    def __init__(self, index, word):
        self.index = index
        self.word = word

    def search(self):
        '''
        Pour un mot, le résultat de la recherche est l'ensemble des documents contenant ce mot
        '''
        return set(self.index.search_word(self.word))


def _tokenize_query(query, index):
    '''
    Tokenisation de la query
    '''
    # On met tout en minuscule
    query = query.lower()

    # On tokenize
    words = word_tokenize(query, 'english')

    # On utlise le preprocessing de l'index pour etre coherent avec le traitement des docs
    # SAUF si le mot est dans ["(", ")", "and", "or", "not"] car ce sont des "mots d'actions"
    # pour la recherche booleene qui seraient sinon retirés par le preprocessing
    tokens = []
    for word in words:
        if _is_word(word):
            # Preprocessing
            tokens += index._text_to_words(word)
        else:
            tokens.append(word)
    return tokens


def _is_word(string):
    '''
    Retourne True si le string passé en argument est un mot
    '''
    return string not in ["(", ")", "and", "or", "not"]


def _add_missing_and(tokens):
    '''
    Ajoute un AND quand c'est nécessaire:
        - entre deux mots consécutifs
        - entre un mot et "("
        - entre ")" et un mot
    '''
    tokens_with_and = []
    for i in range(len(tokens) - 1):
        # On rajoute le mot
        tokens_with_and.append(tokens[i])

        # On check s'il faut une paranthèse
        word_word = _is_word(tokens[i]) and _is_word(tokens[i + 1])
        word_paranthesis = _is_word(tokens[i]) and tokens[i + 1] == "("
        paranthesis_word = tokens[i] == ")" and _is_word(tokens[i + 1])

        # On rajoute le and si necessaire
        if word_word or word_paranthesis or paranthesis_word:
            tokens_with_and.append('and')

    tokens_with_and.append(tokens[-1])
    return tokens_with_and


def build_query_tree(query, index):
    '''
    Construit l'arbre a partir de la query et l'index donnés
    '''
    # On tokenise
    tokens = _tokenize_query(query, index)

    # On rajoute des AND si necessaire
    tokens = _add_missing_and(tokens)

    # On construit l'arbre.
    # Algo basé sur Shunting-Yard par Dijkstra.
    # L'implementation est une adaptation de
    # https://msoulier.wordpress.com/2009/08/01/dijkstras-shunting-yard-algorithm-in-python

    # Stack avec les opérateurs en cours de traitements
    stack = []
    output = []

    # Les opérateurs et leur priorités
    operators = {"not": 3, "and": 2, "or": 1}
    for token in tokens:
        if token in operators:
            if len(stack) == 0:
                stack.append(token)
            else:
                top = stack[-1]
                while (top in operators and operators[top] > operators[token]):
                    top = stack.pop()
                    _build_node(top, index, stack, output)
                    if len(stack) == 0:
                        break
                    top = stack[-1]
                stack.append(token)
        elif token == "(":
            stack.append(token)
            output.append("(")
        elif token == ")":
            top = stack.pop()
            while top != "(":
                _build_node(top, index, stack, output)
                top = stack.pop()
            top = output.pop()
            output.append(top)
        else:  # the token is a word
            output.append(WordNode(index, token))
    while(len(stack) > 0):
        top = stack.pop()
        _build_node(top, index, stack, output)

    return output[0]


def _build_node(node_type, index, stack, output):
    """
    Construit le noeud approprié et le rajoute a l'output
    """
    if node_type == "not":
        output.append(NotNode(output.pop(), index))
    else:
        left = output.pop()
        right = output.pop()
        output.append(
            AndNode(left, right)
            if node_type == "and"
            else OrNode(left, right)
        )


def boolean_search(query, index):
    """
    Effectue la recehrche binaire de la query dans l'index
    """
    tree = build_query_tree(query, index)
    return tree.search()
