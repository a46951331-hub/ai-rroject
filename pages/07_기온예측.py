import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

# 페이지 기본 설정
st.set_page_config(page_title="기온 예측 및 선형회귀 분석", layout="wide")

st.title("🌡️ 과거 기온 데이터 분석 및 미래 기온 예측")
st.markdown("선택한 월의 역대 평균기온 추이를 확인하고, **선형회귀(Linear Regression)** 모델로 미래 기온을 예측합니다.")

# 1. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data(file_path):
    # 기상청 CSV는 주로 cp949(euc-kr) 인코딩을 사용하므로 예외 처리 포함
    try:
        df = pd.read_csv(file_path, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="utf-8")

    # 컬럼명 공백/탭 제거
    df.columns = df.columns.str.strip()

    # 월 영문 약자 매핑
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    # '일시' 컬럼(예: Oct-07)에서 4자리 연도와 월 추출 (1907년 시작 기준 순차 증가)
    years = []
    months = []
    curr_year = 1907
    prev_y2d = 7

    for val in df["일시"]:
        m_str, y_str = str(val).split("-")
        y2d = int(y_str)
        # 두 자리 연도가 작아지면(예: 99 -> 00) 세기가 바뀐 것으로 처리
        if y2d < prev_y2d:
            curr_year += (100 - prev_y2d) + y2d
        else:
            curr_year += (y2d - prev_y2d)
        years.append(curr_year)
        months.append(month_map[m_str])
        prev_y2d = y2d

    df["연도"] = years
    df["월"] = months

    # 평균기온 결측치(NaN) 제거
    df = df.dropna(subset=["평균기온(℃)"]).copy()
    return df

# 파일 로드 (요청하신 파일명 tempersture.csv 적용)
FILE_NAME = "tempersture.csv"

try:
    df = load_data(FILE_NAME)
except FileNotFoundError:
    st.error(f"'{FILE_NAME}' 파일을 찾을 수 없습니다. 깃허브 저장소에 파일이 있는지 확인해주세요.")
    st.stop()

# 2. 사용자 입력 (사이드바)
st.sidebar.header("⚙️ 예측 조건 설정")
selected_month = st.sidebar.selectbox(
    "분석할 월(Month)을 선택하세요",
    options=list(range(1, 13)),
    format_func=lambda x: f"{x}월",
    index=7  # 기본값: 8월
)

max_data_year = int(df["연도"].max())
target_year = st.sidebar.number_input(
    "예측할 연도(Year)를 입력하세요",
    min_value=max_data_year + 1,
    max_value=2150,
    value=2030,
    step=1
)

# 3. 선택한 월 데이터 필터링 및 선형회귀 모델 학습
month_df = df[df["월"] == selected_month].sort_values("연도")

X = month_df[["연도"]].values  # 독립변수 (연도)
y = month_df["평균기온(℃)"].values  # 종속변수 (평균기온)

model = LinearRegression()
model.fit(X, y)

# 예측 수행
predicted_temp = model.predict([[target_year]])[0]
slope = model.coef_[0]          # 기울기 (1년당 기온 변화량)
intercept = model.intercept_    # y절편

# 추세선 계산 (과거 시작 연도 ~ 사용자가 입력한 예측 연도까지)
line_years = np.arange(month_df["연도"].min(), target_year + 1).reshape(-1, 1)
line_temps = model.predict(line_years)

# 4. 핵심 요약 지표 출력
col1, col2, col3 = st.columns(3)
col1.metric(
    label=f"과거 {selected_month}월 전체 평균기온",
    value=f"{y.mean():.2f} ℃"
)
col2.metric(
    label=f"{target_year}년 {selected_month}월 예측 기온",
    value=f"{predicted_temp:.2f} ℃",
    delta=f"{predicted_temp - y.mean():+.2f} ℃ (역대 평균 대비)"
)
col3.metric(
    label="연간 기온 상승 추세 (기울기)",
    value=f"{slope * 100:+.2f} ℃ / 100년",
    delta=f"매년 {slope:+.4f} ℃ 변화"
)

# 5. 선형회귀 작동 원리 시각화 그래프 (Plotly)
fig = go.Figure()

# (1) 실제 과거 기온 데이터 (산점도 + 연한 실선)
fig.add_trace(go.Scatter(
    x=month_df["연도"],
    y=month_df["평균기온(℃)"],
    mode="markers+lines",
    name=f"실제 {selected_month}월 평균기온",
    line=dict(color="rgba(100, 149, 237, 0.35)", width=1.5),
    marker=dict(color="royalblue", size=6),
    hovertemplate="연도: %{x}년<br>실제 기온: %{y:.1f}℃<extra></extra>"
))

