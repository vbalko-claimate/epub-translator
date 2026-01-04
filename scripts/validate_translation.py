#!/usr/bin/env python3
"""
EPUB Translation Validator

Validates that an XHTML chapter file has been fully translated.
Checks for presence of Czech-specific characters.

Usage:
    python validate_translation.py <file.xhtml> [threshold]

Arguments:
    file.xhtml: Path to XHTML file to validate
    threshold: Maximum allowed percentage of Czech characters (default: 1.0%)

Exit codes:
    0: Translation is valid (< threshold Czech characters)
    1: Translation failed (>= threshold Czech characters)
    2: Script error (file not found, etc.)

Example:
    python validate_translation.py workspace/OEBPS/chapter1.xhtml 1.0
"""

import sys
import re
from pathlib import Path


def validate_translation(file_path, threshold=1.0):
    """
    Check if XHTML file is fully translated (minimal Czech text).

    Args:
        file_path: Path to XHTML file
        threshold: Maximum percentage of Czech characters allowed (default 1%)

    Returns:
        tuple: (is_valid, czech_pct, message)
            is_valid: True if translation passes validation
            czech_pct: Percentage of Czech-specific characters
            message: Human-readable status message
    """
    try:
        file_path = Path(file_path)

        if not file_path.exists():
            return (False, 0, f"ERROR: File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count Czech-specific characters (á,č,ď,é,ě,í,ň,ó,ř,š,ť,ú,ů,ý,ž)
        # These characters appear in Czech but rarely in English
        czech_chars = len(re.findall(r'[áčďéěíňóřšťúůýž]', content.lower()))

        # Count all alphabetic characters (including Czech)
        all_alpha_chars = len(re.findall(r'[a-záčďéěíňóřšťúůýž]', content.lower()))

        if all_alpha_chars == 0:
            return (False, 0, "ERROR: No text content found in file")

        # Calculate percentage of Czech characters
        czech_pct = (czech_chars / all_alpha_chars * 100)

        # Determine if translation is valid
        if czech_pct > threshold:
            return (False, czech_pct,
                   f"FAILED: {czech_pct:.1f}% Czech characters (threshold: {threshold}%)")

        return (True, czech_pct,
               f"PASS: {czech_pct:.2f}% Czech characters (threshold: {threshold}%)")

    except UnicodeDecodeError:
        return (False, 0, "ERROR: File encoding error - not valid UTF-8")
    except Exception as e:
        return (False, 0, f"ERROR: {type(e).__name__}: {e}")


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: validate_translation.py <file.xhtml> [threshold]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Validates that XHTML file is fully translated (< threshold Czech chars)", file=sys.stderr)
        print("Default threshold: 1.0%", file=sys.stderr)
        sys.exit(2)

    file_path = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0

    is_valid, czech_pct, message = validate_translation(file_path, threshold)

    # Print result
    print(f"{Path(file_path).name}: {message}")

    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
