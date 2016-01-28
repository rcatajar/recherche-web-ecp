# coding=utf-8
import inspect
import sys
from collections import defaultdict
import string
from math import log10

from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


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
        - get_document_vector(self, document_id, weight_type, index)
            -> retourne vecteur de poids ({mot1: poids1, mot2: poids2, ...}) pour le document id demandé.
               `weight_type` indique le type de poids a utiliser
                    ("tf_idf", "tf_idf_normalized", "tf_idf_log", "tf_idf_log_normalized")
                `index` indique l'index a utiliser pour caculer la dft des mots
                    (Utile pour indexer une query par rapport a une collection)
    '''

    # les "stop words" (mots communs a ne pas considérer dans les indexs)
    STOP_WORDS_PATH = './dataset/common_words'
    stop_words = []

    def __init__(self, documents=[]):
        self._build_stop_words()
        self._initialize_indexs()
        self.add_documents(documents)

    def __sizeof__(self):
        '''
        Retourne la taille en octet de l'objet
        '''
        size = 0
        for (name, val) in inspect.getmembers(self):
            size += sys.getsizeof(val)
            size += sys.getsizeof(name)
        return size

    def _initialize_indexs(self):
        '''
        Initialize les indexs doc -> mots et mots -> docs avec des valeurs par default

        L'utilisation de defaultdict permet de "forcer" la structure des dictionnaires d'index
        Ce qui permettra d'eviter de devoir a chaque fois checker si les clés / valeurs existent
        Comme ca on aura toujours index[doc][mot] = 0 si la valeur n'a pas été set au lieu d'une KeyError
        '''
        # Index document -> mots
        # dictionnaire de la forme:
        # {
        #     'id doc': {
        #         'mot 1': occurence (int)
        #         'mot 2': occurence (int)
        #     },
        #     'id doc 2: {...}
        # }
        self.document_index = defaultdict(lambda: defaultdict(int))

        # Index mots -> document
        # dictionnaire de la forme:
        # {
        #     'mot 1': {
        #         'id doc': occurence (int)
        #         'id doc': occurence (int)
        #     },
        #     'id doc 2: {...}
        # }
        self.word_index = defaultdict(lambda: defaultdict(int))

    @property
    def documents_count(self):
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
            - stemming des mots
        '''
        # On met le texte en minuscule
        text = text.lower()

        # Tokenisation
        tokens = word_tokenize(text, language="english")

        # stop_words
        # On retire les stop words de notre vecteur.
        # En plus des stopwords donnees avec la collection, je rajoute les mots courants
        # Anglais donnés par NLTK et la ponctuation (sauf parantheses car utile pour query bool)
        stop_words = self.stop_words + list(string.punctuation) + stopwords.words("english")
        tokens = [token for token in tokens if token not in stop_words]

        # Stemming
        stemmer = SnowballStemmer(language="english")
        tokens = [stemmer.stem(word) for word in tokens]

        return tokens

    def _dft(self, word):
        '''
        Retourne frequence du mot dans l'index (nombre de docs avec ce mot)
        '''
        return len(self.word_index[word].keys())

    def _tf_idf(self, doc_id, normalize, index):
        '''
        Retourne vecteur avec poids tf-idf pour le document id passé en arguments.
        Poids normalisés si arg `normalize` == True
        '''
        tf_idf = defaultdict(float)
        documents_count = index.documents_count
        for word, count in self.document_index[doc_id].items():
            # Float pour forcer une division "non entiere" dans le log de l'idf
            dft = index._dft(word)
            # "if dft else 0" pour éviter une division par 0.
            # Si dft est nul (mot pas dans l'index de reference), on met le poids à 0
            tf_idf[word] = count * log10(documents_count / dft) if dft else 0

        # Normalisation si demandé
        if normalize:
            # On normalize en divisant par le plus grand poids dans le doc
            normalize_factor = max(tf_idf.values())
            for word, weight in tf_idf.items():
                tf_idf[word] = weight / normalize_factor

        return tf_idf

    def _tf_idf_log(self, doc_id, normalize, index):
        '''
        Retourne vecteur avec poids tf-idf logarithmique pour le document id passé en arguments.
        Poids normalisés si arg `normalize` == True
        '''
        tf_idf_log = defaultdict(float)
        documents_count = index.documents_count
        for word, count in self.document_index[doc_id].items():
            # Float pour forcer une division "non entiere" dans le log de l'idf
            dft = float(index._dft(word))
            # "if dft else 0" pour éviter une division par 0.
            # Si dft est nul (mot pas dans l'index de reference), on met le poids à 0
            tf_idf_log[word] = (1 + log10(count)) * log10(documents_count / dft) if dft else 0

        # Normalisation si demandé
        if normalize:
            # On normalize en divisant par le plus grand poids dans le doc
            normalize_factor = max(tf_idf_log.values())
            for word, weight in tf_idf_log.items():
                tf_idf_log[word] = weight / normalize_factor

        return tf_idf_log

    def get_document_vector(self, doc_id, weight_type, index=None):
        '''
        Retourne vecteur de poids pour le document id demandé.
        (vecteur de la forme {mot1: poids1, mot2: poids2, ...})

        Args:
            - `weight_type` indique le type de poids a utiliser
                Poids supportés: ["tf_idf", "tf_idf_normalized", "tf_idf_log", "tf_idf_log_normalized"]
            - `index`: index a utliser pour calculer la dft (par default self).
                Utile pour indexer une query par rapport a l'index d'une collection
        '''
        index = index or self

        if weight_type == 'tf_idf':
            return self._tf_idf(doc_id, False, index)
        if weight_type == 'tf_idf_normalized':
            return self._tf_idf(doc_id, True, index)
        if weight_type == 'tf_idf_log':
            return self._tf_idf_log(doc_id, False, index)
        if weight_type == 'tf_idf_log_normalized':
            return self._tf_idf_log(doc_id, True, index)
        else:
            raise ValueError("Unsupported weight_type: %s" % weight_type)

    def search_word(self, word):
        '''
        Retourne la liste des ids des documents contenant le mot passé en argument
        '''
        # Si le mot est dans les stop_words, on revoit tout les documents
        if word in self.stop_words:
            return self.documents_ids
        return self.word_index[word].keys()
