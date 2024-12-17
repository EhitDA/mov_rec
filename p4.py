import time
import streamlit as st
import numpy as np
import pandas as pd

@st.cache_data
def load_movs():
    movs = pd.read_csv("https://liangfgithub.github.io/MovieData/movies.dat?raw=true", sep="::", header=None, engine="python", encoding="ISO-8859-1")
    movs[0] = movs[0].apply(lambda x: "m" + str(x))
    movs.columns = ["Movie ID", "Title", "Genres"]
    return movs.set_index("Movie ID")

movs = load_movs()


@st.cache_data
def load_S_mat():
    return pd.read_csv("S.csv", index_col=0)

S_mat = load_S_mat()

@st.cache_data
def load_pop_movs():
    return list(pd.read_csv("pop.csv", index_col=0).iloc[:, 0])

pop_movs = load_pop_movs()

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1


if "w" not in st.session_state:
    st.session_state.w = pd.Series([np.nan] * 3706, index=S_mat.index)


if "mov_num" not in st.session_state:
    st.session_state.mov_num = 1


st.header("Movie Recommender")
st.subheader("Rate this movie!")

mov_id = f"m{st.session_state.mov_num}"
mov_url = f"https://liangfgithub.github.io/MovieImages/{st.session_state.mov_num}.jpg"
mov_ttl = movs.loc[mov_id, "Title"]
st.image(mov_url, caption=mov_ttl, width=150)


def rec_rating():
    time.sleep(1)

rating = st.feedback("stars", key=f"fb_{st.session_state.mov_num}", on_change=rec_rating)

if rating is not None:
    st.write(f"You rated it {rating + 1}")
    st.session_state.w[mov_id] = rating + 1
    st.session_state.mov_num += 1
    st.rerun()
else:
    st.write(f"Rating is None")


col1, col2, _, _, _, _, _ = st.columns(7)

def dec_mov_num():
    if st.session_state.mov_num != 1:
        st.session_state.mov_num -= 1

with col1:
    st.button("Previous", on_click=dec_mov_num)

def inc_mov_num():
    st.session_state.mov_num += 1

with col2:
    st.button("Next", on_click=inc_mov_num)


def reset_rat():
    st.session_state.w = pd.Series([np.nan] * 3706, index=S_mat.index)

st.button("Reset", on_click=reset_rat)

@st.cache_data
def myIBCF(newuser):
    newuser_not_na = (1 - np.isnan(newuser)).astype(float)
    rat_preds = ((S_mat.fillna(0) @ newuser.fillna(0)) / (S_mat.fillna(0) @ newuser_not_na))
    mov_preds = list(rat_preds.dropna().sort_values(ascending=False, kind="mergesort")[:10].index)
    idx = 0
    while (len(mov_preds) < 10):
        if pop_movs[idx] in mov_preds:
            idx += 1
        else:
            mov_preds.append(pop_movs[idx])
    return movs.loc[mov_preds, :]

rats = (~st.session_state.w.isna()).sum()

if rats == 0:
    st.write("You rated no movies yet.")
else:
    st.write(f"You have rated {rats} movies!")


st.write(myIBCF(st.session_state.w))



f"{st.session_state.counter} resets"

