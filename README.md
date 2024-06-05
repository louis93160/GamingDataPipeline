<h2 align="center" style="font-size: 20px;">Mise en place d'un pipeline ETL depuis une base MongoDB</h2>

<div align="center" style="font-size: 22px;">Pojet Data Engineering - Louis Duvieux</div>

<br><br>

<p align="center">
  <img src="https://icon.icepanel.io/Technology/svg/Python.svg" alt="Python" height="80">
  <img src="https://icon.icepanel.io/Technology/svg/MongoDB.svg" alt="MongoDB" height="80">
  <img src="https://icon.icepanel.io/Technology/svg/Apache-Airflow.svg" alt="Airflow" height="80">
  <img src="https://icon.icepanel.io/Technology/svg/PostgresSQL.svg" alt="PostgreSQL" height="80">
</p>








## Introduction

Ce projet a pour objectif d'améliorer le catalogue de vente en ligne d'une enseigne de jeux vidéo en proposant, sur sa page d’accueil et dans ses campagnes de communication (newsletter, réseaux sociaux), une liste des jeux les mieux notés et les plus appréciés de la communauté sur les derniers jours. Pour cela, nous devons récupérer et traiter les avis les plus récents de nos clients en ligne afin de déterminer les jeux les mieux notés.

## Architecture du Projet

### Pipeline de Données

Le pipeline de données est conçu pour alimenter automatiquement un Data Warehouse (base de données SQL) avec les informations sur les jeux les mieux notés, tous les jours, en utilisant les données depuis une base MongoDB.

### Contrainte et Exigences

1. **Exactitude et Facilité de Manipulation**: Les informations sur les jeux doivent être exactes et facilement manipulables pour les différents métiers.
2. **Compatibilité SQL**: Le Data Warehouse doit être compatible SQL (MySQL, PostgreSQL ou MariaDB).
3. **Gestion des Doublons**: Le pipeline doit gérer les doublons et remplacer les valeurs existantes si elles sont déjà présentes.
4. **Période de Temps**: Seuls les avis des 6 derniers mois seront pris en compte.
5. **Quantité de Jeux**: Les 15 jeux les mieux notés seront ajoutés chaque jour au Data Warehouse.


## Description des Données

Les données sont disponibles sous forme de fichier compressé au format JSON. Chaque observation contient les caractéristiques suivantes :

- `reviewerID`: Identifiant unique de l'utilisateur.
- `verified`: Indique si l'utilisateur est un utilisateur vérifié.
- `asin`: Identifiant unique du produit.
- `reviewerName`: Nom ou pseudo de l'utilisateur.
- `vote`: Nombre de votes associés à l'avis de l'utilisateur.
- `style`: Style associé au jeu vidéo.
- `reviewText`: Description complète de l'avis.
- `overall`: Note attribuée par l'utilisateur au jeu vidéo.
- `summary`: Résumé de l'avis.
- `unixReviewTime`: Timestamp de l'avis.
- `reviewTime`: Date de l'avis.
- `image`: URL des images jointes par l'utilisateur.

## Structure du Projet

### Répertoires et Fichiers

<pre>
GamingDataPipeline/
├── dags/
│   └── etl_dag.py          Fichier python contenant le DAG
├── scripts/
│   └── pipeline_etl.py       Script Python du Pipeline
├── logs/                   Répertoire pour les logs Airflow
├── config/
│   └── setup_airflow.sh    Script shell pour configurer et démarrer Airflow
└── README.md               Documentation du projet
</pre>

### Scripts Principaux

1. **Extraction des données et transformation des données**:
    - `pipeline_etl.py`: Script pour extraire les données de la base MongoDB, transformer les données puis les extraire dans le Data Warehouse PostgreSQL.

2. **Planiffication du DAG Airflow**:
    - `etl_dag.py`: Script pour planifier le DAG Airflow ainsi que la task python.

3. **Chargement des Données dans le Data Warehouse**:
    - Chargement des données transformées dans le Data Warehouse SQL.
    - Gestion des doublons et remplacement des valeurs existantes.

