import streamlit as st  # Streamlit 라이브러리 임포트
import pandas as pd  # Pandas 라이브러리 임포트
import plotly.express as px  # Plotly 라이브러리 임포트

# 웹페이지의 제목과 레이아웃 스타일(중앙 정렬) 설정
st.set_page_config(page_title="학생 성적 대시보드", layout="centered")

# 대시보드의 메인 타이틀 출력
st.title("📚 학생 성적 분석 대시보드")
# 대시보드 사용법에 대한 간단한 설명 서브타이틀 출력
st.markdown("### CSV 파일을 업로드하면 과목별 평균을 자동으로 계산하고 시각화합니다.")

# CSV 파일만 업로드할 수 있는 파일 업로더 컴포넌트 생성
uploaded_file = st.file_uploader("성적 CSV 파일을 업로드해주세요.", type=["csv"])

# 사용자가 파일을 정상적으로 업로드했을 경우 실행되는 블록
if uploaded_file is not None:
    try:
        # 업로드된 CSV 파일을 UTF-8 인코딩 방식으로 읽어와 데이터프레임으로 변환
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        # UTF-8 인코딩 실패 시(Excel에서 저장한 한글 파일 등), 파일 포인터를 처음으로 되돌림
        uploaded_file.seek(0)
        # 한글 깨짐을 방지하기 위해 CP949(EUC-KR) 인코딩 방식으로 다시 파일 읽기
        df = pd.read_csv(uploaded_file, encoding='cp949')
    
    # 컬럼명 전후에 들어간 불필요한 공백을 제거하여 띄어쓰기로 인한 오류 원천 차단
    df.columns = df.columns.str.strip()
    
    # 데이터 스키마 검증을 위한 필수 컬럼 목록 정의
    required_columns = ['이름', '과목', '점수']
    
    # 업로드된 파일에 필수 컬럼('이름', '과목', '점수')이 모두 포함되어 있는지 확인
    if all(col in df.columns for col in required_columns):
        # 원본 데이터 확인을 위한 섹션 헤더 출력
        st.subheader("📋 업로드된 원본 데이터 확인")
        # 데이터프레임 원본을 Streamlit 화면에 깔끔한 테이블 형태로 표기
        st.dataframe(df)
        
        # '과목'별로 데이터를 그룹화한 후, '점수' 컬럼의 평균값을 계산하고 인덱스를 초기화
        df_avg = df.groupby('과목')['점수'].mean().reset_index()
        # 계산된 과목별 평균 점수를 소수점 둘째 자리까지 반올림 처리
        df_avg['점수'] = df_avg['점수'].round(2)
        
        # 계산 완료된 통계 데이터 섹션 헤더 출력
        st.subheader("📊 과목별 평균 점수 결과")
        # 사용자가 보기 편하도록 '점수' 컬럼명을 '평균 점수'로 변경하여 화면에 출력
        st.dataframe(df_avg.rename(columns={'점수': '평균 점수'))
        
        # Plotly Express를 활용하여 시각적인 막대 그래프(Bar Chart) 생성
        fig = px.bar(
            df_avg,  # 시각화 데이터로 과목별 평균 데이터프레임 지정
            x='과목',  # X축 축 기준으로 '과목' 설정
            y='점수',  # Y축 축 기준으로 평균 '점수' 설정
            text='점수',  # 막대 그래프 상단에 각 평균 점수 수치가 표시되도록 지정
            title='과목별 평균 점수 시각화 결과',  # 차트 전체 제목 설정
            labels={'점수': '평균 점수', '과목': '과목명'},  # 마우스 오버 시 보일 축 레이블 가독성 개선
            color='과목',  # 과목별로 서로 다른 색상이 자동 부여되도록 설정
            color_discrete_sequence=px.colors.qualitative.Pastel  # 세련되고 예쁜 파스텔톤 컬러 시퀀스 적용
        )
        
        # 차트 내부 세부 속성 설정 (막대 바 바깥쪽에 '점' 단위를 붙여 텍스트 배치)
        fig.update_traces(texttemplate='%{text}점', textposition='outside')
        # 차트 레이아웃 정돈
        fig.update_layout(
            xaxis_title="과목",  # X축 하단 제목 설정
            yaxis_title="평균 점수",  # Y축 좌측 제목 설정
            yaxis=dict(range=[0, 100]),  # 점수 비교가 직관적이도록 Y축의 시작과 끝 범위를 0~100으로 고정
            showlegend=False  # X축 레이블과 내용이 중복되므로 우측 범례 박스는 제거
        )
        
        # 완성된 Plotly 바 차트를 대시보드 화면 너비에 맞추어 유동적으로 출력
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # 데이터 스키마 규칙에 맞지 않는 필수 컬럼 누락 시 에러 메시지 출력
        st.error(f"CSV 파일의 컬럼명을 확인해주세요. 필수 포함 컬럼: {required_columns}")
else:
    # 아직 사용자가 파일을 업로드하지 않았을 때 나타나는 기본 안내 문구 출력
    st.info("💡 성적 분석을 시작하려면 상단의 업로드 창에 CSV 파일을 드래그하거나 선택해주세요.")