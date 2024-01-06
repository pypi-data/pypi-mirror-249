# hito_nsip: module pour synchroniser Hito et NSIP

Ce module fournit des scripts pour gérer la synchronisation entre certaines informations entre Hito et NSIP.
Pour tous les scripts, la commande associée accepte l'option `--help` qui permet de connaitre la liste des
options et paramètres du script.


## Installation

Le déploiement du module `hito_nsip` nécessite le déploiement d'un environnement Python, de préférence distinct
de ce qui est délivré par l'OS car cela pose de gros problèmes avec les prérequis sur les versions
des dépendances. Les environnements recommandés sont [pyenv](https://github.com/pyenv/pyenv),
[poetry](https://python-poetry.org) ou [Anaconda](https://www.anaconda.com/products/individual).
Pour la création d'un environnement virtuel avec Conda, voir la
[documentation spécifique](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands).

Pour installer le module `hito_nsip`, il faut utiliser les commandes suivantes :

```bash
pip install hito_nsip
```

### Dépendances

Pour connaitre la liste des dépendances de ce module, voir la propriété `dependencies`
dans le fichier `pyproject.toml` se trouvant dans les sources de l'application.
Elles sont automatiquement installées par la commande `pip`.



## Mise à jour des informations de NSIP/annuaire à partir d'Hito

*Commande: `hito2nsip [--help]`*

Ce script met à jour dans l'annuaire IN2P3 (NSIP) les informations bureau, 
téléphone et équipe de rattachement à partir de Hito et définit
l'email à `prenom.nom@ijclab.in2p3.fr`. La récupération des informations existantes sur les agents
et leur mise à jour se fait à travers l'API NSIP. Les fichiers nécessaires au fonctionnement 
du script sont :

* Une extraction des données de Hito (`--hito-agents-csv`), typiquement la même que celle requise pour `fix_nsip_team_names.py`,
avec au minimum les colonnes suivantes :
  
  ```csv
  Nom;Prénom;Numéro agent;email;ID Connexion;Archivé ?;Téléphone;Bureau;Equipe
  ```
 
* La liste des mappings explicites entre les noms Hito et RESEDA/NSIP (`--hito-reseda-mappings`), identique à celle
requise pour `fix_nsip_team_names.py`. Le fichier est requis mais son contenu peut être vide (à part l'entête).
  
* Une liste de définition explicite de l'email IJCLab des agents (`--email-fixes`), pour ceux qui n'obéissent pas au "pattern standard",
avec au minimum les colonnes suivantes :
  
  ```csv
  Hito-based email;Fixed email
  ```
  
Par défaut, le script affiche les actions qui sont nécessaires sans les exécuter. Pour les appliquer
il faut utiliser l'option `--execute`.

Le script peut aussi produire :

* Un script (`--aliases-check-script`) à  exécuter sur la machine d'administration Zimbra pour vérifier l'existence 
de tous les emails en `@ijclab.in2p3.fr` (ainsi que les anciens labos IN2P3) et alias `prenom.nom@ijclab.in2p3.fr`.
  
* Un CSV avec la liste de tous les agents et leur email IJCLab (`--email-list`)

Il existe aussi plusieurs options pour afficher les changements qui seront faits (`--show-change_details`), 
les agents non trouvés dans NSIP ou dans Hito (`--show-missing-agents`), les
incohérences entre le mail RESEDA (récupéré dans NSIP) et le mail de connexion dans Hito (`--wrong-connection-emails`)...
Voir le help pour la liste de toutes les options disponibles.
