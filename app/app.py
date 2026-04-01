import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="RDC - Expert Pauvreté", page_icon="🇨🇩", layout="wide")

# --- CHEMINS DE BASE ---
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

# --- CHEMIN DU LOGO ---
logo_path = APP_DIR / "logo_rdc.png"

# --- FONCTION DE CHARGEMENT DU MEILLEUR MODÈLE ---
@st.cache_resource
def load_best_pipeline():
    model_dir = PROJECT_ROOT / "notebooks" / "outputs" / "models"

    list_of_files = sorted(model_dir.glob("*.pkl"), key=lambda p: p.stat().st_mtime) if model_dir.exists() else []

    if not list_of_files:
        return None, None, model_dir

    latest_file = list_of_files[-1]

    try:
        bundle = joblib.load(latest_file)

        if isinstance(bundle, dict) and "model" in bundle:
            model = bundle["model"]
        else:
            model = bundle

        return model, latest_file.name, model_dir

    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle : {e}")
        return None, None, model_dir


pipeline, model_name, model_dir = load_best_pipeline()

# --- DESIGN EN-TÊTE ---
col_logo, col_texte = st.columns([1, 5])

with col_logo:
    if logo_path.exists():
        img = Image.open(logo_path)
        st.image(img, width=140)
    else:
        st.info("Logo introuvable")

with col_texte:
    st.markdown(
        f"""
        <h2 style="margin: 0; color: #1d3557;">République Démocratique du Congo</h2>
        <p style="margin: 0; color: #457b9d; font-size: 1.1em;">
            Système Expert de Prédiction de la Pauvreté (ECVM 2024)
        </p>
        <p style="margin: 0; color: #7f8c8d; font-size: 0.8em;">
            Modèle actif : <b>{model_name if model_name else "Aucun"}</b>
        </p>
        """,
        unsafe_allow_html=True
    )

if pipeline is None:
    st.error("❌ Aucun modèle (.pkl) trouvé dans le dossier spécifié.")
    st.write(f"Dossier recherché : {model_dir}")
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
        handig = c3.radio("Membre avec handicap", ["Oui", "Non"], horizontal=True)
        taille_menage = c3.number_input("Taille du ménage", 1, 30, 5)

        elec_ac = c4.radio("Accès électricité", ["Oui", "Non"], horizontal=True)
        toilet = c4.radio("Toilettes saines", ["Oui", "Non"], horizontal=True)
        telpor = c4.radio("Possède téléphone", ["Oui", "Non"], horizontal=True)
        nb_membres_compte_bancaire = c4.number_input(
            "Nombre de membres avec compte bancaire",
            min_value=0,
            max_value=30,
            value=0,
            step=1
        )
        nb_dependants = c4.number_input(
            "Nombre de personnes à charge (membres de moins de 15 ans + membres de 65 ans et plus)",
            min_value=0,
            max_value=30,
            value=0,
            step=1
        )

    with tab3:
        c5, c6 = st.columns(2)
        province = c5.selectbox("Province", ["Kinshasa", "Bas-Uele", "Equateur", "Haut-Katanga", "Kasaï", "Lualaba", "Nord-Kivu", "Sud-Kivu", "Tshopo", "Autre"])
        milieu = c6.radio("Milieu de résidence", ["Urbain", "Rural"], horizontal=True)

    submit = st.form_submit_button("📊 ANALYSER LE STATUT")

if submit:
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

    st.info(
        f"Variables calculées automatiquement : "
        f"ratio de dépendance = {ratio_dependance:.2f} | "
        f"part membres avec compte bancaire = {part_ayant_compte_bancaire:.2f}"
    )

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

        probabilite = None
        if hasattr(pipeline, "predict_proba"):
            probabilite = pipeline.predict_proba(input_df)[0][1]

        st.markdown("---")
        if prediction == 1:
            st.error("### RÉSULTAT : MÉNAGE PAUVRE")
        else:
            st.success("### RÉSULTAT : MÉNAGE NON PAUVRE")

        if probabilite is not None:
            st.metric("Probabilité de pauvreté", f"{probabilite:.1%}")
            st.progress(float(probabilite))

    except Exception as e:
        st.error(f"Erreur technique : {e}")