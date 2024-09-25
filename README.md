# Bulk Google Calendar Event Importer

Un script Python qui permet d'ajouter en masse des rendez-vous à votre Google Calendar à partir d'un fichier CSV en utilisant l'API Google Calendar via un compte de service.

## Présentation

Ce projet vous permet d'automatiser l'ajout en masse de rendez-vous dans votre Google Calendar en utilisant un fichier CSV. Il utilise un compte de service pour interagir avec l'API Google Calendar, évitant ainsi la nécessité d'une authentification interactive.

## Fonctionnalités

- Importation en masse d'événements depuis un fichier CSV.
- Utilisation de l'API Google Calendar via un compte de service.
- Gestion des fuseaux horaires.
- Gestion des erreurs lors de l'ajout des événements.

## Prérequis

- [Anaconda](https://www.anaconda.com/products/distribution) ou [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installé sur votre système.
- Un compte Google avec accès à Google Calendar.
- Accès au [Google Cloud Console](https://console.cloud.google.com/).

## Installation

### 1. Cloner le Répertoire

Clonez ce dépôt GitHub sur votre machine locale :

```bash
git clone https://github.com/votre-utilisateur/bulk-google-calendar-importer.git
cd bulk-google-calendar-importer

### 2. Installer Conda

Si vous n'avez pas encore installé Conda, téléchargez et installez **Miniconda** ou **Anaconda** :

- **Miniconda** : [Télécharger Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- **Anaconda** : [Télécharger Anaconda](https://www.anaconda.com/products/distribution)

### 3. Créer et Activer l'Environnement Conda

Créez un nouvel environnement Conda en utilisant le fichier `environment.yml` :

```bash
conda env create -f environment.yml
```

Une fois l'environnement créé, activez-le :

```bash
conda activate add_calendar_events_env
```

### 4. Installer les Dépendances

Toutes les dépendances nécessaires sont définies dans le fichier `environment.yml`. L'étape précédente les installe automatiquement. Si vous devez ajouter des dépendances supplémentaires, mettez à jour le fichier `environment.yml` et réexécutez la commande d'installation.

## Configuration de l'API Google Calendar

### 1. Activer l'API Google Calendar

1. Rendez-vous sur le [Google Cloud Console](https://console.cloud.google.com/).
2. Créez un nouveau projet ou sélectionnez un projet existant.
3. Dans le menu de navigation, allez à **API & Services > Bibliothèque**.
4. Recherchez **Google Calendar API** et cliquez sur **Activer**.

### 2. Créer un Compte de Service

1. Dans le Google Cloud Console, allez à **API & Services > Identifiants**.
2. Cliquez sur **Créer des identifiants > Compte de service**.
3. Remplissez les informations requises (nom, description) et cliquez sur **Créer**.
4. Vous pouvez généralement laisser les rôles par défaut et passer ces étapes en cliquant sur **Continuer** jusqu'à la fin.
5. Une fois le compte de service créé, allez dans la section **Clés**.
6. Cliquez sur **Ajouter une clé > Créer une clé** et choisissez le format **JSON**. Téléchargez le fichier `service_account.json` et placez-le dans le répertoire racine du projet.

### 3. Partager le Calendrier avec le Compte de Service

1. Ouvrez [Google Calendar](https://calendar.google.com/).
2. Dans le calendrier où vous souhaitez ajouter des événements, cliquez sur les trois points à côté du nom du calendrier et sélectionnez **Paramètres et partage**.
3. Sous **Partager avec des personnes spécifiques**, ajoutez l'adresse e-mail du compte de service (quelque chose comme `votre-service-account@votre-projet.iam.gserviceaccount.com`) et attribuez-lui le rôle **Modifier les événements**.

## Préparer le Fichier CSV

### Format du CSV

Le fichier CSV doit respecter le format suivant :

```csv
jj/mm/aaaa;sujet;heure début hh:mm;heure de fin hh:mm
25/12/2023;Réunion de Noël;10:00;11:00
01/01/2024;Nouvel An;00:00;01:00
...
```

- **jj/mm/aaaa** : Date de l'événement.
- **sujet** : Titre de l'événement.
- **heure début hh:mm** : Heure de début au format 24 heures.
- **heure de fin hh:mm** : Heure de fin au format 24 heures.

### Exemple de Fichier CSV

Créez un fichier nommé `rendezvous.csv` dans le répertoire racine du projet avec le contenu suivant :

```csv
jj/mm/aaaa;sujet;heure début hh:mm;heure de fin hh:mm
25/12/2023;Réunion de Noël;10:00;11:00
01/01/2024;Nouvel An;00:00;01:00
15/04/2024;Réunion Projet X;14:30;15:30
```

## Exécution du Script

Assurez-vous que votre environnement Conda est activé :

```bash
conda activate add_calendar_events_env
```

Exécutez le script Python `app.py` :

```bash
python app.py
```

### Description du Script

Le script `app.py` lit le fichier `rendezvous.csv`, parse les événements et les ajoute à votre Google Calendar en utilisant l'API via le compte de service configuré.

## Résolution des Problèmes

- **Problèmes de dépendances :** Assurez-vous d'utiliser l'environnement Conda spécifié et d'avoir installé toutes les dépendances via `environment.yml`.
- **Authentification :** Vérifiez que le fichier `service_account.json` est bien placé dans le répertoire racine du projet et que le compte de service a les permissions appropriées sur le calendrier.
- **Format du CSV :** Assurez-vous que le fichier CSV respecte le format requis. Les erreurs de format peuvent empêcher le script de parser correctement les événements.
- **Conflits de versions de `protobuf` :** Si vous rencontrez des erreurs liées à `protobuf`, assurez-vous que la version installée est compatible en suivant les instructions de l'[assistant](#résolution-des-problèmes).

## Sécurité

- **Fichier `service_account.json` :** Ne partagez jamais ce fichier et assurez-vous qu'il est inclus dans votre `.gitignore` si vous utilisez un dépôt Git. Ce fichier contient des informations sensibles permettant l'accès à votre projet Google Cloud.
- **Permissions Minimales :** Accordez au compte de service uniquement les permissions nécessaires pour réduire les risques en cas de compromission.
- **Vérifier les Chemins des Fichiers :** Assurez-vous que tous les fichiers mentionnés (`environment.yml`, `app.py`, `rendezvous.csv`, `service_account.json`) sont présents dans le répertoire racine.
- **Tester l'Installation et l'Exécution :** Suivez les étapes d'installation et d'exécution décrites dans le README pour vérifier que tout fonctionne correctement.

---

### Exemple de Fichier CSV

Voici un exemple de fichier `rendezvous.csv` :

```csv
jj/mm/aaaa;sujet;heure début hh:mm;heure de fin hh:mm
25/12/2023;Réunion de Noël;10:00;11:00
01/01/2024;Nouvel An;00:00;01:00
15/04/2024;Réunion Projet X;14:30;15:30
```

Assurez-vous que le fichier CSV est encodé en UTF-8 et respecte le format spécifié pour éviter les erreurs lors de l'exécution du script.

---

### Bonnes Pratiques

- **Utiliser un Environnement Virtuel Isolé :** Toujours utiliser un environnement Conda dédié pour chaque projet afin d'éviter les conflits de dépendances.
- **Sécuriser les Fichiers Sensibles :** Ajoutez `service_account.json` à votre `.gitignore` pour éviter de le committer dans votre dépôt Git.
- **Vérifier les Permissions :** Assurez-vous que le compte de service a les permissions appropriées sur le calendrier cible.
- **Tester avec un Petit Fichier CSV :** Avant d'importer un grand nombre d'événements, testez le script avec un petit fichier CSV pour vous assurer que tout fonctionne correctement.

### Ressources Utiles

- [Documentation de Conda](https://docs.conda.io/en/latest/)
- [Documentation de l'API Google Calendar](https://developers.google.com/calendar/api)
- [Guide sur les Comptes de Service Google](https://cloud.google.com/iam/docs/service-accounts)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
