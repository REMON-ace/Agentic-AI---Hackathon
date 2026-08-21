"""
Complaint Tools — CRUD helpers for complaint data.

These are thin tool interfaces with MOCK implementations.
Replace the bodies with real PostgreSQL / SQLAlchemy queries when the
backend is connected.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mock in-memory store
# ---------------------------------------------------------------------------
_MOCK_COMPLAINTS: dict[str, dict[str, Any]] = {
    "CMP-001": {
        "complaint_id": "CMP-001",
        "citizen_id": "CIT-100",
        "description": "Large pothole on Main Street near the market causing traffic issues.",
        "image_url": None,
        "latitude": 12.9716,
        "longitude": 77.5946,
        "address": "Main Street, Sector 5",
        "category": "roads",
        "priority": "HIGH",
        "status": "in_progress",
        "department": "Roads",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    },
    "CMP-002": {
        "complaint_id": "CMP-002",
        "citizen_id": "CIT-101",
        "description": "Blocked drainage causing water logging in residential area.",
        "image_url": None,
        "latitude": 12.9720,
        "longitude": 77.5950,
        "address": "2nd Cross Road, Sector 5",
        "category": "drainage",
        "priority": "MEDIUM",
        "status": "assigned",
        "department": "Drainage",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    },
    "CMP-003": {
        "complaint_id": "CMP-003",
        "citizen_id": "CIT-102",
        "description": "Streetlight not working near the park for two weeks.",
        "image_url": None,
        "latitude": 12.9750,
        "longitude": 77.5900,
        "address": "Park Avenue, Sector 8",
        "category": "streetlights",
        "priority": "LOW",
        "status": "submitted",
        "department": None,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    },
}


# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------
async def get_complaint(complaint_id: str) -> Optional[dict[str, Any]]:
    """Retrieve a complaint by ID.

    Replace with: SELECT * FROM complaints WHERE id = %s
    """
    logger.info("get_complaint called for %s", complaint_id)
    return _MOCK_COMPLAINTS.get(complaint_id)


async def update_complaint(
    complaint_id: str, updates: dict[str, Any]
) -> Optional[dict[str, Any]]:
    """Update a complaint's fields.

    Replace with: UPDATE complaints SET ... WHERE id = %s
    """
    logger.info("update_complaint called for %s with %s", complaint_id, updates)
    if complaint_id in _MOCK_COMPLAINTS:
        _MOCK_COMPLAINTS[complaint_id].update(updates)
        _MOCK_COMPLAINTS[complaint_id]["updated_at"] = datetime.now(
            timezone.utc
        ).isoformat()
        return _MOCK_COMPLAINTS[complaint_id]
    return None


async def get_complaint_history(complaint_id: str) -> list[dict[str, Any]]:
    """Return the status-change history for a complaint.

    Replace with: SELECT * FROM complaint_history WHERE complaint_id = %s
    """
    logger.info("get_complaint_history called for %s", complaint_id)
    # Mock: return a single event
    complaint = _MOCK_COMPLAINTS.get(complaint_id)
    if complaint is None:
        return []
    return [
        {
            "complaint_id": complaint_id,
            "old_status": "submitted",
            "new_status": complaint.get("status", "submitted"),
            "changed_at": complaint.get("updated_at", datetime.now(timezone.utc).isoformat()),
            "changed_by": "system",
        }
    ]


async def get_all_complaints(
    filters: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return all complaints, optionally filtered.

    Replace with: SELECT * FROM complaints WHERE ...
    """
    logger.info("get_all_complaints called with filters=%s", filters)
    results = list(_MOCK_COMPLAINTS.values())
    if filters:
        for key, value in filters.items():
            results = [c for c in results if c.get(key) == value]
    return results
