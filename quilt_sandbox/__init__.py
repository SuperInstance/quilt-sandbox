"""quilt-sandbox — canon lore runs in a sandboxed Python environment.

Substrate transition in 24 lines:
- lore text → sandboxed Python → result
- the canon is verified to RUN, not just to read
- the math can BE and grow
"""
from .sandbox import run_lore, safe_exec

__version__ = "0.1.0"
__all__ = ["run_lore", "safe_exec"]
