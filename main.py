import streamlit as st
st.title('동욱이는 사람이 싫어요')
a=st.text_input('이름을 입력해주세요!')
b=st.selectbox(' 좋아하는  음식을 선택해주세요',['치킨','온지음비빔밥','삼겹살])
if st.button('인사말 생성'):
st.write('반갑습니다')                                    
st.info(a+'님,안녕하세요!')
st.wearing(b+'를 좋아하시는군요!')
st.error('잘부탁드립니다!')
sr.balloons()                                    
