from pathlib import Path
#import senetnce transformer
from sentence_transformers import SentenceTransformer
_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed(text: str) -> list[float]:
    model = get_model()
    return model.encode(text).tolist()


#import croma db 

import chromadb

CHROMA_DIR = Path.home() / ".coding-assistant" / "chroma"


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection("codebase")


def add_chunk(chunk_id: str, text: str, source_file: str) -> None:
    collection = get_collection()
    embedding = embed(text)
    collection.upsert(
        ids=[chunk_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"source": source_file}],
    )

def search(query: str, n_results: int = 3) -> list[dict]:
    collection = get_collection()
    query_embedding = embed(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append({"text": doc, "source": meta["source"]})
    return chunks

def chunk_file(path: str, chunk_size: int = 50) -> list[str]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk = "".join(lines[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def index_directory(directory: str = ".") -> int:
    root = Path(directory)
    extensions = ["*.py", "*.md"]

    all_files = []
    for ext in extensions:
        all_files.extend(root.rglob(ext))

    total_chunks = 0
    for file_path in all_files:
        if ".venv" in file_path.parts or "__pycache__" in file_path.parts:
            continue

        chunks = chunk_file(str(file_path))
        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_path}:{i}"
            add_chunk(chunk_id, chunk, str(file_path))
            total_chunks += 1

    return total_chunks