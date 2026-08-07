import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

 


BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"

DEFAULT_POSTER = "https://via.placeholder.com/500x750?text=No+Image"


 
@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_id):

    try:

        url = f"{BASE_URL}/movie/{movie_id}"

        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "append_to_response": "videos"
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return None

        data = response.json()

 
        poster = DEFAULT_POSTER

        if data.get("poster_path"):
            poster = IMAGE_URL + data["poster_path"]

 
        rating = round(data.get("vote_average", 0), 1)

 
        release = data.get("release_date", "")

        year = release[:4] if release else "N/A"

 
        genres = [g["name"] for g in data.get("genres", [])]

        genres = ", ".join(genres[:2])

 
        overview = data.get("overview", "")

        if len(overview) > 60:
            overview = overview[:60] + "..."

 
        trailer = ""

        videos = data.get("videos", {}).get("results", [])

        for video in videos:

            if (
                video["site"] == "YouTube"
                and video["type"] == "Trailer"
            ):

                trailer = (
                    "https://www.youtube.com/watch?v="
                    + video["key"]
                )

                break

        return {

            "title": data.get("title", ""),

            "poster": poster,

            "rating": rating,

            "year": year,

            "genres": genres,

            "overview": overview,

            "runtime": data.get("runtime", ""),

            "trailer": trailer

        }

    except Exception:

        return {

            "title": "Unknown",

            "poster": DEFAULT_POSTER,

            "rating": 0,

            "year": "N/A",

            "genres": "",

            "overview": "",

            "runtime": "",

            "trailer": ""

        }




@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):

    movie = fetch_movie_details(movie_id)

    return movie["poster"]