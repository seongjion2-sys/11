import streamlit as st
import base64
import io
from PIL import Image, ImageFilter

# 1. 페이지 기본 설정
st.set_page_config(page_title="인간 키우기", layout="centered")

# 2. 이미지 Base64 데이터 (배경 및 아기)
BG_IMAGE_B64 = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1000&auto=format&fit=crop"  # 기본 배경용 대체 URL 혹은 로드 기능
# 외부 이미지 URL을 직접 로드할 수 있도록 urllib 요청 지원
import urllib.request

@st.cache_data
def load_default_images():
    # 배경 이미지 (거실)
    bg_url = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1000&auto=format&fit=crop"
    req = urllib.request.Request(bg_url, headers={'User-Agent': 'Mozilla/5.0'})
    bg_data = urllib.request.urlopen(req).read()
    bg_img = Image.open(io.BytesIO(bg_data)).convert("RGBA")
    
    # 아기 이미지 (투명 배경 대체 아이콘/이미지)
    # 이미지 링크 문제 없이 작동하도록 안정적인 아기/어린이 PNG 주소 사용
    baby_url = "https://cdn-icons-png.flaticon.com/512/2922/2922510.png"
    req_baby = urllib.request.Request(baby_url, headers={'User-Agent': 'Mozilla/5.0'})
    baby_data = urllib.request.urlopen(req_baby).read()
    baby_img = Image.open(io.BytesIO(baby_data)).convert("RGBA")
    
    return bg_img, baby_img

# 3. 세션 상태 초기화
if "level_stroke" not in st.session_state:
    st.session_state.level_stroke = 0
if "level_feed" not in st.session_state:
    st.session_state.level_feed = 0
if "level_walk" not in st.session_state:
    st.session_state.level_walk = 0
if "show_upgrade" not in st.session_state:
    st.session_state.show_upgrade = False

# 커스텀 CSS (게임풍 UI 스타일링)
st.markdown("""
    <style>
    .status-bar {
        background-color: #2b2b2b;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 10px;
        font-weight: bold;
    }
    .upgrade-box {
        background-color: rgba(255, 255, 255, 0.95);
        border: 3px solid #f0d082;
        border-radius: 15px;
        padding: 20px;
        margin-top: -320px;
        position: relative;
        z-index: 99;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 4. 이미지 로드 및합성
try:
    bg_img, baby_img = load_default_images()
    
    # 이미지 리사이즈 및 위치 잡기
    bg_img = bg_img.resize((800, 500))
    baby_resized = baby_img.resize((150, 150))
    
    bg_width, bg_height = bg_img.size
    paste_x = (bg_width - baby_resized.width) // 2
    paste_y = int(bg_height * 0.55)

    # 업그레이드 클릭 시 배경 블러 처리
    if st.session_state.show_upgrade:
        main_bg = bg_img.filter(ImageFilter.GaussianBlur(radius=8))
    else:
        main_bg = bg_img.copy()

    main_bg.paste(baby_resized, (paste_x, paste_y), baby_resized)
    st.image(main_bg, use_container_width=True)

except Exception as e:
    st.error(f"이미지를 불러오는 중 오류가 발생했습니다: {e}")

# 5. 상단 상태 표시바
st.markdown("<div style='text-align: center;'><div class='status-bar'>나이: 1세 &nbsp;&nbsp;|&nbsp;&nbsp; 기분: 우는 중</div></div>", unsafe_allow_html=True)
st.write("")

# 6. 업그레이드 모달 창
if st.session_state.show_upgrade:
    with st.container():
        st.markdown("<div class='upgrade-box'>", unsafe_allow_html=True)
        st.subheader("🛠️ 업그레이드")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("🖐️ **쓰다듬기**")
            st.caption(f"레벨: {st.session_state.level_stroke}")
        with col2:
            if st.button("레벨업", key="btn_stroke"):
                st.session_state.level_stroke += 1
                st.rerun()

        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("🍼 **밥 먹이기**")
            st.caption(f"레벨: {st.session_state.level_feed}")
        with col2:
            if st.button("레벨업", key="btn_feed"):
                st.session_state.level_feed += 1
                st.rerun()

        st.divider()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("🛈 **산책시키기**")
            st.caption(f"레벨: {st.session_state.level_walk}")
        with col2:
            if st.button("레벨업", key="btn_walk"):
                st.session_state.level_walk += 1
                st.rerun()

        st.write("")
        if st.button("닫기", use_container_width=True):
            st.session_state.show_upgrade = False
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

# 7. 하단 메뉴 슬롯
st.write("")
menu_col1, menu_col2, menu_col3, menu_col4, menu_col5 = st.columns(5)

with menu_col1:
    if st.button("⚙️ 업그레이드", use_container_width=True):
        st.session_state.show_upgrade = not st.session_state.show_upgrade
        st.rerun()

with menu_col2:
    st.button("📈 성장", use_container_width=True)

with menu_col3:
    st.button("❤️ 상태", use_container_width=True)

with menu_col4:
    st.button("🖼️ 배경", use_container_width=True)

with menu_col5:
    st.button("🔧 옵션", use_container_width=True)
