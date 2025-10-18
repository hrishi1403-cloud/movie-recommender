import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('api_key')

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
        data = response.json()
        
        # Check if API returned an error
        if data.get('success') == False:
            return "placeholder.png"  # Local file
        
        img_base_url = "https://image.tmdb.org/t/p/w500"
        poster_path = data.get('poster_path')
        
        if poster_path:
            return img_base_url + poster_path
        else:
            return "placeholder.png"  # Local file
    except:
        return "placeholder.png"  # Local file


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[movie_id].title)

    return recommended_movies, recommended_movies_poster


movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))

movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System')


select_movie_name  = st.selectbox(

    'Select a Movie' , movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(select_movie_name)
    
    # Display in 5 columns (like Netflix style)
    cols = st.columns(5)
    
    for idx, (name, poster_url) in enumerate(zip(names, posters)):
        with cols[idx]:
            st.image(poster_url, width="stretch")
            st.write(name)



