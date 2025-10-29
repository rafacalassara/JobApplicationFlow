from pathlib import Path

# Absolute path to the repository root (parent of the 'src' directory)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent


def from_root(*parts: str) -> Path:
    """Build an absolute Path anchored at the project root.

    Example:
        from_root("outputs", "file.txt") -> <repo>/outputs/file.txt
    """
    return PROJECT_ROOT.joinpath(*parts).resolve()
