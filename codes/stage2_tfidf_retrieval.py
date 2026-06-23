"""Stage 2: offline TF-IDF retrieval with no network or API key.

TF-IDF turns text into sparse numeric vectors based on token importance. It is a
useful local baseline, but it is not a semantic embedding model.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from stage2_retrieval import CHUNKS

#tuple是一个不可变的序列类型，通常用于存储不同类型的元素。
#这里使用tuple[TfidfVectorizer, object]表示返回一个包含TfidfVectorizer对象和文档矩阵的元组。
def build_index() -> tuple[TfidfVectorizer, object]: 
    """Fit a TF-IDF vectorizer on chunk text and return it with the document matrix."""
    documents = [chunk["text"] for chunk in CHUNKS]
    #TfidfVectorizer是一个用于将文本转换为TF-IDF特征矩阵的类。
    # 它会计算每个词在文档中的重要性，并将文本表示为一个稀疏矩阵。
    vectorizer = TfidfVectorizer()
    #fit_transform方法将文档列表转换为TF-IDF特征矩阵，并返回一个稀疏矩阵对象。
    document_matrix = vectorizer.fit_transform(documents)
    return vectorizer, document_matrix


def retrieve_tfidf(
    query: str,
    vectorizer: TfidfVectorizer,
    document_matrix: object,
) -> list[dict]:
    """Return non-zero cosine-similarity candidates in descending score order.

    TODO:
    1. Convert the query with vectorizer.transform([query]).
    2. Compute cosine_similarity(query_vector, document_matrix).flatten().
    3. Pair each score with its corresponding CHUNKS item.
    4. Keep only scores greater than 0.
    5. Return id, text, source, and tfidf_score sorted descending.
    """
    results=[]
    # Reuse the vocabulary and IDF weights fitted from the documents. Calling
    # fit_transform() here would create a different vector space for the query.
    query_vector = vectorizer.transform([query])
    #下面这句做了什么呢？
    # cosine_similarity returns shape (1, number_of_documents): one score for
    # this query against each document. flatten() makes it a 1D score sequence.
    scores = cosine_similarity(query_vector, document_matrix).flatten()
    #zip用法？
    # zip() pairs CHUNKS[i] with scores[i], so metadata remains attached to the
    # score calculated for that chunk's text.
    for chunk,score in zip(CHUNKS,scores):
        if score>0:
            results.append(
                {
                    "id":chunk["id"],
                    "text":chunk["text"],
                    "source":chunk["source"],
                    "tfidf_score":score,
                }
            )
    results.sort(key=lambda result:result["tfidf_score"],reverse=True)
    return results



def print_results(query: str, results: list[dict]) -> None:
    """Print source-preserving results or a controlled empty-result message."""
    print(f"Query: {query}")

    if not results:
        print("No reliable material found.")
        return

    for result in results:
        print(f"id: {result['id']}")
        print(f"tfidf_score: {result['tfidf_score']:.3f}")
        print(f"text: {result['text']}")
        print(f"source: {result['source']}")
        print()


def main() -> None:
    vectorizer, document_matrix = build_index()

    # This should return quality_exception first after you implement retrieval.
    exact_query = "quality problem after 9 days"
    try:
        exact_results = retrieve_tfidf(exact_query, vectorizer, document_matrix)
    except NotImplementedError as exc:
        print(f"Exercise pending: {exc}")
        return

    print_results(exact_query, exact_results)

    # This paraphrase demonstrates TF-IDF's lexical limitation.
    paraphrase_query = "faulty item one week later"
    paraphrase_results = retrieve_tfidf(
        paraphrase_query,
        vectorizer,
        document_matrix,
    )
    print_results(paraphrase_query, paraphrase_results)


if __name__ == "__main__":
    main()
