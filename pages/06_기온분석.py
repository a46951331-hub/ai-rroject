import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 1. 한글 폰트 및 마이너스 기호 깨짐 방지 설정
def set_korean_font():
    system_name = platform.system()
    if system_name == 'Windows':
        plt.rcParams['font.family'] = 'Malgun Gothic'
    elif system_name == 'Darwin':  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    else:  # Linux / Streamlit Cloud (NanumGothic 설치 시)
        font_list = [f.name for f in fm.fontManager.ttflist]
        if 'NanumGothic' in font_list:
            plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# 2. 데이터 불러오기 및 전처리 (인코딩 처리 포함)
@st.cache_data
def load_data(file_path):
    # cp949 인코딩으로 읽기 (실패 시 utf-8 시도)
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='utf-8')
        
    # 컬럼명 앞뒤 공백 및 탭(\t) 제거
    df.columns = [c.strip() for c in df.columns]
    
    # '일시' 컬럼(예: Oct-07, Jan-08)에서 영문 월과 연도 분리
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    df['월'] = df['일시'].str.split('-').str[0].map(month_map)
    yr_2d = df['일시'].str.split('-').str[1].astype(int)
    
    # 1907년부터 2026년까지 4자리 연도 복원
    years = []
    curr_century = 1900
    prev_yr = 7
    for y in yr_2d:
        if y < prev_yr:
            curr_century += 100
        years.append(curr_century + y)
        prev_yr = y
    df['연도'] = years
    
    return df

# 앱 타이틀 및 데이터 로드
st.title("🌡️ 연도별 기온 데이터 시각화")

df = load_data("tempert.csv")

# 3. 사용자 월 선택 UI
selected_month = st.selectbox(
    "분석할 월을 선택하세요:",
    options=list(range(1, 13)),
    format_func=lambda x: f"{x}월"
)

# 선택된 월 데이터 필터링 및 결측치 제거
filtered_df = df[df['월'] == selected_month].dropna(subset=['최고기온(℃)', '최저기온(℃)'])

# 4. 꺾은선 그래프 그리기
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    filtered_df['연도'], 
    filtered_df['최고기온(℃)'], 
    color='red', 
    marker='o', 
    markersize=4, 
    label='최고기온'
)
ax.plot(
    filtered_df['연도'], 
    filtered_df['최저기온(℃)'], 
    color='blue', 
    marker='o', 
    markersize=4, 
    label='최저기온'
)

# 그래프 제목, 축 이름, 범례 설정
ax.set_title("월별 기온분삭", fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel("연도", fontsize=12)
ax.set_ylabel("온도", fontsize=12)
ax.legend(loc='best')
ax.grid(True, linestyle='--', alpha=0.5)

# 스트림릿 화면에 그래프 출력
st.pyplot(fig)

# 선택된 데이터 표 확인 (옵션)
with st.expander("선택한 월의 상세 데이터 보기"):
    st.dataframe(filtered_df[['연도', '월', '평균기온(℃)', '최고기온(℃)', '최저기온(℃)']], use_container_width=True)
