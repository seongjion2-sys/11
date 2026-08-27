import streamlit as st
import base64
import io
from PIL import Image, ImageDraw, ImageFilter

# 1. 페이지 기본 설정
st.set_page_config(page_title="인간 키우기", layout="centered")

# 2. 세션 상태 초기화
if "level_stroke" not in st.session_state:
    st.session_state.level_stroke = 0
if "level_feed" not in st.session_state:
    st.session_state.level_feed = 0
if "level_walk" not in st.session_state:
    st.session_state.level_walk = 0
if "show_upgrade" not in st.session_state:
    st.session_state.show_upgrade = False

# 3. 이미지 직접 생성 함수 (외부 다운로드 에러 방지)
@st.cache_data
def get_game_images():
    # 배경 (거실)
    bg = Image.new("RGB", (800, 480), color="#f5ede0")
    draw = ImageDraw.Draw(bg)
    draw.rectangle([250, 60, 550, 280], fill="#e0f2fe", outline="#ffffff", width=6)
    draw.line([400, 60, 400, 280], fill="#ffffff", width=4)
    draw.rounded_rectangle([40, 200, 240, 380], radius=15, fill="#d6c5b0")
    draw.rectangle([580, 100, 760, 240], fill="#1e293b", outline="#334155", width=4)
    draw.rectangle([300, 320, 500, 390], fill="#475569")
    
    # 아기 캐릭터
    baby = Image.new("RGBA", (140, 140), (255, 255, 255, 0))
    b_draw = ImageDraw.Draw(baby)
    b_draw.ellipse([30, 10, 110, 90], fill="#fde047") # 머리
    b_draw.ellipse([40, 70, 100, 130], fill="#f472b6") # 몸통
    b_draw.ellipse([50, 40, 60, 50], fill="#1e293b") # 눈 1
    b_draw.ellipse([80, 40, 90, 50], fill="#1e293b") # 눈 2
    
    return bg, baby

bg_img, baby_img = get_game_images()

# 4. 이미지 합성 및 처리
canvas = bg_img.copy()

# 업그레이드 메뉴 열릴 시 배경 블러 처리
if st.session_state.show_upgrade:
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=6))

# 아기 이미지 합성
paste_x = (canvas.width - baby_img.width) // 2
paste_y = int(canvas.height * 0.52)
canvas.paste(baby_img, (paste_x, paste_y), baby_img)

# CSS 디자인 스타일링
st.markdown("""
<style>
    .stApp { background-color: #0f172a; }
    .status-bar {
        background-color: #1e293b;
        color: white;
        padding: 8px 24px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .upgrade-container {
        background-color: #fffdfa;
        border: 3px solid #fbbf24;
        border-radius: 16px;
        padding: 20px;
        margin-top: -340px;
        position: relative;
        z-index: 99;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# 5. 게임 메인 화면 렌더링
st.image(canvas, use_container_width=True)

# 사진 바로 아래 아기 인터랙션(쓰다듬기) 클릭 버튼 배치
if st.button("👶 아기 쓰다듬기 (클릭!)", use_container_width=True):
    st.session_state.level_stroke += 1
    st.rerun()

# 6. 업그레이드 레이어 모달 창 (활성화 시 표시)
if st.session_state.show_upgrade:
    with st.container():
        st.markdown("<div class='upgrade-container'>", unsafe_allow_html=True)
        st.subheader("🛠️ 업그레이드 슬롯")
        
        # 슬롯 1: 쓰다듬기
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"🖐️ **쓰다듬기** (레벨: {st.session_state.level_stroke})")
        with col2:
            if st.button("레벨업 ✚", key="up_stroke"):
                st.session_state.level_stroke += 1
                st.rerun()

        st.divider()

        # 슬롯 2: 밥 먹이기
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"🍼 **밥 먹이기** (레벨: {st.session_state.level_feed})")
        with col2:
            if st.button("레벨업 ✚", key="up_feed"):
                st.session_state.level_feed += 1
                st.rerun()

        st.divider()

        # 슬롯 3: 산책시키기
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"🛈 **산책시키기** (레벨: {st.session_state.level_walk})")
        with col2:
            if st.button("레벨업 ✚", key="up_walk"):
                st.session_state.level_walk += 1
                st.rerun()

        st.write("")
        if st.button("❌ 닫기", use_container_width=True):
            st.session_state.show_upgrade = False
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# 7. 하단 상태창 및 메인 메뉴
st.markdown("<div style='text-align: center;'><div class='status-bar'>나이: 1세 &nbsp;&nbsp;|&nbsp;&nbsp; 기분: 우는 중</div></div>", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    if st.button("⚙️ 업그레이드", use_container_width=True):
        st.session_state.show_upgrade = not st.session_state.show_upgrade
        st.rerun()

with m2:
    st.button("📈 성장", use_container_width=True)

with m3:
    st.button("❤️ 상태", use_container_width=True)

with m4:
    st.button("🖼️ 배경", use_container_width=True)

with m5:
    st.button("🔧 옵션", use_container_width=True)
