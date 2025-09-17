"""Module discovery utilities."""

import importlib
import importlib.util
import pkgutil
from pathlib import Path
from typing import Optional


def get_module_source_file(module_name: str) -> Optional[Path]:
    """Get the source file path for a module."""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec and spec.origin:
            return Path(spec.origin)
    except Exception:
        pass
    return None


def find_all_modules(root_module: str, verbose: bool = False) -> list[str]:
    """Find all modules under a root module.

    Args:
        root_module: The root module to search under
        verbose: If True, print debug information about discovery failures

    Returns:
        List of module names found. Empty list if the root module cannot be imported.
    """
    modules = []

    try:
        root = importlib.import_module(root_module)
        if hasattr(root, "__path__"):
            for importer, modname, ispkg in pkgutil.walk_packages(
                root.__path__, prefix=root_module + "."
            ):
                modules.append(modname)
    except ImportError as e:
        if verbose:
            import sys
            print(f"Warning: Failed to import '{root_module}': {e}", file=sys.stderr)
            print(f"Current Python path: {sys.path}", file=sys.stderr)
            print(f"Make sure the module is installed or accessible from the current directory", file=sys.stderr)

    return sorted(modules)


def should_include_module(module_name: str, include_internal: bool = False) -> bool:
    """Check if a module should be included in the API documentation."""
    parts = module_name.split(".")

    # Exclude any module or submodule that starts with underscore
    for part in parts[1:]:  # Skip the root module
        if part.startswith("_") and not include_internal:
            return False

    return True