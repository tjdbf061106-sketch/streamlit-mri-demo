import streamlit as st
from PIL import Image
import time
import random

st.set_page_config(page_title="AI 치매 예측 시스템", page_icon="🧠", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "info"
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

with st.sidebar:
    st.markdown("### Access")
    admin_name = st.text_input("Password", type="password")
    admin_toggle = st.toggle("관리자 모드", value=st.session_state.is_admin)

    if admin_toggle:
        if admin_name.strip().lower() == "admin":
            st.session_state.is_admin = True
            st.success("admin ON")
        elif admin_name != "":
            st.error("비밀번호가 틀렸습니다.")
    else:
        st.session_state.is_admin = False
        st.info("admin OFF")

    st.divider()

    if st.session_state.is_admin:
        st.markdown("### 페이지 이동")
        target = st.selectbox(
            "바로 이동",
            ["info", "upload", "analysis", "result", "admin"],
            format_func=lambda x: {
                "info": "1. 환자 정보",
                "upload": "2. MRI 업로드",
                "analysis": "3. 분석 진행",
                "result": "4. 결과",
                "admin": "*관리자 대시보드*",
            }[x],
        )
        if st.button("이동 ▶"):
            st.session_state.page = target
            st.rerun()

        if st.button("관리자 대시보드 열기"):
            st.session_state.page = "admin"
            st.rerun()
    else:
        st.caption("admin 전용 기능입니다.")

if st.session_state.page == "info":
    st.title("🧍‍♀️ 환자 인적사항 입력")

    name = st.text_input("이름 *")
    age = st.number_input("나이 *", min_value=0, max_value=120, step=1)
    height = st.number_input("키 (cm) *", min_value=0, max_value=250, step=1)
    weight = st.number_input("몸무게 (kg) *", min_value=0, max_value=200, step=1)
    gender = st.radio("성별 *", ["남자", "여자"])

    st.subheader("🩺 기저질환 선택")
    disease_list = ["고혈압", "당뇨", "심장질환", "간질환(간경화 등)"]
    diseases = st.multiselect("해당되는 항목을 모두 선택하세요", disease_list)

    next_button = st.button("다음으로 ➡️")

    if next_button:
        master_key = name.strip().lower() == "admin"
        if not master_key and (not name or age == 0 or height == 0 or weight == 0 or not gender):
            st.warning("⚠️ 이름, 나이, 키, 몸무게, 성별을 모두 입력해주세요.")
        else:
            st.session_state.patient_info = {
                "이름": name,
                "나이": age,
                "키": height,
                "몸무게": weight,
                "성별": gender,
                "기저질환": diseases,
            }
            st.session_state.page = "upload"
            st.rerun()

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

elif st.session_state.page == "analysis":
    st.title("🔍 AI 분석 중입니다...")

    with st.spinner("AI가 분석을 진행하고 있습니다. 잠시만 기다려주세요."):
        time.sleep(3)

    result = random.choice(["정상 뇌로 판단됩니다.", "치매 가능성이 있습니다."])

    st.success("AI 분석이 완료되었습니다 ✅")
    st.subheader(f"🧩 예측 결과: **{result}**")
    st.info("⚠️ 이 결과는 예시이며, 실제 의료 판단이 아닙니다.")
    st.button("🔁 처음으로 돌아가기", on_click=lambda: st.session_state.update(page="info"))