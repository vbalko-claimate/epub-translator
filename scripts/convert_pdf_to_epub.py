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
    Extract text content AND images from PDF with basic structure.

    Returns:
        tuple: (chapters, images)
        chapters: list of dicts with {"title", "content", "image_refs"}
        images: dict of {image_id: {"data": bytes, "ext": str, "page": int, "bbox": tuple}}
    """
    doc = fitz.open(pdf_path)
    chapters = []
    all_images = {}
    image_counter = 0

    current_chapter = {"title": "Chapter 1", "content": "", "image_refs": []}
    chapter_num = 1

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()

        # Extract images from this page
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]  # Image xref ID

            try:
                # Extract image data
                base_image = doc.extract_image(xref)
                image_data = base_image["image"]  # Binary data
                image_ext = base_image["ext"]     # Extension (jpg, png, etc.)

                # Get image position on page
                img_rects = page.get_image_rects(xref)
                bbox = img_rects[0] if img_rects else page.rect

                # Filter out tiny images (likely decorative)
                width = bbox.width if hasattr(bbox, 'width') else (bbox[2] - bbox[0])
                height = bbox.height if hasattr(bbox, 'height') else (bbox[3] - bbox[1])

                if width < 100 or height < 100:
                    continue  # Skip decorative/small images

                # Store image
                image_id = f"image_{image_counter:03d}"
                all_images[image_id] = {
                    "data": image_data,
                    "ext": image_ext,
                    "page": page_num,
                    "bbox": bbox,
                    "filename": f"{image_id}.{image_ext}"
                }

                # Add reference to current chapter
                y_position = bbox[1] if isinstance(bbox, (list, tuple)) else bbox.y0
                current_chapter["image_refs"].append({
                    "id": image_id,
                    "y_position": y_position,  # Top Y coordinate for ordering
                    "alt": f"Image {image_counter + 1}"
                })

                image_counter += 1
            except Exception as e:
                # Skip problematic images
                print(f"Warning: Could not extract image on page {page_num}: {e}", file=sys.stderr)
                continue

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
            current_chapter = {"title": f"Chapter {chapter_num}", "content": "", "image_refs": []}

        # Add page content
        current_chapter["content"] += f"\n\n{text}"

    # Add last chapter
    if current_chapter["content"].strip():
        chapters.append(current_chapter)

    total_pages = len(doc)
    doc.close()

    # If only one chapter detected, split by page count
    if len(chapters) == 1 and total_pages > 10:
        # Split into 10-page chunks (need to redistribute images)
        old_chapter = chapters[0]
        chapters = []
        doc = fitz.open(pdf_path)

        for i in range(0, total_pages, 10):
            chunk_text = ""
            chunk_images = []

            for page_num in range(i, min(i + 10, total_pages)):
                chunk_text += doc[page_num].get_text() + "\n\n"

                # Find images for this page range
                for img_ref in old_chapter.get("image_refs", []):
                    img_page = all_images[img_ref["id"]]["page"]
                    if img_page >= (i + 1) and img_page <= min(i + 10, total_pages):
                        chunk_images.append(img_ref)

            chapters.append({
                "title": f"Pages {i+1}-{min(i+10, total_pages)}",
                "content": chunk_text,
                "image_refs": chunk_images
            })
        doc.close()

    return chapters, all_images


def create_epub(chapters, images, output_path, title="Converted Book", author="Unknown"):
    """
    Create EPUB from extracted chapters AND images.

    Args:
        chapters: List of {"title": str, "content": str, "image_refs": list}
        images: Dict of {image_id: {"data": bytes, "ext": str, ...}}
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

    # Add images to EPUB
    epub_images = {}
    for image_id, img_data in images.items():
        epub_img = epub.EpubImage()
        epub_img.file_name = f'Images/{img_data["filename"]}'
        epub_img.content = img_data["data"]

        # Determine media type
        media_type = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'tif': 'image/tiff',
            'tiff': 'image/tiff'
        }.get(img_data["ext"].lower(), 'image/jpeg')
        epub_img.media_type = media_type

        book.add_item(epub_img)
        epub_images[image_id] = epub_img.file_name

    # Create chapters with embedded images
    epub_chapters = []
    spine = ['nav']

    for i, chapter_data in enumerate(chapters, start=1):
        chapter = epub.EpubHtml(
            title=chapter_data["title"],
            file_name=f'chap_{i:03d}.xhtml',
            lang='en'
        )

        # Build HTML content with text AND images
        html_content = f'<h1>{chapter_data["title"]}</h1>\n'

        # Convert plain text to HTML paragraphs
        paragraphs = chapter_data["content"].split('\n\n')

        # Sort images by Y position
        sorted_images = sorted(
            chapter_data.get("image_refs", []),
            key=lambda x: x["y_position"]
        )

        # Add text paragraphs
        for para in paragraphs:
            para = para.strip()
            if para:
                # Escape HTML
                para = para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_content += f'<p>{para}</p>\n'

        # Add images at end of chapter content
        # (Strategy: Simple end-of-chapter placement for reliability)
        if sorted_images:
            html_content += '\n'
            for img_ref in sorted_images:
                img_path = epub_images[img_ref["id"]]
                html_content += f'<figure>\n'
                html_content += f'  <img src="{img_path}" alt="{img_ref["alt"]}" style="max-width: 100%; height: auto;" />\n'
                html_content += f'</figure>\n'

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
    Convert PDF to EPUB with text AND images.

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

    # Extract content and images
    if verbose:
        print("Extracting text and images from PDF...")

    chapters, images = extract_pdf_content(str(pdf_file))

    if verbose:
        print(f"  ✓ Detected {len(chapters)} chapters")
        print(f"  ✓ Extracted {len(images)} images")

    # Create EPUB with embedded images
    if verbose:
        print("Creating EPUB with embedded images...")

    title = pdf_file.stem.replace('_', ' ').title()
    create_epub(chapters, images, str(epub_path), title=title)

    if verbose:
        print(f"\n✓ Conversion complete: {epub_path}")
        print(f"  Chapters: {len(chapters)}")
        print(f"  Images: {len(images)}")
        print()
        print("Next steps:")
        print(f'  1. Verify EPUB: open "{epub_path}"')
        print(f'  2. Translate: claude "translate {epub_path} from Czech to English"')
        print()
        print("Note: Chapter detection is heuristic. You may need to manually")
        print("      adjust chapter breaks in Calibre or Sigil.")
        if len(images) > 0:
            print()
            print("Image handling:")
            print(f"  - {len(images)} images extracted and embedded")
            print("  - Images placed at end of each chapter")
            print("  - Small images (<100x100px) filtered out")

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
