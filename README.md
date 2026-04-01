# 📊 Prédiction de la pauvreté – ECVM RDC 2024
## 🌐 Application en ligne

👉 Accéder à l’application :  https://predictionpauvreterdc.streamlit.app/

## Lien vers les résultas
Toutes les analyses et les étapes détaillées sont disponibles dans le notebook suivant :  
👉 https://github.com/Patricia-Koto/memoire/blob/main/notebooks/notebook_prediction_pauvrete_ecvm.ipynb

## 🎯 Objectif du projet

Ce projet vise à prédire la pauvreté des ménages à partir des données ECVM RDC 2024.

La variable `nivie` représentant le niveau de vie étant catégorielle, elle est recodée en variable binaire :

- 1 = Pauvre  
- 0 = Non Pauvre  

Le problème est donc traité comme un problème de **classification**.

L’objectif est de comparer :
- un **modèle statistique classique** (régression logistique / GLM)
- des **modèles de machine learning** (Random Forest, Gradient Boosting)

afin d’évaluer leur capacité à prédire la pauvreté.

Le modèle le plus performant est ensuite intégré dans une **application Streamlit** permettant une prédiction en temps réel.

---

## 📁 Structure du projet

```
memoire/
│
├── data/
├── notebooks/
├── outputs/
├── app/
├── requirements_pauvrete.txt
├── README.md
└── .gitignore
```

---

### 📂 data/
Contient les données du projet :
- fichiers `.dta` (bases ECVM)
- fichiers `.xlsx` (dictionnaires)

👉 Source principale des données.

---

### 📂 notebooks/
Contient les notebooks Jupyter :

- préparation des données  
- fusion des bases  
- construction des variables  
- analyses statistiques  
- modélisation  

👉 Cœur analytique du projet.

---

### 📂 outputs/
Contient les résultats :

- `tables/` → résultats statistiques  
- `figures/` → graphiques  
- `models/` → modèles sauvegardés (`.pkl`)  

👉 Permet de séparer résultats et code.

---

### 📂 app/
Contient l’application **Streamlit** :

- interface utilisateur
- chargement du modèle sauvegardé
- prédiction de la pauvreté

👉 Permet une utilisation opérationnelle du modèle.

---

### 📄 requirements_pauvrete.txt
Liste des dépendances du projet.

---

## ⚙️ Installation

### 1. Se placer dans le dossier

```
cd C:\Users\LENOVO\Desktop\memoire
```

---

### 2. Créer un environnement

```
python -m venv pauvrete_env
```

---

### 3. Activer l’environnement

#### PowerShell
```
.\pauvrete_env\Scripts\Activate.ps1
```

#### CMD
```
pauvrete_env\Scripts\activate.bat
```

---

### 4. Installer les dépendances

```
pip install -r requirements_pauvrete.txt
```

---

### 5. Installer Jupyter (obligatoire)

```
pip install ipykernel
python -m ipykernel install --user --name pauvrete_env --display-name "Python (pauvrete_env)"
```

👉 Permet d’utiliser l’environnement dans Jupyter.

---

## ▶️ Utilisation

### Notebook

1. Lancer Jupyter :
```
jupyter notebook
```

2. Ouvrir un notebook dans `notebooks/`

3. Sélectionner :
👉 **Python (pauvrete_env)**

---

### Application Streamlit

Lancer l’application :

```
streamlit run app/app.py
```

👉 L’application permet de :
- saisir les caractéristiques d’un ménage
- obtenir la probabilité d’être pauvre

---

## ⚙️ Méthodologie

### Données

- Base principale : `welfare`
- Fusion avec :
  - `menage`
  - `individu`

### Feature engineering

- Agrégation des données individuelles (niveau ménage)
- Construction de variables socio-économiques

### Pondération

```
poids_final = hhweight × hhsize
```

### Prétraitement

- Variables binaires → 0 / 1  
- Variables catégorielles → OneHotEncoding  
- Variables numériques → normalisation  

---

## 🤖 Modélisation

Modèles utilisés :

- Régression logistique (modèle classique)
- Random Forest Classifier
- Gradient Boosting Classifier

---

## 📈 Évaluation des modèles

Les modèles sont comparés avec :

- Accuracy  
- Precision  
- Recall  
- F1-score  
- ROC-AUC  

👉 Le meilleur modèle est sélectionné selon la ROC-AUC.

---

## 💾 Sauvegarde du modèle

Le meilleur modèle est :

- réentraîné sur toutes les données
- sauvegardé dans `outputs/models/` au format `.pkl`

---

## 🚀 Application (Streamlit)

Le modèle sauvegardé est utilisé dans une application interactive permettant :

- une prédiction en temps réel  
- une utilisation simple par un utilisateur non technique  

---

## ⚠️ Problèmes fréquents

### Activation PowerShell bloquée
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Module manquant
```
pip install nom_du_module
```

---

## 🔁 Reproductibilité

Le projet est reproductible grâce à :

- `requirements_pauvrete.txt`
- environnement virtuel
- notebook documenté
- sauvegarde du modèle

---

## 👩‍💻 Auteur

Projet réalisé par Patricia KOTO dans le cadre d’un mémoire de DU Dana Analytics.
