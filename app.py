import streamlit as st
from PIL import Image
import time
import random


st.set_page_config(page_title="AI 치매 예측 시스템", page_icon="🧠", layout="centered")


if "page" not in st.session_state:
    st.session_state.page = "info"

 
if st.session_state.page == "info":
    st.title("🧍‍♀️ 환자 인적사항 입력")

    name = st.text_input("이름")
    age = st.number_input("나이", min_value=0, max_value=120, step=1)
    height = st.number_input("키 (cm)", min_value=0, max_value=250, step=1)
    weight = st.number_input("몸무게 (kg)", min_value=0, max_value=200, step=1)

    st.subheader("🩺 기저질환 선택")
    disease_list = ["고혈압", "당뇨", "심장질환", "치매 가족력"]
    diseases = st.multiselect("해당되는 항목을 모두 선택하세요", disease_list)
    etc = st.text_input("기타 질환 (직접 입력)")

    next_button = st.button("다음으로 ➡️")

    if next_button:
        st.session_state.patient_info = {
            "이름": name,
            "나이": age,
            "키": height,
            "몸무게": weight,
            "기저질환": diseases,
            "기타": etc,
        }
        st.session_state.page = "upload"
        st.rerun()

# 2️⃣ MRI 업로드 페이지
elif st.session_state.page == "upload":
    st.title("🧠 MRI 이미지 업로드")
    st.write("환자 정보를 바탕으로 MRI 이미지를 분석합니다.")
    uploaded_file = st.file_uploader("MRI 이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 MRI 이미지", use_container_width=True)
        analyze_button = st.button("AI 분석 시작")

        if analyze_button:
            st.session_state.image = image
            st.session_state.page = "analysis"
            st.rerun()
    else:
        st.warning("⚠️ MRI 이미지를 업로드해주세요.")

# 3️⃣ AI 분석 페이지
elif st.session_state.page == "analysis":
    st.title("🔍 AI 분석 중입니다...")

    with st.spinner("AI가 분석을 진행하고 있습니다. 잠시만 기다려주세요."):
        time.sleep(3)

# 임의 결과 (예시)
    result = random.choice(["정상 뇌로 판단됩니다.", "치매 가능성이 있습니다."])

    st.success("AI 분석이 완료되었습니다 ✅")
    st.subheader(f"🧩 예측 결과: **{result}**")
    st.info("⚠️ 이 결과는 예시이며, 실제 의료 판단이 아닙니다.")
    st.button("🔁 처음으로 돌아가기", on_click=lambda: st.session_state.update(page="info"))