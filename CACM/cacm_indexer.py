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
    MARKER_PUB_DATE = '.B'
    MARKER_AUTHOR = '.A'
    MARKER_COLLECTION_DATE = '.N'
    MARKER_REF = '.X'

    # Les documents non traités, dictionnaire de la forme {'id du document': [liste des lignes]}
    # defaultdict permet de spécifier que les valeurs du dict sont des listes
    raw_documents = defaultdict(list)

    def _separate_documents(self):
        '''
        Ouvre la collection et sépare les documents (remplit self.raw_documents)
        '''
        current_doc = 0
        # Lit le fichier ligne par ligne
        with open(self.COLLECTION_PATH, 'r') as collection:
            for line in collection:
                if line.startswith(self.MARKER_NEW_DOC):
                    # nouveau doc => on recupere son index
                    current_doc = line[2:].strip()
                else:
                    # On rajoute le contenu au document
                    self.raw_documents[current_doc].append(line)
