# recherche-web-ecp
Projet pour le cours de Recherche d'Informations Web: implementation et benchmark de different modele de recherche sur la collection de document CACM

## Prerequis
- Python 2.7 (le code fonctionne probablement avec python3, mais je ne l'ai pas tester)
- la librarie nltk (installer via `sudo pip install nltk`). NLTK est utilisée pour ameliorer le preprocessing des documents et query (stopwords supplémentaires, tokenization plus precise et snowball stemming)
- Les packages `stopwords`, `punkt` et `snowball_data` de nltk. Pour les installer (dans un shell python):
```
    >import ntlk
    >nltk.download()
    # Télécharger stopwords dans corpora, punkt et snowball_data dans Models
```

## Instalation:
2 méthodes possible:
- cloner le repo: `git clone https://github.com/rcatajar/recherche-web-ecp.git`
- telecharger le code: `https://github.com/rcatajar/recherche-web-ecp/archive/master.zip`

## Utlisation et differents fichiers

`python search.py` lance l'interface de recherche.
`python evalution.py` lance une evaluation des performances du moteur pour les queries de reference de la collection et affiche les resultats moyens pour les modeles booleen et vectoriel.

Le reste des fichiers sont les classes et methodes utilisees pour la recherche:
- `documents.py` contient les classes represantant des documents d'une collection
- `collection.py` contient les classes representant des collections (avec des methodes pour importer et parser la collection CACM depuis les fichiers du dataset)
- `index.py` contient la classe d'Index capable d'indexer une serie de documents et de generer pour chaque document des vecteurs de poids de differents types
- `vectorial_search.py` et `boolean_search.py` contiennnent les methodes et la logique de recherche des modeles vectoriel et booléen
- `evaluation_utils.py` contient differentes methodes utile pour faire l'evaluation du moteur de recherche (timing, mesures, import des query et resultats de reference du dataset)
