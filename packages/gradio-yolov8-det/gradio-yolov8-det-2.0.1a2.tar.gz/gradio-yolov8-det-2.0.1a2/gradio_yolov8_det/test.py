from pathlib import Path


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]

print(ROOT)