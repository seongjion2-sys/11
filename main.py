import streamlit as st
import base64
import io
from PIL import Image, ImageDraw

# 1. 페이지 설정
st.set_page_config(page_title="인간 키우기", layout="wide")

# 2. 세션 상태 관리 (레벨, 오버레이 활성화 여부 등)
if "level_stroke" not in st.session_state:
    st.session_state.level_stroke = 0
if "level_feed" not in st.session_state:
    st.session_state.level_feed = 0
if "level_walk" not in st.session_state:
    st.session_state.level_walk = 0
if "show_upgrade" not in st.session_state:
    st.session_state.show_upgrade = False

# 클릭 액션 처리 (쿼리 파라미터 링크 방식)
query_params = st.query_params
if "action" in query_params:
    action = query_params["action"]
    if action == "stroke":
        st.session_state.level_stroke += 1
    elif action == "feed":
        st.session_state.level_feed += 1
    elif action == "walk":
        st.session_state.level_walk += 1
    elif action == "toggle_upgrade":
        st.session_state.show_upgrade = not st.session_state.show_upgrade
    elif action == "baby_click":
        # 이미지 위 아기를 클릭했을 때 실행할 이벤트 (예: 기쁨/레벨UP/사운드 등)
        st.session_state.level_stroke += 1
    st.query_params.clear()
    st.rerun()

# 3. 내장 그래픽 생성 (거실 배경 + 아기 캐릭터)
@st.cache_data
def generate_game_assets():
    bg = Image.new("RGB", (900, 550), color="#f5ede0")
    draw = ImageDraw.Draw(bg)
    draw.rectangle([300, 80, 600, 320], fill="#e0f2fe", outline="#ffffff", width=6)
    draw.line([450, 80, 450, 320], fill="#ffffff", width=4)
    draw.rounded_rectangle([50, 240, 280, 440], radius=15, fill="#d6c5b0")
    draw.rectangle([650, 120, 880, 280], fill="#1e293b", outline="#334155", width=4)
    draw.rectangle([340, 350, 560, 430], fill="#475569")
    
    baby = Image.new("RGBA", (140, 140), (255, 255, 255, 0))
    b_draw = ImageDraw.Draw(baby)
    b_draw.ellipse([30, 10, 110, 90], fill="#fde047")
    b_draw.ellipse([40, 70, 100, 130], fill="#f472b6")
    b_draw.ellipse([50, 40, 60, 50], fill="#1e293b")
