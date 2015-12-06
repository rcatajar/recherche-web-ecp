# coding=utf-8
from collections import defaultdict


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
