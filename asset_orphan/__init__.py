"""asset-orphan: find asset files that are never referenced in source code."""

__version__ = "0.1.0"
__all__ = ["__version__"]
try:
    from .cli import main
except ImportError:  # pragma: no cover - flat execution
    from cli import main
