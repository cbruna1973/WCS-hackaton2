import streamlit as st 
import pandas as pd
from PIL import Image # manipuler des images en Python et qui inclut le module Image
# pip install plotly
#import plotly.express as px # affichage graph plotly




# Config de la page.
st.set_page_config(
    page_title = "Hackaton 2",
    page_icon = ":movie_camera:",
    layout = "wide",
    )


# cacher les menus de streamlit
hide_streamlit_style = """
                <style> div[data-testid="stToolbar"] {visibility: hidden; height: 0%; position: fixed;}
                div[data-testid="stDecoration"] {visibility: hidden; height: 0%; position: fixed;}
                div[data-testid="stStatusWidget"] {visibility: hidden; height: 0%; position: fixed;}
                #MainMenu {visibility: hidden; height: 0%;}
                header {visibility: hidden; height: 0%;}
                footer {visibility: hidden; height: 0%;}
                </style> """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


image = Image.open('loreal-logo.png')
st.sidebar.image(image, use_column_width=True) #caption="Description de l'image"

# barre de navigation vertical
st.sidebar.title("Menu")

# liste des pages 
pages = ["Accueil", "My Skin Routine"]

#page = st.sidebar.radio("Aller vers la page :", pages)
page = st.sidebar.radio("", pages)


# Import fichier CSV
df_soins = pd.read_csv('df_soins.csv')


# Remplacement colonne 'categorie' au format int par le format str
df_soins['categorie'] = df_soins['categorie'].astype(str)

# -----------------------------------------------------------
# -----------------------------------------------------------
############################################
#### menu page Accueil 
############################################

if page == pages[0]:

    st.markdown(
    '<h1 id="section_accueil" style="color: #BD4BFF; text-align: center;">Bienvenue sur My Skin Routine</h1>',
    unsafe_allow_html=True) 

    st.markdown("---")

    st.subheader("Groupe Data Indirim : ")
    st.write("Le groupe est composé de Carole, Claudette,Jonathan, Louka, Vincent")

    # declaration 2 colonnes
    col1, col2 = st.columns(2)

    col1.subheader("Contexte")
    col1.write("Comment l'IA peut-elle améliorer la proposition de valeur dans le domaine de la beauté ?.\n" 
               )

    col1.subheader("Notre idée")
    col1.write("Nous avons mis au point une application afin de guider les personnes qui rencontrent des difficultés à comprendre les rituels de soin, les différents produits qui les composent, leur utilisation et leur fréquence.\n" 
               "Nous avons constaté qu'il n'existait ni page web ni application pour téléphone présentant un rituel de soin.\n"
               "Après selection de l'âge et du type de peau par l'utilisateur, il lui est ensuite proposé une liste de produits par étape du rituel (nettoyage du visage, sérum, soin de jour ou de nuit, soin des yeux, masque, gommage).")

    col2.subheader("Rituel Beauté")
    # col2, affiche l'image
    image = Image.open('rituel.jpg')
    col2.image(image, use_column_width=True)  # caption='rituel beauté',

    col1.subheader("Les outils & bibliothèques utilisés")

    col1.write(
        "- Webscraping - Octoparse \n" 
        "- Python \n" 
        "- Streamlit "
        )


# -----------------------------------------------------------
# -----------------------------------------------------------
############################################
#### menu My Skin Routine
############################################

elif page == pages[1] :

    st.markdown(
    '<h1 id="section_skin routine" style="color: #BD4BFF; text-align: center;">My Skin Routine</h1>',
    unsafe_allow_html=True)

    st.markdown("---")

    # declaration 2 colonnes
    col1, col2 = st.columns(2)


    # Menu déroulant pour la sélection de la tranche d'âge dans col1
    with col1:
        tranche_age_order = ['20-30 ans', '30-40 ans', '40-50 ans', '50-60 ans', '60 ans et plus']
        tranche_age = df_soins['age'].str.split(', ').explode().unique()

        # Filtrer les tranches d'âge dans l'ordre souhaité
        tranche_age = [tranche for tranche in tranche_age_order if tranche in tranche_age]

        choix_tranche_age = st.selectbox("Sélectionnez votre tranche d'âge", [None] + list(tranche_age))

        if choix_tranche_age:
            st.write("Vous avez sélectionné la tranche d'âge :", choix_tranche_age)

    # Menu déroulant pour la sélection du type de peau dans col1
    with col1:
        types_de_peau = df_soins['peau'].str.split(', ').explode().unique()
        choix_type_peau = st.selectbox("Sélectionnez le type de peau", [None] + list(types_de_peau))
        if choix_type_peau:
            st.write("Vous avez sélectionné le type de peau :", choix_type_peau)


    # Utiliser le choix d'âge et de type de peau dans les filtres
    selected_age = choix_tranche_age
    selected_skin_type = choix_type_peau

    # col2, affiche l'image
    image = Image.open('Les-types-de-peaux.png')
    col2.image(image, use_column_width=True)

