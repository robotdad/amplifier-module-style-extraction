"""Amplifier module for extracting and applying writing style."""

from .extractor import StyleExtractor
from .models import StyleExtractionError
from .models import StyleProfile

__version__ = "0.1.0"
__all__ = ["StyleExtractor", "StyleProfile", "StyleExtractionError"]
