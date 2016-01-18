# coding=utf-8


class Document(object):
    '''
    Represente un document.
    Un document doit avoir deux propriétés: text et id
    '''
    @property
    def id(self):
        raise NotImplementedError()

    @property
    def text(self):
        raise NotImplementedError()


class CACMDocument(Document):
    '''
    Represente un document de la collection CACM
    '''
    def __init__(self, doc_id, title, summary, keywords):
        self.doc_id = doc_id
        self.title = title
        self.summary = summary
        self.keywords = keywords

    # Pour avoir un joli "print" du document
    def __str__(self):
        return 'ID: %s  TITRE: %s' % (self.doc_id, self.title)

    @property
    def id(self):
        return int(self.doc_id)

    @property
    def text(self):
        return ' '.join([self.title, self.summary, self.keywords])


class QueryDocument(Document):
    '''
    Represente une recherche
    '''

    def __init__(self, query):
        self.query = query

    @property
    def text(self):
        return self.query

    @property
    def id(self):
        # -1 pour etre sure qu'il n'y aura pas de conflit avec l'id des docs de la collection
        return -1
