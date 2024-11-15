# vts-9k5x2-rag-elk-manual-helper

> 이 프로젝트는 뷰웍스 VTS-9K5X2 모델의 User Manual을 기반으로 문장을 chunk화 하여 Open AI로 질문을 검색할 수 있는 프로젝트입니다.
# [실행해보기(링크클릭)](https://xdapwjpcvhssvjguj6gkxw.streamlit.app/)
1. ~현재 DB(엘라스틱서치) Localhost 연결로 인한 내부동작 X~
2. 엘라스틱서치 네이버 클라우드 서버 Open
3. ~정상 작동~
4. 네이버 클라우드 서버 Down

![image](https://github.com/user-attachments/assets/3db27d32-b92c-453a-96e4-19c28f87ac0c)

# 실행화면
https://github.com/user-attachments/assets/b1c0b90f-12e5-47d0-adf2-52d8d3101135


### 사용한 문서 : User_Manual_VTS-9K5X2_V1.5_EN.pdf
### 문서 출처 : [VIEWORKS Download Center](https://download.vieworks.com/main2?item_type=1&list_type=list&tag_list=)
## ✅ 프로젝트 요약

**목표**: 뷰웍스 VTS-9K5X2 모델의 User Manual을 chunk화하여 OpenAI와 Elasticsearch 기반 검색 기능을 제공하는 프로젝트입니다.

**결과**: PDF 메뉴얼의 텍스트를 청크로 분할해 Elasticsearch에 인덱스화하고, OpenAI API를 통해 사용자가 질문할 수 있는 시스템을 구축했습니다.

**역할 및 기여도**: PDF 전처리 및 청크 생성, Elasticsearch 인덱싱, OpenAI API 통합 작업 전반을 수행했습니다.

# 📒 상세 기술 및 라이브러리

- Python: PDF 처리 및 청크 생성
- Elasticsearch: 청크 인덱싱 및 벡터 저장
- OpenAI API: 질문 답변 생성
- Streamlit: 사용자 인터페이스 구현
- pdflumber: PDF 텍스트 추출
- sentence-transformers: 텍스트 벡터화
- Docker: 컨테이너화된 환경에서 서비스 실행
- Kibana: 데이터 시각화 및 검색
# 🎯 담당 역할

- PDF 처리 및 청크 생성: PDF에서 텍스트 추출 후 청크화하고 JSON으로 저장하는 로직 구현
- Elasticsearch 인덱스 구성: Elasticsearch에 청크 데이터를 인덱싱하고 벡터화하여 검색 가능한 도록 설정
- OpenAI 통합: OpenAI API와 연결하여 사용자가 질문한 내용을 기반으로 답변 생성
- Streamlit 기반 UI 개발: 사용자가 쉽게 검색 및 질문할 수 있도록 직관적인 UI 설계
# 💡 깨달은 점

- PDF 처리에서 복잡성: 특히 표와 같은 복잡한 레이아웃의 텍스트를 처리하는 데 시간이 많이 걸렸고, 이를 개선하기 위해 추가적인 처리 로직이 필요함을 깨달았습니다.
- Elasticsearch 사용의 한계: 사용되는 데이터의 볼륨이 클 경우 인덱싱하고 검색 성능을 높이기 위해 인덱스 및 벡터 저장 방식에 대한 이해를 높일 필요성을 느꼈습니다.


# 엘라스틱서치 / 인덱스 필드(Kibava)

<img width="655" alt="image" src="https://github.com/user-attachments/assets/50632f4a-3ad1-48cc-9b31-5c6e4e371cd1">

# 임베딩된 105개 Chunk_index

<img width="1410" alt="image" src="https://github.com/user-attachments/assets/907c0a97-0fe4-4a0b-9cf0-2d50c9c4d1e3">

<img width="694" alt="image" src="https://github.com/user-attachments/assets/6294b2b1-b423-4ecd-b1dd-febbb8c580d2">

## 사용 방법
1. 먼저, pdf_to_chunker.py 파일에서 ./data/manuals/메뉴얼.pdf, 메뉴얼 pdf를 chunk화 합니다.
(Chunk 결과는 json 형식으로 저장)

2. elk_vector_db_builder.py 파일을 통해 ELK로 [1]과정에서 json 형식으로 된 chunk를 인덱스화 합니다.

3. app.py를 통해서 streamlit을 실행합니다.
```bash
streamlit run app.py
```

4. streamlit 우측에 있는 설명을 따릅니다.

---
# pdf_to_chunker.py 세부 설명

### 주요 구성 요소

#### ChunkConfig 클래스
> 청크 크기와 오버랩을 설정하는 데이터 클래스  
기본값: `chunk_size = 1000`, `overlap = 50`

#### PDFChunker 클래스
> PDF 처리의 핵심 로직

##### 주요 메서드:
1. **chunk_pdf**: PDF를 청크로 나눕니다.
2. **process_pdf**: PDF 처리 전체 과정을 관리합니다.
3. **preview_chunks**: 생성된 청크의 샘플을 보여줍니다.

### 주요 기능
- `pdfplumber`를 사용하여 PDF에서 텍스트 추출
- 추출된 텍스트를 설정된 크기의 청크로 분할
- 청크 간 오버랩 처리
- 결과를 JSON 형식으로 저장
- 로깅을 통한 처리 과정 추적
- 에러 처리

### main 함수
> 스크립트의 실행 흐름을 관리합니다.  
기본 설정값:
- 입력 PDF 경로: `./data/manuals/User_Manual_VTS-9K5X2_V1.5_EN.pdf`
- 출력 JSON 파일: `./data/chunks.json`

---

# elk_vector_db_builder.py 세부설명

## 주요 기능
이 스크립트는 JSON 파일에서 청크 데이터를 로드하고, 이를 벡터화하여 Elasticsearch에 저장하는 기능을 수행

## 주요 구성 요소

### 1. `load_chunks(json_file)`
- **설명**: JSON 파일에서 청크 데이터 로드
- **입력**:
  - `json_file` (JSON 파일 경로)
- **출력**: 로드된 청크 데이터

```python
def load_chunks(json_file):
    """JSON 파일에서 chunk 데이터 로드"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### 2. `create_vector_db(chunks, index_name='manual_chunks')`
- **설명**: 청크를 벡터화하여 Elasticsearch에 저장합니다.
- **입력**: 
  - `chunks` (청크 데이터)
  - `index_name` (인덱스 이름, 기본값: 'manual_chunks')
- **작업 과정**:
  1. Sentence Transformer 모델을 로드
  2. Elasticsearch 클라이언트를 초기화
  3. 인덱스 설정 및 매핑을 정의
  4. 기존 인덱스가 존재할 경우 삭제하고 새로 생성
  5. 각 청크를 벡터화하여 Elasticsearch에 저장

# app.py 세부 설명

## 주요 기능
1. **Elasticsearch 연결**: 환경 변수에서 Elasticsearch 호스트와 포트를 읽어와 연결합니다.
2. **OpenAI API 설정**: OpenAI API 키를 환경 변수에서 로드하여 설정합니다.
3. **자주 묻는 질문(FAQ)**: 사용자가 자주 묻는 질문 목록에서 선택할 수 있는 기능을 제공합니다.
4. **검색 기능**: 사용자가 입력한 질문을 Elasticsearch에서 검색하여 관련 정보를 찾습니다.
5. **답변 생성**: 검색된 정보를 기반으로 OpenAI 모델을 사용하여 질문에 대한 답변을 생성합니다.

```python
# 프롬프트는 아래와 같음
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
```

6. **사용자 인터페이스**: Streamlit을 통해 직관적인 사용자 인터페이스를 제공합니다.

## 주요 구성 요소
- **search_elasticsearch(query)**: 주어진 질문을 Elasticsearch에서 검색하여 관련 내용을 반환합니다.
- **generate_answer(query, context, model)**: 선택한 모델을 사용하여 검색된 정보를 기반으로 답변을 생성합니다.
- **main()**: Streamlit 애플리케이션의 실행 흐름을 관리하며, 질문 입력 및 결과 표시를 담당합니다.

## 사용 방법
1. 자주 묻는 질문을 사이드바에서 선택하거나 직접 질문을 입력합니다.
2. 사용할 GPT 모델을 선택합니다.
3. "답변 받기" 버튼을 클릭하여 AI가 답변을 생성합니다.
4. 생성된 답변과 참고한 정보를 확인합니다.

# [향후해보고싶은 것]추출된 5개 문장, tensorboard 활용 vector visualization
<img width="997" alt="image" src="https://github.com/user-attachments/assets/3f9c1195-0e5a-46dd-b836-5a9905df79a8">

```python
sentences = [
    "The camera provides high-quality images.",
    "Image resolution can be adjusted in the settings.",
    "Trigger mode allows for precise timing of image capture.",
    "The user manual contains important safety information.",
    "Proper lens cleaning is essential for optimal performance."
]
```
> 예시로 5개 문장만 추출하여 vector를 시각화 해봤는데, 우선 PDF 전처리에 시간을 더 투자해야할 것 같다.
> 예로 들면 PDF파일에 있는 표를 텍스트화 하는 것
