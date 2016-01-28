# coding=utf-8
from collections import defaultdict
import time


def get_queries():
    '''
    Parse les queries données avec la collection.

    Renvoie un dict {query_id: query}
    '''
    file = './dataset/query.text'
    queries = defaultdict(str)

    with open(file, 'r') as query_file:
        current_query = 0
        ignore = True
        for line in query_file:
            # On change la query courante quand on recontre le marqueur de nouveau doc
            if line.startswith('.I'):
                current_query = line[2:].strip()
            elif line.startswith('.W'):
                # Marqueur de "titre" = query. On arrete d'ignorer le contenu
                ignore = False
            elif line.startswith('.N') or line.startswith('.A'):
                ignore = True
            elif ignore is False:
                queries[current_query] += line.strip() + ' '  # on rajoute la ligne a la query courante
    return queries


def get_expected_results():
    '''
    Parse les resultats des queries donées avec la collection

    Renvoie un dict {query_id: [documents pertinents]}
    '''
    file = './dataset/qrels.text'
    results = defaultdict(list)

    with open(file, 'r') as qrels:
        for line in qrels:
            query_id, doc_id = line.split(' ')[:2]
            # Petit hack pour virer les 0 devant les nombres, tout en continuant d'utliser des strings
            # ie transforme '01' en '1' pour rester coherent avec le format dans l'index ou il n'y a pas ce 0
            query_id = str(int(query_id))
            doc_id = str(int(doc_id))
            # Rajoute le doc au resultats attendues de la query
            results[query_id].append(doc_id)
    return results


def precision(results, expected_results):
    '''
    Mesure de precision = P(pertinents|retrouvées)
    '''
    # Utilisations de set pour pouvoir facilement faire des intersections entre les 2 ensembles
    results = set(results)
    expected_results = set(expected_results)
    pertinents = results & expected_results
    return len(pertinents) / float(len(results))  # float force une division non entiere


def rappel(results, expected_results):
    '''
    Mesure de rappel = P(retrouvées|pertinents)
    '''
    # Utilisations de set pour pouvoir facilement faire des intersections entre les 2 ensembles
    results = set(results)
    expected_results = set(expected_results)
    pertinents = results & expected_results
    return len(pertinents) / float(len(expected_results))  # float force une division non entiere


def time_func(func, *args):
    '''
    Mesure le temps pris par le calcul de func avec les arguments données

    Renvoie un couple time, resultats
    '''
    start = time.time()
    results = func(*args)
    end = time.time()

    return (end - start, results)
