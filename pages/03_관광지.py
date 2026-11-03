import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="북한 주요 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인이 좋아하는 북한 주요 관광지 TOP 10")
st.write("지도 위 마커를 클릭하여 위치를 확인하고, 아래에서 상세 설명과 1박 2일 추천 일정을 확인해보세요.")

# 북한 주요 관광지 TOP 10 데이터 (평양 및 주요 지역)
nk_spots = [
    {
        "rank": 1,
        "name": "주체사상탑 (평양)",
        "lat": 39.0179,
        "lon": 125.7634,
        "desc": "대동강변에 위치한 170m 높이의 탑으로, 평양 시내 전경을 한눈에 바라볼 수 있는 대표적인 랜드마크입니다.",
        "color": "red"
    },
    {
        "rank": 2,
        "name": "김일성광장 (평양)",
        "lat": 39.0194,
        "lon": 125.7539,
        "desc": "세계에서 손꼽히는 대형 광장으로, 주요 국가 행사와 군사 퍼레이드가 열리는 핵심 장소입니다.",
        "color": "blue"
    },
    {
        "rank": 3,
        "name": "평양 지하철도 (평양)",
        "lat": 39.0205,
        "lon": 125.7335,
        "desc": "지하 100m 깊이에 조성된 지하철로, 화려한 샹들리에와 벽화 등 웅장한 내부 인테리어가 외국인들에게 유명합니다.",
        "color": "green"
    },
    {
        "rank": 4,
        "name": "개성 한옥마을 및 선죽교 (개성)",
        "lat": 37.9744,
        "lon": 126.5590,
        "desc": "고려 시대의 역사 유적이 잘 보존된 구시가지로, 전통 한옥 숙박 체험이 가능한 곳입니다.",
        "color": "purple"
    },
    {
        "rank": 5,
        "name": "판문점 / DMZ (개성/파주 경계)",
        "lat": 37.9560,
        "lon": 126.6773,
        "desc": "한반도 분단의 역사적 현장을 직접 볼 수 있어 해외 안보 관광객들에게 관심이 높은 명소입니다.",
        "color": "darkred"
    },
    {
        "rank": 6,
        "name": "금강산 (강원도 고성)",
        "lat": 38.6534,
        "lon": 128.1065,
        "desc": "기암괴석과 빼어난 자연경관을 자랑하는 한반도의 명산으로, 구룡폭포와 만물상이 유명합니다.",
        "color": "orange"
    },
    {
        "rank": 7,
        "name": "묘향산 & 국제친선전람관 (평안북도)",
        "lat": 40.0031,
        "lon": 126.2114,
        "desc": "수려한 산세와 더불어 각국 정상들에게 받은 선물들을 전시해 놓은 대규모 전람관이 위치해 있습니다.",
        "color": "cadetblue"
    },
    {
        "rank": 8,
        "name": "백두산 천지 (량강도 삼지연)",
        "lat": 41.9944,
        "lon": 128.0772,
        "desc": "한반도에서 가장 높은 산이자 화산호수인 '천지'의 장엄한 풍경을 관람할 수 있는 명승지입니다.",
        "color": "darkgreen"
    },
    {
        "rank": 9,
        "name": "평양 개선문 (평양)",
        "lat": 39.0436,
        "lon": 125.7533,
        "desc": "파리의 개선문보다 높게 설계된 대형 석조 건축물로, 모란봉 구역 인근에 위치해 있습니다.",
        "color": "pink"
    },
    {
        "rank": 10,
        "name": "마식령 스키장 (강원도 원산)",
        "lat": 39.0645,
        "lon": 127.3015,
        "desc": "현대적인 리조트 시설과 슬로프를 갖춘 대규모 스키장으로, 겨울철 스포츠 관광지로 알려져 있습니다.",
        "color": "lightblue"
    }
]

# 1. 지도 생성 (평양 중심으로 배치)
m = folium.Map(location=[39.02, 125.75], zoom_start=8)

for spot in nk_spots:
    popup_text = f"<b>{spot['rank']}. {spot['name']}</b>"
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(popup_text, max_width=200),
        tooltip=f"{spot['rank']}. {spot['name']}",
        icon=folium.Icon(color=spot["color"], icon="info-sign")
    ).add_to(m)

# 2. 지도 출력
st.subheader("📍 북한 관광 명소 지도")
st_folium(m, width="100%", height=500)

st.markdown("---")

# 3. 상세 설명 출력
st.subheader("📜 주요 관광지 상세 설명")
col1, col2 = st.columns(2)

for i, spot in enumerate(nk_spots):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"### {spot['rank']}. {spot['name']}")
        st.write(spot['desc'])
        st.write("")

st.markdown("---")

# 4. 1박 2일 추천 투어 일정
st.subheader("🗓️ 평양-개성 핵심 1박 2일 추천 투어 코스")

col_day1, col_day2 = st.columns(2)

with col_day1:
    st.info("### 1일차: 평양 상징 및 도심 투어")
    st.markdown("""
    * **오전**: 평양 지하철도 체험 및 개선문 방문
    * **점심**: 평양옥류관 냉면 시식
    * **오후**: 김일성광장 산책 및 주체사상탑 전망대 관람
    * **저녁**: 대동강 유람선 식사 및 평양 야경 감상
    """)

with col_day2:
    st.success("### 2일차: 개성 역사 유적 및 DMZ 탐방")
    st.markdown("""
    * **오전**: 개성 이동 (차량 이용) 및 선죽교, 고려성균관 방문
    * **점심**: 개성 전통 12첩 반상(개성 놋그릇 정식)
    * **오후**: 판문점 및 DMZ 현장 답사
    * **저녁**: 개성 한옥마을 산책 후 투어 종료
    """)
