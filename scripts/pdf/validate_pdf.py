#!/usr/bin/env python3
"""
PDF Translation Validation

Validates translated PDF for integrity, structure, and translation quality.

Checks performed:
1. PDF integrity (can be opened, not corrupted)
2. Page count matches original
3. Text extraction works
4. Glossary compliance (PRESERVE terms still present, TRANSLATE terms replaced)
5. Visual comparison (optional screenshots for manual review)

Usage:
    python validate_pdf.py <translated.pdf> --original original.pdf --glossary warhammer40k-en-cs.json

Example:
    python validate_pdf.py book_translated.pdf --original book.pdf
"""

import fitz  # PyMuPDF
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def validate_pdf_integrity(pdf_path: str, verbose: bool = True) -> bool:
    """
    Validate PDF can be opened and is not corrupted.

    Args:
        pdf_path: Path to PDF file
        verbose: Print messages

    Returns:
        True if valid, False otherwise
    """
    if verbose:
        print(f"1. PDF Integrity Check")
        print(f"   Testing: {pdf_path}")

    try:
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        doc.close()

        if verbose:
            print(f"   ✓ PDF opens successfully")
            print(f"   ✓ Page count: {page_count}\n")

        return True

    except Exception as e:
        if verbose:
            print(f"   ✗ PDF corrupted: {e}\n")
        return False


def validate_page_count(
    translated_pdf: str,
    original_pdf: str,
    verbose: bool = True
) -> bool:
    """
    Validate page count matches original.

    Args:
        translated_pdf: Path to translated PDF
        original_pdf: Path to original PDF
        verbose: Print messages

    Returns:
        True if page counts match, False otherwise
    """
    if verbose:
        print(f"2. Page Count Check")

    try:
        original_doc = fitz.open(original_pdf)
        translated_doc = fitz.open(translated_pdf)

        original_count = len(original_doc)
        translated_count = len(translated_doc)

        original_doc.close()
        translated_doc.close()

        matches = original_count == translated_count

        if verbose:
            print(f"   Original: {original_count} pages")
            print(f"   Translated: {translated_count} pages")
            if matches:
                print(f"   ✓ Page counts match\n")
            else:
                print(f"   ✗ Page counts differ!\n")

        return matches

    except Exception as e:
        if verbose:
            print(f"   ✗ Error: {e}\n")
        return False


def validate_text_extraction(
    translated_pdf: str,
    sample_pages: int = 5,
    verbose: bool = True
) -> bool:
    """
    Validate text can be extracted from translated PDF.

    Args:
        translated_pdf: Path to translated PDF
        sample_pages: Number of random pages to test
        verbose: Print messages

    Returns:
        True if text extraction works, False otherwise
    """
    if verbose:
        print(f"3. Text Extraction Check")

    try:
        doc = fitz.open(translated_pdf)
        page_count = len(doc)

        # Sample pages evenly distributed
        import random
        if page_count <= sample_pages:
            pages_to_test = list(range(page_count))
        else:
            step = page_count // sample_pages
            pages_to_test = [i * step for i in range(sample_pages)]

        all_success = True

        for page_num in pages_to_test:
            page = doc[page_num]
            text = page.get_text()

            if not text or len(text.strip()) == 0:
                if verbose:
                    print(f"   ✗ Page {page_num + 1}: No text extracted")
                all_success = False
            elif verbose:
                print(f"   ✓ Page {page_num + 1}: {len(text)} characters extracted")

        doc.close()

        if verbose:
            if all_success:
                print(f"   ✓ Text extraction working\n")
            else:
                print(f"   ⚠ Some pages have extraction issues\n")

        return all_success

    except Exception as e:
        if verbose:
            print(f"   ✗ Error: {e}\n")
        return False


