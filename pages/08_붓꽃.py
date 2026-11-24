import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="Iris 3대 알고리즘 비교 예측",
    page_icon="🌸",
    layout="centered"
)

st.title("🌸 붓꽃(Iris) 3대 알고리즘 비교 및 품종 예측")
st.write("사용자가 입력한 **꽃잎 길이**와 **꽃잎 너비**를 바탕으로 **3가지 머신러닝 알고리즘**이 각각 어떤 예측 결과를 내는지 비교하고 확인합니다.")

# 2. 3가지 분류 알고리즘 작동 원리 쉬운 설명 섹션
with st.expander("💡 [학습 자료] 3가지 분류 알고리즘의 작동 원리가 궁금하신가요? (클릭해서 열기)", expanded=True):
    st.markdown("""
    ### 1. 🌲 랜덤 포레스트 (Random Forest)
    * **비유**: *"100명의 붓꽃 전문가가 모여 다수결로 투표하는 방식"*
    * **원리**: 데이터 특성을 이용해 여러 개의 '의사결정나무(스무고개)'를 만들고, 각 나무가 내린 예측을 모아 가장 표를 많이 받은 결과로 최종 품종을 결정합니다. 성능이 매우 뛰어나고 안정적입니다.
    
    ### 2. 📏 서포트 벡터 머신 (SVM, Support Vector Machine)
    * **비유**: *"서로 다른 품종 사이에 가장 완벽한 '경계선(울타리)'을 긋는 방식"*
    * **원리**: 데이터들을 공간에 점으로 찍은 뒤, 품종과 품종 사이의 간격(마진)이 가장 넓어지도록 최적의 경계선을 찾아냅니다. 새로운 데이터가 경계선의 어느 쪽에 위치하느냐에 따라 품종을 판별합니다.
    
    ### 3. 👥 K-최근접 이웃 (KNN, K-Nearest Neighbors)
    * **비유**: *"내 주변에 어떤 이웃들이 살고 있는지 보고 판단하는 방식"*
    * **원리**: 새로운 데이터가 들어오면 가장 가까운 곳에 있는 이웃 데이터(여기서는 K=5개)를 찾습니다. 그 이웃들 중 가장 많은 품종이 무엇이냐에 따라 내 품종을 결정합니다.
    """)

st.divider()

# 3. 데이터 로드 및 3개 모델 학습 (캐싱 활용)
@st.cache_resource
def load_data_and_models():
    # 한글 컬럼명에 맞춰 cp949 인코딩 사용
    df = pd.read_csv("Iris.csv", encoding="cp949")
    
    X = df[['꽃잎길이', '꽃잎너비']]
    y = df['품종']
    
    # 3가지 알고리즘 모델 초기화 및 학습
    model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    model_rf.fit(X, y)
    
    model_svm = SVC(probability=True, random_state=42)
    model_svm.fit(X, y)
    
    model_knn = KNeighborsClassifier(n_neighbors=5)
    model_knn.fit(X, y)
    
    return df, {
        '랜덤 포레스트 (Random Forest)': model_rf, 
        '서포트 벡터 머신 (SVM)': model_svm, 
        'K-최근접 이웃 (KNN)': model_knn
    }

try:
    df, models = load_data_and_models()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 4. 입력값 범위 확인 및 슬라이더 제공
st.subheader("🔍 1. 꽃잎 제원 입력")

min_length = float(df['꽃잎길이'].min())
max_length = float(df['꽃잎길이'].max())
mean_length = float(df['꽃잎길이'].mean())

min_width = float(df['꽃잎너비'].min())
max_width = float(df['꽃잎너비'].max())
mean_width = float(df['꽃잎너비'].mean())

# 사용자가 입력할 수 있는 값의 범위 사전 안내
st.info(f"📌 **입력 가능 범위 안내**\n- **꽃잎 길이**: `{min_length} cm` ~ `{max_length} cm`\n- **꽃잎 너비**: `{min_width} cm` ~ `{max_width} cm`")

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

# 5. 예측 수행 및 알고리즘별 결과 비교 출력
if st.button("3개 알고리즘으로 품종 예측 및 비교하기", type="primary"):
    input_df = pd.DataFrame([[petal_length, petal_width]], columns=['꽃잎길이', '꽃잎너비'])
    
    st.subheader("📊 2. 3개 알고리즘 예측 결과 비교")
    
    comparison_data = []
    
    # 각 모델별 예측 수행 및 결과 수집
    for name, model in models.items():
        pred = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0]
        max_proba = max(proba) * 100
        
        comparison_data.append({
            '사용한 알고리즘': name,
            '예측된 품종': pred,
            '확신도 (최고 확률)': f"{max_proba:.2f}%"
        })
    
    # 알고리즘 비교 테이블 표시
    comp_df = pd.DataFrame(comparison_data)
    st.table(comp_df)
    
    # 상세 확률 비교 확장 뷰
    with st.expander("🔍 알고리즘별 상세 예측 확률 전체 보기"):
        for name, model in models.items():
            proba = model.predict_proba(input_df)[0]
            classes = model.classes_
            st.write(f"**[{name}]**")
            p_df = pd.DataFrame({'품종': classes, '확률(%)': proba * 100})
            st.dataframe(p_df.set_index('품종').T.style.format("{:.2f}%"))

    # 6. 시각화 (가로축: 꽃잎 길이, 세로축: 꽃잎 너비 + 노란색 별)
    st.subheader("🗺️ 3. 데이터 분포 및 사용자 입력 위치 (⭐)")
    st.write("가로축을 **꽃잎 길이**, 세로축을 **꽃잎 너비**로 하여 전체 데이터 분포 속에서 사용자가 입력한 위치를 노란색 별(⭐)로 표시합니다.")
    
    fig = px.scatter(
        df, 
        x='꽃잎길이', 
        y='꽃잎너비', 
        color='품종',
        title="꽃잎 길이 vs 꽃잎 너비 분포도",
        labels={'꽃잎길이': '꽃잎 길이 (cm)', '꽃잎너비': '꽃잎 너비 (cm)'},
        opacity=0.7
    )
    
    # 사용자가 입력한 위치를 노란색 큰 별(⭐)로 추가
    user_point = pd.DataFrame({
        '꽃잎길이': [petal_length],
        '꽃잎너비': [petal_width],
        '품종': ['사용자 입력값']
    })
    
    fig.add_scatter(
        x=user_point['꽃잎길이'],
        y=user_point['꽃잎너비'],
        mode='markers',
        marker=dict(size=24, color='gold', symbol='star', line=dict(width=1.5, color='black')),
        name='사용자 입력 위치 (⭐)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# 부가 정보
with st.expander("📁 원본 데이터셋 보기"):
    st.dataframe(df)
