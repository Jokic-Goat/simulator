import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="양면게임이론 - Win-Set 시각화", layout="centered")
st.title("🎯 양면게임이론 시뮬레이터: 수직선 위의 Win-Set")

# 초기값 설정
if "us_winset" not in st.session_state:
    st.session_state.us_winset = [30, 70]
    st.session_state.cn_winset = [40, 80]
    st.session_state.history = []

# 전략에 따른 Win-set 조정 함수
strategy_effects = {
    "확장": (+10, +10),
    "유지": (0, 0),
    "축소": (-10, -10)
}

# 사용자 인터페이스
st.subheader("전략 선택")
col1, col2 = st.columns(2)

with col1:
    us_strategy = st.selectbox("🇺🇸 미국의 전략", ["확장", "유지", "축소"])
with col2:
    cn_strategy = st.selectbox("🇨🇳 중국의 전략", ["확장", "유지", "축소"])

if st.button("턴 실행"):
    # Win-set 조정
    us_shift = strategy_effects[us_strategy]
    cn_shift = strategy_effects[cn_strategy]
    st.session_state.us_winset[0] += us_shift[0]
    st.session_state.us_winset[1] += us_shift[1]
    st.session_state.cn_winset[0] += cn_shift[0]
    st.session_state.cn_winset[1] += cn_shift[1]

    # 윈셋 교차 여부
    us_start, us_end = st.session_state.us_winset
    cn_start, cn_end = st.session_state.cn_winset
    overlap = max(0, min(us_end, cn_end) - max(us_start, cn_start))

    result = "✅ 합의 가능 (Win-set 존재)" if overlap > 0 else "❌ 합의 불가능 (Win-set 없음)"
    st.session_state.history.append({
        "미국 전략": us_strategy,
        "중국 전략": cn_strategy,
        "미국 Win-set": f"[{us_start}, {us_end}]",
        "중국 Win-set": f"[{cn_start}, {cn_end}]",
        "결과": result
    })

# 그래프 시각화
st.subheader("Win-set 시각화 (수직선)")
fig, ax = plt.subplots(figsize=(2, 6))
ax.set_ylim(0, 100)
ax.set_xlim(0, 3)
ax.set_xticks([1, 2])
ax.set_xticklabels(["미국", "중국"])

# 미국/중국 Win-set 그리기
ax.vlines(1, *st.session_state.us_winset, color="blue", linewidth=10, label="미국 Win-set")
ax.vlines(2, *st.session_state.cn_winset, color="red", linewidth=10, label="중국 Win-set")

ax.text(1.05, st.session_state.us_winset[1] + 2, f"{st.session_state.us_winset}", fontsize=9)
ax.text(2.05, st.session_state.cn_winset[1] + 2, f"{st.session_state.cn_winset}", fontsize=9)
ax.set_ylabel("합의안 수직선 상 위치")
st.pyplot(fig)

# 기록 출력
if st.session_state.history:
    st.subheader("📜 턴별 전략 및 결과 기록")
    st.table(st.session_state.history)
