#!/usr/bin/env python
# coding=utf-8

# Interface principale de recherche
# Demande a l'utilisateur de choisir collection et modele de recherche
# Et lui permet d'effectuer des recherches


import time
import sys

from collection import CACMCollection
from index import Index
from vectorial_search import vectorial_search
from boolean_search import boolean_search


def choose_collection():
    """
    Demande à l'utilisateurs la collection et renvoie la collection et l'index
    """
    print('CHOIX DE LA COLLECTION:')
    print('1 - CACM')
    print('2 - Wikipedia (non implémenté pour le moment)')
    collection_choice = input('Choisissez une collection: ')
    if collection_choice == 1:
        start = time.time()
        collection = CACMCollection()
        collection_imported = time.time()
        print("\n")
        print("Collection CACM importée en %s secondes" % (collection_imported - start))
        index = Index(collection.documents)
        collection_indexed = time.time()
        print("Collection CACM indéxée en %s secondes" % (collection_indexed - collection_imported))
        print("Taille de l'index en mémoire: ~ %s Méga-octets" % (sys.getsizeof(index) / float(10**6)))
        print("\n")
        print("En realite, ce script utilise plus de memoire car on garde egalement dans la RAM")
        print("la collection entiere (~40 Mega-octets) pour pouvoir afficher le contenu des")
        print("resultats de recherche a l'utilisateur (et non juste l'id des documents).")
        print("Cependant, les fonctions de recherche utilisent exclusivement les indexes")
        print("(cf methodes boolean_search et vectorial_search)")

        return collection, index
    else:
        raise ValueError("Input invalide")


def choose_search_type():
    """
    Demande à l'utilisateur le type de recherche à effectuer la renvoie
    """
    print('\n')
    print('CHOIX DU TYPE DE RECHERCHE:')
    print('1 - Recherche vectorielle')
    print('2 - Recherche booléenne')
    print('3 - Recherche probabiliste (non implémenté pour le moment)')
    print('0 - quitter')
    search_choice = input('Choisissez un type de recherche: ')
    print('\n')
    if search_choice == 1:
        return "vectorial"
    if search_choice == 2:
        return "boolean"
    if search_choice == 0:
        sys.exit(0)
    else:
        raise ValueError("Input invalide")


def choose_weight_type():
    """
    Demande à l'utilisateur le type de ponderation à utiliser et la renvoie
    """
    # Recherche vectorielle
    ponderations = ["tf_idf", "tf_idf_normalized", "tf_idf_log", "tf_idf_log_normalized"]
    print('CHOIX DE LA PONDERATION:')
    for idx, ponderation in enumerate(ponderations):
        print('%s - %s' % (idx, ponderation))
    ponderation_choice = input('Choisissez une pondération: ')
    print('\n')
    if ponderation_choice >= len(ponderations):
        raise ValueError('Input invalide')
    else:
        return ponderations[ponderation_choice]


def choose_query():
    """
    Demande la query à l'utilisateur et la renvoie
    """
    print('CHOIX DE LA QUERY:')
    query = raw_input("Entrez votre query: ")
    print('\n')
    return query


def choose_query_bool():
    """
    Demande la query booléenne à l'utilisateur et la revoie
    """
    print('CHOIX DE LA QUERY BOOLEENNE:')
    print('La query doit être une "phrase" booléenne valide.')
    print('Opérateurs acceptés: "(", ")", "AND", "OR", "NOT"')
    print('Le nombre de paranthèses ouvertes doit matcher le nombre de paranthèses fermées')
    query = raw_input("Entrez votre query: ")
    print('\n')
    return query


def print_results_vectorial_search(search_results, query, collection):
    """
    Demande le nombre de résultats à afficher et les affichent
    """
    print('%s resultats pour la recherche "%s"' % (len(search_results), query))
    nb_doc_to_show = input('Combien de résultats (trier par ordre décroissant de similarité voulez vous afficher ? ')
    print('\n')
    for (doc_id, similarity) in search_results[:nb_doc_to_show]:
        print("Document: %sSimilarité: %s \n" % (collection.get_document_by_id(doc_id), similarity))


def print_results_boolean_search(search_results, query, collection):
    print('%s resultats pour la recherche "%s"' % (len(search_results), query))
    for doc_id in search_results:
        print("%s" % collection.get_document_by_id(doc_id))


# Run uniquement si le script est appelé directement
if __name__ == '__main__':
    # Choix de collection
    collection, index = choose_collection()

    while True:  # la possibilite de quitter est dans le choix du type de recherche
        search_type = choose_search_type()
        if search_type == "vectorial":
            weight = choose_weight_type()
            query = choose_query()
            start = time.time()
            search_results = vectorial_search(query, index, weight)
            end = time.time()
            print("Temps d'exécution de la recherche: %s secondes" % (end - start))
            print_results_vectorial_search(search_results, query, collection)

        if search_type == "boolean":
            query = choose_query_bool()
            start = time.time()
            search_results = boolean_search(query, index)
            end = time.time()
            print("Temps d'exécution de la recherche: %s secondes" % (end - start))
            print_results_boolean_search(search_results, query, collection)
