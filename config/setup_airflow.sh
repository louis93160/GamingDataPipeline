#!/bin/bash

# Activer l'environnement virtuel
source ../airflow_venv/bin/activate

# Définir le répertoire Airflow
export AIRFLOW_HOME=~/GamingDataPipeline

# Initialiser la base de données Airflow
airflow db init


# Démarrer le scheduler et le webserver
airflow scheduler &
airflow webserver --port 8080