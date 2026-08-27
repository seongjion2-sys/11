import streamlit as st
from PIL import Image, ImageFilter

# 1. 페이지 기본 설정
st.set_page_config(page_title="인간 키우기", layout="centered")

# 2. 세션 상태 초기화 (레벨 및 UI 상태 관리)
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
    .main-container {
        position: relative;
        text-align: center;
    }
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
        margin-top: -350px;
        position: relative;
        z-index: 99;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 3. 이미지 로드 및 합성
# 실제 프로젝트 디렉터리에 bg.jpg(거실)와 baby.png(아기) 이미지를 준비해주세요.
try:
    bg_img = Image.open("bg.jpg").convert("RGBA")
    baby_img = Image.open("baby.png").convert("RGBA")

    # 아기 이미지 크기 조절 및 거실 배경 중앙 하단(테이블 위) 배치
    baby_resized = baby_img.resize((180, 180))
    bg_width, bg_height = bg_img.size
    paste_x = (bg_width - baby_resized.width) // 2
    paste_y = int(bg_height * 0.55)

    # 업그레이드 버튼을 누르면 배경 블러 처리
    if st.session_state.show_upgrade:
        main_bg = bg_img.filter(ImageFilter.GaussianBlur(radius=8))
    else:
        main_bg = bg_img.copy()

    main_bg.paste(baby_resized, (paste_x, paste_y), baby_resized)
    st.image(main_bg, use_column_width=True)

except FileNotFoundError:
    st.warning("⚠️ 'bg.jpg' 및 'baby.png' 이미지 파일을 프로젝트 폴더에 넣어주세요.")

# 4. 상단 상태 표시바
st.markdown("<div style='text-align: center;'><div class='status-bar'>나이: 1세 &nbsp;&nbsp;|&nbsp;&nbsp; 기분: 우는 중</div></div>", unsafe_allow_html=True)
st.write("")

# 5. 업그레이드 모달 창 (업그레이드 버튼 클릭 시 팝업)
if st.session_state.show_upgrade:
    with st.container():
        st.markdown("<div class='upgrade-box'>", unsafe_allow_html=True)
        st.subheader("🛠️ 업그레이드")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write("🖐️ **쓰다듬기**")
            st.caption(f"레벨: {st.session_state.level_stroke}")
        with col3:
            if st.button("레벨업", key="btn_stroke"):
                st.session_state.level_stroke += 1
                st.rerun()

        st.divider()

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write("🍼 **밥 먹이기**")
            st.caption(f"레벨: {st.session_state.level_feed}")
        with col3:
            if st.button("레벨업", key="btn_feed"):
                st.session_state.level_feed += 1
                st.rerun()

        st.divider()

        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write("🛈 **산책시키기**")
            st.caption(f"레벨: {st.session_state.level_walk}")
        with col3:
            if st.button("레벨업", key="btn_walk"):
                st.session_state.level_walk += 1
                st.rerun()

        st.write("")
        if st.button("닫기", use_container_width=True):
            st.session_state.show_upgrade = False
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)

# 6. 하단 게임 메뉴 슬롯
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
