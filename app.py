import os
import streamlit as st
import openai
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import config

# Load environment variables from .env file
load_dotenv()

# Elasticsearch 연결
es = Elasticsearch(config.ELASTICSEARCH_HOST)

# OpenAI API key 설정 (from .env)
openai.api_key = os.getenv("OPENAI_API_KEY")

# 사용 가능한 모델 리스트
AVAILABLE_MODELS = ["gpt-3.5-turbo", "gpt-4"]

# 자주 묻는 질문 리스트
FAQ_LIST = [
    "VTS-9K5X2-H550I 카메라의 주요 특징은 무엇인가요?",
    "이 카메라의 최대 라인 레이트(line rate)는 얼마인가요?",
    "DSNU(Dark Signal Non-Uniformity) 보정 기능은 어떻게 작동하나요?",
    "LUT(Look Up Table) 기능을 어떻게 사용할 수 있나요?",
    "CoaXPress 인터페이스 설정은 어떻게 하나요?",
    "카메라 설정을 저장하고 불러오는 User Set Control 기능은 어떻게 작동하나요?"
]

def search_elasticsearch(query, index_name=config.ELASTICSEARCH_INDEX):
    """Elasticsearch에서 검색 수행"""
    search_body = {
        "query": {
            "match": {
                "content": query
            }
        }
    }
    results = es.search(index=index_name, body=search_body, size=3)
    return [hit["_source"]["content"] for hit in results["hits"]["hits"]]

def generate_answer(query, context, model):
    """선택된 GPT 모델을 사용하여 답변 생성"""
    try:
        prompt = f"다음 정보를 바탕으로 질문에 답변해주세요:\n\n정보: {context}\n\n질문: {query}\n\n답변:"
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "당신은 제품 메뉴얼에 대한 질문에 답변하는 AI 어시스턴트입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"OpenAI API 오류: {str(e)}")
        return None

def main():
    st.set_page_config(page_title=config.APP_TITLE, layout="wide")
    st.title(config.APP_TITLE)
    st.write(config.APP_DESCRIPTION)

    # 사이드바에 자주 묻는 질문 추가
    st.sidebar.title("자주 묻는 질문 (가상)")
    selected_faq = st.sidebar.radio("질문을 선택하세요:", FAQ_LIST)

    # 메인 영역
    col1, col2 = st.columns([3, 1])

    with col1:
        # 모델 선택
        selected_model = st.selectbox("사용할 모델을 선택하세요:", AVAILABLE_MODELS)

        # 질문 입력 필드 (선택된 FAQ로 자동 채워짐)
        query = st.text_input("질문을 입력하세요:", value=selected_faq)

        if st.button("답변 받기"):
            if not openai.api_key:
                st.error("OpenAI API 키가 설정되지 않았습니다. 환경 변수 OPENAI_API_KEY를 설정해주세요.")
                return

            if query:
                with st.spinner("답변을 생성 중입니다..."):
                    try:
                        # Elasticsearch에서 관련 정보 검색
                        search_results = search_elasticsearch(query)
                        if not search_results:
                            st.warning("관련 정보를 찾을 수 없습니다.")
                            return
                        context = "\n".join(search_results)

                        # 선택된 GPT 모델을 사용하여 답변 생성
                        answer = generate_answer(query, context, selected_model)
                        if answer:
                            st.subheader("답변:")
                            st.write(answer)

                            st.subheader("참고한 정보:")
                            for i, result in enumerate(search_results, 1):
                                st.text(f"참고 정보 {i}:")
                                st.text(result[:200] + "...")  # 처음 200자만 표시
                        else:
                            st.error("답변을 생성하는 데 문제가 발생했습니다.")
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {str(e)}")
            else:
                st.warning("질문을 입력해주세요.")

    with col2:
        st.subheader("사용 방법")
        st.write("1. 왼쪽 사이드바에서 자주 묻는 질문을 선택하거나 직접 질문을 입력하세요.")
        st.write("2. 사용할 GPT 모델을 선택하세요.")
        st.write("3. '답변 받기' 버튼을 클릭하면 AI가 답변을 생성합니다.")
        st.write("4. 생성된 답변과 참고한 정보를 확인하세요.")
        st.write("사용한 문서 : User_Manual_VTS-9K5X2_V1.5_EN.pdf")
        st.write("문서 출처 : [VIEWORKS Download Center](https://download.vieworks.com/main2?item_type=1&list_type=list&tag_list=)")


if __name__ == "__main__":
    main()
