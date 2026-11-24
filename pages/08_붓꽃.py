import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 기본 설정 (와이드 레이아웃 적용)
st.set_page_config(
    page_title="Iris AI Classifier Pro",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 디자인
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)

# 2. 데이터 로드 및 3개 모델 학습
@st.cache_resource
def load_data_and_models():
    df = pd.read_csv("Iris.csv", encoding="cp949")
    X = df[['꽃잎길이', '꽃잎너비']]
    y = df['품종']
    
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'KNN': KNeighborsClassifier(n_neighbors=5)
    }
    
    for model in models.values():
        model.fit(X, y)
        
    return df, models

try:
    df, models = load_data_and_models()
except Exception as e:
    st.error(f"데이터 파일을 불러올 수 없습니다. 'Iris.csv' 파일이 같은 폴더에 있는지 확인해주세요. (오류: {e})")
    st.stop()

# 수치 범위 계산
min_len, max_len, mean_len = float(df['꽃잎길이'].min()), float(df['꽃잎길이'].max()), float(df['꽃잎길이'].mean())
min_wid, max_wid, mean_wid = float(df['꽃잎너비'].min()), float(df['꽃잎너비'].max()), float(df['꽃잎너비'].mean())

# 3. 사이드바: 사용자 입력 컨트롤 패널 (입력값 범위 사전 안내 포함)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Iris_versicolor_3.jpg/320px-Iris_versicolor_3.jpg", use_container_width=True)
    st.markdown("## 🎛️ 제원 입력 패널")
    st.write("아래 슬라이더를 조절하여 예측할 꽃잎의 크기를 설정하세요.")
    
    st.info(
        f"**📏 입력 가능 범위 안내**\n"
        f"- **꽃잎 길이**: `{min_len} cm` ~ `{max_len} cm`\n"
        f"- **꽃잎 너비**: `{min_wid} cm` ~ `{max_wid} cm`"
    )
    
    petal_length = st.slider(
        "꽃잎 길이 (Petal Length, cm)",
        min_value=min_len,
        max_value=max_len,
        value=round(mean_len, 1),
        step=0.1
    )
    
    petal_width = st.slider(
        "꽃잎 너비 (Petal Width, cm)",
        min_value=min_wid,
        max_value=max_wid,
        value=round(mean_wid, 1),
        step=0.1
    )
    
    st.divider()
    st.caption("💡 슬라이더를 움직이면 3가지 알고리즘의 예측 결과와 시각화가 실시간으로 반영됩니다.")

# 4. 메인 화면 헤더
st.markdown('<div class="main-header">🌸 붓꽃(Iris) AI 3대 알고리즘 비교 대시보드</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">3가지 분류 알고리즘(Random Forest, SVM, KNN)의 예측 결과를 비교하고, 입력한 위치의 분석 결과를 확인합니다.</div>', unsafe_allow_html=True)

# 입력 데이터 구성
input_df = pd.DataFrame([[petal_length, petal_width]], columns=['꽃잎길이', '꽃잎너비'])

# 3개 모델 예측 수행
results = {}
proba_list = []

for algo_name, model in models.items():
    pred
