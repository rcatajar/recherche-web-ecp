# coding=utf-8
from collections import defaultdict
import string


class CACMIndexer():
    '''
    Indexe une collection de documents
    '''

    # L'emplacement de la collection
    COLLECTION_PATH = './dataset/cacm.all'

    # Les marqueurs qui nous intéressent
    MARKER_NEW_DOC = '.I'
    MARKER_TITLE = '.T'
    MARKER_SUMMARY = '.W'
    MARKER_KEYWORDS = '.K'

    # Les marqueurs à ignorer (cf sujet du projet)
    IGNORED_MARKERS = ['.B', '.A', '.N', '.X', '.C']

    # Les documents non traités, dictionnaire de la forme {'id du document': [liste des lignes]}
    # defaultdict permet de spécifier que les valeurs du dict sont des listes
    raw_documents = defaultdict(list)

    # Les documents parsés, dictionnaire de la forme:
    # 'id doc': {
    #    'title': 'titre du doc'
    #    'summary': 'résumé du documents'
    #    'keywords': 'mots clés'
    # }
    documents = defaultdict(dict)

    # L'Index qu'on va construire, dictionnaire de la forme:
    # 'id doc': {
    #    'mot 1': occurence (int)
    #    'mot 2': occurence (int)
    # }
    index = defaultdict(dict)

    # Un index inversé basique, qui nous sera utile pour construire les indexs inversés avec pondération.
    # Dictionnaire de la forme:
    # 'mot': {
    #    'occurences': 42,  # nbre d'occurences du mot dans toute la collection
    #    'documents': [liste des docs qui contiennent ce mot]
    # }
    basic_reversed_index = defaultdict(lambda: {'occurences': 0, 'documents': []})

    # la stop-liste
    STOP_LIST_PATH = './dataset/common_words'
    stop_list = []

    def __init__(self):
        self._separate_documents()
        self._parse_documents()
        self._build_stop_list()
        self._build_index()
        self._build_basic_reversed_index()

    def _build_stop_list(self):
        '''
        Remplit la stop liste a a partir des common_words du dataset
        '''
        with open(self.STOP_LIST_PATH, 'r') as common_words:
            for word in common_words:
                self.stop_list.append(word.strip().lower())

    def _separate_documents(self):
        '''
        Ouvre la collection et sépare les documents (remplit self.raw_documents)
        '''
        current_doc = 0
        # Lit le fichier ligne par ligne
        with open(self.COLLECTION_PATH, 'r') as collection:
            for line in collection:
                # On change le document courant quand on recontre le marqueur de nouveau doc
                if line.startswith(self.MARKER_NEW_DOC):
                    current_doc = line[2:].strip()
                # Sinon, on rajoute la ligne courante dans le document
                else:
                    self.raw_documents[current_doc].append(line)

    def _parse_documents(self):
        '''
        Parse les documents, traite les différents champs et remplit self.documents
        '''
        for _id, document in self.raw_documents.items():
            self.documents[_id] = self._parse_document(document)

    def _parse_document(self, document):
        '''
        Parse le document passé en argument et retourne le document processé
        '''
        ignore = False  # Pour savoir si le champ courant est a ignorer
        current_field = None  # le champ courant
        # le document qu'on va construire
        processed_document = {'title': '', 'summary': '', 'keywords': ''}

        for line in document:
            # Si la ligne commence par un marqueur, on set ignore et current_field selon le type de marqueur
            if any(line.startswith(marker) for marker in self.IGNORED_MARKERS):
                ignore = True
            elif line.startswith(self.MARKER_TITLE):
                ignore = False
                current_field = 'title'
            elif line.startswith(self.MARKER_SUMMARY):
                ignore = False
                current_field = 'summary'
            elif line.startswith(self.MARKER_KEYWORDS):
                ignore = False
                current_field = 'keywords'

            # Sinon, on remplit le champ approprié s'il ne faut pas l'ignorer
            elif ignore is False:
                processed_document[current_field] += line

        return processed_document

    def _build_index(self):
        '''
        Construit notre index
        '''
        for _id, document in self.documents.items():
            self.index[_id] = self._index_document(document)

    def _index_document(self, document):
        '''
        Construit et retourne un index pour le documents donnés
        '''
        # L'index du document. On set la valeur par default d'un mot a 0
        index = defaultdict(int)

        # TRAITEMENTS PRELIMINAIRES:
        # on recupere tout le texte du document, et on met tout en minuscule
        text = '\n'.join([document['title'], document['summary'], document['summary']])
        text = text.lower()

        # TOKENISATION:
        # TODO: tokenisation plus précise via NLTK http://www.nltk.org/howto/tokenize.html
        # On remplace la ponctuation et les sauts de ligne par des espaces
        # puis on recupere la liste de mots dans le texte
        for punct in (string.punctuation):
            text = text.replace(punct, ' ')
        text = text.replace('\n', ' ')
        words = [word for word in text.split(' ') if word]

        # STOPLIST:
        # on retire les mots qui sont dans la stoplist
        words = [word for word in words if word not in self.stop_list]

        # STEMMING (Non demandé)
        # TODO: si j'ai le temps (facile a faire avec nltk => http://www.nltk.org/howto/stem.html)

        # STATISTIQUE
        for word in words:
            index[word] += 1

        return index

    def _build_basic_reversed_index(self):
        for _id, index_doc in self.index.items():
            for word, occurences in index_doc.items():
                self.basic_reversed_index[word]['occurences'] += occurences
                self.basic_reversed_index[word]['documents'].append(_id)
