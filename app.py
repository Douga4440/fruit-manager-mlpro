import streamlit as st
from fruit_manager import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


st.title("🍇 Dashboard de la Plantation")

inventaire = ouvrir_inventaire()
prix = ouvrir_prix()
tresorerie = ouvrir_tresorerie()

with st.sidebar:
    st.header("🛒 Vendre des Fruits")
    fruit_vendre = st.selectbox("Choisir un fruit", list(inventaire.keys()))
    quantite_vendre = st.number_input("Quantité a vendre", min_value=1, step=1)

    if st.button("Vendre"):
        inventaire, tresorerie, message = vendre(inventaire, fruit_vendre, quantite_vendre, tresorerie, prix)
        st.success(message['text'])

    st.header("🌱 Récolter des Fruits")
    fruit_recolter = st.selectbox("Choisir un fruit à récolter", list(inventaire.keys()), key="recolte_individuelle")
    quantite_recolter = st.number_input("Quantité à récolter", min_value=1, step=1, key="quantite_recolte")

    if st.button("Récolter"):
        inventaire, message = recolter(inventaire, fruit_recolter, quantite_recolter)
        st.success(message['text'])


st.header("💰 Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie:.2f} $")

st.header("📈 Évolution de la trésorerie")
historique = lire_tresorerie_historique()
if historique:

    df = pd.DataFrame(historique).tail(20)  # Derniers 20 points
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["tresorerie"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Trésorerie ($)")
    ax.set_title("Évolution de la trésorerie")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    fig.autofmt_xdate()
    _, mid_col, _ = st.columns([1, 2, 1])
    mid_col.pyplot(fig)
else:
    st.info("Aucune donnée d'historique de trésorerie pour le moment.")


st.header("📦 Inventaire")
# Inventaire sous forme de tableau
st.table(inventaire)
# Inventraire sous forme de graphique
fig, ax = plt.subplots()
# Trier l'inventaire par quantité décroissante
inventaire = dict(sorted(inventaire.items(), key=lambda item: item[1], reverse=True))
ax.bar(inventaire.keys(), inventaire.values(), color="salmon", edgecolor='k')
ax.set_xlabel("Fruit")
ax.set_ylabel("Quantité")
ax.set_title("Inventaire")
st.pyplot(fig)


ecrire_inventaire(inventaire)
ecrire_tresorerie(tresorerie)

# --- Gestion des commandes (vue gérant) ---
st.divider()
st.header("📋 Gestion des commandes clients")

commandes = lire_commandes()
en_attente = [c for c in commandes if c["statut"] == "en_attente"]
validees = [c for c in commandes if c["statut"] == "validée"]
annulees = [c for c in commandes if c["statut"] == "annulée"]
ca_commandes = sum(c["total"] for c in validees)

# Métriques rapides
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("⏳ En attente", len(en_attente))
col_m2.metric("✅ Validées", len(validees))
col_m3.metric("❌ Annulées", len(annulees))
col_m4.metric("💵 CA commandes", f"{ca_commandes:.2f} $")

tab_attente, tab_historique, tab_nouvelle, tab_stats = st.tabs(
    ["⏳ En attente", "📂 Historique", "➕ Nouvelle commande", "📊 Statistiques"]
)


