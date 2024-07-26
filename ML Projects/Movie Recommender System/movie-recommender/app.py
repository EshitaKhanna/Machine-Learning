import streamlit as st
import pickle
import requests

movies = pickle.load(open('/Users/Eshita/Desktop/Stuff/Github.nosync/ML Projects/Movie Recommender System/movies.pkl', 'rb'))
movies_title = movies['title'].values

similarity = pickle.load(open('/Users/Eshita/Desktop/Stuff/Github.nosync/ML Projects/Movie Recommender System/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f9333f04fd670235d1a2d0dcef263fae'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters 

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('What would you like to see?', movies_title)

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

