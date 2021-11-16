# Projet 7 DA-Python OC (Hélène Mignon)
***Livrable du Projet 7 du parcours D-A Python d'OpenClassrooms : calcul de la meilleure combinaison d'actions en fonction de leur bénéfices. Utilisation de l'algorithme du sac à dos.***

_Testé sous Windows 10 - Python version 3.9.5_

## Initialisation du projet

### Windows :
    git clone https://github.com/hmignon/P7_mignon_helene.git

    cd P7_mignon_helene 
    python -m venv env 
    env\scripts\activate

    pip install -r requirements.txt


### MacOS et Linux :
    git clone https://github.com/hmignon/P7_mignon_helene.git

    cd P7_mignon_helene 
    python3 -m venv env 
    source env/bin/activate

    pip install -r requirements.txt


Note : Lors du traitement des données, le programme affiche une barre de progression (tqdm).

## Exécution du programme

### Bruteforce.py

    python bruteforce.py

**Le montant d'investissement par défaut est fixé à 500€.** Il est toutefois possible d'entrer un montant personnalisé comme suit :

    python bruteforce.py 345

*Note : Le bruteforce ne traîte que les données du fichier "test_shares.csv", contenant 20 actions. Les datasets 1 et 2 résulteraient à un temps d'exécution extrêmement long.*

### Optimized.py

La version optimisée nécessite d'entrer le nom du fichier à traîter, **sans le chemin d'accès ni l'extension de fichier** :

    python optimized.py dataset1

Comme pour le bruteforce, il est possible d'entrer un montant personnalisé, comme suit :

    python optimized.py dataset2 720

Enfin, il est également possible de traîter le fichier de test (20 actions), avec ou sans montant personnalisé :

    python optimized.py test_shares

    python optimized.py test_shares 450
