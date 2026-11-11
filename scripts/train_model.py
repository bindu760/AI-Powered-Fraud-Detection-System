"""Convenience entry point for training a model from any working directory."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ml.training.train import main

if __name__ == "__main__":
    main()
