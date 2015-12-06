# coding=utf-8


class CACMIndexer():
    '''
    Indexe une collection de documents
    '''

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
