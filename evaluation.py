# coding=utf-8

# Script pour evaluer les performances du moteur de recheche

# Pour l'indexation, on evalue:
#   - temps de parsing de la collection
#   - temps d'indexation
#   - taille de l'index en memoire

# Pour une recherche on evalue:
#   - temps de recherche
#   - precision et rappel
#   - F et E measure

# Pour une collection de recheches, on evalue:
#   - Mean Average Precision
# (temps d'indexation, temps de recherche, precision, rappel)

import sys
from collections import defaultdict

from collection import CACMCollection
from index import Index
from vectorial_search import vectorial_search
from boolean_search import boolean_search
from evaluation_utils import time_func, precision, rappel, R_precision, E_measure, F_measure, moyenne, get_queries, get_expected_results

##############
# INDEXATION #
##############
# Timing de l'import de la collection
import_time, collection = time_func(CACMCollection)

# Timing de l'indexation et taille de l'index obtenu
indexation_time, index = time_func(Index, collection.documents)
index_size = sys.getsizeof(index) / float(10**6)


##############
# RECHERCHES #
##############

def evaluate_search(query, expected_results):
    '''
    Evalue la performance de la recherche donnée pour les differents modeles
    Calcule temps de recherche, precision, R precision, rappel, F et E measure
    '''

    # Ce qu'on va renvoyer
    # dict {'modele': {'time': x, 'precision': x, 'rappel': x}}
    evaluation = defaultdict(dict)

    # modele booleen
    bool_time, search_results = time_func(boolean_search, query, index)
    evaluation['bool']['time'] = bool_time
    evaluation['bool']['precision'] = precision(search_results, expected_results)
    evaluation['bool']['rappel'] = rappel(search_results, expected_results)
    # pas de R precision car resultats non ordonées
    evaluation['bool']['F_measure'] = F_measure(search_results, expected_results)
    evaluation['bool']['E_measure'] = E_measure(search_results, expected_results)

    # modele vectoriel (evalué avec poids tf idf log normalisee
    # (d'apres mes tests, c'est la ponderation qui donne les meilleurs resultats)
    vect_time, search_results = time_func(vectorial_search, query, index, "tf_idf_log_normalized")
    search_results = [result.doc_id for result in search_results]
    evaluation['vect']['time'] = bool_time
    evaluation['vect']['precision'] = precision(search_results, expected_results)
    evaluation['vect']['rappel'] = rappel(search_results, expected_results)
    evaluation['vect']['R_precision'] = R_precision(search_results, expected_results)
    evaluation['vect']['F_measure'] = F_measure(search_results, expected_results)
    evaluation['vect']['E_measure'] = E_measure(search_results, expected_results)

    return evaluation

# EVALUATION DE TOUTES LES QUERYS

queries = get_queries()
results = get_expected_results()
evaluations = {}

# On evalue les perfs de la query donnée
for idx, query in queries.iteritems():
    expected_results = results[idx]
    evaluations[idx] = evaluate_search(query, expected_results)
