"""
Search Tools — embedding generation and similarity search.

Mock implementation stores embeddings in memory.  Replace with
pgvector / Pinecone / Qdrant when the database layer is ready.
"""

from __future__ import annotations

import logging
import math
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mock embedding store  (complaint_id → vector)
# ---------------------------------------------------------------------------
_MOCK_EMBEDDINGS: dict[str, list[float]] = {}

# Pre-seeded mock similar complaints for demo purposes
_MOCK_SIMILAR_RESULTS: list[dict[str, Any]] = [
    {
        "complaint_id": "CMP-001",
        "similarity_score": 0.87,
        "category": "roads",
        "description_snippet": "Large pothole on Main Street near the market.",
        "location": "Main Street, Sector 5",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
    },
    {
        "complaint_id": "CMP-002",
        "similarity_score": 0.62,
        "category": "drainage",
        "description_snippet": "Blocked drainage causing water logging.",
        "location": "2nd Cross Road, Sector 5",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat(),
    },
]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------
async def generate_embedding(text: str) -> list[float]:
    """Generate an embedding vector for *text*.

    In production, this will call the LLM client's embed() method or
    a dedicated embedding API.  The mock returns a simple hash-based
    deterministic vector.
    """
    logger.info("generate_embedding called (text length=%d)", len(text))
    # Deterministic mock: convert chars → floats, pad/truncate to 64 dims
    raw = [float(ord(c) % 50) / 50.0 for c in text[:64]]
    raw += [0.0] * max(0, 64 - len(raw))
    return raw


async def search_similar_complaints(
    embedding: list[float],
    *,
    top_k: int = 5,
    threshold: float = 0.5,
) -> list[dict[str, Any]]:
    """Search for complaints similar to the given embedding vector.

    Replace with: pgvector nearest-neighbour query.
    """
    logger.info(
        "search_similar_complaints called (top_k=%d, threshold=%s)",
        top_k,
        threshold,
    )
    # If we have stored embeddings, compute real cosine similarity
    results: list[dict[str, Any]] = []
    if _MOCK_EMBEDDINGS:
        for cid, vec in _MOCK_EMBEDDINGS.items():
            score = _cosine_similarity(embedding, vec)
            if score >= threshold:
                results.append(
                    {
                        "complaint_id": cid,
                        "similarity_score": round(score, 4),
                        "category": None,
                        "description_snippet": "",
                        "location": None,
                        "created_at": None,
                    }
                )
        results.sort(key=lambda r: r["similarity_score"], reverse=True)
        return results[:top_k]

    # Fallback: return pre-seeded mock data filtered by threshold
    return [r for r in _MOCK_SIMILAR_RESULTS if r["similarity_score"] >= threshold][
        :top_k
    ]


async def search_complaints_by_location(
    latitude: float,
    longitude: float,
    radius_km: float = 1.0,
) -> list[dict[str, Any]]:
    """Find complaints within *radius_km* of the given coordinates.

    Replace with: PostGIS spatial query.
    """
    logger.info(
        "search_complaints_by_location called (lat=%s, lon=%s, radius=%s km)",
        latitude,
        longitude,
        radius_km,
    )
    # Mock: return the pre-seeded list (all are "nearby")
    return _MOCK_SIMILAR_RESULTS


async def store_embedding(complaint_id: str, embedding: list[float]) -> None:
    """Persist an embedding for later retrieval.

    Replace with: INSERT INTO complaint_embeddings ...
    """
    logger.info("store_embedding called for %s", complaint_id)
    _MOCK_EMBEDDINGS[complaint_id] = embedding
