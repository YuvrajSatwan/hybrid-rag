import sys
import json
from dataclasses import dataclass
from pathlib import Path

import tiktoken

from src.ingestion.loader import Document, load_documents


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# CHUNK DATA MODEL
# ============================================================

@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    text: str
    chunk_index: int
    source_path: str
    title: str
    service: str
    version: str
    source_url: str


# ============================================================
# TOKENIZER
# ============================================================

encoder = tiktoken.get_encoding("cl100k_base")


def tokenize(text: str) -> list[int]:
    return encoder.encode(text)


def detokenize(tokens: list[int]) -> str:
    return encoder.decode(tokens)


# ============================================================
# CHUNK TEXT
# ============================================================

def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[str]:

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    tokens = tokenize(text)

    chunks = []

    start = 0
    step = chunk_size - overlap

    while start < len(tokens):

        end = start + chunk_size

        chunk_tokens = tokens[start:end]

        if not chunk_tokens:
            break

        chunks.append(
            detokenize(chunk_tokens)
        )

        start += step

    return chunks


# ============================================================
# SAVE CHUNKS
# ============================================================

def save_chunks(
    chunks: list[Chunk],
    output_path: Path,
) -> None:

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as f:

        for chunk in chunks:

            record = {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "text": chunk.text,
                "chunk_index": chunk.chunk_index,
                "title": chunk.title,
                "service": chunk.service,
                "version": chunk.version,
                "source_url": chunk.source_url,
                "source_path": chunk.source_path,
            }

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                ) + "\n"
            )


# ============================================================
# CHUNK DOCUMENTS
# ============================================================

def chunk_documents(
    documents: list[Document],
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[Chunk]:

    chunks = []

    for document in documents:

        text_chunks = chunk_text(
            document.text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        # ----------------------------------------------------
        # Use the short filename as the document name.
        #
        # Example:
        # output/cleaned/nova_architecture.md
        #
        # becomes:
        # nova_architecture
        # ----------------------------------------------------

        document_name = Path(
            document.source_path
        ).stem

        for index, text in enumerate(text_chunks):

            # ------------------------------------------------
            # Human-readable chunk ID
            #
            # nova_architecture_0001
            # nova_architecture_0002
            # nova_architecture_0003
            # ------------------------------------------------

            chunk_id = (
                f"{document_name}_{index + 1:04d}"
            )

            chunk = Chunk(
                chunk_id=chunk_id,
                document_id=document.document_id,
                text=text,
                chunk_index=index,
                title=document.title,
                service=document.service,
                version=document.version,
                source_url=document.source_url,
                source_path=document.source_path,
            )

            chunks.append(chunk)

    return chunks


# ============================================================
# CHUNK STATISTICS
# ============================================================

def print_chunk_stats(
    chunks: list[Chunk],
) -> None:

    if not chunks:
        print("No chunks generated.")
        return

    token_counts = [
        len(tokenize(chunk.text))
        for chunk in chunks
    ]

    token_counts.sort()

    n = len(token_counts)

    print("\n=== Chunk Statistics ===")
    print(f"Total chunks: {n}")
    print(f"Minimum: {token_counts[0]}")
    print(f"Maximum: {token_counts[-1]}")
    print(
        f"Average: {sum(token_counts) / n:.1f}"
    )
    print(
        f"Median: {token_counts[n // 2]}"
    )
    print(
        f"P90: {token_counts[int(n * 0.90)]}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # Load documents
    documents = load_documents(
        Path("data/metadata/documents.jsonl")
    )

    print(f"Documents: {len(documents)}")

    # Create chunks
    chunks = chunk_documents(
        documents,
        chunk_size=500,
        overlap=100,
    )

    print(f"Chunks: {len(chunks)}")

    # Save chunks
    output_path = Path(
        "data/processed/chunks.jsonl"
    )

    save_chunks(
        chunks,
        output_path,
    )

    print(
        f"\nSaved chunks to: {output_path}"
    )

    # Statistics
    print_chunk_stats(chunks)

    # Sample chunks
    print("\n=== Sample Chunks ===")

    for chunk in chunks[:3]:

        print(
            "\n-----------------------------"
        )

        print("ID:", chunk.chunk_id)
        print("Document ID:", chunk.document_id)
        print("Title:", chunk.title)
        print(
            "Tokens:",
            len(tokenize(chunk.text))
        )

        print(chunk.text[:700])