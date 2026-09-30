# Evaluation DevOps

## Prérequis

Pour lancer le projet en local :

- Docker et Docker Compose
- Python 3.11 ou 3.12
- Git

Projet réalisé dans le cadre de l'évaluation DevOps.

L'application est une API Flask utilisant Redis. Elle est conteneurisée avec Docker et dispose d'une CI/CD avec GitHub Actions.

## Services

Le projet utilise trois services :

- Flask : application web
- Redis : stockage du compteur de visites
- Prometheus : récupération des métriques

## Endpoints

- `/` : page principale
- `/health` : vérifie que l'application et Redis fonctionnent
- `/visits` : incrémente un compteur stocké dans Redis
- `/metrics` : expose les métriques Prometheus
- `/simulate-error` : génère une erreur 500 pour tester les métriques

## Lancer le projet

Construire et démarrer les conteneurs :

```powershell
docker compose up -d --build
```

Vérifier les conteneurs :

```powershell
docker compose ps
```

Tester l'application :

```powershell
curl.exe http://localhost:5000/
curl.exe http://localhost:5000/health
curl.exe http://localhost:5000/visits
```

Prometheus est accessible sur :

```text
http://localhost:9090
```

Pour arrêter les conteneurs :

```powershell
docker compose down
```

## Tests

Installer les dépendances :

```powershell
pip install -r requirements.txt
```

Lancer les tests :

```powershell
python -m pytest
```

Lancer le lint Python :

```powershell
flake8 app tests
```

Lancer le lint YAML :

```powershell
yamllint .github docker-compose.yml prometheus.yml alert_rules.yml
```

## CI

La CI est exécutée lors d'un push sur `main` et lors d'une pull request.

Elle contient les jobs suivants :

- lint
- test
- build
- ci-ok

Les tests sont exécutés avec Python 3.11 et Python 3.12.

## CD

Après une CI réussie, la CD construit l'image Docker et la pousse sur GitHub Container Registry.

Les tags utilisés sont :

- `latest`
- SHA court du commit
- `v1.0.0`

Le déploiement est effectué sur un runner GitHub self-hosted.

Après le déploiement, l'endpoint `/health` est testé avec trois tentatives. En cas d'échec, un rollback vers l'image précédente est prévu.

## Métriques

Prometheus récupère notamment :

- le nombre de requêtes HTTP par endpoint et code HTTP
- la durée des requêtes
- le SHA ou la version actuellement déployée

Deux règles d'alerte sont configurées :

- taux d'erreurs HTTP 5xx supérieur à 10 % pendant 1 minute
- latence p95 supérieure à 500 ms pendant 2 minutes
