"""Placeholder service functions.

These functions are intentionally left unimplemented.  Human developers
will later replace them with real implementations for parsing G‑Code
files and rendering thumbnails.
"""


def gcode_parser(path: str) -> dict:
    """Parse a G‑Code file and return useful statistics.

    Args:
        path: The filesystem path to the uploaded G‑Code file.

    Returns:
        A dictionary containing statistics extracted from the file.
        This stub always returns a not‑implemented message.
    """
    # Stub. Human will parse .gcode.
    return {"msg": "parser not implemented"}


def thumbnail_render(path: str) -> str | None:
    """Render a thumbnail for a 3D model.

    Args:
        path: The filesystem path to the uploaded model file (e.g. STL).

    Returns:
        The relative path to the generated PNG within the uploads
        directory, or ``None`` if rendering is not implemented.  This
        stub always returns ``None``.
    """
    # Stub. Human will render PNG and return relative path.
    return None