def load_glossary(glossary_path: Optional[str]) -> Dict:
    """Load glossary file (reused from translate_pdf.py)."""
    if not glossary_path:
        return {"preserve": [], "translate": {}}

    glossary_file = Path(glossary_path)

    if not glossary_file.exists():
        # Try glossaries/ directory
        alt_path = Path("glossaries") / glossary_file.name
        if alt_path.exists():
            glossary_file = alt_path
        else:
            return {"preserve": [], "translate": {}}

    if glossary_file.suffix == ".json":
        with open(glossary_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            glossary = {"preserve": [], "translate": {}}

            for category, terms in data.items():
                if category == "metadata":
                    continue

                for term, info in terms.items():
                    mode = info.get("mode", "preserve")

                    if mode == "preserve":
                        glossary["preserve"].append(term)
                    elif mode == "translate":
                        glossary["translate"][term] = info.get("translation", term)

            return glossary

    return {"preserve": [], "translate": {}}


def validate_glossary_compliance(
    translated_pdf: str,
    glossary_path: Optional[str],
    verbose: bool = True
) -> Tuple[int, int]:
    """
    Validate glossary rules are applied correctly.

    Args:
        translated_pdf: Path to translated PDF
        glossary_path: Path to glossary file
        verbose: Print messages

    Returns:
        Tuple of (preserve_found, translate_found)
    """
    if not glossary_path:
        if verbose:
            print(f"4. Glossary Compliance Check")
            print(f"   (Skipped - no glossary provided)\n")
        return 0, 0

    if verbose:
        print(f"4. Glossary Compliance Check")
        print(f"   Glossary: {glossary_path}")

    glossary = load_glossary(glossary_path)

    if not glossary["preserve"] and not glossary["translate"]:
        if verbose:
            print(f"   (No terms to check)\n")
        return 0, 0

    try:
        doc = fitz.open(translated_pdf)

        # Extract all text
        full_text = ""
        for page in doc:
            full_text += page.get_text() + " "

        doc.close()

        # Check PRESERVE terms (should still be in text)
        preserve_found = 0
        preserve_total = len(glossary["preserve"])

        for term in glossary["preserve"][:20]:  # Check sample
            if term in full_text:
                preserve_found += 1

        # Check TRANSLATE terms (source should be gone, target should exist)
        translate_found = 0
        translate_total = len(glossary["translate"])

        for source, target in list(glossary["translate"].items())[:20]:  # Check sample
            source_exists = source in full_text
            target_exists = target in full_text

            if not source_exists and target_exists:
                translate_found += 1

        if verbose:
            print(f"   PRESERVE terms found: {preserve_found}/{min(preserve_total, 20)}")
            print(f"   TRANSLATE applied: {translate_found}/{min(translate_total, 20)}")

            if preserve_found >= min(preserve_total, 20) * 0.9:
                print(f"   ✓ Glossary compliance good (>90%)\n")
            else:
                print(f"   ⚠ Some glossary terms missing\n")

        return preserve_found, translate_found

    except Exception as e:
        if verbose:
            print(f"   ✗ Error: {e}\n")
        return 0, 0


def generate_visual_comparison(
    original_pdf: str,
    translated_pdf: str,
    page_nums: List[int],
    output_dir: str = "pdf_workspace/comparison",
    verbose: bool = True
) -> bool:
    """
    Generate screenshot comparison for manual review.

    Args:
        original_pdf: Path to original PDF
        translated_pdf: Path to translated PDF
        page_nums: Page numbers to screenshot (1-indexed)
        output_dir: Output directory for screenshots
        verbose: Print messages

    Returns:
        True if successful, False otherwise
    """
    if verbose:
        print(f"5. Visual Comparison (Optional)")
        print(f"   Generating screenshots for pages: {page_nums}")

    try:
        original_doc = fitz.open(original_pdf)
        translated_doc = fitz.open(translated_pdf)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for page_num in page_nums:
            if page_num > len(original_doc) or page_num > len(translated_doc):
                continue

            # Convert to 0-indexed
            idx = page_num - 1

            # Render original
            original_page = original_doc[idx]
            original_pix = original_page.get_pixmap(dpi=150)
            original_file = output_path / f"page_{page_num:03d}_original.png"
            original_pix.save(str(original_file))

            # Render translated
            translated_page = translated_doc[idx]
            translated_pix = translated_page.get_pixmap(dpi=150)
            translated_file = output_path / f"page_{page_num:03d}_translated.png"
            translated_pix.save(str(translated_file))

            if verbose:
                print(f"   ✓ Page {page_num}: {original_file.name} + {translated_file.name}")

        original_doc.close()
        translated_doc.close()

        if verbose:
            print(f"   ✓ Screenshots saved to: {output_dir}/\n")
            print(f"   Manual review: Compare original vs translated side-by-side\n")

        return True

    except Exception as e:
        if verbose:
            print(f"   ✗ Error: {e}\n")
        return False


def main():
    """Command-line interface for PDF validation."""
    parser = argparse.ArgumentParser(
        description="Validate translated PDF for integrity and quality",
        epilog="Example: python validate_pdf.py translated.pdf --original original.pdf"
    )

    parser.add_argument(
        "translated_pdf",
        help="Path to translated PDF file"
    )

    parser.add_argument(
        "--original",
        help="Path to original PDF (for comparison)"
    )

    parser.add_argument(
        "--glossary",
        help="Path to glossary file (for compliance check)"
    )

    parser.add_argument(
        "--visual",
        metavar="PAGES",
        help="Generate visual comparison for pages (e.g., '1,5,10')"
    )

    parser.add_argument(
        "--comparison-dir",
        default="pdf_workspace/comparison",
        help="Output directory for comparison screenshots (default: pdf_workspace/comparison)"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages"
    )

    args = parser.parse_args()

    verbose = not args.quiet

    if verbose:
        print(f"\n{'='*60}")
        print(f"PDF TRANSLATION VALIDATION")
        print(f"{'='*60}\n")

    # Run validations
    results = []

    # 1. PDF integrity
    integrity_ok = validate_pdf_integrity(args.translated_pdf, verbose)
    results.append(("Integrity", integrity_ok))

    # 2. Page count (if original provided)
    if args.original:
        page_count_ok = validate_page_count(args.translated_pdf, args.original, verbose)
        results.append(("Page Count", page_count_ok))

    # 3. Text extraction
    extraction_ok = validate_text_extraction(args.translated_pdf, verbose=verbose)
    results.append(("Text Extraction", extraction_ok))

    # 4. Glossary compliance (if glossary provided)
    if args.glossary:
        preserve_count, translate_count = validate_glossary_compliance(
            args.translated_pdf,
            args.glossary,
            verbose
        )
        results.append(("Glossary Compliance", preserve_count > 0 or translate_count > 0))

    # 5. Visual comparison (if requested)
    if args.visual and args.original:
        page_nums = [int(p.strip()) for p in args.visual.split(",")]
        visual_ok = generate_visual_comparison(
            args.original,
            args.translated_pdf,
            page_nums,
            args.comparison_dir,
            verbose
        )
        results.append(("Visual Comparison", visual_ok))

    # Summary
    if verbose:
        print(f"{'='*60}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*60}\n")

        for check, passed in results:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {check:20s} {status}")

        all_passed = all(passed for _, passed in results)

        print(f"\n{'='*60}")
        if all_passed:
            print(f"✓ All validations passed!")
        else:
            print(f"⚠ Some validations failed - review above")
        print(f"{'='*60}\n")

        return 0 if all_passed else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
