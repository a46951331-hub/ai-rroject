import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="국가별 MBTI 비율 시각화", layout="wide")


# 데이터 로드
@st.cache_data
def load_data():
  return pd.read_csv("countriesMBTI_16types.csv")


df = load_data()

st.title("🌍 국가별 MBTI 비율 분석 대시보드")
st.write("국가를 선택하면 16가지 MBTI 유형의 비율을 시각화합니다.")

# 1. 국가 선택 셀렉트박스
country_list = sorted(df["Country"].unique())
selected_country = st.selectbox("국가를 선택하세요:", country_list)

if selected_country:
  # 해당 국가의 MBTI 데이터 추출 및 정렬 (내림차순)
  mbti_cols = [col for col in df.columns if col != "Country"]
  country_df = df[df["Country"] == selected_country][mbti_cols].T
  country_df.columns = ["Ratio"]
  country_df = country_df.sort_values(by="Ratio", ascending=False).reset_index()
  country_df.columns = ["MBTI", "Ratio"]

  # 색상 팔레트 생성 (1등: 빨간색, 2~16등: 파란색 그라데이션 - 진한 파랑에서 연한 파랑으로)
  n = len(country_df)
  blue_cmap = plt.get_cmap("Blues_r")

  # 2등부터 16등까지의 파란색 그라데이션 색상값 계산
  blue_colors = [
      mcolors.to_hex(blue_cmap(i)) for i in np.linspace(0.2, 0.7, n - 1)
  ]

  # 1등은 빨간색, 나머지는 파란색 그라데이션 지정
  colors = ["#FF3333"] + blue_colors

  # 시각화 (Matplotlib)
  fig, ax = plt.subplots(figsize=(12, 6))
  bars = ax.bar(
      country_df["MBTI"],
      country_df["Ratio"] * 100,
      color=colors,
      edgecolor="none",
  )

  # 그래프 스타일링
  ax.set_title(
      f"[{selected_country}] MBTI 유형별 비율 (%)",
      fontsize=16,
      pad=15,
      fontweight="bold",
  )
  ax.set_xlabel("MBTI 유형", fontsize=12, labelpad=10)
  ax.set_ylabel("비율 (%)", fontsize=12, labelpad=10)
  ax.set_ylim(0, max(country_df["Ratio"] * 100) * 1.15)
  ax.spines["top"].set_visible(False)
  ax.spines["right"].set_visible(False)

  # 막대 상단에 비율 값 표시
  for bar in bars:
    height = bar.get_height()
    ax.annotate(
        f"{height:.2f}%",
        xy=(bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 3),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )

  # Streamlit에 그래프 출력
  st.pyplot(fig)

  # 데이터 테이블 표시
  st.subheader(f"📋 {selected_country} MBTI 수치 데이터 (내림차순)")
  country_df["Ratio (%)"] = (country_df["Ratio"] * 100).map("{:.2f}%".format)
  st.dataframe(country_df[["MBTI", "Ratio (%)"]], use_container_width=True)
