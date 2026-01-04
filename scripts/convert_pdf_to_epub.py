#!/usr/bin/env python3
"""
PDF to EPUB Converter (Pure Python)

Converts PDF to EPUB using PyMuPDF + ebooklib.
No external dependencies like Calibre required.

Usage:
    python convert_pdf_to_epub.py <input.pdf> [output.epub]

Example:
    python convert_pdf_to_epub.py book.pdf book.epub
"""

import sys
import subprocess
from pathlib import Path


def check_and_install_dependencies():
    """
    Check and auto-install required dependencies.

    CRITICAL: This function MUST install all dependencies automatically
    without user intervention. No manual pip install commands allowed!
    """
    required = {
        'fitz': 'PyMuPDF',      # PDF extraction
        'ebooklib': 'ebooklib'  # EPUB creation
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
            except subprocess.CalledProcessError:
                print(f"\n❌ Failed to install {package}", file=sys.stderr)
                print(f"Please install manually: pip install {package}\n", file=sys.stderr)
                sys.exit(1)

        print(f"✓ All dependencies installed!\n", file=sys.stderr)


# Install dependencies first
check_and_install_dependencies()

# Now import
import fitz  # PyMuPDF
from ebooklib import epub
import argparse


def extract_pdf_content(pdf_path):
    """
    Extract text content from PDF with basic structure.

    Returns:
        list of dicts: [{"title": "Chapter 1", "content": "..."}, ...]
    """
    doc = fitz.open(pdf_path)
    chapters = []

    current_chapter = {"title": "Chapter 1", "content": ""}
    chapter_num = 1

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()

        # Simple heuristic: New chapter if page starts with large text
        blocks = page.get_text("dict")["blocks"]

        is_new_chapter = False
        for block in blocks:
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        # Large font = potential heading
                        if span.get("size", 0) > 16:
                            is_new_chapter = True
                            break
                    if is_new_chapter:
                        break
            if is_new_chapter:
                break

        if is_new_chapter and current_chapter["content"].strip():
            # Save previous chapter
            chapters.append(current_chapter)
            chapter_num += 1
            current_chapter = {"title": f"Chapter {chapter_num}", "content": ""}

        # Add page content
        current_chapter["content"] += f"\n\n{text}"

    # Add last chapter
    if current_chapter["content"].strip():
        chapters.append(current_chapter)

    doc.close()

    # If only one chapter detected, split by page count
    if len(chapters) == 1 and len(doc) > 10:
        # Split into 10-page chunks
        chapters = []
        doc = fitz.open(pdf_path)
        for i in range(0, len(doc), 10):
            chunk_text = ""
            for page_num in range(i, min(i + 10, len(doc))):
                chunk_text += doc[page_num].get_text() + "\n\n"

            chapters.append({
                "title": f"Pages {i+1}-{min(i+10, len(doc))}",
                "content": chunk_text
            })
        doc.close()

    return chapters


def create_epub(chapters, output_path, title="Converted Book", author="Unknown"):
    """
    Create EPUB from extracted chapters.

    Args:
        chapters: List of {"title": str, "content": str}
        output_path: Output EPUB file path
        title: Book title
        author: Book author
    """
    book = epub.EpubBook()

    # Metadata
    book.set_identifier(f'id_{Path(output_path).stem}')
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # Create chapters
    epub_chapters = []
    spine = ['nav']

    for i, chapter_data in enumerate(chapters, start=1):
        chapter = epub.EpubHtml(
            title=chapter_data["title"],
            file_name=f'chap_{i:03d}.xhtml',
            lang='en'
        )

        # Convert plain text to HTML paragraphs
        paragraphs = chapter_data["content"].split('\n\n')
        html_content = f'<h1>{chapter_data["title"]}</h1>\n'

        for para in paragraphs:
            para = para.strip()
            if para:
                # Escape HTML
                para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_content += f'<p>{para}</p>\n'

        chapter.content = html_content

        book.add_item(chapter)
        epub_chapters.append(chapter)
        spine.append(chapter)

    # Table of contents
    book.toc = tuple(epub_chapters)

    # Navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Spine
    book.spine = spine

    # Write EPUB
    epub.write_epub(output_path, book)


def convert_pdf_to_epub(pdf_path, epub_path=None, verbose=True):
    """
    Convert PDF to EPUB.

    Args:
        pdf_path: Input PDF file
        epub_path: Output EPUB file (optional)
        verbose: Print progress
    """
    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        return False

    if epub_path is None:
        epub_path = pdf_file.with_suffix('.epub')
    else:
        epub_path = Path(epub_path)

    if verbose:
        print(f"Converting PDF to EPUB...")
        print(f"Input:  {pdf_path}")
        print(f"Output: {epub_path}")
        print()

    # Extract content
    if verbose:
        print("Extracting text from PDF...")

    chapters = extract_pdf_content(str(pdf_file))

    if verbose:
        print(f"  ✓ Detected {len(chapters)} chapters")

    # Create EPUB
    if verbose:
        print("Creating EPUB...")

    title = pdf_file.stem.replace('_', ' ').title()
    create_epub(chapters, str(epub_path), title=title)

    if verbose:
        print(f"\n✓ Conversion complete: {epub_path}")
        print()
        print("Next steps:")
        print(f'  1. Verify EPUB: open "{epub_path}"')
        print(f'  2. Translate: claude "translate {epub_path} from Czech to English"')
        print()
        print("Note: Chapter detection is heuristic. You may need to manually")
        print("      adjust chapter breaks in Calibre or Sigil.")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to EPUB using PyMuPDF + ebooklib",
        epilog="Example: python convert_pdf_to_epub.py book.pdf"
    )

    parser.add_argument("pdf_file", help="Input PDF file")
    parser.add_argument("-o", "--output", help="Output EPUB file (default: same name as PDF)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress progress messages")

    args = parser.parse_args()

    success = convert_pdf_to_epub(
        args.pdf_file,
        args.output,
        verbose=not args.quiet
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
