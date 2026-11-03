import streamlit as st
import folium
from streamlit_folium import st_folium

# 웹페이지 기본 설정
st.set_page_config(
    page_title="외국인이 좋아하는 서울 주요 관광지 TOP 10",
    page_icon="🗽",
    layout="wide"
)

st.title("🗽 외국인이 좋아하는 서울 주요 관광지 TOP 10")
st.write("지도 위의 마커를 클릭하여 위치를 확인하고, 아래에서 간략한 설명을 확인해보세요!")

# 서울 주요 관광지 TOP 10 데이터
spots = [
    {
        "rank": 1,
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선 시대의 대표적인 웅장한 법궁으로, 한복 착용 체험과 수문장 교대식이 외국인 관광객들에게 큰 인기를 끌고 있습니다.",
        "icon_color": "red"
    },
    {
        "rank": 2,
        "name": "N서울타워 (남산타워)",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울 도심 전경을 360도로 한눈에 조망할 수 있는 랜드마크로, 사랑의 자물쇠 명소이자 밤 야경이 매우 아름다운 곳입니다.",
        "icon_color": "blue"
    },
    {
        "rank": 3,
        "name": "명동 거리",
        "lat": 37.5636,
        "lon": 126.9856,
        "desc": "K-뷰티 쇼핑몰과 화려한 길거리 음식이 모여있는 쇼핑과 식도락의 천국입니다.",
        "icon_color": "green"
    },
    {
        "rank": 4,
        "name": "북촌한옥마을",
        "lat": 37.5826,
        "lon": 126.9837,
        "desc": "전통 한옥이 잘 보존된 골목길로, 고즈넉한 한국 고유의 미와 서울 도심 전경을 함께 즐길 수 있습니다.",
        "icon_color": "purple"
    },
    {
        "rank": 5,
        "name": "동대문디자인플라자 (DDP)",
        "lat": 37.5665,
        "lon": 127.0092,
        "desc": "세계적인 건축가 자하 하디드가 설계한 곡선 형태의 미래지향적 건축물로, 패션 행사 및 문화 전시가 매일 열립니다.",
        "icon_color": "orange"
    },
    {
        "rank": 6,
        "name": "홍대 거리",
        "lat": 37.5563,
        "lon": 126.9226,
        "desc": "젊음과 버스킹 공연, 독특한 인디 문화 및 클럽, 감성 카페가 유기적으로 얽혀있는 역동적인 거리입니다.",
        "icon_color": "darkred"
    },
    {
        "rank": 7,
        "name": "롯데월드타워 & 서울스카이",
        "lat": 37.5126,
        "lon": 127.1025,
        "desc": "세계 5위 높이(555m)의 초고층 마천루로, 초고속 엘리베이터와 스카이데크에서 스릴과 야경을 모두 체험할 수 있습니다.",
        "icon_color": "cadetblue"
    },
    {
        "rank": 8,
        "name": "광장시장",
        "lat": 37.5701,
        "lon": 126.9997,
        "desc": "마약김밥, 빈대떡, 육회 등 전통 한국 재래시장의 먹거리를 있는 그대로 경험할 수 있는 K-푸드 핫플레이스입니다.",
        "icon_color": "darkgreen"
    },
    {
        "rank": 9,
        "name": "이태원 & 해방촌",
        "lat": 37.5345,
        "lon": 126.9946,
        "desc": "다양한 국적의 문화와 세계 각국의 다채로운 음식점, 루프탑 바가 모여있는 국제적인 거리입니다.",
        "icon_color": "pink"
    },
    {
        "rank": 10,
        "name": "반포한강공원 (무지개분수)",
        "lat": 37.5098,
        "lon": 126.9950,
        "desc": "한강변에서 '한강 라면'과 피크닉을 즐기거나, 세계 최장 교량 분수인 달빛무지개분수를 관람할 수 있는 휴식 명소입니다.",
        "icon_color": "lightblue"
    }
]

# 1. 서울 지도 생성 (서울 중심 좌표)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 지도에 관광지 10곳 마커 추가
for spot in spots:
    popup_text = f"<b>{spot['rank']}. {spot['name']}</b>"
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(popup_text, max_width=200),
        tooltip=f"{spot['rank']}. {spot['name']}",
        icon=folium.Icon(color=spot["icon_color"], icon="info-sign")
    ).add_to(m)

# 2. 지도 화면 출력
st.subheader("📍 서울 주요 관광지 지도")
st_folium(m, width="100%", height=500)

st.markdown("---")

# 3. 지도 밑 관광지 상세 설명 출력
st.subheader("📜 관광지 상세 설명")

# 2열(Column) 레이아웃으로 보기 쉽게 정리
col1, col2 = st.columns(2)

for i, spot in enumerate(spots):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"### {spot['rank']}. {spot['name']}")
        st.write(spot['desc'])
        st.write("")
