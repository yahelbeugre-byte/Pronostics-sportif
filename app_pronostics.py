# app_pronostics.py
import streamlit as st
import requests
from datetime import datetime, timedelta

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Pronostics Sportifs IA", layout="wide")
API_KEY = st.secrets["API_KEY"]  # Clé RapidAPI ou autre API sportive
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

# ----------------- FONCTIONS -----------------
def get_current_season():
    """Renvoie automatiquement la saison actuelle en format 2025 par exemple"""
    return datetime.now().year if datetime.now().month < 7 else datetime.now().year

def get_leagues_by_country(country):
    """Renvoie les ligues disponibles pour un pays"""
    url = f"https://v3.football.api-sports.io/leagues?country={country}"
    response = requests.get(url, headers=HEADERS).json()
    return {league['name']: league['id'] for league in response['response']}

def get_teams_by_league(league_id, season):
    """Renvoie toutes les équipes d'une ligue et saison donnée"""
    url = f"https://v3.football.api-sports.io/teams?league={league_id}&season={season}"
    response = requests.get(url, headers=HEADERS).json()
    return {team['team']['name']: team['team']['id'] for team in response['response']}

def get_match_data(league_id, date, home_id, away_id):
    """Récupère le match selon la date et les équipes"""
    url = f"https://v3.football.api-sports.io/fixtures?league={league_id}&date={date}&team={home_id}"
    response = requests.get(url, headers=HEADERS).json()
    for match in response['response']:
        if match['teams']['home']['id'] == home_id and match['teams']['away']['id'] == away_id:
            return match
    return None

def generate_pronostic(match):
    """Exemple simplifié d'IA pour pronostic"""
    # On peut ici intégrer un modèle plus complexe
    home_score = match['goals']['home'] if match['goals']['home'] is not None else "?"
    away_score = match['goals']['away'] if match['goals']['away'] is not None else "?"
    return f"Pronostic : {home_score} - {away_score}"

# ----------------- INTERFACE -----------------
st.title("Pronostics Sportifs IA")

# Sélection pays
countries = ["England", "Spain", "France", "Italy", "Germany", "Portugal", "Turkey", "Netherlands"]
country = st.selectbox("Sélectionner le pays", countries)

# Sélection ligue
leagues = get_leagues_by_country(country)
league_name = st.selectbox("Sélectionner la ligue", list(leagues.keys()))
league_id = leagues[league_name]

# Saison automatique
season = get_current_season()

# Sélection équipes
teams = get_teams_by_league(league_id, season)
home_team = st.selectbox("Équipe à domicile", list(teams.keys()))
away_team = st.selectbox("Équipe à l'extérieur", list(teams.keys()))
home_id = teams[home_team]
away_id = teams[away_team]

# Sélection date
selected_date = st.date_input("Sélectionner la date du match", datetime.now().date())

# Bouton pronostic
if st.button("Obtenir pronostic"):
    match = get_match_data(league_id, selected_date.strftime("%Y-%m-%d"), home_id, away_id)
    
    if match is None:
        st.warning("Il n'y a pas de match entre ces équipes à la date sélectionnée.")
    else:
        # Détecter si le match est passé
        match_date_time = datetime.strptime(match['fixture']['date'], "%Y-%m-%dT%H:%M:%S%z")
        delta = datetime.now(match_date_time.tzinfo) - match_date_time
        if delta.total_seconds() > 0:
            st.info(f"Ce match s'est joué il y a {int(delta.total_seconds()/3600)} heures. Score final : {match['goals']['home']} - {match['goals']['away']}")
        else:
            st.success(generate_pronostic(match))
