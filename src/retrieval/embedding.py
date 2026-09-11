import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.embeddings import JinaEmbeddings

load_dotenv()

embeddings = JinaEmbeddings(
    jina_api_key=os.environ["JINA_API_KEY"],
    model_name="jina-embeddings-v3",
)
def load_chunks(path: Path) -> list[dict]:
    chunks = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))

    return chunks


def save_embeddings(
    chunks: list[dict],
    vectors: list[list[float]],
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for chunk, vector in zip(chunks, vectors):
            record = {
                "chunk_id": chunk["chunk_id"],
                "embedding": vector,
            }

            f.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    # Use the Jina embedding model created in jina_embedder.py
    embedder = embeddings

    # Input and output paths
    input_path = Path("data/processed/chunks.jsonl")
    output_path = Path("data/processed/embeddings.jsonl")

    # Load only 10 chunks for V1 development
    chunks = load_chunks(input_path)

    if not chunks:
        raise ValueError("No chunks found in the input file.")

    # Extract chunk text
    texts = [chunk["text"] for chunk in chunks]

    print(f"Embedding {len(texts)} chunks...")

    # Generate embeddings
    vectors = embedder.embed_documents(texts)

    # Basic validation
    if len(vectors) != len(chunks):
        raise ValueError(
            f"Number of embeddings ({len(vectors)}) "
            f"does not match number of chunks ({len(chunks)})."
        )

    print(f"Generated {len(vectors)} embeddings")
    print(f"Embedding dimension: {len(vectors[0])}")

    # Save embeddings
    save_embeddings(
        chunks,
        vectors,
        output_path,
    )

    print(f"Saved embeddings to: {output_path}")