#!/usr/bin/env python3
"""
PDF Rebuild with Translation

Rebuilds PDF by replacing original text with translations using PyMuPDF redaction API.
Preserves layout, fonts, and formatting as much as possible.

Usage:
    python rebuild_pdf.py <original.pdf> --translated-dir pdf_workspace/translated --output translated.pdf

Example:
    python rebuild_pdf.py book.pdf --output book_translated.pdf
    # Creates: book_translated.pdf with Czech translations
"""

import sys
import subprocess
from pathlib import Path


def check_and_install_dependencies():
    """
    Check if required dependencies are installed, and install them if missing.

    Required: PyMuPDF (fitz)
    """
    required = {
        'fitz': 'PyMuPDF',
    }

    missing = []

    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}", file=sys.stderr)
        print(f"📦 Installing automatically...\n", file=sys.stderr)

        for package in missing:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--quiet", package],
                    stdout=subprocess.DEVNULL
                )
                print(f"✓ Installed: {package}", file=sys.stderr)
            except subprocess.CalledProcessError as e:
                print(f"\n❌ Failed to install {package}", file=sys.stderr)
                print(f"\nPlease install manually:", file=sys.stderr)
                print(f"  pip install {package}\n", file=sys.stderr)
                sys.exit(1)

        print(f"✓ All dependencies installed!\n", file=sys.stderr)


# Install dependencies if needed
check_and_install_dependencies()

# Now import dependencies
import fitz  # PyMuPDF
import json
import argparse
from typing import Dict, List, Tuple, Optional

# Phase 2: Import text matcher for fuzzy matching
try:
    from scripts.pdf.text_matcher import find_text_in_page
except ImportError:
    # Fallback for when running from scripts/pdf/ directory
    from text_matcher import find_text_in_page


