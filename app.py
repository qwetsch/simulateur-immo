import streamlit as st
import numpy_financial as npf

st.set_page_config(page_title="Simulateur Immo", page_icon="🏠")

st.title("🏠 Simulateur Immobilier")

st.header("🔢 ACQUISITION")
prix = st.number_input("Prix d'achat (hors frais d'agence) (€)", value=100000)
surface = st.number_input("Surface (m²)", min_value=8, value=8)
frais_notaire_defaut = 0.09 * prix
frais_notaire = st.number_input(
    "Frais de notaire - automatique si ancien (€)",
    value=frais_notaire_defaut,
    key="frais_notaire"
)
with st.expander("⚙️ Paramètres avancés (optionnels)"):
    frais_agence = st.number_input("Frais d'agence si non inclus dans prix d'achat (€)", value=0)
    achat_mobilier = st.number_input("Achat de mobilier (optionnel) (€)", value=0)
    travaux = st.number_input("Frais travaux (€)", value=0)
cout_total_acquisition = prix + frais_notaire + frais_agence + travaux + achat_mobilier
st.write(f"💰 Total d'acquisition : **{cout_total_acquisition:.0f} €**")

st.header("🔢 EXPLOITATION - Revenus & coûts récurrents")
loyer = st.number_input("Loyer mensuel (vacances locative 0%) (€)", value=500)
charges_recuperable = st.number_input("Charges mensuelles récupérables (€)", value=0)
charges_copro = st.number_input("Charges annuelles de copro (€)", value=0)
taxe_fonciere = st.number_input("Taxe foncière annuelle (€)", value=500)
assurance = st.number_input("Assurance PNO annuelle (€)", value=200)
with st.expander("⚙️ Paramètres avancés (optionnels)"):
    frais_gestion = st.number_input("Frais de gestion locative (€)", value=0)
total_charge = taxe_fonciere/12 + charges_copro/12 + assurance/12 + charges_recuperable

st.header("🔢 FINANCEMENT")
frais_dossier = st.number_input("Frais de dossier ", value=1000)
apport_personnel_defaut = frais_notaire + frais_agence + frais_dossier + achat_mobilier
apport_personnel = st.number_input(
    "Apport personnel ",
    value=apport_personnel_defaut,
    key="apport personnel")
montant_pret = st.number_input("Montant du prêt", value = cout_total_acquisition-apport_personnel)
taux_interet = st.number_input("Taux d'intérêt", value=3.2)
duree_pret = st.number_input("Durée du prêt", value=20)
# simulation emprunt /!\ taux intéret mensualisé (linéaire)
mensualite_emprunt = npf.pmt(taux_interet/100/12, duree_pret * 12, -montant_pret)
st.write(f"💰 Mensualité d'emprunt : **{mensualite_emprunt:.0f} €**")


prix_m2 = prix / surface
rentabilite_brute = (loyer * 12) / cout_total_acquisition * 100 if prix else 0
rentabilite_nette = ((loyer-total_charge) * 12) / cout_total_acquisition * 100 if prix else 0
cashflow_mensuel = loyer - total_charge - mensualite_emprunt
cashflow_annuel = cashflow_mensuel * 12
rendement_fond_propre = loyer / apport_personnel * 100

st.header("📊 Résultats")
st.write(f"💰 Prix au m² : **{prix_m2:.0f} €**")
st.write(f"📈 Rentabilité brute : **{rentabilite_brute:.0f} %**")
st.write(f"📈 Rentabilité nette : **{rentabilite_nette:.0f} %**")
st.write(f"💰 Cashflow mensuel : **{cashflow_mensuel:.0f} €**")
st.write(f"💰 Cashflow annuel : **{cashflow_annuel:.0f} €**")
st.write(f"💰 Rendement sur fonds propres : **{rendement_fond_propre:.0f} %**")

