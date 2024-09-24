import json
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer

def load_chunks(json_file):
    """JSON 파일에서 chunk 데이터 로드"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_vector_db(chunks, index_name='manual_chunks'):
    """chunk를 벡터화하여 Elasticsearch에 저장"""
    # Sentence Transformer 모델 로드
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Elasticsearch 클라이언트 초기화
    es = Elasticsearch(['http://localhost:9200'])

    # 인덱스 설정 및 매핑 정의
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "file": {"type": "keyword"},
                "chunk_id": {"type": "keyword"},
                "content": {"type": "text"},
                "content_vector": {
                    "type": "dense_vector",
                    "dims": model.get_sentence_embedding_dimension()
                }
            }
        }
    }

    # 인덱스 생성 (이미 존재하면 삭제 후 재생성)
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name, body=index_settings)

    # chunk를 벡터화하고 Elasticsearch에 저장
    def generate_actions():
        for i, chunk in enumerate(chunks):
            vector = model.encode(chunk['content']).tolist()
            yield {
                "_index": index_name,
                "_source": {
                    "file": chunk['file'],
                    "chunk_id": chunk['chunk_id'],
                    "content": chunk['content'],
                    "content_vector": vector
                }
            }
            if (i + 1) % 10 == 0:  # 10개의 chunk마다 진행상황 출력
                print(f"{i+1}개의 chunk 처리 완료")

    helpers.bulk(es, generate_actions())
    print(f"총 {len(chunks)}개의 chunk를 Elasticsearch에 저장했습니다.")

def main():
    chunks_file = "./data/chunks.json"
    chunks = load_chunks(chunks_file)
    create_vector_db(chunks)
    print("인덱싱이 완료되었습니다. 이제 rag_qa_system.py를 실행할 수 있습니다.")

if __name__ == "__main__":
    main()
