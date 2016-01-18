# coding=utf-8

from collections import namedtuple
from math import sqrt

from index import Index
from documents import QueryDocument


# Un resultat de recherche, couple (document_id, similarité avec la query)
SearchResult = namedtuple("SearchResult", ['doc_id', 'similarity'])


def vectorial_search(querystring, collection_index, weight_type):
    '''
    Recherche vectorielle de `querystring` dans `collection_index` en utilisant les poids
    de type `weight_type`. Renvoie les résultats de similarité > 0 (ordonnées par similarité)
    '''
    search_results = []  # Resultat de la recherche

    # On indexe la recherche et on crée son vecteur
    query_doc = QueryDocument(querystring)
    query_index = Index([query_doc])
    # On calcule le vecteur de la query par rappport a l'index de la collection
    query_vector = query_index.get_document_vector(query_doc.id, weight_type, collection_index)

    # On calcule la similarité entre la query et chaque document de la collection
    for doc_id in collection_index.documents_ids:
        doc_vector = collection_index.get_document_vector(doc_id, weight_type)
        similarity = cosinus_similarity(query_vector, doc_vector)
        search_result = SearchResult(doc_id, similarity)
        search_results.append(search_result)

    # On trie nos resultats par ordre decroissant de similarité
    search_results = sorted(search_results, key=lambda result: -result.similarity)

    # On revoie les résultats qui ont une similarité > 0
    return [result for result in search_results if result.similarity > 0]


def cosinus_similarity(query_vector, doc_vector):
    '''
    Calcule la similarité entre query_vector et doc_vector, via la mesure cosinus
    '''
    # TODO: cacher norm_query pour ne pas la recalculer a chaque fois
    norm_query = sqrt(sum(weight ** 2 for weight in query_vector.values()))
    norm_doc = sqrt(sum(weight ** 2 for weight in doc_vector.values()))

    # On itere sur les mots de la query plutot que sur ceux du documents
    # car cette liste est generalement plus courte
    similarity = sum(query_vector[word] * doc_vector[word] for word in query_vector.keys())
    similarity = similarity / (norm_query * norm_doc)

    return similarity
