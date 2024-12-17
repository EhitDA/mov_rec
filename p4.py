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


df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)


option = st.selectbox(
    'Which number do you like best?',
    [1, 2, 3, 4, 5]
)

'You selected: ', option




st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")
