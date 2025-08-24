# streamlit_app.py

import streamlit as st
import requests  # 외부 API와 통신하기 위한 라이브러리

# --- 변경된 부분 1: 고양이 API 주소 변경 ---
# 기존의 'aws.random.cat/meow'가 불안정하여 새로운 API로 교체했습니다.
ANIMAL_API_URLS = {
    '강아지': 'https://random.dog/woof.json',
    '고양이': 'https://api.thecatapi.com/v1/images/search', # 새롭고 안정적인 API
    '여우': 'https://randomfox.ca/floof/'
}

# 각 API 응답에서 이미지 URL이 담긴 키의 이름이 다르므로, 이를 매핑
ANIMAL_API_KEYS = {
    '강아지': 'url',
    # 고양이 API는 응답 구조가 달라서 아래 함수에서 별도로 처리합니다.
    '여우': 'image'
}

def get_random_animal_image(animal_name):
    """
    선택된 동물의 랜덤 이미지 URL을 API를 통해 가져오는 함수.
    성공 시 이미지 URL을, 실패 시 None을 반환합니다.
    """
    api_url = ANIMAL_API_URLS.get(animal_name)
    if not api_url:
        return None

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # --- 변경된 부분 2: 새로운 고양이 API 응답 처리 로직 추가 ---
        if animal_name == '고양이':
            # 이 API는 [{ 'url': '...' }] 형태의 리스트로 응답을 줍니다.
            # 따라서 첫 번째 요소의 'url' 값을 가져와야 합니다.
            if data and isinstance(data, list):
                return data[0].get('url')
        else:
            # 강아지, 여우는 기존 방식대로 키 이름을 사용해 URL을 가져옵니다.
            key_name = ANIMAL_API_KEYS.get(animal_name)
            return data.get(key_name)

    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return None
    except (KeyError, IndexError, TypeError) as e:
        # 데이터 구조가 예상과 다를 경우의 오류 처리
        st.error(f"API 응답 데이터 처리 중 오류가 발생했습니다: {e}")
        return None

# --- Streamlit 앱 UI 구성 (이 부분은 변경 없음) ---

st.title("🐾 랜덤 동물 사진 생성기")

selected_animal = st.selectbox(
    "보고 싶은 동물을 선택하세요!",
    list(ANIMAL_API_URLS.keys())
)

if st.button("랜덤 사진 생성 ✨"):
    with st.spinner(f'{selected_animal} 사진을 불러오는 중...'):
        image_url = get_random_animal_image(selected_animal)

        if image_url:
            # 강아지 사진 중 동영상(mp4, webm) 파일은 이미지로 표시할 수 없으므로 제외
            if image_url.endswith(('.mp4', '.webm')):
                st.warning("동영상 파일이 반환되어 다른 사진을 표시합니다. 버튼을 다시 눌러주세요!")
            else:
                st.image(image_url, caption=f"짜잔! 귀여운 {selected_animal} 사진이에요!")
        else:
            st.error("사진을 불러오는 데 실패했습니다. 다시 시도해 주세요.")
            