###################################
##### My Morning Routine
###################################
    st.subheader("My Morning Routine")


    # Vérifier si les valeurs de sélection sont non nulles
    if selected_age is not None and selected_skin_type is not None:
        # Filtre en fonction de l'âge et du type de peau pour la routine du matin
        filtered_data_morning = df_soins[df_soins['age'].str.contains(selected_age, na=False) & df_soins['peau'].str.contains(selected_skin_type, na=False)]

        # Trie en fonction des catégories de 1 à 3 pour la routine du matin
        sorted_data_morning = filtered_data_morning[filtered_data_morning['categorie'].between('1', '3')].sort_values(by='categorie')

        if not sorted_data_morning.empty:
            # Utilisation de colonnes pour afficher les informations
            cols = st.columns(7)
            cols[0].subheader("Catégorie")
            cols[1].subheader("Image")
            cols[2].subheader("Nom")
            cols[3].subheader("Description")
            cols[4].subheader("Application")
            cols[5].subheader("Prix")
            cols[6].subheader("Lien")

            # Afficher les produits
            for index, row in sorted_data_morning.iterrows():
                cols = st.columns(7)
                cols[0].write(row['categorie_name'])
                cols[1].image(row['image'], use_column_width=True)
                cols[2].write(row['nom'])
                cols[3].write(row['description'])
                cols[4].write(row['application'])
                cols[5].write(row['prix'])
                cols[6].markdown(f"[Cliquer ici]({row['lien']})")
        else:
            st.write("Aucun produit trouvé pour les critères sélectionnés.")
    else:
        st.write("Les valeurs de sélection ne doivent pas être None.")

    # Ligne de séparation
    st.write("---")


###################################
##### My Evening Routine
###################################

    st.subheader("My Evening Routine")


    # Vérifier si les valeurs de sélection sont non nulles
    if selected_age is not None and selected_skin_type is not None:
        # Filtre en fonction de l'âge et du type de peau pour la routine du soir
        filtered_data_evening = df_soins[df_soins['age'].str.contains(selected_age, na=False) & df_soins['peau'].str.contains(selected_skin_type, na=False)]

        # Trie en fonction des catégories 1, 2 et 4 pour la routine du soir
        sorted_data_evening = filtered_data_evening[filtered_data_evening['categorie'].isin(['1', '2', '4'])].sort_values(by='categorie')

        # Informations à afficher pour la routine du soir
        if not sorted_data_evening.empty:
            # Utilisation de colonnes pour afficher les informations
            cols = st.columns(7)
            cols[0].subheader("Catégorie")
            cols[1].subheader("Image")
            cols[2].subheader("Nom")
            cols[3].subheader("Description")
            cols[4].subheader("Application")
            cols[5].subheader("Prix")
            cols[6].subheader("Lien")

            # Afficher les produits
            for index, row in sorted_data_evening.iterrows():
                cols = st.columns(7)
                cols[0].write(row['categorie_name'])
                cols[1].image(row['image'], use_column_width=True)
                cols[2].write(row['nom'])
                cols[3].write(row['description'])
                cols[4].write(row['application'])
                cols[5].write(row['prix'])
                cols[6].markdown(f"[Cliquer ici]({row['lien']})")
        else:
            st.write("Aucun produit trouvé pour les critères sélectionnés.")
    else:
        st.write("Les valeurs de sélection ne doivent pas être None.")

    # Ligne de séparation
    st.write("---")




###################################
##### More
###################################
    st.subheader("More")


    # Vérifier si les valeurs de sélection sont non nulles
    if selected_age is not None and selected_skin_type is not None:
        # Filtre en fonction de l'âge et du type de peau pour la section 'More'
        filtered_data_more = df_soins[df_soins['age'].str.contains(selected_age, na=False) & df_soins['peau'].str.contains(selected_skin_type, na=False)]

        # Trie en fonction des catégories 5 à 7 pour la section 'More'
        sorted_data_more = filtered_data_more[filtered_data_more['categorie'].between('5', '7')].sort_values(by='categorie')

        if not sorted_data_more.empty:
            # Utilisation de colonnes pour afficher les informations
            cols = st.columns(7)
            cols[0].subheader("Catégorie")
            cols[1].subheader("Image")
            cols[2].subheader("Nom")
            cols[3].subheader("Description")
            cols[4].subheader("Application")
            cols[5].subheader("Prix")
            cols[6].subheader("Lien")

            # Afficher les produits
            for index, row in sorted_data_more.iterrows():
                cols = st.columns(7)
                cols[0].write(row['categorie_name'])
                cols[1].image(row['image'], use_column_width=True)
                cols[2].write(row['nom'])
                cols[3].write(row['description'])
                cols[4].write(row['application'])
                cols[5].write(row['prix'])
                cols[6].markdown(f"[Cliquer ici]({row['lien']})")
        else:
            st.write("Aucun produit trouvé pour les critères sélectionnés.")
    else:
        st.write("Les valeurs de sélection ne doivent pas être None.")






    # Ligne de séparation
    st.write("---")




