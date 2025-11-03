import streamlit as st
from PIL import Image
import time
import random
import io
# from fpdf import FPDF # fpdf 라이브러리는 한글 지원 문제로 주석 처리하거나 제거합니다.

# 페이지 설정
st.set_page_config(page_title="AI 치매 예측 시스템", page_icon="🧠", layout="centered")

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "info"
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# --- 사이드바 (Admin Access) ---
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

    # Admin 전용 페이지 이동 기능은 원본 코드에서 유지
    if st.session_state.is_admin:
        st.markdown("### 페이지 이동")
        target = st.selectbox(
            "바로 이동",
            ["info", "upload", "analysis", "result"],
            format_func=lambda x: {
                "info": "1. 환자 정보",
                "upload": "2. MRI 업로드",
                "analysis": "3. 분석 진행",
                "result": "4. 결과",
            }[x],
        )
        if st.button("이동 ▶"):
            st.session_state.page = target
            st.rerun()
    else:
        st.caption("admin 전용 기능입니다.")

# --- 1. 환자 정보 입력 페이지 (info) ---
if st.session_state.page == "info":
    st.title("🧍‍♀️ 환자 인적사항 입력")
    # 이름, 나이, 키, 몸무게, 성별은 필수 입력
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
        # 필수 입력값 검사
        if not name or age == 0 or height == 0 or weight == 0 or not gender:
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

# --- 2. MRI 이미지 업로드 페이지 (upload) ---
elif st.session_state.page == "upload":
    st.title("🧠 MRI 이미지 업로드")
    st.write(f"**{st.session_state.get('patient_info', {}).get('이름', '환자')}**님의 MRI 이미지를 분석합니다.")
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

# --- 3. 분석 진행 페이지 (analysis) ---
elif st.session_state.page == "analysis":
    st.title("🔍 AI 분석 중입니다...")
    with st.spinner("AI가 분석을 진행하고 있습니다. 잠시만 기다려주세요. (약 3초 소요)"):
        time.sleep(3)
        
    # 랜덤 결과 생성 (원본 코드 유지)
    result = random.choice(["정상","치매 가능성 있음"])
    severity = None
    if result == "정상":
        label = "NonDemented (정상)"
    else:
        severity_en = random.choice(["VeryMildDemented","MildDemented","ModerateDemented"])
        severity_ko = {"VeryMildDemented":"매우 경증", "MildDemented":"경증", "ModerateDemented":"중등도"}.get(severity_en, "알 수 없음")
        label = f"{severity_en} ({severity_ko})"
        severity = severity_ko # 중증도는 한글로 저장
        
    st.session_state.analysis_result = {
        "예측 결과": label,
        "치매 여부": result,
        "중증도": severity,
    }
    
    st.session_state.page = "result"
    st.rerun()

