# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(
    page_title="학생 성적 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("📊 학생 성적 분석 대시보드")
st.markdown("CSV 파일을 업로드하면 과목별 평균 점수를 자동으로 시각화해줘요!")

# -----------------------------
# Step 1: CSV 파일 업로드
# -----------------------------
uploaded_file = st.file_uploader(
    "성적 CSV 파일 업로드",
    type=["csv"]
)

# -----------------------------
# 파일이 업로드되었을 때 실행
# -----------------------------
if uploaded_file is not None:

    # CSV 읽기
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 업로드된 데이터")
    st.dataframe(df, use_container_width=True)

    # -----------------------------
    # Step 2: 과목별 평균 계산
    # -----------------------------
    # 숫자형 컬럼만 선택
    score_columns = df.select_dtypes(include="number").columns

    if len(score_columns) == 0:
        st.error("숫자 데이터가 포함된 과목 컬럼이 없습니다.")
    else:
        subject_means = df[score_columns].mean().reset_index()

        # 컬럼 이름 변경
        subject_means.columns = ["과목", "평균 점수"]

        st.subheader("📈 과목별 평균 점수")
        st.dataframe(subject_means, use_container_width=True)

        # -----------------------------
        # Step 3: Plotly 바 차트 시각화
        # -----------------------------
        fig = px.bar(
            subject_means,
            x="과목",
            y="평균 점수",
            text="평균 점수",
            color="평균 점수",
            color_continuous_scale="Tealgrn",
            title="과목별 평균 점수 분석"
        )

        # 차트 꾸미기
        fig.update_traces(
            texttemplate='%{text:.2f}',
            textposition='outside'
        )

        fig.update_layout(
            height=550,
            xaxis_title="과목",
            yaxis_title="평균 점수",
            title_x=0.5,
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 안내 메시지
# -----------------------------
else:
    st.info("CSV 파일을 업로드해주세요!")
