from .health import router as health_router
from .xhs import router as xhs_router

__all__ = ["health", "xhs"]

# Re-export modules so `from ...routers import health, xhs` works
from . import health
from . import xhs
