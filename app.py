import streamlit as st
import pickle
import pandas as pd
from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("api_key")

st.markdown(
    """
    <style>
    /* Remove top padding/margin from the main container */
    .block-container {
        padding-top: .5rem;
        padding-bottom: .5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <style>
    .movie-title {
        font-size:20px !important;
        font-weight:bold !important;
        text-align:center !important;
        height: 50px !important;
        line-height: 1.2em !important;
        overflow: hidden !important;
        white-space: normal !important; /* allow wrapping */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    img {
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)



def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    # url = "https://api.themoviedb.org/3/movie/{}?api_key=de09735b36540574b0d863c2a3c4d454&language=en-US".format(movie_id)
    data = requests.get(url, timeout=10).json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:11]

    recommended_movies =[]
    posters = []
    for i in movie_list:
        movie_id =  movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies, posters

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(layout="wide")
st.title('Movie Recommender✨')
selected_movie = st.selectbox("Search for similar movies like", movies['title'])

if st.button('Recommend') or selected_movie:
    st.header("Recommendations")
    names, posters = recommend(selected_movie)

    for row_start in range(0, 10, 5):
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            movie_idx = row_start + idx
            if movie_idx < len(names):
                with col:
                    st.markdown(
                        f"<p class='movie-title'>{names[movie_idx]}</p>",
                        unsafe_allow_html=True
                    )
                    st.image(posters[movie_idx])
