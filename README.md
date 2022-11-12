# NOTICE

Script permettant l'extraction, transformation et chargement des donnée venant du site [books.toscrape.com](https://books.toscrape.com/) dans plusieurs fichier CSV.

## Description

Plusieur script permettant l'extraction, la transformation et le chargement des donnée relatif à des articles proposé sur [books.toscrape.com](https://books.toscrape.com) dans un format de fichier CSV.

Chacun des ces scripts permettent d'effectuer la charge de travail necessaire sur un niveau different.

## Activation de l'environement virtuel

```shell
python -m pip install -r requirements.txt
```

## Execution

### Phase 1 - Extraction depuis un article simple

```shell
python phase1.py "<URL DU LIVRE>"
```

Le resultat ce trouvera dans le dossier `output\phase1\` et aura pour nom de fichier `<NOM DU LIVRE>-<UPC>.csv`

### Phase 2 - Extration depuis une categorie

```shell
python phase2.py "<URL DE LA CATEGORIE>"
```

Le resultat se trouvera dans le dossier `output\phase2\` et aura pour nom de fichier `<NOM DE LA CATEGORIE>.csv`.

### Phase 3 - Extraction de toutes les categories du site

```shell
python phase3.py
```

Les resultats se trouveront dans le dossier `output\phase3\`.
Ce script genere un fichier CSV par categorie nommé de façon identique à la phase 2.

### Phase 3 - Extraction de toutes les categories du site avec les images de couvertures.

```shell
python phase4.py
```

Les resultats se trouveront dans le dosier `output\phase4\`.
Ce script est similaire à la phase 3 avec pour seule difference que des sous-dossier seront creer pour chaque categorie et contiendront toute les images couvertures des chacun des livres contenue par ces categories.