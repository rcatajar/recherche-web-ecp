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
from evaluation_utils import time_func

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
    Evalue la recherche donnée pour les differents modeles
    Calcule temps de recherche, precision, rappel, F et E measure
    '''

    # Ce qu'on va renvoyer
    # dict {'modele': {'time': x, 'precision': x, 'rappel': x}}
    evaluation = defaultdict(dict)

    # modele booleen
    bool_time, search_results = time_func(boolean_search, query, index)
    evaluation['bool']['time'] = bool_time

# Pour chaque modele et ponderation
# Parser les requetes donnes et leurs resultats
# pour chaqune de ces requetes calculer toutes les mesures

# Calculer MAP de toutes ces requetes
