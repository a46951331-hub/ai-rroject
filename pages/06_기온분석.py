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
    else:  # Linux / Streamlit Cloud
        font_list = [f.name for f in fm.fontManager.ttflist]
        if 'NanumGothic' in font_list:
            plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# 2. 데이터 불러오기 및 전처리
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='utf-8')
        
    df.columns = [c.strip() for c in df.columns]
    
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    df['월'] = df['일시'].str.split('-').str[0].map(month_map)
    yr_2d = df['일시'].str.split('-').str[1].astype(int)
    
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

st.title("🌡️ 서울 기온 데이터 다각도 분석")
df = load_data("tempert.csv")

# 유효한 데이터가 존재하는 연도 목록 추출
valid_years = sorted(df.dropna(subset=['평균기온(℃)'])['연도'].unique())

# 4개 기능을 탭으로 구분
tab1, tab2, tab3, tab4 = st.tabs([
    "1. 월 선택 (연도별 추이)",
    "2. 1~12월 전체 평균기온",
    "3. 연도 1개 선택 (최고/최저)",
    "4. 연도 2개 선택 (비교)"
])

# ---------------------------------------------------------
# [탭 1] 기존 기능: 월 선택 시 연도별 최고/최저기온
# ---------------------------------------------------------
with tab1:
    st.subheader("선택한 월의 연도별 최고·최저기온 추이")
    selected_month = st.selectbox(
        "분석할 월을 선택하세요:",
        options=list(range(1, 13)),
        format_func=lambda x: f"{x}월",
        key="tab1_month"
    )
    filtered_month_df = df[df['월'] == selected_month].dropna(subset=['최고기온(℃)', '최저기온(℃)'])

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(filtered_month_df['연도'], filtered_month_df['최고기온(℃)'], color='red', marker='o', markersize=4, label='최고기온')
    ax1.plot(filtered_month_df['연도'], filtered_month_df['최저기온(℃)'], color='blue', marker='o', markersize=4, label='최저기온')
    
    ax1.set_title("월별 기온분삭", fontsize=16, fontweight='bold', pad=15)
    ax1.set_xlabel("연도", fontsize=12)
    ax1.set_ylabel("온도", fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig1)

# ---------------------------------------------------------
# [탭 2] 추가 1: 가로축 1~12월 서울의 월별 평균기온 그래프
# ---------------------------------------------------------
with tab2:
    st.subheader("서울의 월별 평균기온 (1907~2026년 전체 평균)")
    monthly_avg = df.groupby('월')['평균기온(℃)'].mean().reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(monthly_avg['월'], monthly_avg['평균기온(℃)'], color='green', marker='o', linewidth=2, label='평균기온')
    
    # 각 포인트 위에 기온 수치 표시
    for _, row in monthly_avg.iterrows():
        ax2.annotate(f"{row['평균기온(℃)']:.1f}℃", (row['월'], row['평균기온(℃)']),
                     textcoords="offset points", xytext=(0, 8), ha='center', fontsize=9)

    ax2.set_title("서울의 월별 평균기온 (1월~12월)", fontsize=16, fontweight='bold', pad=15)
    ax2.set_xlabel("월", fontsize=12)
    ax2.set_ylabel("평균기온 (℃)", fontsize=12)
    ax2.set_xticks(range(1, 13))
    ax2.set_xticklabels([f"{m}월" for m in range(1, 13)])
    ax2.set_ylim(monthly_avg['평균기온(℃)'].min() - 5, monthly_avg['평균기온(℃)'].max() + 5)
    ax2.legend(loc='best')
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)

# ---------------------------------------------------------
# [탭 3] 추가 2: 연도 1개 선택 시 해당 연도의 최고기온과 최저기온
# ---------------------------------------------------------
with tab3:
    st.subheader("선택한 연도의 월별 최고기온 및 최저기온")
    selected_year = st.selectbox(
        "연도를 선택하세요:",
        options=valid_years,
        index=len(valid_years) - 2,  # 기본값: 최근 온전한 연도(2025년)
        key="tab3_year"
    )
    year_df = df[df['연도'] == selected_year].sort_values('월')

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(year_df['월'], year_df['최고기온(℃)'], color='red', marker='o', linewidth=2, label='최고기온')
    ax3.plot(year_df['월'], year_df['최저기온(℃)'], color='blue', marker='o', linewidth=2, label='최저기온')

    ax3.set_title(f"{selected_year}년 월별 최고·최저기온", fontsize=16, fontweight='bold', pad=15)
    ax3.set_xlabel("월", fontsize=12)
    ax3.set_ylabel("온도 (℃)", fontsize=12)
    ax3.set_xticks(range(1, 13))
    ax3.set_xticklabels([f"{m}월" for m in range(1, 13)])
    ax3.legend(loc='best')
    ax3.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig3)

# ---------------------------------------------------------
# [탭 4] 추가 3: 연도 2개 선택 시 2개 연도의 비교 그래프
# ---------------------------------------------------------
with tab4:
    st.subheader("두 연도의 월별 기온 비교")
    col1, col2, col3 = st.columns([1, 1, 1.2])
    with col1:
        year1 = st.selectbox("첫 번째 연도:", options=valid_years, index=0, key="tab4_y1")  # 기본값: 1907/1908
    with col2:
        year2 = st.selectbox("두 번째 연도:", options=valid_years, index=len(valid_years) - 2, key="tab4_y2")  # 기본값: 2025
    with col3:
        metric = st.selectbox(
            "비교할 기온 항목:",
            options=['평균기온(℃)', '최고기온(℃)', '최저기온(℃)'],
            key="tab4_metric"
        )

    df_y1 = df[df['연도'] == year1].sort_values('월')
    df_y2 = df[df['연도'] == year2].sort_values('월')

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.plot(df_y1['월'], df_y1[metric], color='royalblue', marker='o', linewidth=2, label=f"{year1}년 {metric}")
    ax4.plot(df_y2['월'], df_y2[metric], color='crimson', marker='s', linewidth=2, label=f"{year2}년 {metric}")

    ax4.set_title(f"{year1}년 vs {year2}년 월별 {metric} 비교", fontsize=16, fontweight='bold', pad=15)
    ax4.set_xlabel("월", fontsize=12)
    ax4.set_ylabel("온도 (℃)", fontsize=12)
    ax4.set_xticks(range(1, 13))
    ax4.set_xticklabels([f"{m}월" for m in range(1, 13)])
    ax4.legend(loc='best')
    ax4.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig4)
