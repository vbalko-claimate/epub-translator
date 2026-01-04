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
import argparse
import json
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


# Phase 2: Enhanced Visual Comparison Functions

def pix_to_pil(pix: fitz.Pixmap):
    """
    Convert PyMuPDF Pixmap to PIL Image.

    Args:
        pix: PyMuPDF Pixmap object

    Returns:
        PIL Image object
    """
    try:
        from PIL import Image
        import io

        # Get PNG bytes from pixmap
        png_bytes = pix.tobytes("png")

        # Load as PIL Image
        return Image.open(io.BytesIO(png_bytes))
    except ImportError:
        return None


def create_diff_image(img1, img2, threshold: int = 30):
    """
    Create visual diff highlighting differences between two images.

    Args:
        img1, img2: PIL Image objects
        threshold: Pixel difference threshold (0-255)

    Returns:
        PIL Image with differences highlighted in red/yellow
    """
    try:
        import numpy as np

        # Ensure same size
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)

        # Convert to numpy arrays
        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Compute absolute difference
        diff = np.abs(arr1.astype(int) - arr2.astype(int))

        # Create mask where difference exceeds threshold
        mask = np.any(diff > threshold, axis=-1)

        # Create output image (start with img2)
        output = arr2.copy()

        # Highlight differences in red/yellow overlay
        output[mask] = output[mask] // 2 + np.array([128, 64, 0])  # Red-yellow tint

        from PIL import Image
        return Image.fromarray(output.astype(np.uint8))
    except ImportError:
        return None


def create_side_by_side_comparison(
    original_pdf: str,
    translated_pdf: str,
    page_nums: List[int],
    output_dir: str = "pdf_workspace/comparison",
    include_diff: bool = True,
    verbose: bool = True
) -> bool:
    """
    Generate side-by-side comparison images with optional diff overlay.

    Creates images with 2 or 3 panels:
    - Panel 1: Original page
    - Panel 2: Translated page
    - Panel 3 (if include_diff): Diff visualization

    Args:
        original_pdf: Path to original PDF
        translated_pdf: Path to translated PDF
        page_nums: Page numbers to compare (1-indexed)
        output_dir: Output directory for comparison images
        include_diff: Include diff panel (default: True)
        verbose: Print progress messages

    Returns:
        True if successful, False otherwise
    """
    try:
        from PIL import Image, ImageDraw
        import numpy as np
    except ImportError:
        if verbose:
            print("  ⚠ Pillow not installed, skipping enhanced comparison")
            print("  Install with: pip install Pillow numpy")
        return False

    if verbose:
        print(f"5. Side-by-Side Visual Comparison (Phase 2)")
        print(f"   Generating comparison images for pages: {page_nums}")

    try:
        original_doc = fitz.open(original_pdf)
        translated_doc = fitz.open(translated_pdf)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for page_num in page_nums:
            if page_num > len(original_doc) or page_num > len(translated_doc):
                continue

            idx = page_num - 1

            # Render both pages as pixmaps
            original_page = original_doc[idx]
            translated_page = translated_doc[idx]

            original_pix = original_page.get_pixmap(dpi=150)
            translated_pix = translated_page.get_pixmap(dpi=150)

            # Convert to PIL Images
            original_img = pix_to_pil(original_pix)
            translated_img = pix_to_pil(translated_pix)

            if not original_img or not translated_img:
                continue

            # Create diff if requested
            if include_diff:
                diff_img = create_diff_image(original_img, translated_img)

                if diff_img:
                    # Concatenate horizontally: Original | Translated | Diff
                    total_width = original_img.width * 3
                    max_height = max(original_img.height, translated_img.height, diff_img.height)

                    combined = Image.new('RGB', (total_width, max_height), (255, 255, 255))
                    combined.paste(original_img, (0, 0))
                    combined.paste(translated_img, (original_img.width, 0))
                    combined.paste(diff_img, (original_img.width * 2, 0))
                else:
                    # Fallback to 2 panels if diff failed
                    total_width = original_img.width * 2
                    max_height = max(original_img.height, translated_img.height)

                    combined = Image.new('RGB', (total_width, max_height), (255, 255, 255))
                    combined.paste(original_img, (0, 0))
                    combined.paste(translated_img, (original_img.width, 0))
            else:
                # Just original | translated
                total_width = original_img.width * 2
                max_height = max(original_img.height, translated_img.height)

                combined = Image.new('RGB', (total_width, max_height), (255, 255, 255))
                combined.paste(original_img, (0, 0))
                combined.paste(translated_img, (original_img.width, 0))

            # Save
            output_file = output_path / f"page_{page_num:03d}_sidebyside.png"
            combined.save(str(output_file))

            if verbose:
                panels = "3 panels" if (include_diff and diff_img) else "2 panels"
                print(f"   ✓ Page {page_num}: {output_file.name} ({panels})")

        original_doc.close()
        translated_doc.close()

        if verbose:
            print(f"   ✓ Comparison images saved to: {output_dir}/\n")

        return True

    except Exception as e:
        if verbose:
            print(f"   ✗ Error: {e}\n")
        return False


