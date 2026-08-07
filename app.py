import streamlit as st
import pickle

from poster import fetch_movie_details

 

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

 

def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

 

@st.cache_resource
def load_data():

    movies = pickle.load(open("movies.pkl", "rb"))

    similarity = pickle.load(open("similarity.pkl", "rb"))

    return movies, similarity


movies, similarity = load_data()
 

@st.cache_data(show_spinner=False)
def recommend(movie_name):

    movie_index = movies[movies["title"] == movie_name].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommendations = []

    for movie in movie_list:

        index = movie[0]

        score = round(movie[1] * 100)

        movie_id = movies.iloc[index].movie_id

        details = fetch_movie_details(movie_id)

        if details:

            details["match"] = score

            recommendations.append(details)

    return recommendations

 

with st.sidebar:

    st.title("🎬 Movie Recommender")

    st.markdown("---")

    st.subheader("🛠 Tech Stack")

    st.markdown("""
- Python
- Pandas
- NLP
- CountVectorizer
- Cosine Similarity
- Streamlit
- TMDB API
""")

    st.markdown("---")

    st.subheader("📈 Features")

    st.markdown("""
✅ Smart Recommendation

✅ Movie Posters

✅ Ratings

✅ Genres

✅ Release Year

✅ Trailer

✅ Overview
""")

    st.markdown("---")

    st.success("Data Science and Machine Learning MRS")

 

st.markdown("""
<div class="fade">

<h1 class="hero-title">
🎬 <span>Movie Recommendation</span> System
</h1>

<p class="hero-subtitle">
Discover amazing movies similar to your favourites.
</p>

</div>
""", unsafe_allow_html=True)
 

st.markdown('<div class="glass">', unsafe_allow_html=True)

selected_movie = st.selectbox(
    "🔍 Search Movie",
    movies["title"].values,
    index=0
)

recommend_btn = st.button(
    "🎥 Get Recommendations",
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)

st.write("")

 

if recommend_btn:

    with st.spinner("Finding Similar Movies..."):

        recommendations = recommend(selected_movie)

        cols = st.columns(5)

        for i, movie in enumerate(recommendations):

            with cols[i]:

                st.markdown('<div class="movie-card fade">', unsafe_allow_html=True)

                
                st.image(
                    movie["poster"],
                    use_container_width=True
                )

                
                st.markdown(
                    f"""
                    <div class="movie-title">
                    {movie["title"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                 
                st.markdown(
                    f"""
                    <div class="movie-rating">
                    ⭐ {movie["rating"]}/10
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                 
                st.markdown(
                    f"""
                    <div class="movie-year">
                    📅 {movie["year"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                
                st.markdown(
                    f"""
                    <div class="movie-genre">
                    🎭 {movie["genres"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                
                
                
                st.markdown(
                    f"""
                    <p style='text-align:center;color:#bdbdbd;font-size:14px;'>
                    ⏱️ {movie["runtime"]} min
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                 
                st.markdown(
                    f"""
                    <div class="movie-overview">
                    {movie["overview"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")

                 
                if movie["trailer"] != "":

                    st.link_button(
                        "▶ Watch Trailer",
                        movie["trailer"],
                        use_container_width=True
                    )

                else:

                    st.button(
                        "Trailer Not Available",
                        disabled=True,
                        use_container_width=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)

 

st.write("")
st.write("")
st.markdown("---")

st.markdown(
    """
    <div class="footer">

    <h3 style="color:white;">
    🎬 Movie Recommendation System
    </h3>

    <p>
    Using
    <b>Python</b> |
    <b>Streamlit</b> |
    <b>NLP</b> |
    <b>Cosine Similarity</b> |
    <b>TMDB API</b>
    </p>

    <p style="color:gray;">
    Mohiuddin MRS
    </p>

    </div>
    """,
    unsafe_allow_html=True
)