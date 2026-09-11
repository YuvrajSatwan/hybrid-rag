from dataclasses import dataclass
from pathlib import Path
import re 
import json

@dataclass
class Document:
    document_id: str
    title: str
    text: str
    source_path:str
    service: str
    version:str
    source_url:str


raw_dir = Path('data/raw/')
metadata_path = Path("data/metadata/documents.jsonl")

def load_metadata(path:Path) -> list[dict]:
    records = []

    with path.open("r", encoding ='utf-8') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records



def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)

    if match:
        return match.group(1).strip()

    return fallback


def load_markdown_file(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="replace"
    )


def clean_title(text: str) -> str:
    return text.replace("¶", "").strip()


def clean_markdown(text: str) -> str:
    lines = []

    for line in text.splitlines():
        if line.startswith("#"):
            line = line.replace("¶", "")

        lines.append(line)

    return "\n".join(lines)


_MIN_DEDUPE_LEN = 10


def fix_mojibake(text: str) -> str:
    if not any(
        marker in text
        for marker in ["Â", "â", "ð", "Ã"]
    ):
        return text

    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

    
def remove_duplicate_lines(text: str) -> str:
    seen_recent: list[str] = []
    window = 4
    out: list[str] = []

    for line in text.split("\n"):
        stripped = line.strip()

        # Remove Markdown bullet before comparison
        key = re.sub(r"^[-*]\s*", "", stripped)

        if len(key) >= _MIN_DEDUPE_LEN and key in seen_recent:
            continue

        out.append(line)

        if stripped:
            seen_recent.append(key)

            if len(seen_recent) > window:
                seen_recent.pop(0)

    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()



def load_documents(metadata_path: Path) -> list[Document]:
    documents = []

    records = load_metadata(metadata_path)

    for record in records:
        text_path = Path(record["text_path"])

        text = load_markdown_file(text_path)

        text = clean_markdown(text)
        text = remove_duplicate_lines(text)
        text = fix_mojibake(text)

        document = Document(
            document_id=record["document_id"],
            title=clean_title(record["title"]),
            text=text,
            source_path=str(text_path),
            service=record["project"],
            version=record["release"],
            source_url=record["url"],
        )

        documents.append(document)

    return documents


if __name__ == '__main__':

    documents = load_documents(metadata_path)

    



    print(f"Documents loaded: {len(documents)}")

    doc = documents[0]

    print("\nFirst document:")
    print("ID:", doc.document_id)
    print("Title:", doc.title)
    print("Service:", doc.service)
    print("Version:", doc.version)
    print("Source URL:", doc.source_url)
    print("Characters:", len(doc.text))        

    