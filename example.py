import streamlit as st  # 스트리밋 라이브러리를 불러옵니다.
import pandas as pd  # 데이터 처리를 위한 판다스 라이브러리를 불러옵니다.
import plotly.express as px  # 시각화를 위한 플롯리 익스프레스 라이브러리를 불러옵니다.

# 웹 애플리케이션의 페이지 제목, 아이콘, 레이아웃을 설정합니다.
st.set_page_config(page_title="학생 성적 대시보드", page_icon="📊", layout="centered")

# 대시보드의 메인 제목을 화면에 표시합니다.
st.title("📊 학생 성적 분석 대시보드")
# 대시보드 사용법에 대한 간단한 설명을 추가합니다.
st.markdown("학생들의 성적 CSV 파일을 업로드하면 과목별 평균을 자동으로 계산하고 예쁜 그래프로 시각화합니다.")

# 화면을 깔끔하게 분리하기 위해 구분선을 추가합니다.
st.divider()

# 사용자가 CSV 파일을 브라우저에 업로드할 수 있는 컴포넌트를 생성합니다.
uploaded_file = st.file_uploader("학생 성적 CSV 파일을 업로드해주세요. (확장자 .csv)", type=["csv"])

# 사용자가 파일을 정상적으로 업로드했을 경우 실행되는 조건문입니다.
if uploaded_file is not None:
    try:
        # 업로드된 CSV 파일을 판다스 데이터프레임 데이터 구조로 읽어옵니다.
        df = pd.read_csv(uploaded_file)
        
        # 데이터가 잘 들어왔인지 확인하기 위해 상단에 서브 제목을 표시합니다.
        st.subheader("📋 업로드된 성적 데이터 미리보기")
        # 업로드된 원본 데이터를 테이블 형태로 화면에 깔끔하게 보여줍니다.
        st.dataframe(df, use_container_width=True)
        
        # 데이터프레임에서 숫자(정수형, 실수형) 데이터가 포함된 컬럼만 자동으로 추출합니다. (과목 점수 타겟팅)
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        # 만약 파일 내에 숫자 데이터가 하나도 존재하지 않을 경우의 예외 처리입니다.
        if not numeric_cols:
            # 사용자에게 숫자 데이터가 없다는 에러 메시지를 보여줍니다.
            st.error("과목 점수(숫자 데이터)를 포함한 컬럼이 파일에 존재하지 않습니다. 확인 후 다시 시도해주세요.")
        else:
            # 추출된 숫자 컬럼(과목들)의 평균값을 계산하고 행렬 구조를 초기화(reset_index)합니다.
            df_means = df[numeric_cols].mean().reset_index()
            # 컬럼의 이름을 사용자가 보기 편하도록 '과목'과 '평균 점수'로 변경합니다.
            df_means.columns = ['과목', '평균 점수']
            # 평균 점수가 소수점이 너무 길어지지 않게 둘째 자리까지 반올림합니다.
            df_means['평균 점수'] = df_means['평균 점수'].round(2)
            
            # 시각화 섹션 구분을 위해 구분선을 다시 추가합니다.
            st.divider()
            
            # 분석 결과 요약 섹션의 서브 제목을 표시합니다.
            st.subheader("📈 과목별 평균 점수 분석 결과")
            
            # 화면을 2개의 컬럼(좌측 표, 우측 간단 정보 카드)으로 가로 분할합니다. 비율은 2:1입니다.
            col1, col2 = st.columns([2, 1])
            
            # 첫 번째 컬럼(좌측)에 들어갈 내용입니다.
            with col1:
                # 계산이 완료된 과목별 평균 점수 데이터프레임을 화면에 깔끔하게 표로 띄웁니다.
                st.dataframe(df_means, use_container_width=True)
                
            # 두 번째 컬럼(우측)에 들어갈 내용입니다.
            with col2:
                # 평균 점수가 가장 높은 과목의 행을 찾습니다.
                max_subject = df_means.loc[df_means['평균 점수'].idxmax()]
                # 평균 점수가 가장 낮은 과목의 행을 찾습니다.
                min_subject = df_means.loc[df_means['평균 점수'].idxmin()]
                # 최고 평균 과목 정보를 카드 형태로 이쁘게 화면에 띄웁니다.
                st.metric(label="최고 평균 과목", value=max_subject['과목'], delta=f"{max_subject['평균 점수']}점")
                # 최저 평균 과목 정보를 카드 형태로 이쁘게 화면에 띄웁니다.
                st.metric(label="최저 평균 과목", value=min_subject['과목'], delta=f"{min_subject['평균 점수']}점", delta_color="inverse")

            # Plotly Express를 사용하여 과목별 평균 점수를 나타내는 바(막대) 차트를 생성합니다.
            fig = px.bar(
                df_means, # 시각화의 기반이 되는 데이터프레임입니다.
                x='과목', # X축에 과목명을 매핑합니다.
                y='평균 점수', # Y축에 평균 점수를 매핑합니다.
                text='평균 점수', # 막대그래프 상단에 실제 평균 점수 수치가 표시되도록 설정합니다.
                title='📊 과목별 평균 점수 시각화 그래프', # 그래프 전체의 제목을 설정합니다.
                color='평균 점수', # 점수 크기에 따라 자동으로 막대 색상에 그라데이션이 들어가도록 설정합니다.
                color_continuous_scale=px.colors.sequential.Plasma # 세련되고 이쁜 'Plasma' 색상 테마를 적용합니다.
            )
            
            # 그래프의 가독성을 높이기 위해 차트 내부 요소들의 세부 속성을 수정합니다.
            fig.update_traces(texttemplate='%{text}점', textposition='outside') # 수치 뒤에 '점'을 붙이고 막대 바깥쪽에 배치합니다.
            fig.update_layout(
                xaxis_title="과목명", # X축 아래에 표시될 타이틀을 변경합니다.
                yaxis_title="평균 점수 (점)", # Y축 왼쪽에 표시될 타이틀을 변경합니다.
                yaxis=dict(range=[0, 100]), # 모든 과목 점수의 만점이 100점이므로 Y축 범위를 0~100으로 고정합니다.
                coloraxis_showscale=False # 우측에 생기는 복잡한 색상 기준표(Color Bar)를 제거하여 깔끔하게 만듭니다.
            )
            
            # 스트리밋에서 지원하는 Plotly 전용 출력 함수를 사용해 웹앱 화면에 그래프를 그려냅니다.
            st.plotly_chart(fig, use_container_width=True)
            
    # 파일 읽기 과정 등에서 예상치 못한 오류가 발생했을 때 앱이 멈추지 않도록 예외 처리합니다.
    except Exception as e:
        # 사용자 화면에 발생한 에러 메시지를 빨간색 창으로 친절하게 안내합니다.
        st.error(f"파일을 처리하는 과정에서 에러가 발생했습니다: {e}")

# 사용자가 아직 파일을 업로드하지 않았을 때 작동하는 조건문입니다.
else:
    # 파일을 업로드하라는 직관적인 안내 팁 메시지를 파란색 박스로 화면에 보여줍니다.
    st.info("💡 상단의 'Browse files' 버튼을 누르거나 CSV 파일을 드래그하여 업로드하면 자동으로 분석이 시작됩니다.")