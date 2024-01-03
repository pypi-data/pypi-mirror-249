__version__ = "1.0.4"

__usage__ = """
    
Usage:
    left shift + 1   -> Task: Marking rectangle
    left shift + 2   -> Task: Marking keypoint
    E                -> Task: Doodle
    R                -> Mode: Read <-> Mark
    F                -> Auto label
    A/D              -> Switch between images or objects
    W/S              -> Switch between class names
    C                -> Delete all bound bboxes & points in current image
    L                -> Shuffle color palette
    N                -> Hiding label text
    B                -> Blinking
    T                -> Switch between line-width-current and line-width=1
    +                -> Increase the line width
    -                -> Decrease the line width
    I                -> Image path (for the purpose of no-qt)
    Left mouse double click -> Select object
    Right mouse click -> Delete object


    (Keys're case-insensetive)
"""


from .marker import MarkerApp
from .main import run
from .basics import Profiler

__all__ = [
    "__version__",
    "run",
    "MarkerApp",
    "Profiler"
]
