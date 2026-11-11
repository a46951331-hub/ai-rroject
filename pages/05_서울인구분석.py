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

# 데이터 불러오기 함수 (pages/ 상위 폴더인 ../population.csv 경로 반영)
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '..', 'population.csv')
    
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

# 탭을 활용하여 기능 분리
tab1, tab2 = st.tabs(["📈 행정구 남녀 연령대 비교 꺾은선 그래프", "📊 특정 연령대 상위 자치구 막대그래프"])

# ==========================================
# [탭 1] 수정 기능: 서울시 전체 제외, 구와 연도 선택 시 남녀(핑크/초록) 비교 그래프
# ==========================================
with tab1:
    st.subheader("선택한 자치구의 남녀 연령대별 인구 비교")
    
    # 서울시 전체(첫 번째 행) 제외한 구 목록만 추출
    district_list_only = df.iloc[1:]['행정구역'].tolist()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_district = st.selectbox("행정구 선택", district_list_only, key="t1_district")
    with col2:
        years = ['2020', '2021', '2022', '2023', '2024', '2025']
        selected_year = st.selectbox("연도 선택", years, key="t1_year")

    age_labels = ['0~9세', '10~19세', '20~29세', '30~39세', '40~49세', 
                  '50~59세', '60~69세', '70~79세', '80~89세', '90~99세', '100세 이상']

    # 남성, 여성 컬럼 접두사
    male_prefix = f"{selected_year}년_남_거주자_"
    female_prefix = f"{selected_year}년_여_거주자_"

    male_columns = [f"{male_prefix}{age}" for age in age_labels]
    female_columns = [f"{female_prefix}{age}" for age in age_labels]

    row_data = df[df['행정구역'] == selected_district].iloc[0]

    # 남녀 인구수 파싱
    male_values, female_values = [], []
    for m_col, f_col in zip(male_columns, female_columns):
        m_val = str(row_data[m_col]).replace(',', '').strip()
        f_val = str(row_data[f_col]).replace(',', '').strip()
        male_values.append(int(m_val) if m_val.isdigit() else 0)
        female_values.append(int(f_val) if f_val.isdigit() else 0)

    # 시각화 (남성: 핑크색, 여성: 초록색 꺾은선)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(age_labels, male_values, color='#ff69b4', marker='o', linewidth=2.5, markersize=7, label='남성')
    ax.plot(age_labels, female_values, color='#2ca02c', marker='s', linewidth=2.5, markersize=7, label='여성')

    clean_district_name = selected_district.split('(')[0].strip()
    ax.set_title(f"[{clean_district_name}] {selected_year}년 남녀 연령대별 인구 분포", fontsize=14, pad=15, fontweight='bold')
    ax.set_xlabel("나이 구간", fontsize=11, labelpad=8)
    ax.set_ylabel("인구수 (명)", fontsize=11, labelpad=8)

    # Y축 1,000명 단위 눈금 및 그리드
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1000))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax.grid(True, which='both', axis='y', linestyle='--', alpha=0.6)
    ax.grid(True, axis='x', linestyle=':', alpha=0.3)
    ax.legend(fontsize=11)

    plt.xticks(rotation=15)
    plt.tight_layout()
    st.pyplot(fig)

    # 세부 데이터 표
    with st.expander("📋 세부 성별 인구 데이터 테이블 보기"):
        data_df = pd.DataFrame({
            '연령대': age_labels,
            '남성(명)': [f"{val:,}" for val in male_values],
            '여성(명)': [f"{val:,}" for val in female_values]
        })
        st.dataframe(data_df.set_index('연령대'), use_container_width=True)

# ==========================================
# [탭 2] 추가 기능: 10살 단위 나이대 선택 -> 인구 많은 구 순서대로 초록색 막대그래프
# ==========================================
with tab2:
    st.subheader("특정 연령대 인구 상위 자치구 비교 (내림차순)")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        selected_age = st.selectbox("나이대 선택", age_labels, key="t2_age")
    with col_b:
        selected_year_t2 = st.selectbox("연도 선택", years, key="t2_year")
    with col_c:
        gender_options = ["전체", "남성", "여성"]
        selected_gender_t2 = st.selectbox("성별 선택", gender_options, key="t2_gender")

    if selected_gender_t2 == "전체":
        prefix_t2 = f"{selected_year_t2}년_거주자_"
    elif selected_gender_t2 == "남성":
        prefix_t2 = f"{selected_year_t2}년_남_거주자_"
    else:
        prefix_t2 = f"{selected_year_t2}년_여_거주자_"
        
    target_col = f"{prefix_t2}{selected_age}"

    # 서울시 전체(첫 번째 행) 제외 자치구 추출
    districts_df = df.iloc[1:].copy()
    
    pop_list = []
    for idx, row in districts_df.iterrows():
        val_str = str(row[target_col]).replace(',', '').strip()
        val = int(val_str) if val_str.isdigit() else 0
        clean_name = row['행정구역'].split('(')[0].strip()
        pop_list.append({'행정구': clean_name, '인구수': val})

    result_df = pd.DataFrame(pop_list)
    # 인구수가 많은 구 순서대로 내림차순 정렬
    result_df = result_df.sort_values(by='인구수', ascending=False).reset_index(drop=True)

    # 시각화 (초록색 막대그래프)
    fig2, ax2 = plt.subplots(figsize=(14, 6))
    bars = ax2.bar(result_df['행정구'], result_df['인구수'], color='#2ca02c', alpha=0.85, edgecolor='green')

    ax2.set_title(f"[{selected_year_t2}년] '{selected_age}' 인구 자치구별 순위 ({selected_gender_t2})", fontsize=14, pad=15, fontweight='bold')
    ax2.set_xlabel("행정구", fontsize=11, labelpad=8)
    ax2.set_ylabel("인구수 (명)", fontsize=11, labelpad=8)

    ax2.yaxis.set_major_locator(ticker.MultipleLocator(1000))
    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax2.grid(True, which='major', axis='y', linestyle='--', alpha=0.6)

    # 막대 위에 값 표시
    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f'{height:,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, rotation=30)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig2)

    # 전체 자치구 순위 표
    with st.expander("📋 전체 자치구 순위 데이터 표 보기"):
        display_rank_df = result_df.copy()
        display_rank_df.index = display_rank_df.index + 1
        display_rank_df['인구수(명)'] = display_rank_df['인구수'].apply(lambda x: f'{x:,}')
        st.dataframe(display_rank_df[['행정구', '인구수(명)']], use_container_width=True)
