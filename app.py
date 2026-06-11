import os
import pickle
import requests
import streamlit as st
from PIL import Image

# 1. Set page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

# 2. Introduction
st.title("Film Recommendation System")
st.write("Welcome to the Film Recommendation System!")
st.write(
    "Unlock Your Next Cinematic Adventure with Our Movie Recommendation System – Tailored Suggestions for Every Film Enthusiast!"
)

# 3. File Configurations
FILE_ID = "1StVVF1vP6s4XizTl4A78S2eIVvzVOaAC"
PICKLE_FILE = "movie_Similarity.pkl"


# 4. Google Drive Se Barri File Download Karne Ka Function
@st.cache_resource
def load_large_similarity_matrix(file_id, destination):
    if not os.path.exists(destination) or os.path.getsize(destination) == 0:
        with st.spinner(
            "Downloading movie matrix from cloud storage (this takes a moment)..."
        ):
            URL = "https://google.com"
            session = requests.Session()
            response = session.get(
                URL, params={"id": file_id}, stream=True
            )

            # Google Drive ka virus-scan bypass token check karne ke liye loop
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

            # File ko binary mode mein save karna chunks mein
            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)

    # Jab download complete ho jaye tab load karna
    with open(destination, "rb") as f:
        return pickle.load(f)


# 5. Data Models Load Krein (Pehle big file download execute hogi)
movies = pickle.load(open("movie_recommender.pkl", "rb"))
similarity = load_large_similarity_matrix(FILE_ID, PICKLE_FILE)


# 6. Define the fetch_poster function
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id
    )
    try:
        data = requests.get(url).json()
        if "poster_path" in data and data["poster_path"] is not None:
            poster_path = data["poster_path"]
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://placeholder.com"
    except Exception:
        return "https://placeholder.com"


# 7. Define the recommend function
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


# 8. Movie selection UI
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
