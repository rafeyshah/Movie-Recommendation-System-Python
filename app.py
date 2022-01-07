from requests.exceptions import ReadTimeout
import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_posters(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=5c71e64f55616d4c12c4f19475b11c8c&language=en-US".format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    # Sorting list on the base of 2nd key not(enumerate), first 5 movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # Fetch Posters from API 5c71e64f55616d4c12c4f19475b11c8c
        recommended_movies_poster.append(fetch_posters(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies,recommended_movies_poster

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System');

movies_list = movies['title'].values
selected_movie_name = st.selectbox ('Please select your movie name', movies_list) 

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])