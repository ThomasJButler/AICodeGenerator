"""
@author Tom Butler
@date 2025-10-23
@description API endpoints package.
             Centralised imports for all FastAPI routers.
"""
from . import health
from . import generate
from . import analyze
from . import languages

__all__ = [
    "health",
    "generate",
    "analyze",
    "languages"
]