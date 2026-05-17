import pandas as pd  # 데이터 처리를 위한 판다스 라이브러리를 불러옵니다.
import plotly.express as px  # 예쁜 시각화를 위한 플롯리 라이브러리를 불러옵니다.
import streamlit as st  # 웹 앱 구성을 위한 스트림릿 라이브러리를 불러옵니다.

st.set_page_config(page_title="학생 성적 대시보드", layout="wide")  # 웹 페이지의 타이틀을 설정하고 와이드 레이아웃을 적용합니다.
st.title("📊 학생 성적 분석 대시보드")  # 대시보드 화면 맨 위에 메인 타이틀을 출력합니다.
st.markdown("### 📅 CSV 파일을 업로드하면 과목별 평균 점수를 자동으로 계산하여 시각화합니다.")  # 앱의 목적을 설명하는 서브 타이틀을 마크다운으로 출력합니다.

uploaded_file = st.file_uploader("학생 성적 CSV 파일을 선택해주세요.", type=["csv"])  # 사용자가 CSV 파일을 드래그하거나 선택하여 파일업로드할 수 있는 공간을 만듭니다.

if uploaded_file is not None:  # 업로드된 파일이 존재할 경우에만 이하의 분석 코드를 작동시킵니다.
    df = pd.read_csv(uploaded_file)  # 업로드된 CSV 데이터를 판다스 데이터프레임 형태로 읽어와 변수에 저장합니다.
    
    st.subheader("📋 업로드된 원본 성적 데이터 확인")  # 데이터 확인용 섹션의 제목을 화면에 표시합니다.
    st.dataframe(df, use_container_width=True)  # 가져온 성적 전체 데이터를 표 형태로 화면 너비에 맞춰 시각적으로 보여줍니다.
    
    numeric_df = df.select_dtypes(include=['number'])  # 이름이나 학번 같은 문자열 열을 자동으로 제외하고 성적 점수가 적힌 숫자형 열만 필터링합니다.
    
    if not numeric_df.empty:  # 점수 데이터(숫자형 열)가 정상적으로 존재한다면 과목별 평균 계산 및 시각화를 시작합니다.
        subject_means = numeric_df.mean().reset_index()  # 모든 숫자형 과목 열의 평균을 계산하고 구조를 다듬어 새로운 데이터프레임으로 바꿉니다.
        subject_means.columns = ['과목', '평균점수']  # 그래프를 그리기 편하도록 컬럼명을 각각 '과목'과 '평균점수'로 명확하게 일괄 수정합니다.
        
        st.subheader("📈 과목별 평균 점수 시각화 차트")  # 시각화 그래프 결과 섹션의 서브 타이틀을 생성합니다.
        
        fig = px.bar(subject_means, x='과목', y='평균점수', text='평균점수', color='평균점수', color_continuous_scale='Viridis')  # 플롯리를 사용해 과목별 평균 점수를 다채로운 막대 그래프로 빌드합니다.
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')  # 막대 상단에 표기되는 점수 수치를 소수점 둘째 자리까지 지정하고 막대 바깥에 배치합니다.
        fig.update_layout(xaxis_title="시험 과목", yaxis_title="평균 점수 (점)", plot_bgcolor="rgba(0,0,0,0)")  # 가독성을 위해 축 제목을 달아주고 그래프의 회색 배경을 투명하게 청소합니다.
        
        st.plotly_chart(fig, use_container_width=True)  # 완성된 Plotly 막대 그래프 차트 객체를 스트림릿 화면 크기에 맞춰 동적으로 렌더링합니다.
        
    else:  # 만약 업로드한 CSV 파일 내에 숫자로 된 성적 데이터가 단 하나도 포함되어 있지 않은 경우 실행됩니다.
        st.error("업로드된 파일에서 계산 가능한 숫자형 데이터(점수)를 찾을 수 없습니다. 파일을 다시 확인해주세요.")  # 직관적인 빨간색 에러 메시지 박스를 출력하여 사용자에게 경고를 전달합니다.