def visualize_overflow_regions(
    translated_pdf: str,
    translated_json_dir: str,
    output_dir: str = "pdf_workspace/comparison",
    verbose: bool = True
) -> bool:
    """
    Highlight text blocks that had overflow warnings with bounding boxes.

    Reads translated JSON files to find overflow_warning=True blocks,
    then renders PDF pages with red rectangles around those regions.

    Args:
        translated_pdf: Path to translated PDF
        translated_json_dir: Directory with translated JSON files
        output_dir: Output directory for overflow visualizations
        verbose: Print progress messages

    Returns:
        True if successful, False otherwise
    """
    try:
        from PIL import ImageDraw
    except ImportError:
        if verbose:
            print("  ⚠ Pillow not installed, skipping overflow visualization")
        return False

    if verbose:
        print(f"6. Overflow Region Visualization (Phase 2)")

    try:
        doc = fitz.open(translated_pdf)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        json_path = Path(translated_json_dir)
        overflow_pages = []

        for page_num in range(1, len(doc) + 1):
            json_file = json_path / f"page_{page_num:03d}.json"

            if not json_file.exists():
                continue

            with open(json_file, "r", encoding="utf-8") as f:
                page_data = json.load(f)

            # Find blocks with overflow warnings
            overflow_blocks = [
                block for block in page_data.get("blocks", [])
                if block.get("overflow_warning", False)
            ]

            if not overflow_blocks:
                continue

            overflow_pages.append(page_num)

            # Render page
            page = doc[page_num - 1]
            pix = page.get_pixmap(dpi=150)
            img = pix_to_pil(pix)

            if not img:
                continue

            # Draw rectangles around overflow regions
            draw = ImageDraw.Draw(img)

            for block in overflow_blocks:
                bbox = block["bbox"]
                # Convert PDF coordinates to image coordinates (DPI scaling)
                scale = 150 / 72  # 150 DPI / 72 points per inch
                x0, y0, x1, y1 = [coord * scale for coord in bbox]

                # Draw red rectangle
                draw.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=3)

                # Add label with font size info
                original_size = block.get("size", 12)
                suggested_size = block.get("suggested_size", original_size)
                label = f"{original_size:.1f}→{suggested_size:.1f}pt"
                draw.text((x0, y0 - 15), label, fill=(255, 0, 0))

            # Save
            output_file = output_path / f"page_{page_num:03d}_overflow.png"
            img.save(str(output_file))

            if verbose:
                print(f"   ✓ Page {page_num}: {len(overflow_blocks)} overflow regions highlighted")

        doc.close()

        if verbose:
            print(f"   Total pages with overflow: {len(overflow_pages)}\n")

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
        help="Generate visual comparison for pages (e.g., '1,5,10') - Phase 1"
    )

    # Phase 2: Enhanced visual comparison arguments
    parser.add_argument(
        "--visual-diff",
        metavar="PAGES",
        help="Generate side-by-side comparison with diff overlay (e.g., '1,5,10') - Phase 2"
    )

    parser.add_argument(
        "--visual-overflow",
        action="store_true",
        help="Visualize overflow regions on translated PDF (requires --translated-dir) - Phase 2"
    )

    parser.add_argument(
        "--translated-dir",
        default="pdf_workspace/translated",
        help="Directory with translated JSON files for overflow visualization (default: pdf_workspace/translated)"
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

    # Phase 2: Enhanced visual comparison (if requested)
    if args.visual_diff and args.original:
        page_nums = [int(p.strip()) for p in args.visual_diff.split(",")]
        sidebyside_ok = create_side_by_side_comparison(
            args.original,
            args.translated_pdf,
            page_nums,
            args.comparison_dir,
            include_diff=True,
            verbose=verbose
        )
        results.append(("Side-by-Side Comparison", sidebyside_ok))

    # Phase 2: Overflow visualization (if requested)
    if args.visual_overflow:
        overflow_ok = visualize_overflow_regions(
            args.translated_pdf,
            args.translated_dir,
            args.comparison_dir,
            verbose=verbose
        )
        results.append(("Overflow Visualization", overflow_ok))

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
