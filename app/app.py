import streamlit as st
import pandas as pd
import joblib
import os
import glob
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="RDC - Expert Pauvreté", page_icon="🇨🇩", layout="wide")

# --- CHARGEMENT DU LOGO LOCAL ---
# Assurez-vous que l'image est dans le même dossier que ce script
logo_filename = "logo_rdc.png"

# --- FONCTION DE SÉLECTION AUTOMATIQUE DU MEILLEUR MODÈLE ---
@st.cache_resource
def load_best_pipeline():
    # Chemin vers votre dossier de modèles
    model_dir = r"C:\Users\LENOVO\Desktop\memoire\notebooks\outputs\models"

    # On cherche tous les fichiers .pkl dans ce dossier
    list_of_files = glob.glob(os.path.join(model_dir, "*.pkl"))

    if not list_of_files:
        return None, None

    # Sélection automatique du fichier le plus récent
    latest_file = max(list_of_files, key=os.path.getctime)

    try:
        bundle = joblib.load(latest_file)
        return bundle['model'], os.path.basename(latest_file)
    except Exception:
        return None, None

pipeline, model_name = load_best_pipeline()

# --- DESIGN EN-TÊTE ---
col_logo, col_texte = st.columns([1, 5])

with col_logo:
    if os.path.exists(logo_filename):
        img = Image.open(logo_filename)
        st.image(img, width=100)
    else:
        st.info("Logo local")

with col_texte:
    st.markdown(f"""
        <h2 style="margin: 0; color: #1d3557;">République Démocratique du Congo</h2>
        <p style="margin: 0; color: #457b9d; font-size: 1.1em;">
            Système Expert de Prédiction de la Pauvreté (ECVM 2024)
        </p>
        <p style="margin: 0; color: #7f8c8d; font-size: 0.8em;">Modèle actif : <b>{model_name if model_name else "Aucun"}</b></p>
    """, unsafe_allow_html=True)

if pipeline is None:
    st.error("❌ Aucun modèle (.pkl) trouvé dans le dossier spécifié.")
    st.stop()

# --- FORMULAIRE ---
with st.form("form_ecvm_final"):
    tab1, tab2, tab3 = st.tabs(["👤 Chef de Ménage", "🏠 Logement & Équipements", "📍 Localisation"])

    with tab1:
        c1, c2 = st.columns(2)
        hage = c1.number_input("Âge du chef", 15, 100, 40)
        hgender = c1.selectbox("Sexe", ["Masculin", "Féminin"])
        heduc = c2.selectbox("Niveau d'éducation", ["Aucun", "Primaire", "Secondaire", "Supérieur"])
        hmar = c2.selectbox("État matrimonial", ["Marié monogame", "Marié polygame", "Union libre", "Veuf", "Divorcé", "Célibataire"])
        hreligion = c1.selectbox("Religion", ["Catholique", "Protestant", "Kimbanguiste", "Musulman", "Eglise de réveil", "Autre", "Sans religion"])
        hactiv12m = c2.selectbox("Activité économique", ["Occupé", "Chômeur", "Inactif"])
        hcsp = c1.selectbox("CSP", ["Cadre", "Employé", "Ouvrier", "Indépendant", "Apprenti", "Autre"])
        hbranch = c2.selectbox("Branche d'activité", ["Agriculture", "Commerce", "Administration", "Services", "Industrie/Mines", "Autre"])

    with tab2:
        c3, c4 = st.columns(2)
        logem = c3.selectbox("Statut d'occupation", ["Propriétaire", "Locataire", "Logé gratuitement", "Autre"])
        typmen = c3.selectbox("Type de ménage", ["Nucléaire", "Élargi", "Monoparental", "Isolé"])
        elec_ac = c4.radio("Accès électricité", ["Oui", "Non"], horizontal=True)
        toilet = c4.radio("Toilettes saines", ["Oui", "Non"], horizontal=True)
        telpor = c4.radio("Possède téléphone", ["Oui", "Non"], horizontal=True)
        handig = c3.radio("Membre avec handicap", ["Oui", "Non"], horizontal=True)
        nb_membres_compte_bancaire = c4.number_input(
            "Nombre de membres avec compte bancaire",
            min_value=0,
            max_value=30,
            value=0,
            step=1
        )

    with tab3:
        c5, c6 = st.columns(2)
        province = c5.selectbox("Province", ["Kinshasa", "Bas-Uele", "Equateur", "Haut-Katanga", "Kasaï", "Lualaba", "Nord-Kivu", "Sud-Kivu", "Tshopo", "Autre"])
        milieu = c5.radio("Milieu de résidence", ["Urbain", "Rural"], horizontal=True)
        taille_menage = c6.number_input("Taille du ménage", 1, 30, 5)
        nb_dependants = c6.number_input(
            "Nombre de personnes à charge",
            min_value=0,
            max_value=30,
            value=0,
            step=1
        )

    submit = st.form_submit_button("📊 ANALYSER LE STATUT")

if submit:
    # --- Contrôles de cohérence ---
    if nb_membres_compte_bancaire > taille_menage:
        st.error("Le nombre de membres avec compte bancaire ne peut pas dépasser la taille du ménage.")
        st.stop()

    if nb_dependants > taille_menage:
        st.error("Le nombre de personnes à charge ne peut pas dépasser la taille du ménage.")
        st.stop()

    nb_actifs = taille_menage - nb_dependants

    if nb_actifs <= 0:
        ratio_dependance = 20.0
    else:
        ratio_dependance = nb_dependants / nb_actifs

    part_ayant_compte_bancaire = nb_membres_compte_bancaire / taille_menage

    # Optionnel, juste pour information
    st.info(
        f"Variables calculées automatiquement : "
        f"ratio de dépendance = {ratio_dependance:.2f} | "
        f"part membres avec compte bancaire = {part_ayant_compte_bancaire:.2f}"
    )

    # 1. Préparation des données
    data = {
        'hage': hage,
        'hgender': hgender,
        'heduc': heduc,
        'hmar': hmar,
        'hreligion': hreligion,
        'hactiv12m': hactiv12m,
        'hbranch': hbranch,
        'hcsp': hcsp,
        'province': province,
        'milieu': milieu,
        'taille_menage': taille_menage,
        'ratio_dependance': ratio_dependance,
        'typmen': typmen,
        'part_ayant_compte_bancaire': part_ayant_compte_bancaire,
        'toilet': toilet,
        'handig': handig,
        'elec_ac': elec_ac,
        'telpor': telpor,
        'logem': logem
    }

    input_df = pd.DataFrame([data])

    # 2. Normalisation des textes
    obj_cols = input_df.select_dtypes(include=['object']).columns
    for col in obj_cols:
        input_df[col] = (
            input_df[col]
            .astype(str)
            .str.lower()
            .str.normalize('NFKD')
            .str.encode('ascii', errors='ignore')
            .str.decode('utf-8')
        )

    try:
        prediction = pipeline.predict(input_df)[0]
        probabilite = pipeline.predict_proba(input_df)[0][1]

        st.markdown("---")
        if prediction == 1:
            st.error("### RÉSULTAT : MÉNAGE PAUVRE")
        else:
            st.success("### RÉSULTAT : MÉNAGE NON PAUVRE")

        st.metric("Probabilité de pauvreté", f"{probabilite:.1%}")
        st.progress(probabilite)

    except Exception as e:
        st.error(f"Erreur technique : {e}")