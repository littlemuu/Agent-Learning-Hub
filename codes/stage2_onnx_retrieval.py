"""Stage 2：使用本地 ONNX embedding 的最小检索练习。

运行时请使用 .venv-py310，因为该环境已经验证 ONNX Runtime 可用：
    .\.venv-py310\Scripts\python.exe codes\stage2_onnx_retrieval.py
"""

import os
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

from stage2_retrieval import CHUNKS


MODEL_NAME = "BAAI/bge-small-en-v1.5"
# 模型已下载到这个缓存目录。TEMP 目录若被系统清理，需要重新下载模型。
CACHE_DIR = Path(os.environ["TEMP"]) / "fastembed-cache-py310"


def create_model() -> TextEmbedding:
    """创建当前环境已验证稳定的 CPU ONNX embedding 模型。"""
    return TextEmbedding(
        model_name=MODEL_NAME,
        cache_dir=str(CACHE_DIR),
        providers=["CPUExecutionProvider"],
        threads=1,
        enable_cpu_mem_arena=False,
    )


def embed_texts(model: TextEmbedding, texts: list[str]) -> np.ndarray:
    """把多个文本编码为二维向量矩阵。

    返回结果应满足：每一行对应 texts 中同索引的一段文本。
    例如 texts 有 3 段文本，返回矩阵形状应类似 (3, 384)。

    model.embed(...) 返回的是逐个产出向量的迭代器；先用 list(...) 收集，
    再用 np.vstack(...) 把多个一维向量堆叠为二维矩阵。
    """
    vectors = list(model.embed(texts, batch_size=1))
    matrix = np.vstack(vectors)
    return matrix


def prepare_documents(model)->dict:
    documents = [chunk["text"] for chunk in CHUNKS]
    document_vectors = embed_texts(model, documents)
    return{
        "chunks":CHUNKS,
        "document_vectors":document_vectors,
    }


def cosine_scores(query_vector: np.ndarray, document_vectors: np.ndarray) -> np.ndarray:
    """计算一个 query 向量与所有文档向量的余弦相似度。

    注意：当前练习的向量都非零，不需要额外处理零向量。
    """
    query_norm = np.linalg.norm(query_vector)
    # axis=1 表示沿“列”的方向计算，因此会对每一行文档向量分别求长度。
    # 若 document_vectors 形状为 (3, 384)，这里的结果形状为 (3,)。
    document_norms = np.linalg.norm(document_vectors, axis=1)
    # @ 是 NumPy 的矩阵乘法运算符。这里计算每一行文档向量与 query_vector
    # 的点积，(3, 384) @ (384,) 会得到 3 个点积分数，形状为 (3,)。
    dot_products = document_vectors @ query_vector
    scores = dot_products / (document_norms * query_norm)
    return scores


def retrieve_from_index(query:str,model:TextEmbedding,index:dict,
                        threshold:float=0.65,top_k:int=2)->list[dict]:
    query_vector=embed_texts(model,[query])[0]
    scores=cosine_scores(query_vector,index["document_vectors"])
    results=[]
    for chunk, score in zip(index["chunks"], scores):
        if score >= threshold:
            results.append(
                {
                    "id": chunk["id"],
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "semantic_score": float(score),
                }
            )
    results.sort(key=lambda result: result["semantic_score"], reverse=True)
    return results[:top_k]

def print_results(query: str, results: list[dict]) -> None:
    """打印检索到的原文、来源与真实语义分数。"""
    print(f"Query: {query}")

    if not results:
        print("No reliable material found.")
        return

    for result in results:
        print(f"id: {result['id']}")
        print(f"semantic_score: {result['semantic_score']:.3f}")
        print(f"text: {result['text']}")
        print(f"source: {result['source']}")
        print()

def build_answer_input(query:str,results:list[dict])->dict:
    ans={}
    if results:
        ans["status"]="ready"
        ans["question"]=query
        evi=[]
        for result in results:
            evi.append(
                {
                    "id":result['id'],
                    "text":result['text'],
                    "source":result['source']
                }
            )
        ans["evidence"]=evi
        return ans
    
    ans["status"]="insufficient_evidence"
    ans["question"]=query
    ans["evidence"]=[]
    return ans

def generate_answer(answer_input:dict)->str:
    final_results=""
    status=answer_input["status"]
    if status=="ready":
        if not answer_input["evidence"]:
            raise ValueError("Ready answer requires at least one evidence item.")
        for evi in answer_input["evidence"]:
            if "text" not in evi:
                raise ValueError("Evidence item requires text.")
            if "source" not in evi:
                raise ValueError("Evidence item requires source.")
            final_results+=f"{evi['text']}，来源：{evi['source']}。\n"
        return final_results
    
    elif status=="insufficient_evidence":
        final_results="没有找到足够可靠的资料，无法基于证据回答。"
        return final_results
    
    raise ValueError(f"Unknown answer:{status}")

def assert_raises_value_error(answer_input: dict, expected_message: str) -> None:
    try:
        generate_answer(answer_input)
    except ValueError as exc:
        assert expected_message in str(exc)
        return
    raise AssertionError("Expected ValueError, but generate_answer returned normally.")

def run_answer_tests()->None:
    ready_input = {
        "status": "ready",
        "question": "test",
        "evidence": [
            {
                "id": "x",
                "text": "Refund requests must be submitted within 7 days.",
                "source": "policy.md",
            }
        ],
    }
    ready_answer = generate_answer(ready_input)
    assert "Refund requests" in ready_answer
    assert "policy.md" in ready_answer

    insufficient_input = {
        "status": "insufficient_evidence",
        "question": "test",
        "evidence": [],
    }
    assert generate_answer(insufficient_input) == "没有找到足够可靠的资料，无法基于证据回答。"

    assert_raises_value_error(
        {
            "status": "weird_status",
            "question": "test",
            "evidence": [],
        },
        "Unknown answer",
    )
    assert_raises_value_error(
        {
            "status": "ready",
            "question": "test",
            "evidence": [],
        },
        "at least one evidence",
    )
    assert_raises_value_error(
        {
            "status": "ready",
            "question": "test",
            "evidence": [{"id": "x", "source": "policy.md"}],
        },
        "requires text",
    )
    assert_raises_value_error(
        {
            "status": "ready",
            "question": "test",
            "evidence": [{"id": "x", "text": "Some evidence."}],
        },
        "requires source",
    )
    print("answer tests passed")

def main() -> None:
    # 模型已在本地缓存；设置离线模式，避免练习时再次发起网络请求。
    os.environ["HF_HUB_OFFLINE"] = "1"
    model = create_model()
    query = "faulty item one week later"
    index=prepare_documents(model)

    results = retrieve_from_index(query, model,index, threshold=0.65, top_k=2)
    answer_input=build_answer_input(query,results)
    print(answer_input)
    assert answer_input["status"]=="ready"
    assert "semantic_score" not in answer_input["evidence"][0]

    print_results(query, results)
    print(generate_answer(answer_input))

    # 提高阈值，演示没有证据满足可靠性要求时的兜底回答。
    results = retrieve_from_index(query, model, index, threshold=0.75, top_k=2)
    answer_input = build_answer_input(query, results)
    print(answer_input)
    assert answer_input["status"] == "insufficient_evidence"
    assert answer_input["evidence"] == []

    print_results(query, results)
    print(generate_answer(answer_input))
    run_answer_tests()
    
if __name__ == "__main__":
    main()