# --- 4. 결과 페이지 (result) ---
elif st.session_state.page == "result":
    info = st.session_state.get("patient_info",{})
    analysis = st.session_state.get("analysis_result",{})
    
    st.title("🩺 AI 치매 예측 보고서")
    
    # 약물 추천 로직 (원본 코드 유지)
    diseases = info.get("기저질환",[])
    if analysis.get("치매 여부") == "치매 가능성 있음":
        all_drugs = ["도네페질(Donepezil)","리바스티그민(Rivastigmin)","갈란타민(Galantamin)","메만틴(Memantin)"]
        contraindicated = []
        if "간질환(간경화 등)" in diseases:
            contraindicated.append("도네페질(Donepezil)")
        if "심장질환" in diseases:
            contraindicated.append("리바스티그민(Rivastigmin)")
        if "고혈압" in diseases:
            contraindicated.append("메만틴(Memantin)")
            
        recommended = [drug for drug in all_drugs if drug not in contraindicated]
        recommended_drugs = ", ".join(recommended) if recommended else "※ 기저질환으로 인해 권장 약물 없음. 전문의와 상의하십시오."
    else:
        recommended_drugs = "정상으로 판정되어 약물 치료 불필요"

    # --- 약국/병원 진단서 형식 HTML/CSS 적용 ---
    result_color = "red" if analysis.get("치매 여부") == "치매 가능성 있음" else "green"
    
    report_data = {
        "이름": info.get('이름','-'),
        "나이": f"{info.get('나이','-')} 세",
        "성별": info.get('성별','-'),
        "신체정보": f"{info.get('키','-')} cm / {info.get('몸무게','-')} kg",
        "기저질환": (', '.join(info.get('기저질환',[])) if info.get('기저질환') else '없음'),
        "AI 예측 결과": f"<span style='font-weight:bold; color:{result_color};'>{analysis.get('치매 여부','-')}</span>",
        "상세 중증도": analysis.get('예측 결과','-'),
        "권장 약물": recommended_drugs,
    }

    # 진단서 스타일 HTML
    diagnosis_html = f"""
    <style>
    .diagnosis-box {{
        border: 2px solid #333;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 8px;
        background-color: #ffffff;
    }}
    .diagnosis-header {{
        text-align: center;
        border-bottom: 2px solid #ddd;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }}
    .diagnosis-header h3 {{
        margin: 0;
        color: #1E90FF; /* 포인트 색상 */
    }}
    .diagnosis-table {{
        width: 100%;
        border-collapse: collapse;
    }}
    .diagnosis-table th, .diagnosis-table td {{
        border: 1px solid #eee;
        padding: 10px;
        text-align: left;
        font-size: 15px;
    }}
    .diagnosis-table th {{
        background-color: #f8f8f8;
        width: 30%;
        font-weight: bold;
        color: #333;
    }}
    .important-result td {{
        background-color: #fffacd; /* Light Yellow */
        font-size: 16px;
    }}
    </style>
    <div class="diagnosis-box">
        <div class="diagnosis-header">
            <h3>AI 치매 예측 결과 보고서</h3>
            <p style="font-size: 12px; color: #555;">(본 보고서는 의료 진단을 대체할 수 없습니다.)</p>
        </div>
        <table class="diagnosis-table">
            <tr><th>환자 이름</th><td>{report_data['이름']}</td></tr>
            <tr><th>나이 / 성별</th><td>{report_data['나이']} / {report_data['성별']}</td></tr>
            <tr><th>키 / 몸무게</th><td>{report_data['신체정보']}</td></tr>
            <tr><th>기저질환</th><td>{report_data['기저질환']}</td></tr>
            <tr class="important-result"><th>AI 분석 진단</th><td>{report_data['AI 예측 결과']}</td></tr>
            <tr><th>상세 분류</th><td>{report_data['상세 중증도']}</td></tr>
            <tr><th>권장 약물 가이드</th><td>{report_data['권장 약물']}</td></tr>
        </table>
    </div>
    """
    
    st.markdown(diagnosis_html, unsafe_allow_html=True)
    st.divider()

    # --- 텍스트 보고서 다운로드 (fpdf 에러 회피) ---
    report_text = f"""
    [AI 치매 예측 보고서 - {report_data['이름']} ({time.strftime('%Y-%m-%d')})]
    
    1. 환자 기본 정보
    --------------------------------------------------
    이름: {report_data['이름']}
    나이: {report_data['나이']}
    성별: {report_data['성별']}
    키/몸무게: {report_data['신체정보']}
    기저질환: {report_data['기저질환']}
    
    2. AI 분석 결과
    --------------------------------------------------
    최종 치매 여부: {analysis.get('치매 여부','-')}
    상세 중증도: {analysis.get('예측 결과','-')}
    
    3. 약물 권장 가이드
    --------------------------------------------------
    {report_data['권장 약물']}
    
    (본 보고서는 AI 분석 결과이며, 최종적인 의료 판단은 전문의에게 받아야 합니다.)
    """

    st.download_button(
        label="📄 텍스트 보고서 저장", # PDF 오류 방지를 위해 텍스트로 저장하도록 변경
        data=report_text.encode('utf-8'),
        file_name=f"{info.get('이름', '환자')}_AI_치매_예측_보고서.txt",
        mime="text/plain"
    )

    # 처음으로 돌아가기 버튼
    st.button("🔁 처음으로 돌아가기", on_click=lambda: st.session_state.update({"page":"info"}))