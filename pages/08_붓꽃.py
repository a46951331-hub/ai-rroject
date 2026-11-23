import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="Iris 품종 예측 및 시각화",
    page_icon="🌸",
    layout="centered"
)

st.title("🌸 붓꽃(Iris) 품종 예측 및 위치 시각화")
st.write("사용자가 입력한 **꽃잎 길이**와 **꽃잎 너비**를 기반으로 머신러닝 모델이 품종을 예측하고, 전체 데이터 분포 속에서 사용자의 입력 위치를 확인합니다.")

# 사용된 알고리즘 명시 및 쉬운 설명 섹션
st.markdown("### 🤖 사용된 예측 알고리즘: **랜덤 포레스트 (Random Forest)**")
with st.expander("💡 랜덤 포레스트 알고리즘은 어떻게 작동하나요? (알기 쉬운 설명 보기)", expanded=True):
    st.markdown("""
    **랜덤 포레스트(Random Forest)**는 쉽게 말해 **'100명의 붓꽃 전문가(의사결정나무)가 모여 다수결로 품종을 결정하는 방식'**입니다.
    
    1. **스무고개 질문지 만들기 (의사결정나무)**:
       - 한 명의 전문가가 *"꽃잎 길이가 2.5cm보다 짧은가요? 네 → 그렇다면 Setosa입니다!"* 처럼 스무고개 질문을 던지며 품종을 찾아냅니다.
    2. **100명의 전문가 모으기 (숲 구성)**:
       - 한 사람의 판단은 실수할 수 있기 때문에, 조금씩 다른 기준과 질문을 가진 **100개의 의사결정나무(나무들이 모여 '숲'을 이룸)**를 만듭니다.
    3. **다수결 투표로 최종 결정**:
       - 사용자가 꽃잎 길이와 너비를 입력하면, 100명의 전문가가 각자 품종을 예측합니다.
       - 예를 들어 95명이 `Setosa`, 5명이 `Versicolor`라고 답하면, 가장 많은 표를 받은 **`Setosa`를 최종 품종으로 결정**합니다. (아래 표의 '예측 확률'이 바로 이 투표 비율입니다!)
    """)

st.divider()

# 2. 데이터 로드 및 모델 학습 (캐싱 활용)
@st.cache_resource
def load_data_and_model():
    # 한글 컬럼명에 맞춰 cp949 인코딩 사용
    df = pd.read_csv("Iris.csv", encoding="cp949")
    
    # 학습에 사용할 특성(X)과 레이블(y) 정의 (꽃잎 길이, 꽃잎 너비)
    X = df[['꽃잎길이', '꽃잎너비']]
    y = df['품종']
    
    # 분류 알고리즘: Random Forest 적용 (100개의 나무 사용)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return df, model

try:
    df, model = load_data_and_model()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 3. 입력값 범위 확인 및 슬라이더 제공
st.subheader("🔍 1. 꽃잎 제원 입력")

min_length = float(df['꽃잎길이'].min())
max_length = float(df['꽃잎길이'].max())
mean_length = float(df['꽃잎길이'].mean())

min_width = float(df['꽃잎너비'].min())
max_width = float(df['꽃잎너비'].max())
mean_width = float(df['꽃잎너비'].mean())

st.info(f"📌 **입력 가능 범위 안내**\n- **꽃잎 길이**: `{min_length} cm` ~ `{max_length} cm`\n- **꽃잎 너비**: `{min_width} cm` ~ `{max_width} cm`")

# 사용자가 입력할 수 있는 슬라이더
petal_length = st.slider(
    "꽃잎 길이 (Petal Length, cm)", 
    min_value=min_length, 
    max_value=max_length, 
    value=mean_length,
    step=0.1
)

petal_width = st.slider(
    "꽃잎 너비 (Petal Width, cm)", 
    min_value=min_width, 
    max_value=max_width, 
    value=mean_width,
    step=0.1
)
