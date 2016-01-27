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

import time
import sys

from collection import CACMCollection
from index import Index
from vectorial_search import vectorial_search
from boolean_search import boolean_search

##############
# INDEXATION #
##############
# Timing de l'import de la collection
start = time.time()
collection = CACMCollection()
done = time.time()
import_time = done - start

# Timing de l'indexation et taille de l'index obtenu
start = time.time()
index = Index(collection.documents)
done = time.time()
indexation_time = done - start
index_size = sys.getsizeof(index) / float(10**6)


# Pour chaque modele et ponderation
# Parser les requetes donnes et leurs resultats
# pour chaqune de ces requetes calculer toutes les mesures

# Calculer MAP de toutes ces requetes
