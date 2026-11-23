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
st.write("사용자가 입력한 **꽃잎 길이**와 **꽃잎 너비**를 기반으로 **랜덤 포레스트(Random Forest)** 알고리즘을 통해 품종을 예측하고, 전체 데이터 분포 속에서 사용자의 입력 위치를 확인합니다.")

# 2. 데이터 로드 및 모델 학습 (캐싱 활용)
@st.cache_resource
def load_data_and_model():
    # 한글 컬럼명에 맞춰 cp949 인코딩 사용
    df = pd.read_csv("Iris.csv", encoding="cp949")
    
    # 학습에 사용할 특성(X)과 레이블(y) 정의 (꽃잎 길이, 꽃잎 너비)
    X = df[['꽃잎길이', '꽃잎너비']]
    y = df['품종']
    
    # 분류 알고리즘: Random Forest 적용
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

# 4. 예측 수행 및 결과 출력
if st.button("품종 예측 및 위치 확인하기", type="primary"):
    # 입력값 데이터프레임 변환
    input_df = pd.DataFrame([[petal_length, petal_width]], columns=['꽃잎길이', '꽃잎너비'])
    
    # 예측 실행
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0]
    classes = model.classes_
    
    st.success(f"🎉 예측된 붓꽃 품종은 **{prediction}** 입니다!")
    
    # 확률 바 차트
    st.write("### 📊 품종별 예측 확률")
    proba_df = pd.DataFrame({
        '품종': classes,
        '확률(%)': prediction_proba * 100
    })
    st.dataframe(proba_df.set_index('품종').T.style.format("{:.2f}%"))
    
    # 5. 가로축: 꽃잎 길이, 세로축: 꽃잎 너비 산점도 시각화 (노란색 별 표시)
    st.write("### 🗺️ 데이터 분포 및 사용자 입력 위치 (⭐)")
    st.write("전체 붓꽃 데이터 분포와 사용자가 입력한 값(노란색 별)의 위치를 비교합니다.")
    
    # 원본 데이터 시각화
    fig = px.scatter(
        df, 
        x='꽃잎길이', 
        y='꽃잎너비', 
        color='품종',
        title="꽃잎 길이 vs 꽃잎 너비 분포",
        labels={'꽃잎길이': '꽃잎 길이 (cm)', '꽃잎너비': '꽃잎 너비 (cm)'},
        opacity=0.7
    )
    
    # 사용자가 입력한 위치를 노란색 큰 별(⭐)로 추가
    user_point = pd.DataFrame({
        '꽃잎길이': [petal_length],
        '꽃잎너비': [petal_width],
        '품종': [f"입력값 ({prediction})"]
    })
    
    fig.add_scatter(
        x=user_point['꽃잎길이'],
        y=user_point['꽃잎너비'],
        mode='markers',
        marker=dict(size=20, color='gold', symbol='star', line=dict(width=1, color='black')),
        name='사용자 입력 위치 (⭐)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 부가 정보
with st.expander("📁 원본 데이터셋 보기"):
    st.dataframe(df)
