#!/bin/bash
# EPUB Extractor - Extract EPUB archive to workspace for translation
# Usage: ./extract.sh <book.epub>

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
EPUB_FILE="$1"
WORKSPACE="epub_workspace"

# Show usage if no file provided
if [ -z "$EPUB_FILE" ]; then
    echo "Usage: $0 <file.epub>"
    echo
    echo "Example:"
    echo "  $0 my-book.epub"
    echo
    echo "This will create:"
    echo "  epub_workspace/original/   - Backup copy (never modify)"
    echo "  epub_workspace/translated/ - Working copy (translate this)"
    echo "  epub_workspace/temp/       - Temporary files"
    exit 1
fi

# Check if file exists
if [ ! -f "$EPUB_FILE" ]; then
    echo -e "${RED}Error: File '$EPUB_FILE' not found${NC}"
    exit 1
fi

# Check if file is a ZIP archive (EPUB is ZIP)
if ! file "$EPUB_FILE" | grep -q "Zip archive"; then
    echo -e "${RED}Error: '$EPUB_FILE' is not a valid EPUB file (not a ZIP archive)${NC}"
    exit 1
fi

echo -e "${BLUE}📚 EPUB Extractor${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "File: $EPUB_FILE"
echo

# Create workspace directories
echo -e "${GREEN}→${NC} Creating workspace directories..."
mkdir -p "$WORKSPACE"/{original,translated,temp}

# Extract to original directory
echo -e "${GREEN}→${NC} Extracting EPUB to $WORKSPACE/original/..."
unzip -q "$EPUB_FILE" -d "$WORKSPACE/original/"

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to extract EPUB${NC}"
    exit 1
fi

# Copy to translated directory (working copy)
echo -e "${GREEN}→${NC} Creating working copy in $WORKSPACE/translated/..."
cp -r "$WORKSPACE/original/"* "$WORKSPACE/translated/"

echo
echo -e "${GREEN}✓ EPUB extracted successfully!${NC}"
echo
echo "Structure:"
echo "  📁 $WORKSPACE/"
echo "    ├── original/    ← Backup (never modify)"
echo "    ├── translated/  ← Working copy (translate this)"
echo "    └── temp/        ← Temporary files"
echo
echo "Next steps:"
echo "  1. Identify content files:"
echo "     ls $WORKSPACE/translated/OEBPS/*.xhtml"
echo
echo "  2. Start translating chapters"
echo
echo "  3. When done, rebuild with:"
echo "     ./rebuild.sh output_name.epub"
echo
