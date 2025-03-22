
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="눈 건강 시각화",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("👁️ 눈 건강 측정 데이터 시각화")

uploaded_file = st.file_uploader("📤 엑셀 파일을 업로드하세요", type=["xlsx"])

def evaluate_eye_health(blinks, distance):
    blink_status = "✅ 적정" if 15 <= blinks <= 20 else "🟠 부족" if blinks < 15 else "🔴 과다"
    distance_status = "✅ 적정" if 50 <= distance <= 70 else "🟠 가까움" if distance < 50 else "🔴 멀음"
    return blink_status, distance_status

def generate_comment(blinks, distance):
    comment = ""
    if blinks < 15:
        comment += "눈 깜빡임이 부족합니다. 인위적으로 자주 깜빡여 주세요.\n"
    elif blinks > 20:
        comment += "눈 깜빡임이 과도합니다. 눈의 피로를 의심해 보세요.\n"
    else:
        comment += "눈 깜빡임은 적정 수준입니다.\n"

    if distance < 50:
        comment += "화면이 너무 가깝습니다. 눈과 화면 사이를 50cm 이상 유지하세요.\n"
    elif distance > 70:
        comment += "화면이 너무 멀 수 있습니다. 가독성을 확인해 주세요.\n"
    else:
        comment += "화면과의 거리는 적정합니다."
    return comment.strip()

def colorize(val):
    if isinstance(val, str):
        if "✅" in val:
            return "background-color: #d4edda; color: #155724"
        elif "🟠" in val:
            return "background-color: #fff3cd; color: #856404"
        elif "🔴" in val:
            return "background-color: #f8d7da; color: #721c24"
    return ""

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("📋 데이터 미리보기")
        st.dataframe(df)

        if "1분당 눈깜빡임 횟수" in df.columns and "화면과의 거리(cm)" in df.columns:
            blink_eval, distance_eval, comments = [], [], []
            for i, row in df.iterrows():
                blink_status, distance_status = evaluate_eye_health(row["1분당 눈깜빡임 횟수"], row["화면과의 거리(cm)"])
                comment = generate_comment(row["1분당 눈깜빡임 횟수"], row["화면과의 거리(cm)"])
                blink_eval.append(blink_status)
                distance_eval.append(distance_status)
                comments.append(comment)

            df["눈깜빡임 평가"] = blink_eval
            df["거리 평가"] = distance_eval
            df["자동 진단 멘트"] = comments

        st.subheader("🩺 건강 평가 결과")
        styled_df = df.style.applymap(colorize, subset=["눈깜빡임 평가", "거리 평가"])
        st.dataframe(styled_df, use_container_width=True)

        st.subheader("📄 자동 진단 요약")
        for i, row in df.iterrows():
            st.markdown(f"**📅 {row['측정일자']}**")
            st.info(row["자동 진단 멘트"])

        st.subheader("📈 시각화")
        selected_column = st.selectbox("시각화할 항목을 선택하세요", df.columns)
        fig = px.line(df, x=df.columns[0], y=selected_column, title=f"{selected_column} 변화 추이")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"파일을 읽는 도중 오류가 발생했습니다: {e}")
else:
    st.info("엑셀 파일을 업로드하면 결과가 여기에 표시됩니다.")
