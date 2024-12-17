import time
import streamlit as st
import numpy as np
import pandas as pd

# Load movie data
@st.cache_data
def load_movs():
    movs = pd.read_csv("https://liangfgithub.github.io/MovieData/movies.dat?raw=true", sep="::", header=None, engine="python", encoding="ISO-8859-1")
    movs[0] = movs[0].apply(lambda x: "m" + str(x))
    movs.columns = ["Movie ID", "Title", "Genres"]
    return movs.set_index("Movie ID")
movs = load_movs()

# Load similarity matrix
@st.cache_data
def load_S_mat():
    return pd.read_csv("S.csv", index_col=0)
S_mat = load_S_mat()

# Load popular movies
@st.cache_data
def load_pop_movs():
    return list(pd.read_csv("pop.csv", index_col=0).iloc[:, 0])
pop_movs = load_pop_movs()

# List of ratings provided by user
if "w" not in st.session_state:
    st.session_state.w = pd.Series([np.nan] * 3706, index=S_mat.index)

# Movie number of current movie
if "mov_num" not in st.session_state:
    st.session_state.mov_num = 1

# Information of current movie
mov_id = f"m{st.session_state.mov_num}"
mov_url = f"https://liangfgithub.github.io/MovieImages/{st.session_state.mov_num}.jpg"
mov_ttl = movs.loc[mov_id, "Title"]

# Display UI
st.header("Movie Recommender System")
st.subheader("Rate this movie!")

col1, col2 = st.columns(2)

with col1:
    st.image(mov_url, caption=mov_ttl, width=150)

def rec_rating():
    time.sleep(1)

def dec_mov_num():
    if st.session_state.mov_num != 1:
        st.session_state.mov_num -= 1
    time.sleep(1)

def inc_mov_num():
    st.session_state.mov_num += 1
    time.sleep(1)

def reset_rat():
    st.session_state.w = pd.Series([np.nan] * 3706, index=S_mat.index)
    time.sleep(1)

with col2:
    rating = st.feedback("stars", key=f"fb_{st.session_state.mov_num}", on_change=rec_rating)
    st.button("Previous", on_click=dec_mov_num)
    st.button("Next", on_click=inc_mov_num)
    rats = (~st.session_state.w.isna()).sum()
    match rats:
        case 0:
            st.write("You have rated 0 movies.")
        case 1:
            st.write(f"You have rated 1 movie!")
        case _:
            st.write(f"You have rated {rats} movies!")
    st.button("Reset", on_click=reset_rat)

# Update ratings list
if rating is not None:
    st.session_state.w[mov_id] = rating + 1
    st.session_state.mov_num += 1
    st.rerun()

# Compute recommendations
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

recs = myIBCF(st.session_state.w)

# Display recommendations
st.subheader("Recommendations")

@st.cache_data
def show_recs(recs):
    for i in range(2):
        cols = st.columns(5)
        j = 0
        for index, row in recs.iloc[(5 * i):(5 * i + 5), :].iterrows():
            with cols[j]:
                mov_url = f"https://liangfgithub.github.io/MovieImages/{index[1:]}.jpg"
                mov_ttl = movs.loc[index, "Title"]
                st.image(mov_url, caption=mov_ttl, width=100)
                j += 1
show_recs(recs)