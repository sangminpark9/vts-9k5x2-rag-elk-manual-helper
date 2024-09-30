import tensorflow as tf
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorboard.plugins import projector
import os

# 실제 JSON 파일에서 추출한 문장
sentences = [
    "The camera provides high-quality images.",
    "Image resolution can be adjusted in the settings.",
    "Trigger mode allows for precise timing of image capture.",
    "The user manual contains important safety information.",
    "Proper lens cleaning is essential for optimal performance."
]

# TF-IDF 벡터화
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(sentences).toarray()

# 로그 디렉토리 설정
log_dir = 'logs/sentence_embeddings'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 임베딩 변수 생성
embedding_var = tf.Variable(vectors, name='sentence_embeddings')

# 체크포인트 저장
checkpoint = tf.train.Checkpoint(embedding=embedding_var)
checkpoint.save(os.path.join(log_dir, "embedding.ckpt"))

# 메타데이터 파일 작성
with open(os.path.join(log_dir, 'metadata.tsv'), 'w') as f:
    for sentence in sentences:
        f.write(sentence + '\n')

# 프로젝터 설정
config = projector.ProjectorConfig()
embedding = config.embeddings.add()
embedding.tensor_name = "sentence_embeddings/.ATTRIBUTES/VARIABLE_VALUE"
embedding.metadata_path = 'metadata.tsv'
projector.visualize_embeddings(log_dir, config)

print(f"Run 'tensorboard --logdir={log_dir}' to view visualizations.")
