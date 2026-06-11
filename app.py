
import pickle
import streamlit as st
import requests
from PIL import Image
import urllib.request
import os

# Set page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)




# Introduction
st.title('Film Recommendation System')
st.write("Welcome to the Film Recommendation System!")
st.write("Unlock Your Next Cinematic Adventure with Our Movie Recommendation System – Tailored Suggestions for Every Film Enthusiast!")


# Put your long Google Drive sharing file ID between the quotes below:
FILE_ID = "1StVVF1vP6s4XizTl4A78S2eIVvzVOaAC"
PICKLE_FILE = "movie_Similarity.pkl"
URL = f"https://google.com{FILE_ID}"



# Load data
movies = pickle.load(open('movie_recommender.pkl', 'rb'))
similarity = pickle.load(open(PICKLE_FILE, 'rb'))

# Define the fetch_poster function
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()

    # Check if the poster_path is available in the data
    if 'poster_path' in data and data['poster_path'] is not None:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        # Return a placeholder image or handle the case where the poster_path is not available
        return "https://example.com/placeholder.jpg"


# Define the recommend function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Movie selection
selected_movie = st.selectbox(
    "Select a movie or search for one",
    movies['title'].values,
    help="Start typing to search or select from the list."
)

if st.button('Display The Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[0])
        st.caption(recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1])
        st.caption(recommended_movie_names[1])
    with col3:
        st.image(recommended_movie_posters[2])
        st.caption(recommended_movie_names[2])
    with col4:
        st.image(recommended_movie_posters[3])
        st.caption(recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4])
        st.caption(recommended_movie_names[4])

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[5])
        st.caption(recommended_movie_names[5])
    with col2:
        st.image(recommended_movie_posters[6])
        st.caption(recommended_movie_names[6])
    with col3:
        st.image(recommended_movie_posters[7])
        st.caption(recommended_movie_names[7])
    with col4:
        st.image(recommended_movie_posters[8])
        st.caption(recommended_movie_names[8])
    with col5:
        st.image(recommended_movie_posters[9])
        st.caption(recommended_movie_names[9])

# Footer
st.markdown("---")
st.write("Made by Dania Ahmed")


