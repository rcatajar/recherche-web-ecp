# coding=utf-8
from collections import defaultdict

from documents import CACMDocument


class Collection(object):
    '''
    Represente une collection de documents
    '''
    _documents = {}  # {id: Document}


class CACMCollection(Collection):
    '''
    La collection CACM.
    La classe gere l'import et le parsing de la collection depuis le fichier texte
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

    def __init__(self):
        raw_documents = self._separate_documents()
        self._import_documents(raw_documents)

    def get_document_by_id(self, doc_id):
        '''
        Renvoi le document avec l'id donné s'il existe (sinon None)
        '''
        return self._documents.get(doc_id, None)

    @property
    def documents(self):
        '''
        Liste des documents dans la collection
        '''
        return self._documents.values()

    def _separate_documents(self):
        '''
        Ouvre la collection et sépare les documents (remplit self.raw_documents)
        '''
        raw_documents = defaultdict(list)   # Dict {id_doc: [lignes du doc]}
        current_doc = 0
        # Lit le fichier ligne par ligne
        with open(self.COLLECTION_PATH, 'r') as collection:
            for line in collection:
                # On change le document courant quand on recontre le marqueur de nouveau doc
                if line.startswith(self.MARKER_NEW_DOC):
                    current_doc = line[2:].strip()
                # Sinon, on rajoute la ligne courante dans le document
                else:
                    raw_documents[current_doc].append(line)
        return raw_documents

    def _import_documents(self, raw_documents):
        '''
        Parse les documents, traite les différents champs et remplit self.documents
        '''
        for _id, document in raw_documents.items():
            document = self._parse_document(document)
            document = CACMDocument(_id, document['title'], document['summary'], document['keywords'])
            self._documents.append(document)

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
