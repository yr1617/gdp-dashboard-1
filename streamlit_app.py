# streamlit_app.py

import streamlit as st
import requests  # 외부 API와 통신하기 위한 라이브러리

# 동물 사진을 가져오는 API 엔드포인트(URL)를 딕셔너리로 관리
ANIMAL_API_URLS = {
    '강아지': 'https://random.dog/woof.json',    # 랜덤 강아지 사진 API
    '고양이': 'https://aws.random.cat/meow',    # 랜덤 고양이 사진 API. [1]
    '여우': 'https://randomfox.ca/floof/'        # 랜덤 여우 사진 API. [2]
}

# 각 API 응답에서 이미지 URL이 담긴 키의 이름이 다르므로, 이를 매핑
ANIMAL_API_KEYS = {
    '강아지': 'url',
    '고양이': 'file',
    '여우': 'image'
}

def get_random_animal_image(animal_name):
    """
    선택된 동물의 랜덤 이미지 URL을 API를 통해 가져오는 함수.
    성공 시 이미지 URL을, 실패 시 None을 반환합니다.
    """
    api_url = ANIMAL_API_URLS.get(animal_name)
    key_name = ANIMAL_API_KEYS.get(animal_name)

    if not api_url or not key_name:
        return None

    try:
        # 해당 API에 GET 요청을 보냄 (5초 타임아웃)
        response = requests.get(api_url, timeout=5)
        # 응답 상태 코드가 200 (성공)이 아니면 예외 발생
        response.raise_for_status()
        # 응답받은 JSON 데이터에서 이미지 URL을 추출
        data = response.json()
        return data.get(key_name)
    except requests.exceptions.RequestException as e:
        # 네트워크 오류나 API 서버 문제 발생 시 에러 메시지 반환
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return None


# --- Streamlit 앱 UI 구성 ---

# 1. 앱 제목 설정
st.title("🐾 랜덤 동물 사진 생성기")

# 2. 동물 선택 드롭다운 메뉴 생성
# ANIMAL_API_URLS 딕셔너리의 키들('강아지', '고양이', '여우')을 선택 옵션으로 사용
selected_animal = st.selectbox(
    "보고 싶은 동물을 선택하세요!",
    list(ANIMAL_API_URLS.keys())
)

# 3. '랜덤 사진 생성' 버튼 생성
if st.button("랜덤 사진 생성 ✨"):
    # 버튼이 클릭되면 로딩 스피너를 표시
    with st.spinner(f'{selected_animal} 사진을 불러오는 중...'):
        # 위에서 정의한 함수를 호출하여 이미지 URL을 가져옴
        image_url = get_random_animal_image(selected_animal)

        if image_url:
            # 이미지 URL을 성공적으로 가져왔다면 화면에 이미지 표시
            st.image(image_url, caption=f"짜잔! 귀여운 {selected_animal} 사진이에요!")
        else:
            # 이미지 URL을 가져오지 못했다면 에러 메시지 표시
            st.error("사진을 불러오는 데 실패했습니다. 다시 시도해 주세요.")
            