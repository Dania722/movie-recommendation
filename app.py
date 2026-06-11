import os
import pickle
import requests
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

# Introduction
st.title("Film Recommendation System")
st.write("Welcome to the Film Recommendation System!")
st.write(
    "Unlock Your Next Cinematic Adventure with Our Movie Recommendation System – Tailored Suggestions for Every Film Enthusiast!"
)

# Configuration
FILE_ID = "1StVVF1vP6s4XizTl4A78S2eIVvzVOaAC"
PICKLE_FILE = "movie_Similarity.pkl"


# --- GOOGLE DRIVE DOWNLOAD FUNCTION ---
@st.cache_resource
def load_large_similarity_matrix(file_id, destination):
    # Agar file exist nahi karti ya size 0 hai (corrupted), to naye siray se download karein
    if not os.path.exists(destination) or os.path.getsize(destination) == 0:
        with st.spinner(
            "Downloading movie matrix from Google Drive (this takes a moment)..."
        ):
            URL = "https://google.com"
            session = requests.Session()
            response = session.get(
                URL, params={"id": file_id}, stream=True
            )

            # Large file authorization token extraction
            token = None
            for key, value in response.cookies.items():
                if key.startswith("download_warning"):
                    token = value
                    break

            if token:
                response = session.get(
                    URL,
                    params={"id": file_id, "confirm": token},
                    stream=True,
                )

            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)

    # Load file only after download is fully completed
    with open(destination, "rb") as f:
        return pickle.load(f)


# --- LOAD DATA MODELS ---
movies = pickle.load(open("movie_recommender.pkl", "rb"))
# Istemal karein secure downloader function
similarity = load_large_similarity_matrix(FILE_ID, PICKLE_FILE)


# Fetch poster function
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        if "poster_path" in data and data["poster_path"] is not None:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    except Exception:
        pass
    return "https://placeholder.com"


# Recommendation logic
def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


# UI Selection
selected_movie = st.selectbox(
    "Select a movie or search for one",
    movies["title"].values,
    help="Start typing to search or select from the list.",
)

if st.button("Display The Recommendations"):
    recommended_movie_names, recommended_movie_posters = recommend(
        selected_movie
    )

    # First row of 5 movies
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

    # Second row of 5 movies
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
