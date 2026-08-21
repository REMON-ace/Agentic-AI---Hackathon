"""
Department Tools — department lookup, SLA retrieval.

Mock implementation.  Replace with database queries later.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from agents.config import (
    CATEGORY_DEPARTMENT_MAP,
    Department,
    SLA_HOURS,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mock department data
# ---------------------------------------------------------------------------
_DEPARTMENTS: list[dict[str, Any]] = [
    {
        "id": "DEPT-01",
        "name": Department.WATER,
        "description": "Handles water supply, leaks, and quality issues.",
        "contact_email": "water@municipality.gov",
    },
    {
        "id": "DEPT-02",
        "name": Department.SANITATION,
        "description": "Handles waste collection, garbage, and sanitation.",
        "contact_email": "sanitation@municipality.gov",
    },
    {
        "id": "DEPT-03",
        "name": Department.ROADS,
        "description": "Handles road repairs, potholes, and traffic signage.",
        "contact_email": "roads@municipality.gov",
    },
    {
        "id": "DEPT-04",
        "name": Department.DRAINAGE,
        "description": "Handles drainage blockages and waterlogging.",
        "contact_email": "drainage@municipality.gov",
    },
    {
        "id": "DEPT-05",
        "name": Department.STREETLIGHTS,
        "description": "Handles streetlight installation and repair.",
        "contact_email": "streetlights@municipality.gov",
    },
    {
        "id": "DEPT-06",
        "name": Department.PUBLIC_FACILITIES,
        "description": "Handles parks, benches, public restrooms, and other facilities.",
        "contact_email": "facilities@municipality.gov",
    },
]


# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------
async def get_departments() -> list[dict[str, Any]]:
    """Return the list of all departments.

    Replace with: SELECT * FROM departments
    """
    logger.info("get_departments called")
    return _DEPARTMENTS


async def get_department_for_category(category: str) -> Optional[str]:
    """Return the default department name for a complaint category.

    Replace with: SELECT dept_name FROM category_dept_map WHERE category = %s
    """
    logger.info("get_department_for_category called for %s", category)
    return CATEGORY_DEPARTMENT_MAP.get(category)


async def get_department_sla(
    department_name: str, priority: str
) -> Optional[int]:
    """Return the SLA deadline in hours for a department+priority combo.

    Replace with: SELECT sla_hours FROM department_sla WHERE ...
    """
    logger.info(
        "get_department_sla called for dept=%s, priority=%s",
        department_name,
        priority,
    )
    return SLA_HOURS.get(priority)


async def get_department_by_name(name: str) -> Optional[dict[str, Any]]:
    """Lookup a single department by name.

    Replace with: SELECT * FROM departments WHERE name = %s
    """
    logger.info("get_department_by_name called for %s", name)
    for dept in _DEPARTMENTS:
        if dept["name"] == name:
            return dept
    return None
