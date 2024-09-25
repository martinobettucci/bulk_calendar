import csv
from datetime import datetime
import os.path
import pandas as pd

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Définir les SCOPES requis
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR = 'martino.bettucci@gmail.com'

def authenticate_service_account(json_keyfile):
    """Authentifie le compte de service et retourne un service Google Calendar."""
    credentials = service_account.Credentials.from_service_account_file(
        json_keyfile, scopes=SCOPES)

    # Si vous devez accéder à un calendrier d'utilisateur spécifique, utilisez 'subject'
    # credentials = credentials.with_subject('utilisateur@domaine.com')

    service = build('calendar', 'v3', credentials=credentials)
    return service


def lire_csv(fichier_csv):
    """Lit le fichier CSV et retourne une liste de dictionnaires avec les événements."""
    df = pd.read_csv(fichier_csv, sep=';', header=None, names=['date', 'sujet', 'heure_debut', 'heure_fin'])
    evenements = []
    for index, row in df.iterrows():
        date_str = row['date']
        sujet = row['sujet']
        heure_debut_str = row['heure_debut']
        heure_fin_str = row['heure_fin']

        # Parse la date et les heures
        date = datetime.strptime(date_str, '%d/%m/%Y')
        heure_debut = datetime.strptime(heure_debut_str, '%H:%M').time()
        heure_fin = datetime.strptime(heure_fin_str, '%H:%M').time()

        # Combiner la date et l'heure
        debut = datetime.combine(date, heure_debut)
        fin = datetime.combine(date, heure_fin)

        # Convertir en format RFC3339 avec fuseau horaire
        debut_iso = debut.isoformat()
        fin_iso = fin.isoformat()

        evenement = {
            'summary': sujet,
            'start': {
                'dateTime': debut_iso,
                'timeZone': 'Europe/Paris',  # Ajustez votre fuseau horaire
            },
            'end': {
                'dateTime': fin_iso,
                'timeZone': 'Europe/Paris',
            },
        }
        evenements.append(evenement)
    return evenements


def ajouter_evenements(service, evenements, calendar_id):
    """Ajoute une liste d'événements au Google Calendar spécifié."""
    for evenement in evenements:
        try:
            event = service.events().insert(calendarId=calendar_id, body=evenement).execute()
            print(f"Événement créé: {event.get('htmlLink')}")
        except Exception as e:
            print(f"Erreur lors de la création de l'événement '{evenement['summary']}': {e}")


def lister_evenements(service, calendar_id, max_results=10):
    """Liste les prochains événements dans le calendrier spécifié."""
    events_result = service.events().list(calendarId=calendar_id, maxResults=max_results, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('Aucun événement trouvé.')
        return

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def main():
    fichier_csv = 'rendezvous.csv'
    json_keyfile = 'service_account.json'

    if not os.path.exists(fichier_csv):
        print(f"Le fichier {fichier_csv} n'existe pas.")
        return

    if not os.path.exists(json_keyfile):
        print(f"Le fichier {json_keyfile} est manquant.")
        return

    service = authenticate_service_account(json_keyfile)
    evenements = lire_csv(fichier_csv)
    ajouter_evenements(service, evenements, calendar_id=CALENDAR)

    # Liste les 10 prochains événements pour vérifier
    lister_evenements(service, calendar_id=CALENDAR, max_results=10)


if __name__ == '__main__':
    main()
