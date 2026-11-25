import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="국민 다빈도 음식 추천 🍽️", page_icon="🍚", layout="centered"
)


# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
  # 인코딩 오류 방지를 위해 cp949 사용
  df = pd.read_csv(
      "한국보건산업진흥원_국민영양통계 다빈도음식의 식품섭취량_20231231.csv",
      encoding="cp949",
  )
  return df


try:
  df = load_data()
except Exception as e:
  st.error(
      "데이터 파일을 불러오지 못했어요! 파일명이 올바른지 확인해 주세요."
      f" 에러 내용: {e}"
  )
  st.stop()

# --- 화면 UI 구성 ---
st.title("🍽️ 국민 다빈도 음식 취향 추천기!")
st.markdown(
    "국민영양통계 데이터를 바탕으로 **카테고리별로 자주 먹는 인기 음식**을"
    " 추천해 줄게요! 아래에서 원하는 음식 종류를 골라봐! 😎"
)
st.divider()

# 2. 사람이 음식의 종류를 선택할 수 있는 목록 (간식류, 밥류, 면류, 빵류)
category_options = ["밥류 🍚", "면류 🍜", "간식류 🍪", "빵류 🍞"]
selected_category = st.radio("👇 원하는 음식 종류를 선택해 주세요!", category_options)

# 카테고리별 키워드 매핑 정의
category_keywords = {
    "밥류 🍚": [
        "밥",
        "덮밥",
        "볶음밥",
        "김밥",
        "국밥",
        "찌개",
        "구이",
        "삼겹살",
        "비빔밥",
    ],
    "면류 🍜": ["라면", "국수", "자장면", "파스타", "짬뽕", "우동", "냉면"],
    "간식류 🍪": [
        "과자",
        "음료",
        "탄산음료",
        "커피",
        "아이스크림",
        "요구르트",
        "초콜릿",
        "사탕",
        "젤리",
        "우유",
        "사과",
        "귤",
        "토마토",
        "포도",
        "복숭아",
        "수박",
        "감",
    ],
    "빵류 🍞": ["빵", "샌드위치", "와플", "크로플", "도넛"],
}


# 음식 이름에 키워드가 포함되는지 확인하는 함수
def filter_foods(food_name, keywords):
  for kw in keywords:
    if kw in food_name:
      return True
  return False


# 3. 선택된 카테고리에 맞는 음식 필터링
keywords = category_keywords[selected_category]

# 데이터프레임에서 조건에 맞는 음식 필터링 (중복 제거 및 상위 항목 추출)
matched_df = df[df["음식"].apply(lambda x: filter_foods(str(x), keywords))]

# 통계 데이터 활용 (연도별 전체 기준 또는 가장 많이 나타나는 순서 등)
if not matched_df.empty:
  # 섭취 비율(비율 평균 혹은 최신 연도 기준)이 높은 순으로 정렬하거나 고유 음식 추출
  top_foods = (
      matched_df.groupby("음식")["비율"].mean().reset_index()
  )  # 평균 비율 계산
  top_foods = top_foods.sort_values(by="비율", ascending=False).head(10)

  st.success(
      f"✨ **{selected_category}** 카테고리에서 가장 인기 있는 추천 음식들이야!"
  )

  # 결과를 카드 형태로 깔끔하게 출력
  for idx, row in top_foods.reset_index(drop=True).iterrows():
    with st.container(border=True):
      st.subheader(
          f"추천 {idx+1}. {row['음식']} 😋"
      )  # 섭취 비율이 높을수록 상위 노출
      st.markdown(
          f"📊 **국민 섭취 비율 점수:** `약 {row['비율']:.2f}%` (통계 기준)"
      )
      st.caption("이 음식을 선택하면 실패 확률이 적어! 오늘 이걸로 골라볼까?")

  st.balloons()
else:
  st.warning(
      "⚠️ 해당 카테고리에 매칭되는 음식 데이터를 데이터에서 찾지 못했어!"
  )

st.divider()
st.caption(
    "💡 데이터 출처: 한국보건산업진흥원 국민영양통계 다빈도음식의 식품섭취량"
)
