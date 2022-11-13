[![Python](https://img.shields.io/badge/python-3.11-blue)](https://github.com/MeldSnake/oc_p1)

Script permettant l'extraction, transformation et chargement des données venant du site [books.toscrape.com](https://books.toscrape.com/) dans plusieurs fichiers CSV.

# __Description__

Plusieurs scripts permettant l'extraction, la transformation et le chargement des données relatif à des articles proposé sur books.toscrape.com dans un format de fichier CSV.

Chacun de ces scripts permettent d'effectuer la charge de travail nécessaire sur un niveau diffèrent.


# __Installation__

## Programmes requis
- [Git](https://git-scm.org/)
- [Python 3.11](https://www.python.org/downloads/) ou supérieur.
- [pip](https://docs.python.org/fr/3/library/ensurepip.html) si non installé par défaut avec Python.

## Initialisation de l'environnement virtuel

- Linux (sh) :
    ```bash
    > python -m venv .venv
    > sh ./.venv/scripts/activate
    ```
- Windows (cmd) :
    ```cmd
    > python -m venv .venv
    > 
    > .\.venv\Scripts\activate.bat
    ```
- Windows (PowerShell) :
    ```powershell
    > python -m venv .venv
    > & .\.venv\Scripts\Activate.ps1
    ```

Activation de l'environnement :
```shell
(.venv) > python -m pip install -r requirements.txt
```

# __Utilisation__

> **Toute utilisation nécessite l'environnement d'avoir préalablement été activé.**

## Phase 1 - Extraction depuis un article simple

```shell
(.venv) > python phase1.py "<URL DU LIVRE>"
```

Avec `<URL DU LIVRE>` étant l'adresse URL du livre demandé.

Le résultat se trouvera dans le dossier `output\phase1\` et aura pour nom de fichier `<NOM DU LIVRE>-<UPC>.csv`.

## Phase 2 - Extraction depuis une catégorie

```shell
(.venv) > python phase2.py "<URL DE LA CATEGORIE>"
```

Avec `<URL DE LA CATEGORIE>` étant l'adresse URL de la catégorie demandée.

Le résultat se trouvera dans le dossier `output\phase2\` et aura pour nom de fichier `<NOM DE LA CATEGORIE>.csv`.


## Phase 3 - Extraction de toutes les catégories du site

```shell
(.venv) > python phase3.py
```

Les résultats se trouveront dans le dossier `output\phase3\`. Ce script génère un fichier CSV par catégorie nommé de façon identique à la phase 2.

## Phase 4 - Extraction de toutes les catégories du site avec les images de couvertures.

```shell
(.venv) > python phase4.py
```

Les résultats se trouveront dans le dossier `output\phase4\`. Ce script est similaire à la phase 3 avec pour seule différence que des sous-dossiers seront créer pour chaque catégorie et contiendront toutes les images de couvertures de chacun des livres contenus par ces catégories.