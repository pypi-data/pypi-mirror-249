# %%
import tempfile
from pathlib import Path


def get_pytars_path():
    """Get the path to the project root directory."""
    return Path(__file__).parent.parent.parent


def get_temp_path():
    """Get the path to store temp files."""
    return Path(tempfile.TemporaryDirectory().name).parent / "pytars"
