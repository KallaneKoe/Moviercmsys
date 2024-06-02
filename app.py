import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def rcm(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similary[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_poster = []
    for i in distances[1:21]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movie_dict = pickle.load(open('movie_list_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similary = pickle.load(open('similary.pkl', 'rb'))

st.title('Movie Recommender')

option = st.selectbox(
    'What movie you have been liked so far?',
    movies['title'].values
)
if st.button('Recommend for me!'):
    recommended_movie_names,recommended_movie_posters = rcm(option)
    cols = st.columns(5 , gap="medium")
    for i in range(0,5):
        with cols[i]:
            st.text(recommended_movie_names[i+0])
            st.image(recommended_movie_posters[i+0])
            st.text(recommended_movie_names[i + 5])
            st.image(recommended_movie_posters[i + 5])
            st.text(recommended_movie_names[i + 10])
            st.image(recommended_movie_posters[i + 10])
            st.text(recommended_movie_names[i+15])
            st.image(recommended_movie_posters[i+15])