def rebuild_pdf_with_translations(
    original_pdf_path: str,
    translated_dir: str,
    output_pdf_path: str,
    verbose: bool = True,
    fuzzy_matching: bool = False,
    fuzzy_threshold: float = 0.85,
    match_strategies: Optional[List[str]] = None,
    verbose_matching: bool = False
) -> Tuple[int, int, int]:
    """
    Rebuild PDF by replacing text with translations using redaction.

    Args:
        original_pdf_path: Path to original PDF file
        translated_dir: Directory with translated JSON files
        output_pdf_path: Path for output translated PDF
        verbose: Print progress messages

    Returns:
        Tuple of (pages_processed, blocks_replaced, overflow_warnings)

    Raises:
        FileNotFoundError: If PDF or JSON files not found
        Exception: If PDF processing fails
    """
    # Validate input
    original_pdf = Path(original_pdf_path)
    if not original_pdf.exists():
        raise FileNotFoundError(f"PDF file not found: {original_pdf_path}")

    translated_path = Path(translated_dir)
    if not translated_path.exists():
        raise FileNotFoundError(f"Translated directory not found: {translated_dir}")

    if verbose:
        print(f"\nRebuilding PDF with translations")
        print(f"  Original: {original_pdf_path}")
        print(f"  Translations: {translated_dir}")
        print(f"  Output: {output_pdf_path}\n")

    # Open original PDF
    try:
        doc = fitz.open(original_pdf_path)
    except Exception as e:
        raise Exception(f"Cannot open PDF: {e}")

    total_pages = len(doc)
    total_blocks = 0
    total_overflow = 0

    if verbose:
        print(f"Processing {total_pages} pages...\n")

    # Process each page
    for page_num, page in enumerate(doc, start=1):
        # Load translated JSON for this page
        json_file = translated_path / f"page_{page_num:03d}.json"

        if not json_file.exists():
            if verbose:
                print(f"  ⚠ Page {page_num:3d}: No translation found, skipping")
            continue

        with open(json_file, "r", encoding="utf-8") as f:
            page_data = json.load(f)

        blocks_on_page = 0
        overflow_on_page = 0

        # Process each block on this page
        for block in page_data.get("blocks", []):
            # Skip if no translation available
            if "translated_text" not in block:
                continue

            original_text = block.get("original_text", block.get("text", ""))
            translated_text = block["translated_text"]

            # Skip if translation same as original (header/footer)
            if original_text == translated_text:
                continue

            bbox = block["bbox"]
            font = block.get("font", "helv")  # Default to Helvetica
            size = block.get("size", 12)

            # Use suggested size if overflow detected
            if block.get("overflow_warning", False):
                size = block.get("suggested_size", size)
                overflow_on_page += 1

            # Search for original text in PDF
            # Phase 2: Use multi-strategy text matching if enabled
            if fuzzy_matching:
                text_instances, match_strategy = find_text_in_page(
                    page=page,
                    target_text=original_text,
                    bbox=bbox,
                    strategies=match_strategies,
                    fuzzy_threshold=fuzzy_threshold,
                    verbose=verbose_matching
                )

                # Log non-standard matches
                if verbose and match_strategy not in ["exact", "bbox"]:
                    print(f"    Used {match_strategy} matching for: {original_text[:50]}...")
            else:
                # Original logic (Phase 1): exact match with fallbacks
                text_instances = page.search_for(original_text)

                if not text_instances:
                    # Try searching for first few words if full text not found
                    words = original_text.split()[:3]
                    if words:
                        text_instances = page.search_for(" ".join(words))

                # If still not found, use bbox from JSON
                if not text_instances:
                    text_instances = [fitz.Rect(bbox)]

            # Add redaction annotation for each instance
            for inst_rect in text_instances:
                try:
                    # Add redaction: removes original, inserts translation
                    page.add_redact_annot(
                        inst_rect,
                        text=translated_text,
                        fontname=font,
                        fontsize=size,
                        fill=(1, 1, 1),  # White background
                        text_color=(0, 0, 0),  # Black text
                        align=fitz.TEXT_ALIGN_LEFT
                    )
                    blocks_on_page += 1

                except Exception as e:
                    # Always print errors to stderr, not just in verbose mode
                    print(f"    ⚠ Warning: Could not redact block: {e}", file=sys.stderr)
                    if verbose:
                        import traceback
                        traceback.print_exc()

        # Apply all redactions on this page
        try:
            page.apply_redactions()
        except Exception as e:
            # Always print critical errors to stderr
            print(f"  ⚠ Page {page_num:3d}: Redaction failed: {e}", file=sys.stderr)
            if verbose:
                import traceback
                traceback.print_exc()
            continue

        total_blocks += blocks_on_page
        total_overflow += overflow_on_page

        if verbose:
            status = f"  ✓ Page {page_num:3d}: {blocks_on_page:4d} blocks replaced"
            if overflow_on_page > 0:
                status += f" (⚠ {overflow_on_page} overflow adjustments)"
            print(status)

    # Save translated PDF
    try:
        doc.save(
            output_pdf_path,
            garbage=4,  # Remove unused objects
            deflate=True,  # Compress streams
            clean=True  # Clean up document structure
        )
    except Exception as e:
        raise Exception(f"Cannot save PDF: {e}")
    finally:
        doc.close()

    if verbose:
        print(f"\n✓ PDF rebuild complete!")
        print(f"  Pages processed: {total_pages}")
        print(f"  Blocks replaced: {total_blocks}")
        print(f"  Overflow adjustments: {total_overflow}")
        print(f"  Output: {output_pdf_path}\n")

    return total_pages, total_blocks, total_overflow


def main():
    """Command-line interface for PDF rebuild."""
    parser = argparse.ArgumentParser(
        description="Rebuild PDF with translations using PyMuPDF redaction",
        epilog="Example: python rebuild_pdf.py book.pdf --output book_translated.pdf"
    )

    parser.add_argument(
        "pdf_file",
        help="Path to original PDF file"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output path for translated PDF"
    )

    parser.add_argument(
        "-t", "--translated-dir",
        default="pdf_workspace/translated",
        help="Directory with translated JSON files (default: pdf_workspace/translated)"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages"
    )

    # Phase 2: Fuzzy text matching arguments
    parser.add_argument(
        "--fuzzy-matching",
        action="store_true",
        help="Enable fuzzy text matching for better accuracy (Phase 2)"
    )

    parser.add_argument(
        "--fuzzy-threshold",
        type=float,
        default=0.85,
        help="Minimum similarity ratio for fuzzy match (default: 0.85, range: 0-1)"
    )

    parser.add_argument(
        "--match-strategies",
        nargs="+",
        default=None,
        help="Text matching strategies to try in order (default: exact normalized first_words fuzzy bbox)"
    )

    parser.add_argument(
        "--verbose-matching",
        action="store_true",
        help="Print which matching strategy was used for each block"
    )

    args = parser.parse_args()

    try:
        rebuild_pdf_with_translations(
            original_pdf_path=args.pdf_file,
            translated_dir=args.translated_dir,
            output_pdf_path=args.output,
            verbose=not args.quiet,
            fuzzy_matching=args.fuzzy_matching,
            fuzzy_threshold=args.fuzzy_threshold,
            match_strategies=args.match_strategies,
            verbose_matching=args.verbose_matching
        )
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
