import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 게임 (High-Low)",
    page_icon="🎯",
    layout="centered"
)

# 세션 상태 초기화
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "best_score" not in st.session_state:
    st.session_state.best_score = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "history" not in st.session_state:
    st.session_state.history = []
if "message" not in st.session_state:
    st.session_state.message = None

def start_new_game():
    """새로운 게임 라운드를 시작합니다."""
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.message = None

def handle_guess(guess_val):
    """사용자가 입력한 숫자를 판정합니다."""
    if st.session_state.game_over:
        return

    st.session_state.attempts += 1
    attempts = st.session_state.attempts
    secret = st.session_state.secret_number

    if guess_val < secret:
        res_type = "UP"
        msg = f"📈 UP! ({guess_val}보다 큽니다.)"
    elif guess_val > secret:
        res_type = "DOWN"
        msg = f"📉 DOWN! ({guess_val}보다 작습니다.)"
    else:
        res_type = "CORRECT"
        msg = f"🎉 정답입니다! 정답 숫자: {secret} (총 {attempts}회 시도)"
        st.session_state.game_over = True
        
        # 최고 기록 업데이트
        if st.session_state.best_score is None or attempts < st.session_state.best_score:
            st.session_state.best_score = attempts
            st.session_state.is_new_record = True
        else:
            st.session_state.is_new_record = False

    st.session_state.message = (res_type, msg)
    st.session_state.history.insert(0, {
        "attempt": attempts,
        "guess": guess_val,
        "result": res_type
    })

# 사용자 지정 스타일링 (커스텀 CSS)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #555555;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .history-card {
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .up-card { background-color: #E3F2FD; border-left: 5px solid #2196F3; color: #0D47A1; }
    .down-card { background-color: #FBE9E7; border-left: 5px solid #FF5722; color: #BF360C; }
    .correct-card { background-color: #E8F5E9; border-left: 5px solid #4CAF50; color: #1B5E20; }
    </style>
""", unsafe_allow_html=True)

# 헤더 영역
st.markdown("<h1 class='main-title'>🎯 숫자 맞추기 게임</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>1부터 100 사이의 임의의 숫자를 맞춰보세요!</p>", unsafe_allow_html=True)

# 대시보드 메트릭 영역
col1, col2, col3 = st.columns(3)
with col1:
    best_display = f"{st.session_state.best_score}회" if st.session_state.best_score is not None else "아직 없음"
    st.metric("🏆 최고 기록", best_display)
with col2:
    st.metric("🔢 현재 시도 횟수", f"{st.session_state.attempts}회")
with col3:
    status_text = "게임 완료 🎉" if st.session_state.game_over else "진행 중 🎮"
    st.metric("📊 게임 상태", status_text)

st.divider()

# 게임 진행 및 입력 영역
if not st.session_state.game_over:
    with st.form(key="guess_form", clear_on_submit=True):
        guess_input = st.number_input(
            "1부터 100 사이의 숫자를 입력하세요:",
            min_value=1,
            max_value=100,
            step=1,
            value=50
        )
        submit_button = st.form_submit_button(label="🎯 정답 확인", use_container_width=True)

    if submit_button:
        handle_guess(guess_input)
        st.rerun()
else:
    st.success(f"🎊 축하합니다! {st.session_state.attempts}회 만에 정답({st.session_state.secret_number})을 맞추셨습니다!")
    st.balloons()
    
    if getattr(st.session_state, "is_new_record", False):
        st.info("🏆 **새로운 최고 기록을 달성했습니다!**")

    if st.button("🔄 새 게임 시작하기", use_container_width=True, type="primary"):
        start_new_game()
        st.rerun()

# 최신 피드백 메시지 표시
if st.session_state.message and not st.session_state.game_over:
    res_type, msg = st.session_state.message
    if res_type == "UP":
        st.info(msg)
    elif res_type == "DOWN":
        st.warning(msg)

# 입력 기록 리스트
if st.session_state.history:
    st.markdown("### 📜 시도 기록")
    for item in st.session_state.history:
        if item["result"] == "UP":
            badge_class = "up-card"
            icon = "📈 UP"
        elif item["result"] == "DOWN":
            badge_class = "down-card"
            icon = "📉 DOWN"
        else:
            badge_class = "correct-card"
            icon = "🎉 정답!"

        st.markdown(
            f"""
            <div class="history-card {badge_class}">
                <span><b>#{item['attempt']}회차 시도:</b> {item['guess']}</span>
                <span><b>{icon}</b></span>
            </div>
            """,
            unsafe_allow_html=True
        )

# 하단 게임 리셋 옵션 (사이드바)
with st.sidebar:
    st.header("⚙️ 게임 설정")
    if st.button("🔄 게임 초기화 (현재 라운드)"):
        start_new_game()
        st.rerun()
    if st.button("🗑️ 최고 기록 초기화"):
        st.session_state.best_score = None
        start_new_game()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📌 게임 규칙")
    st.markdown("""
    - 1부터 100 사이의 숫자를 입력합니다.
    - 힌트(**UP / DOWN**)를 받아 최단 시도 횟수로 정답을 획득하세요!
    """)
