import streamlit as st
import requests
from datetime import datetime, timedelta
import random

# Configuration de la page
st.set_page_config(page_title="Elite Sports Predictor AI", layout="wide")

# Simulation de base de données / API
# Note : Pour un usage réel, remplacez par une clé API de football-data.org ou api-football.com
API_KEY = "VOTRE_CLE_API" 

def get_prediction_logic(home, away, league):
    """
    Logique IA simulée basée sur les stats (Corners, Cartons, Fautes)
    """
    # Ici, on simule l'analyse de l'IA
    score_home = random.randint(0, 3)
    score_away = random.randint(0, 2)
    corners = random.randint(6, 14)
    cards = random.randint(2, 7)
    fouls = random.randint(15, 28)
    
    return {
        "score": f"{score_home} - {score_away}",
        "corners": corners,
        "cards": cards,
        "fouls": fouls,
        "confiance": f"{random.randint(65, 95)}%"
    }

# --- INTERFACE ---
st.title("⚽ Analytics & Predictions AI")
st.sidebar.header("Configuration de l'analyse")

# 1. Sélection de la Zone (Pays / Continent / International)
zone = st.sidebar.selectbox("Sélectionnez la Zone", 
    ["Europe (Top 5)", "Portugal", "Turquie", "Pays-Bas", "International (CAN/Euro/CM)", "Coupes d'Europe"])

# 2. Sélection dynamique du Championnat (Automatique)
leagues_dict = {
    "Europe (Top 5)": ["Premier League", "Championship", "La Liga", "Segunda", "Ligue 1", "Ligue 2", "Serie A", "Serie B", "Bundesliga", "2. Bundesliga"],
    "Portugal": ["Primeira Liga", "Segunda Liga"],
    "International (CAN/Euro/CM)": ["Coupe du Monde", "CAN", "Euro", "Matchs Amicaux", "Éliminatoires"],
    "Coupes d'Europe": ["Champions League", "Europa League", "Supercoupe d'Espagne"]
}

selected_league = st.sidebar.selectbox("Championnat / Tournoi", leagues_dict.get(zone, ["Ligue 1"]))

# 3. Sélection de la Date
selected_date = st.sidebar.date_input("Date du match", datetime.now())

# 4. Sélection des Équipes (Pré-remplies selon le championnat)
# Simulation de liste d'équipes pour l'exemple
teams_list = ["Real Madrid", "Atletico Madrid", "PSG", "Marseille", "Man City", "Arsenal", "Benfica", "Porto"]
home_team = st.sidebar.selectbox("Équipe à Domicile", teams_list)
away_team = st.sidebar.selectbox("Équipe à l'Extérieur", teams_list)

# --- LOGIQUE DE VÉRIFICATION ---
current_date = datetime.now().date()
diff_days = (current_date - selected_date).days

if st.button("Lancer l'Analyse Complète"):
    # Vérification si le match a déjà eu lieu
    if diff_days >= 1:
        st.warning(f"⚠️ Ce match s'est joué il y a {diff_days} jour(s).")
        st.info(f"Résultat final enregistré : {random.randint(0,4)}-{random.randint(0,4)}")
    
    # Vérification de l'existence du match (Simulé ici)
    elif random.choice([True, False]): # Simulation d'absence de match
        st.error(f"❌ Il n'y a pas de match entre {home_team} et {away_team} à la date du {selected_date}.")
    
    else:
        # Analyse IA
        res = get_prediction_logic(home_team, away_team, selected_league)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score Prévu", res["score"])
        with col2:
            st.metric("Corners attendus", res["corners"])
        with col3:
            st.metric("Cartons / Fautes", f"{res['cards']} / {res['fouls']}")
            
        st.success(f"Indice de confiance de l'IA : {res['confiance']}")
        
        # Météo et caractéristiques (Simulées)
        st.write(f"🌤️ **Météo prévue :** 18°C, Ciel dégagé. Avantage léger pour l'équipe à domicile sur terrain sec.")

# --- SECTION TICKET / COMBINÉ ---
st.divider()
st.subheader("🎫 Générateur de Ticket (Combiné)")
cote_cible = st.select_slider("Choisissez la cote souhaitée", options=[2, 4, 6, 10, 20, 100])

if st.button(f"Générer un ticket Cote {cote_cible}"):
    st.write("### Votre combiné conseillé :")
    st.write(f"1. {home_team} gagne ou Nul")
    st.write(f"2. Plus de 8.5 corners dans le match")
    st.write(f"3. {away_team} reçoit +1.5 cartons")
    st.info(f"Cote totale estimée : {float(cote_cible)}")
