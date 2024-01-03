from lemon_rag.dependencies.data_access import data_access
from lemon_rag.dependencies.vector_access import embed_sentence, vector_access


def vectorize_sentences():
    # 搜索所有未向量化的文件，执行向量化操作。
    for file in data_access.find_file_not_vectorized():
        for sentence in file.sentences:
            vectors = embed_sentence([sentence.raw_content])
            vector_access.save_sentence(sentence, vectors[0])
            sentence.vectorized = True
            sentence.save(only=["vectorized"])
        data_access.update_file_vectorized_count(file)
