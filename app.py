import numpy_financial as npf
import streamlit as st
from db import  init_db, save_project, load_project, list_projects

init_db()

st.set_page_config(page_title="Simulateur d'investissement immobilier", page_icon="📈")

st.title("🏠 Simulateur Immobilier 💸")

# Charger un projet existant
with st.expander("🔄 Charger un projet"):
    projets_disponibles = list_projects()
    projet_choisi = st.selectbox("📂 Charger un projet existant :", projets_disponibles)

    if st.button("Charger le projet sélectionné"):
        donnees = load_project(projet_choisi)
        if donnees:
            for k, v in donnees.items():
                st.session_state[k] = v
            st.success(f"Projet '{projet_choisi}' chargé dans les champs ✅")

st.header("💰 ACQUISITION")
prix = st.number_input("Prix d'achat (hors frais d'agence) (€)", value=100000, key="prix")
surface = st.number_input("Surface (m²)", min_value=8, value=8, key="surface")
frais_notaire_defaut = 0.09 * prix
frais_notaire = st.number_input(
    "Frais de notaire - automatique si ancien (€)",
    value=frais_notaire_defaut,
    key="frais_notaire"
)
with st.expander("⚙️ Paramètres avancés (optionnels)"):
    frais_agence = st.number_input("Frais d'agence si non inclus dans prix d'achat (€)", value=0, key="frais_agence")
    achat_mobilier = st.number_input("Achat de mobilier (optionnel) (€)", value=0, key="achat_mobilier")
    travaux = st.number_input("Frais travaux (€)", value=0, key="travaux")
cout_total_acquisition = prix + frais_notaire + frais_agence + travaux + achat_mobilier
st.write(f"💰 Total d'acquisition : **{cout_total_acquisition:.0f} €**")

st.header("📊 EXPLOITATION - Revenus & coûts récurrents")
loyer = st.number_input("Loyer mensuel (vacances locative 0%) (€)", value=500, key="loyer")
charges_recuperable = st.number_input("Charges mensuelles récupérables (€)", value=0, key="charges_recuperable")
charges_copro = st.number_input("Charges annuelles de copro (€)", value=0, key="charges_copro")
taxe_fonciere = st.number_input("Taxe foncière annuelle (€)", value=500, key="taxe_fonciere")
assurance = st.number_input("Assurance PNO annuelle (€)", value=200, key="assurance")
with st.expander("⚙️ Paramètres avancés (optionnels)"):
    frais_gestion = st.number_input("Frais de gestion locative (€)", value=0, key="frais_gestion")
total_charge = taxe_fonciere/12 + charges_copro/12 + assurance/12 + charges_recuperable

st.header("🏦 FINANCEMENT")
frais_dossier = st.number_input("Frais de dossier", value=1000, key="frais_dossier")
apport_personnel_defaut = frais_notaire + frais_agence + frais_dossier + achat_mobilier
apport_personnel = st.number_input(
    "Apport personnel ",
    value=apport_personnel_defaut,
    key="apport personnel")
montant_pret = st.number_input("Montant du prêt", value=cout_total_acquisition-apport_personnel, key="montant_pret")
taux_interet = st.number_input("Taux d'intérêt", value=3.2, key="taux_interet")
duree_pret = st.number_input("Durée du prêt", value=20, key="duree_pret")
# simulation emprunt /!\ taux intéret mensualisé (linéaire)
mensualite_emprunt = npf.pmt(taux_interet/100/12, duree_pret * 12, -montant_pret)
st.write(f"Mensualité d'emprunt : **{mensualite_emprunt:.0f} €**")


prix_m2 = prix / surface
rentabilite_brute = (loyer * 12) / cout_total_acquisition * 100 if prix else 0
rentabilite_nette = ((loyer-total_charge) * 12) / cout_total_acquisition * 100 if prix else 0
cashflow_mensuel = loyer - total_charge - mensualite_emprunt
cashflow_annuel = cashflow_mensuel * 12
rendement_fond_propre = loyer / apport_personnel * 100

st.header("💸 Résultats")
st.write(f"Prix au m² : **{prix_m2:.0f} €**")
st.write(f"Rentabilité brute : **{rentabilite_brute:.0f} %**")
st.write(f"Rentabilité nette : **{rentabilite_nette:.0f} %**")
st.write(f"Cashflow mensuel : **{cashflow_mensuel:.0f} €**")
st.write(f"Cashflow annuel : **{cashflow_annuel:.0f} €**")
st.write(f"Rendement sur fonds propres : **{rendement_fond_propre:.0f} %**")

with st.expander("⚙️ Sauvegarde"):
    nom_projet = st.text_input("Nom du projet à sauvegarder")
    if st.button("💾 Sauvegarder ce projet"):
        data = {
            "prix": prix,
            "surface": surface,
            "frais_notaire": frais_notaire,
            "frais_agence": frais_agence,
            "achat_mobilier": achat_mobilier,
            "travaux": travaux,
            "loyer": loyer,
            "charges_recuperable": charges_recuperable,
            "charges_copro": charges_copro,
            "taxe_fonciere": taxe_fonciere,
            "assurance": assurance,
            "frais_gestion": frais_gestion,
            "frais_dossier": frais_dossier,
            "apport_personnel": apport_personnel,
            "montant_pret": montant_pret,
            "taux_interet": taux_interet,
            "duree_pret": duree_pret
        }
        save_project(nom_projet, data)
        st.success(f"Projet '{nom_projet}' sauvegardé ✅")


st.markdown("---")
st.markdown("💖 **Soutenir ce projet**")
st.markdown("""
Si cette application vous est utile, vous pouvez soutenir son développement ici :

👉 [☕ Offrir un café](https://buymeacoffee.com/qwetsch)
""")
