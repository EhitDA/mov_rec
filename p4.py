import streamlit as st
import pandas as pd

@st.cache_data
def load_movs():
    movs = pd.read_csv("https://liangfgithub.github.io/MovieData/movies.dat?raw=true", sep="::", header=None, engine="python", encoding="ISO-8859-1")
    movs[0] = movs[0].apply(lambda x: "m" + str(x))
    movs.columns = ["Movie ID", "Title", "Genres"]
    return movs.set_index("Movie ID")

@st.cache_data
def load_S_mat():
    return pd.read_csv("S.csv")



movs = load_movs()

S_mat = load_S_mat()

st.header("Movie Recommender")



if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

mov_id = f"m{st.session_state.counter}"
mov_url = f"https://liangfgithub.github.io/MovieImages/{st.session_state.counter}.jpg"
mov_ttl = movs.loc[mov_id, "Title"]

st.image(mov_url, caption=mov_ttl, width=300)

rating = st.feedback("stars")

if rating is not None:
    st.write(f"You gave a rating of {rating + 1} star(s)!")


