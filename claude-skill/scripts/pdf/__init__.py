"""
PDF Translation Module

This module provides PDF extraction, translation, and rebuilding capabilities
for the epub-translator project.

Key Components:
- extract_pdf.py: Extract text with coordinates using PyMuPDF
- translate_pdf.py: Translate with glossary support
- rebuild_pdf.py: Rebuild PDF via redaction-based replacement
- validate_pdf.py: Validate PDF integrity and translation quality
- utils.py: Shared utilities for layout detection
- font_manager.py: Font embedding and fallback handling
- auto_glossary.py: Auto-detection of code/math for preservation

Usage:
    See docs/pdf-translation-guide.md for detailed documentation.
"""

__version__ = "1.0.0-mvp"
__author__ = "Vladimir Balko"

# Export key functions when implemented
__all__ = [
    # Will be populated as modules are created
]
