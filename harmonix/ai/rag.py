from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class KnowledgeDocument:
    source: str
    content: str


@dataclass(slots=True)
class KnowledgeBase:
    documents_dir: Path
    documents: list[KnowledgeDocument] = field(default_factory=list)

    def load_stub_documents(self) -> None:
        if self.documents or not self.documents_dir.exists():
            return
        for path in self.documents_dir.glob("*.txt"):
            self.documents.append(
                KnowledgeDocument(source=path.name, content=path.read_text(encoding="utf-8"))
            )

    def search(self, query: str, n_results: int = 3) -> list[dict]:
        self.load_stub_documents()
        tokens = {token.lower() for token in query.split() if token}
        scored: list[tuple[int, KnowledgeDocument]] = []
        for document in self.documents:
            score = sum(token in document.content.lower() for token in tokens)
            if score:
                scored.append((score, document))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {"source": document.source, "content": document.content[:400], "score": score}
            for score, document in scored[:n_results]
        ]

    def build_context(self, query: str, max_chars: int = 2000) -> str:
        matches = self.search(query, n_results=3)
        if not matches:
            return ""
        chunks = [f"[{match['source']}] {match['content']}" for match in matches]
        return "\n\n".join(chunks)[:max_chars]