# (2) 오차(잔차, Residual) 시각화: 실제 점과 회귀선 사이의 수직 거리 (최근 15개 데이터만 표시하여 가독성 유지)
recent_df = month_df.tail(15)
recent_pred = model.predict(recent_df[["연도"]].values)
for idx, (yr, actual_t, pred_t) in enumerate(zip(recent_df["연도"], recent_df["평균기온(℃)"], recent_pred)):
    fig.add_trace(go.Scatter(
        x=[yr, yr],
        y=[actual_t, pred_t],
        mode="lines",
        line=dict(color="gray", width=1, dash="dot"),
        name="오차(잔차: 실제값-예측선)" if idx == 0 else None,
        showlegend=(idx == 0),
        hoverinfo="skip"
    ))

# (3) 선형회귀 추세선 (과거 구간 학습선)
past_mask = line_years.flatten() <= max_data_year
fig.add_trace(go.Scatter(
    x=line_years.flatten()[past_mask],
    y=line_temps[past_mask],
    mode="lines",
    name=f"선형회귀 추세선 (y = {slope:.4f}x + {intercept:.1f})",
    line=dict(color="orange", width=3),
    hovertemplate="연도: %{x}년<br>추세선 기온: %{y:.2f}℃<extra></extra>"
))

# (4) 미래 연장 예측선 (점선)
future_mask = line_years.flatten() >= max_data_year
fig.add_trace(go.Scatter(
    x=line_years.flatten()[future_mask],
    y=line_temps[future_mask],
    mode="lines",
    name="미래 연장 예측 경로",
    line=dict(color="crimson", width=3, dash="dash"),
    hovertemplate="연도: %{x}년<br>예측 기온: %{y:.2f}℃<extra></extra>"
))

# (5) 최종 예측 지점 강조 마커
fig.add_trace(go.Scatter(
    x=[target_year],
    y=[predicted_temp],
    mode="markers+text",
    name=f"{target_year}년 예측 결과",
    marker=dict(color="crimson", size=14, symbol="star", line=dict(color="black", width=1.5)),
    text=[f"  {target_year}년: {predicted_temp:.2f}℃"],
    textposition="top left",
    textfont=dict(color="crimson", size=13, family="sans-serif"),
    hovertemplate=f"<b>{target_year}년 {selected_month}월 예측</b><br>기온: {predicted_temp:.2f}℃<extra></extra>"
))

fig.update_layout(
    title=f"📈 {selected_month}월 평균기온 변화 및 {target_year}년 선형회귀 예측 시각화",
    xaxis_title="연도 (Year)",
    yaxis_title="평균기온 (℃)",
    hovermode="closest",
    template="plotly_white",
    height=550,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# 6. 선형회귀 알고리즘 쉬운 설명 (그래프 하단)
st.divider()
st.subheader("💡 그래프 속 '선형회귀 알고리즘'은 어떻게 작동할까요?")

st.markdown(f"""
**선형회귀(Linear Regression)**는 흩어져 있는 과거 데이터들의 전체적인 흐름을 가장 잘 대표하는 **'하나의 직선(추세선)'**을 찾아 미래를 예측하는 인공지능·통계 기법입니다.

1. **데이터 점 찍기 (파란색 점):** 먼저 과거부터 현재까지 매년 **{selected_month}월**의 실제 평균기온을 그래프 위에 점으로 찍습니다. 해마다 날씨가 달라서 점들이 위아래로 오르락내리락합니다.
2. **가장 알맞은 직선 찾기 (주황색 실선):** 컴퓨터는 모든 파란 점들과 직선 사이의 수직 거리(**회색 점선 = 오차**)를 제곱해서 모두 더한 값이 **가장 작아지는(최소제곱법)** 단 하나의 직선을 계산해 냅니다.
   * 현재 데이터에서 찾은 직선의 공식: **`예측 기온 = {slope:.4f} × 연도 + ({intercept:.2f})`**
   * 여기서 **`{slope:.4f}`(기울기)**는 매년 {selected_month}월 기온이 평균적으로 얼마나 변하는지를 뜻합니다.
3. **미래로 직선 연장하기 (빨간색 점선 및 별표):** 과거의 추세가 앞으로도 똑같이 이어진다고 가정하고, 주황색 직선을 **{target_year}년**까지 자를 대고 쭉 연장합니다. 그 직선이 **{target_year}년**과 만나는 지점(**빨간 별표, `{predicted_temp:.2f}℃`**)이 바로 모델이 예측한 미래 기온입니다.
""")

with st.expander("📋 선택한 월의 원본 데이터 표 보기"):
    st.dataframe(month_df[["연도", "월", "평균기온(℃)", "평균최고기온(℃)", "평균최저기온(℃)"]].sort_values("연도", ascending=False), use_container_width=True)
