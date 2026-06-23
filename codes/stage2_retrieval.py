"""Stage 2: a deterministic local retrieval exercise.

This deliberately does not call an embedding API. The learning goal is to make
the retrieval flow observable before replacing keyword scoring with embeddings.
"""

import re


CHUNKS = [
    {
        "id": "refund_deadline",
        "text": "Refund requests must be submitted within 7 days of purchase.",
        "source": "policy.md#refund-deadline",
    },
    {
        "id": "quality_exception",
        "text": "After 7 days, products with quality problems may be manually reviewed.",
        "source": "policy.md#quality-exception",
    },
    {
        "id": "shipping",
        "text": "Standard shipping takes 3 to 5 business days.",
        "source": "policy.md#shipping",
    },
]

SEMANTIC_SCORES = {
    "refund_deadline": 0.72,
    "quality_exception": 0.93,
    "shipping": 0.12,
}


def tokenize(text: str) -> set[str]:
    """Return lowercase words; remove a trailing 's' for this tiny demo."""
    words = re.findall(r"[a-z0-9]+", text.lower()) 
    return {word.rstrip("s") for word in words} 


def score_chunk(query: str, chunk_text: str) -> int:
    """Return the number of unique normalized query words found in a chunk.

    Example: query terms {"quality", "problem", "day"} and chunk terms
    {"quality", "problem", "day", "manual"} should score 3.

    TODO: implement this using tokenize() and set intersection.
    """
    query_text=tokenize(query)
    chunk_text=tokenize(chunk_text)
    return len(query_text&chunk_text)


def retrieve_hybrid(query: str) -> list[dict]:
    """
        保留 lexical_score > 0 或 semantic_score >= 0.70 的候选；
        按 semantic_score 降序，再按 lexical_score 降序排序。
    """
    results=[]
    for chunk in CHUNKS:
        chunk_id=chunk["id"]
        chunk_text=chunk["text"]
        source=chunk["source"]
        semantic_score=SEMANTIC_SCORES[chunk_id]

        lexical_score=score_chunk(query,chunk_text)
        if lexical_score>0 or semantic_score>=0.70:
            result={
                "id":chunk_id,
                "text":chunk_text,
                "source":source,
                "lexical_score":lexical_score,
                "semantic_score":semantic_score,
            }
            results.append(result)

    results.sort(key=lambda result:result["lexical_score"],reverse=True)        
    results.sort(key=lambda result:result["semantic_score"],reverse=True)
    return results


def print_results(query: str, results: list[dict]) -> None:
    """Print either evidence with citations or a controlled empty-result message."""
    print(f"Query: {query}")

    if not results:
        print("No reliable material found.")
        return

    for result in results:
        print(f"id: {result['id']}")
        print(f"lexical_score: {result['lexical_score']}")
        print(f"semantic_score: {result['semantic_score']}")
        print(f"text: {result['text']}")
        print(f"source: {result['source']}")
        print()


def main() -> None:
    query = "faulty item one week later"

    # After you implement retrieve(), this should print quality_exception first
    # and include its source as evidence.
    try:
        results = retrieve_hybrid(query)
    except NotImplementedError as exc:
        print(f"Exercise pending: {exc}")
        return

    print_results(query, results)


if __name__ == "__main__":
    main()
