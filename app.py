import streamlit as st
from PIL import Image
import time
import random
import io
from fpdf import FPDF

st.set_page_config(page_title="AI 치매 예측 시스템", page_icon="🧠", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "info"
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

with st.sidebar:
    st.markdown("### Access")
    admin_name = st.text_input("Password", type="password")
    admin_toggle = st.checkbox("관리자 모드", value=st.session_state.is_admin)

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
    uploaded_file = st.file_uploader("MRI 이미지를 업로드하세요", type=["jpg","jpeg","png"])
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
    result = random.choice(["정상","치매 가능성 있음"])
    severity = None
    if result == "정상":
        label = "NonDemented"
    else:
        severity = random.choice(["VeryMildDemented","MildDemented","ModerateDemented"])
        label = severity
    st.session_state.analysis_result = {
        "예측 결과": label,
        "치매 여부": result,
        "중증도": severity,
    }
    st.session_state.page = "result"
    st.rerun()

elif st.session_state.page == "result":
    info = st.session_state.get("patient_info",{})
    analysis = st.session_state.get("analysis_result",{})
    st.title("🩺 AI 치매 예측 보고서")
    diseases = info.get("기저질환",[])
    if analysis.get("예측 결과") != "NonDemented":
        all_drugs = ["도네페질(Donepezil)","리바스티그민(Rivastigmine)","갈란타민(Galantamine)","메만틴(Memantine)"]
        contraindicated = []
        if "간질환(간경화 등)" in diseases:
            contraindicated.append("도네페질(Donepezil)")
        if "심장질환" in diseases:
            contraindicated.append("리바스티그민(Rivastigmine)")
        if "고혈압" in diseases:
            contraindicated.append("메만틴(Memantine)")
        recommended = [drug for drug in all_drugs if drug not in contraindicated]
        recommended_drugs = ", ".join(recommended) if recommended else "권장 약물 없음"
    else:
        recommended_drugs = "정상으로 판정되어 약물 치료 불필요"
    table_html = f"""
    <style>
    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 16px;
    }}
    th, td {{
        border: 1px solid #ddd;
        text-align: left;
        padding: 8px;
    }}
    th {{
        background-color: #f2f2f2;
        width: 25%;
    }}
    tr:nth-child(even) {{background-color: #fafafa;}}
    </style>
    <table>
        <tr><th>이름</th><td>{info.get('이름','')}</td></tr>
        <tr><th>나이</th><td>{info.get('나이','')} 세</td></tr>
        <tr><th>성별</th><td>{info.get('성별','')}</td></tr>
        <tr><th>키 / 몸무게</th><td>{info.get('키','')} cm / {info.get('몸무게','')} kg</td></tr>
        <tr><th>기저질환</th><td>{', '.join(info.get('기저질환',[])) if info.get('기저질환') else '없음'}</td></tr>
        <tr><th>치매 여부</th><td>{analysis.get('치매 여부','')}</td></tr>
        <tr><th>중증도</th><td>{analysis.get('예측 결과','')}</td></tr>
        <tr><th>추천 약물</th><td>{recommended_drugs}</td></tr>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    st.divider()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"🩺 AI 치매 예측 보고서",ln=True,align="C")
    pdf.ln(10)

    col_width = 60
    row_height = 10
    pdf.set_font("Arial","B",12)
    fields = [("이름",info.get("이름","")),("나이",f"{info.get('나이','')} 세"),("성별",info.get("성별","")),
              ("키 / 몸무게",f"{info.get('키','')} cm / {info.get('몸무게','')} kg"),
              ("기저질환",', '.join(info.get("기저질환",[])) if info.get("기저질환") else "없음"),
              ("치매 여부",analysis.get("치매 여부","")),
              ("중증도",analysis.get("예측 결과","")),
              ("추천 약물",recommended_drugs)]
    for k,v in fields:
        pdf.set_fill_color(240,240,240)
        pdf.cell(col_width,row_height,f"{k}",border=1,fill=True)
        pdf.set_font("Arial","",12)
        pdf.cell(0,row_height,str(v),border=1,ln=True)
        pdf.set_font("Arial","B",12)

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="📄 PDF로 저장",
        data=pdf_buffer.getvalue(),
        file_name="AI_치매_예측_보고서.pdf",
        mime="application/pdf"
    )

    st.button("🔁 처음으로 돌아가기", on_click=lambda: st.session_state.update({"page":"info"}))
