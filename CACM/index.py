# coding=utf-8
from collections import defaultdict
import string
from math import log10


class Index(object):
    '''
    Represente un index.

    Arguments:
        - (list) documents: optionel, liste de documents intiaux a ajouter a l'index

    Méthodes utiles:
        - add_documents(self, documents)
            -> ajoute une liste de documents a l'index
        - add_document(self, document)
            ->ajoute un document a l'index
        - tf_idf(self, document_id, normalize)
            -> retorune vecteur de poids tf-idf pour le document id demandé.
               normalise si `normalize` == True
        - tf_idf(self, document_id, normalize)
            -> retorune vecteur de poids tf-idf logarithmique pour le document id demandé.
               normalise si `normalize` == True

    '''

    # L'utilisation de defaultdict permet de "forcer" la structure des dictionnaires d'index
    # Ce qui permettra d'eviter de devoir a chaque fois checker si les clés / valeurs existent

    # Index document -> mots
    # dictionnaire de la forme:
    # {
    #     'id doc': {
    #         'mot 1': occurence (int)
    #         'mot 2': occurence (int)
    #     },
    #     'id doc 2: {...}
    # }
    document_index = defaultdict(lambda: defaultdict(int))

    # Index mots -> document
    # dictionnaire de la forme:
    # {
    #     'mot 1': {
    #         'id doc': occurence (int)
    #         'id doc': occurence (int)
    #     },
    #     'id doc 2: {...}
    # }
    word_index = defaultdict(lambda: defaultdict(int))

    # les "stop words" (mots communs a ne pas considérer dans les indexs)
    STOP_WORDS_PATH = './dataset/common_words'
    stop_words = []

    def __init__(self, documents=[]):
        self._build_stop_words()
        self.add_documents(documents)

    @property
    def document_count(self):
        '''
        Nombre de documents indexés
        '''
        return len(self.document_index.keys())

    @property
    def documents_ids(self):
        '''
        Liste des ids des documents indexés
        '''
        return self.document_index.keys()

    def _build_stop_words(self):
        '''
        Remplit self.stop_words a partir des common_words du dataset
        '''
        with open(self.STOP_WORDS_PATH, 'r') as common_words:
            for word in common_words:
                self.stop_words.append(word.strip().lower())

    def add_documents(self, documents):
        for document in documents:
            self.add_document(document)

    def add_document(self, document):
        '''
        Ajoute un document a l'index.
        document devrait etre une sous classe de documents.Document (pour les attributs `id` et `text`)
        '''
        words = self._text_to_words(document.text)
        # On remplit nos indexs avec les mots du documents
        for word in words:
            self.document_index[document.id][word] += 1
            self.word_index[word][document.id] += 1

    def _text_to_words(self, text):
        '''
        Processe un texte et retourne une liste de mots
        Le processing effectue les actions suivantes:
            - mise en minuscule du texte
            - tokenisation
            - retrait des stop_words
            - stemming des mots (TODO)
        '''
        # On met le texte en minuscule
        text = text.lower()

        # Tokenisation
        # TODO: tokenisation plus précise via NLTK http://www.nltk.org/howto/tokenize.html
        # On remplace la ponctuation et les sauts de lignes par des espaces
        # puis on recupere la liste des mots
        text = text.replace('\n', ' ')
        for punct in string.punctuation:
            text = text.replace(punct, ' ')
        words = [word for word in text.split(' ') if word]

        # stop_words
        # On retire les stop words de notre liste de mots
        words = [word for word in words if word not in self.stop_words]

        # Stemming (optionel)
        # TODO Porter ou Snowball stemming via NLTK (http://www.nltk.org/howto/stem.html)

        return words

    def _dft(self, word):
        '''
        Retourne frequence du mot dans l'index (nombre de docs avec ce mot)
        '''
        return len(self.word_index[word].keys())

    def tf_idf(self, doc_id, normalize):
        '''
        Retourne vecteur avec poids tf-idf pour le document id passé en arguments.
        Poids normalisés si arg `normalize` == True
        '''
        tf_idf = {}
        documents_count = self.documents_count
        for word, count in self.document_index.items():
            dft = self._dft(word)
            tf_idf[word] = count * log10(documents_count / dft)

        # Normalisation si demandé
        if normalize:
            # On normalize en divisant par le plus grand poids dans le doc
            normalize_factor = max(tf_idf.values())
            tf_idf = {word: weight / normalize_factor for word, weight in tf_idf.items()}

        return tf_idf

    def tf_idf_log(self, doc_id, normalize):
        '''
        Retourne vecteur avec poids tf-idf logarithmique pour le document id passé en arguments.
        Poids normalisés si arg `normalize` == True
        '''
        tf_idf_log = {}
        documents_count = self.documents_count
        for word, count in self.document_index.items():
            dft = self._dft(word)
            tf_idf_log[word] = (1 + log10(count)) * log10(documents_count / dft)

        # Normalisation si demandé
        if normalize:
            # On normalize en divisant par le plus grand poids dans le doc
            normalize_factor = max(tf_idf_log.values())
            tf_idf_log = {word: weight / normalize_factor for word, weight in tf_idf_log.items()}

        return tf_idf_log
