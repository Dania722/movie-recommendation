import os
import pickle
import requests
import gdown
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

# Introduction
st.title("🎬 Film Recommendation System")
st.write("Welcome to the Film Recommendation System!")
st.write(
    "Unlock Your Next Cinematic Adventure with Our Movie Recommendation System – Tailored Suggestions for Every Film Enthusiast!"
)

# Google Drive Configuration
FILE_ID = "1StVVF1vP6s4XizTl4A78S2eIVvzVOaAC"
PICKLE_FILE = "movie_Similarity.pkl"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Download Similarity Matrix
@st.cache_resource
def load_large_similarity_matrix(file_id, destination):
    if os.path.exists(destination) and os.path.getsize(destination) < 100_000_000:
        os.remove(destination)

    if not os.path.exists(destination):
        with st.spinner("Downloading similarity matrix from Google Drive... Please wait."):
            url = f"https://drive.google.com/uc?export=download&confirm=t&id={file_id}"
            try:
                gdown.download(url, destination, quiet=False)
            except Exception as e:
                st.error(f"Download failed: {e}")
                st.stop()

    with open(destination, "rb") as f:
        return pickle.load(f)


# Load Models Safely
try:
    movies = pickle.load(open(os.path.join(BASE_DIR, "movie_recommender.pkl"), "rb"))
    similarity = load_large_similarity_matrix(FILE_ID, PICKLE_FILE)
except (pickle.UnpicklingError, EOFError, ValueError) as e:
    if os.path.exists(PICKLE_FILE):
        os.remove(PICKLE_FILE)

    st.error("⚠️ Google Drive Download Limit Exceeded! Google Drive ne temporary download block kar diya hai.")
    st.warning("👉 Iska hal yeh hai: Apne Google Drive par jayen, file par right-click karke uski ek 'Make a copy' banayein. Us nayi copy ko dubara share karke 'Anyone with link' karein aur uski FILE_ID yahan app.py mein badal dein.")
    st.info("App ko dubara chalane ke liye niche right corner mein 'Manage app' -> 'Reboot App' par click karein.")
    st.stop()


# Fetch Poster Function
def fetch_poster(movie_id):
    api_key = "8265bd1679663a7ea12ac168da84d2e8"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        data = requests.get(url).json()
        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    except Exception:
        pass
    return "https://via.placeholder.com/300x450?text=No+Poster"


# Recommendation Function
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1],
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters


# Movie Selection
selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values,
)

# Recommendation Button
if st.button("Display Recommendations"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])

    cols = st.columns(5)
    for i in range(5, 10):
        with cols[i - 5]:
            st.image(posters[i])
            st.caption(names[i])


# Footer
st.markdown("---")
st.write("Made by Dania Ahmed ❤️")
