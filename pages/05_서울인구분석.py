import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
import os

# 페이지 기본 설정
st.set_page_config(page_title="서울시 인구 연령대별 분석", layout="wide")

# 한글 폰트 설정 (Streamlit Cloud의 폰트 지원 처리)
@st.cache_resource
def setup_font():
    font_dirs = ['/usr/share/fonts/truetype/nanum']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    plt.rc('font', family='NanumGothic')
    plt.rcParams['axes.unicode_minus'] = False

setup_font()

# 데이터 불러오기 함수 (상위 폴더 ../population.csv 경로 반영)
@st.cache_data
def load_data():
    # 현재 파일(pages/인근 py파일) 위치 기준 상위 폴더 경로 탐색
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'population.csv')
    
    # 예비 경로 (실행 루트 위치 기준 탐색)
    if not os.path.exists(file_path):
        file_path = 'population.csv'
        
    for enc in ['cp949', 'euc-kr', 'utf-8']:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            return df
        except Exception:
            continue
    return None

df = load_data()

if df is None:
    st.error("`population.csv` 파일을 상위 폴더에서 찾을 수 없거나 불러오는데 실패했습니다.")
    st.stop()

st.title("📊 서울시 행정구별 연령대 인구수 분석")
st.markdown("행정구, 연도, 성별을 선택하여 연령대별 인구 분포를 확인하세요.")

# 사이드바 컨트롤러
st.sidebar.header("조회 조건 선택")

# 1. 행정구 선택
district_list = df['행정구역'].tolist()
selected_district = st.sidebar.selectbox("행정구 선택", district_list)

# 2. 연도 선택
years = ['2020', '2021', '2022', '2023', '2024', '2025']
selected_year = st.sidebar.selectbox("연도 선택", years)

# 3. 성별 선택
gender_options = ["전체", "남성", "여성"]
selected_gender = st.sidebar.radio("성별 선택", gender_options)

# 나이 구간 정의
age_labels = ['0~9세', '10~19세', '20~29세', '30~39세', '40~49세', 
              '50~59세', '60~69세', '70~79세', '80~89세', '90~99세', '100세 이상']

# 데이터 컬럼 접두사 매핑
if selected_gender == "전체":
    column_prefix = f"{selected_year}년_거주자_"
elif selected_gender == "남성":
    column_prefix = f"{selected_year}년_남_거주자_"
else:
    column_prefix = f"{selected_year}년_여_거주자_"

# 해당 연도 및 성별의 나이 컬럼 생성
age_columns = [f"{column_prefix}{age}" for age in age_labels]

# 선택된 행정구의 데이터 추출
row_data = df[df['행정구역'] == selected_district].iloc[0]

# 인구수 값 정형화 (쉼표 제거 및 정수 변환)
population_values = []
for col in age_columns:
    val = str(row_data[col]).replace(',', '').strip()
    population_values.append(int(val) if val.isdigit() else 0)

# 시각화 (Matplotlib 꺾은선 그래프)
fig, ax = plt.subplots(figsize=(12, 6))

# 초록색 꺾은선 그래프
ax.plot(age_labels, population_values, color='#2ca02c', marker='o', linewidth=2.5, markersize=7, label='인구수')

# 축 및 타이틀 설정
clean_district_name = selected_district.split('(')[0].strip()
ax.set_title(f"[{clean_district_name}] {selected_year}년 {selected_gender} 연령대별 인구 분포", fontsize=16, pad=15, fontweight='bold')
ax.set_xlabel("나이 구간", fontsize=12, labelpad=10)
ax.set_ylabel("인구수 (명)", fontsize=12, labelpad=10)

# Y축 구분선: 1,000명 단위 주 눈금(Major Ticks) 및 눈금선 설정
ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))

# 그리드 선 표시 (세로축 1,000명 단위 점선)
ax.grid(True, which='both', axis='y', linestyle='--', alpha=0.6)
ax.grid(True, axis='x', linestyle=':', alpha=0.3)

# 그래프 레이아웃 최적화
plt.xticks(rotation=15)
plt.tight_layout()

# Streamlit 화면에 그래프 출력
st.pyplot(fig)

# 요약 데이터 표 출력
st.subheader("📋 세부 인구 데이터")
data_df = pd.DataFrame({
    '연령대': age_labels,
    '인구수(명)': [f"{val:,}" for val in population_values]
})
st.dataframe(data_df.T, use_container_width=True)
