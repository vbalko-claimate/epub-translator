#!/usr/bin/env python3
"""
PDF Text Extraction with Layout Preservation

Extracts text with coordinates, fonts, and structure from PDF files for translation.
Uses PyMuPDF (fitz) for fast and accurate extraction.

Usage:
    python extract_pdf.py <input.pdf> [--output-dir pdf_workspace/extracted]

Example:
    python extract_pdf.py book.pdf
    # Creates: pdf_workspace/extracted/page_001.json, page_002.json, ...
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
        'fitz': 'PyMuPDF',  # package name on PyPI
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
from typing import Dict, List, Tuple


def classify_text_type(bbox: List[float], font_size: float, page_rect: fitz.Rect) -> str:
    """
    Classify text block type based on position and font size.

    Args:
        bbox: Bounding box [x0, y0, x1, y1]
        font_size: Font size in points
        page_rect: Page rectangle for height calculation

    Returns:
        Text type: "header", "footer", "heading", "footnote", or "body"
    """
    y_position = bbox[1]  # Top y-coordinate
    page_height = page_rect.height

    # Header: Top 50px of page
    if y_position < 50:
        return "header"

    # Footer: Bottom 50px of page
    elif y_position > page_height - 50:
        return "footer"

    # Heading: Large font (>16pt)
    elif font_size > 16:
        return "heading"

    # Footnote: Small font (<10pt)
    elif font_size < 10:
        return "footnote"

    # Default: Body text
    else:
        return "body"


def extract_page_text(page: fitz.Page) -> Dict:
    """
    Extract text blocks with metadata from a PDF page.

    Args:
        page: PyMuPDF page object

    Returns:
        Dictionary containing page metadata and text blocks with:
        - page_num: Page number (1-indexed)
        - width: Page width in points
        - height: Page height in points
        - blocks: List of text blocks with text, bbox, font, size, type
    """
    # Extract text with detailed information
    blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)

    page_data = {
        "page_num": page.number + 1,  # 1-indexed
        "width": page.rect.width,
        "height": page.rect.height,
        "blocks": []
    }

    # Process each block
    for block in blocks["blocks"]:
        if block["type"] != 0:  # Skip non-text blocks (images, etc.)
            continue

        # Process each line in the block
        for line in block["lines"]:
            line_text = ""
            line_bbox = None
            line_font = None
            line_size = None
            line_flags = None
            line_color = None

            # Merge spans (text segments) into full line
            for span in line["spans"]:
                line_text += span["text"]

                # Merge bounding boxes for full line
                if line_bbox is None:
                    line_bbox = list(span["bbox"])
                else:
                    # Extend bbox to encompass all spans
                    line_bbox[0] = min(line_bbox[0], span["bbox"][0])  # Left
                    line_bbox[1] = min(line_bbox[1], span["bbox"][1])  # Top
                    line_bbox[2] = max(line_bbox[2], span["bbox"][2])  # Right
                    line_bbox[3] = max(line_bbox[3], span["bbox"][3])  # Bottom

                # Use first span's font properties (assume consistent per line)
                if line_font is None:
                    line_font = span["font"]
                    line_size = span["size"]
                    line_flags = span["flags"]  # Bold, italic, etc.
                    line_color = span["color"]

            # Skip empty lines
            if not line_text.strip():
                continue

            # Classify text type
            text_type = classify_text_type(line_bbox, line_size, page.rect)

            # Add block to page data
            page_data["blocks"].append({
                "text": line_text.strip(),
                "bbox": line_bbox,
                "font": line_font,
                "size": line_size,
                "flags": line_flags,
                "color": line_color,
                "type": text_type
            })

    return page_data


def extract_pdf(
    pdf_path: str,
    output_dir: str = "pdf_workspace/extracted",
    verbose: bool = True
) -> Tuple[int, int]:
    """
    Extract all pages from PDF to JSON files.

    Args:
        pdf_path: Path to input PDF file
        output_dir: Output directory for JSON files
        verbose: Print progress messages

    Returns:
        Tuple of (total_pages, total_blocks)

    Raises:
        FileNotFoundError: If PDF file not found
        Exception: If PDF cannot be opened or processed
    """
    # Validate input
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"\nExtracting PDF: {pdf_path}")
        print(f"Output directory: {output_dir}\n")

    # Open PDF
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise Exception(f"Cannot open PDF: {e}")

    total_pages = len(doc)
    total_blocks = 0

    if verbose:
        print(f"Processing {total_pages} pages...\n")

    # Extract each page
    for page in doc:
        page_data = extract_page_text(page)
        page_num = page_data["page_num"]
        block_count = len(page_data["blocks"])
        total_blocks += block_count

        # Save to JSON
        output_file = output_path / f"page_{page_num:03d}.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)

        if verbose:
            print(f"  ✓ Page {page_num:3d}: {block_count:4d} text blocks → {output_file.name}")

    # Close PDF
    doc.close()

    if verbose:
        print(f"\n✓ Extraction complete!")
        print(f"  Pages processed: {total_pages}")
        print(f"  Total text blocks: {total_blocks}")
        print(f"  Average blocks/page: {total_blocks / total_pages:.1f}")
        print(f"  Output: {output_dir}/\n")

    return total_pages, total_blocks


def main():
    """Command-line interface for PDF extraction."""
    parser = argparse.ArgumentParser(
        description="Extract text with layout information from PDF files",
        epilog="Example: python extract_pdf.py book.pdf"
    )

    parser.add_argument(
        "pdf_file",
        help="Path to input PDF file"
    )

    parser.add_argument(
        "-o", "--output-dir",
        default="pdf_workspace/extracted",
        help="Output directory for JSON files (default: pdf_workspace/extracted)"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress messages"
    )

    args = parser.parse_args()

    try:
        extract_pdf(
            pdf_path=args.pdf_file,
            output_dir=args.output_dir,
            verbose=not args.quiet
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
