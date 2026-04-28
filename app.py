import streamlit as st
import math

st.set_page_config(layout="centered")

# --- GAME CONSTANTS ---
WIDTH = 600
HEIGHT = 400
CAR_SPEED = 10
BALL_FRICTION = 0.98

# --- SESSION STATE INIT ---
if "car_x" not in st.session_state:
    st.session_state.car_x = WIDTH // 2
    st.session_state.car_y = HEIGHT - 50
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = 0
    st.session_state.ball_dy = 0
    st.session_state.score = 0

# --- CONTROLS ---
st.title("🚗⚽ Car Football (Streamlit Edition)")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Left"):
        st.session_state.car_x -= CAR_SPEED
with col2:
    if st.button("⬆️ Up"):
        st.session_state.car_y -= CAR_SPEED
with col3:
    if st.button("➡️ Right"):
        st.session_state.car_x += CAR_SPEED

if st.button("⬇️ Down"):
    st.session_state.car_y += CAR_SPEED

# --- BOUNDARIES ---
st.session_state.car_x = max(0, min(WIDTH, st.session_state.car_x))
st.session_state.car_y = max(0, min(HEIGHT, st.session_state.car_y))

# --- COLLISION (CAR -> BALL) ---
dx = st.session_state.ball_x - st.session_state.car_x
dy = st.session_state.ball_y - st.session_state.car_y
dist = math.sqrt(dx**2 + dy**2)

if dist < 40:
    angle = math.atan2(dy, dx)
    st.session_state.ball_dx = math.cos(angle) * 10
    st.session_state.ball_dy = math.sin(angle) * 10

# --- BALL PHYSICS ---
st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

st.session_state.ball_dx *= BALL_FRICTION
st.session_state.ball_dy *= BALL_FRICTION

# --- WALL BOUNCE ---
if st.session_state.ball_x <= 0 or st.session_state.ball_x >= WIDTH:
    st.session_state.ball_dx *= -1

if st.session_state.ball_y <= 0:
    st.session_state.score += 1
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = 0
    st.session_state.ball_dy = 0

if st.session_state.ball_y >= HEIGHT:
    st.session_state.ball_dy *= -1

# --- DRAW FIELD ---
field = f"""
<div style="
    position: relative;
    width: {WIDTH}px;
    height: {HEIGHT}px;
    background-color: green;
    border: 3px solid white;
">
    <!-- Goal -->
    <div style="
        position:absolute;
        top:0;
        left:{WIDTH//2 - 50}px;
        width:100px;
        height:10px;
        background:white;
    "></div>

    <!-- Car -->
    <div style="
        position:absolute;
        left:{st.session_state.car_x}px;
        top:{st.session_state.car_y}px;
        width:30px;
        height:20px;
        background:red;
    "></div>

    <!-- Ball -->
    <div style="
        position:absolute;
        left:{st.session_state.ball_x}px;
        top:{st.session_state.ball_y}px;
        width:20px;
        height:20px;
        border-radius:50%;
        background:white;
    "></div>
</div>
"""

st.markdown(field, unsafe_allow_html=True)

st.subheader(f"Score: {st.session_state.score}")
