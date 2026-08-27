import streamlit as st
import base64
import urllib.request

# 1. 페이지 설정 및 레이아웃 정의
st.set_page_config(page_title="인간 키우기", layout="wide", initial_sidebar_state="collapsed")

# 2. 세션 상태 초기화
if "level_stroke" not in st.session_state:
    st.session_state.level_stroke = 0
if "level_feed" not in st.session_state:
    st.session_state.level_feed = 0
if "level_walk" not in st.session_state:
    st.session_state.level_walk = 0
if "show_upgrade" not in st.session_state:
    st.session_state.show_upgrade = False

# 쿼리 파라미터를 통한 레벨업 동작 처리 (HTML 버튼 클릭 대응)
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
    elif action == "close_upgrade":
        st.session_state.show_upgrade = False
    st.query_params.clear()
    st.rerun()

# 3. 기본 제공 원본 이미지 (URL을 Base64로 자동 변환)
@st.cache_data
def get_image_base64(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return base64.b64encode(response.read()).decode('utf-8')

try:
    bg_b64 = get_image_base64("https://i.ibb.co/L9Hvh3R/bg.jpg") # 거실 배경
    baby_b64 = get_image_base64("https://i.ibb.co/1fW5g32/baby.png") # 아기
except:
    bg_b64, baby_b64 = "", ""

# 블러 효과 및 UI 상태 적용
blur_style = "filter: blur(5px) brightness(0.8);" if st.session_state.show_upgrade else ""
modal_display = "flex" if st.session_state.show_upgrade else "none"

# 4. 방치형 게임 게임풍 HTML/CSS 렌더링
html_code = f"""
<style>
    .stApp {{
        background-color: #121212;
        color: #000;
        font-family: 'Pretendard', sans-serif;
    }}
    .game-container {{
        position: relative;
        width: 100%;
        max-width: 900px;
        height: 600px;
        margin: 0 auto;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .game-bg {{
        width: 100%;
        height: 100%;
        background-image: url('data:image/jpeg;base64,{bg_b64}');
        background-size: cover;
        background-position: center;
        transition: filter 0.3s ease;
        {blur_style}
    }}
    .baby-char {{
        position: absolute;
        bottom: 110px;
        left: 50%;
        transform: translateX(-50%);
        width: 140px;
        z-index: 2;
    }}
    .bottom-bar {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(245, 245, 247, 0.92);
        backdrop-filter: blur(10px);
        padding: 10px 15px;
        box-sizing: border-box;
        z-index: 10;
        border-top: 1px solid rgba(0,0,0,0.1);
    }}
    .status-pill {{
        background: #232323;
        color: #fff;
        padding: 4px 16px;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 600;
        width: fit-content;
        margin: 0 auto 8px auto;
        display: flex;
        gap: 20px;
    }}
    .nav-slots {{
        display: flex;
        justify-content: space-around;
        gap: 8px;
    }}
    .nav-btn {{
        flex: 1;
        background: #fff;
        border: 1px solid #d0d0d0;
        border-radius: 10px;
        padding: 8px 0;
        text-align: center;
        font-size: 13px;
        font-weight: bold;
        color: #333;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .nav-btn.active {{
        border: 2px solid #e2b047;
        background: #fffdf5;
    }}
    
    /* 모달 UI */
    .upgrade-modal {{
        position: absolute;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 380px;
        background: linear-gradient(135deg, #fbf7ee 0%, #f1e4cb 100%);
        border: 3px solid #ffd700;
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        z-index: 20;
        display: {modal_display};
        flex-direction: column;
        gap: 10px;
    }}
    .modal-header {{
        font-weight: bold;
        font-size: 15px;
        color: #444;
    }}
    .slot-card {{
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid #e6d3ad;
        border-radius: 12px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .slot-info {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .slot-title {{
        font-weight: bold;
        font-size: 15px;
    }}
    .slot-level {{
        font-size: 13px;
        color: #d97706;
        font-weight: bold;
    }}
    .lvl-btn {{
        background: linear-gradient(to bottom, #ffe885, #f5bd38);
        border: 1px solid #d49b13;
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 13px;
        font-weight: bold;
        color: #333;
        text-decoration: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
</style>

<div class="game-container">
    <div class="game-bg"></div>
    <img src="data:image/png;base64,{baby_b64}" class="baby-char" />
    
    <!-- 업그레이드 슬롯 창 -->
    <div class="upgrade-modal">
        <div class="modal-header">나이: 1세</div>
        
        <div class="slot-card">
            <div class="slot-info">
                <span style="font-size:24px;">🖐️</span>
                <div>
                    <div class="slot-title">쓰다듬기</div>
                    <div class="slot-level">레벨: {st.session_state.level_stroke}</div>
                </div>
            </div>
            <a href="?action=stroke" target="_self" class="lvl-btn">레벨업 ✚</a>
        </div>

        <div class="slot-card">
            <div class="slot-info">
                <span style="font-size:24px;">🍼</span>
                <div>
                    <div class="slot-title">밥 먹이기</div>
                    <div class="slot-level">레벨: {st.session_state.level_feed}</div>
                </div>
            </div>
            <a href="?action=feed" target="_self" class="lvl-btn">레벨업 ✚</a>
        </div>

        <div class="slot-card">
            <div class="slot-info">
                <span style="font-size:24px;">🛈</span>
                <div>
                    <div class="slot-title">산책시키기</div>
                    <div class="slot-level">레벨: {st.session_state.level_walk}</div>
                </div>
            </div>
            <a href="?action=walk" target="_self" class="lvl-btn">레벨업 ✚</a>
        </div>
    </div>

    <!-- 하단 메뉴 -->
    <div class="bottom-bar">
        <div class="status-pill">
            <span>나이: 1세</span>
            <span>기분: 우는 중</span>
        </div>
        <div class="nav-slots">
            <a href="?action=toggle_upgrade" target="_self" class="nav-btn {'active' if st.session_state.show_upgrade else ''}">⚙️ 업그레이드</a>
            <a href="#" class="nav-btn">📈 성장</a>
            <a href="#" class="nav-btn">❤️ 상태</a>
            <a href="#" class="nav-btn">🖼️ 배경</a>
            <a href="#" class="nav-btn">🔧 옵션</a>
        </div>
    </div>
</div>
"""

st.components.v1.html(html_code, height=620)
