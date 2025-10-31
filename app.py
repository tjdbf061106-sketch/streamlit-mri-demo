import streamlit as st
from PIL import Image
import time

# 페이지 설정
st.set_page_config(page_title="CT/MRI 분석 데모", page_icon="🧠", layout="centered")

st.title("🧠 뇌 CT/MRI 이미지 업로드 페이지")
st.write("환자의 뇌 CT/MRI 이미지를 업로드하고 '분석하기' 버튼을 눌러주세요.")

# --- 1. 이미지 업로드 영역 ---
uploaded_file = st.file_uploader("환자의 뇌 CT/MRI 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

# 업로드된 이미지가 있을 경우 (File is present)
if uploaded_file is not None:
    try:
        # 이미지를 열어 화면에 표시
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 CT/MRI 이미지", use_container_width=True)
        
        # --- 2. 분석 버튼 (ONLY appears after upload) ---
        if st.button("분석하기"):
            # --- 3. 분석 중 로딩 메시지 ---
            # 실제 백엔드 연동 전, 로딩 스피너만 보여줍니다.
            with st.spinner("🔍 AI가 CT/MRI를 분석 중입니다..."):
                time.sleep(2) # 2초 동안 로딩을 시뮬레이션
            
            # 분석이 완료되었음을 알리는 메시지 (실제 결과는 백엔드 연동 후 추가)
            st.success("✅ 분석을 완료되었습니다. (추후 추가)")

    except Exception as e:
        # 파일 열기 오류 처리
        st.error(f"이미지를 처리하는 중 오류가 발생했습니다: {e}")

# 업로드된 이미지가 없을 경우 (File is NOT present)
else:
    # --- 4. 초기 경고 메시지 ---
    st.warning("⚠️ 아직 CT/MRI 이미지를 업로드하지 않았습니다. 이미지를 선택해주세요.")
