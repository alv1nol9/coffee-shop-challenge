# tests/conftest.py
import sys
import os

# prepend the project root so "import lib.models..." works
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
