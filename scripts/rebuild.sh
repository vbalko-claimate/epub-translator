#!/bin/bash
# EPUB Rebuilder - Compile translated files back into EPUB
# Usage: ./rebuild.sh <output.epub>

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
OUTPUT="$1"
WORKSPACE="epub_workspace/translated"

# Show usage if no output name provided
if [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <output.epub>"
    echo
    echo "Example:"
    echo "  $0 translated_book.epub"
    echo
    echo "This will compile files from:"
    echo "  $WORKSPACE/"
    echo
    echo "Into a valid EPUB archive"
    exit 1
fi

# Add .epub extension if not present
if [[ ! "$OUTPUT" =~ \.epub$ ]]; then
    OUTPUT="${OUTPUT}.epub"
fi

# Check if workspace exists
if [ ! -d "$WORKSPACE" ]; then
    echo -e "${RED}Error: Workspace directory '$WORKSPACE' not found${NC}"
    echo "Did you run ./extract.sh first?"
    exit 1
fi

# Check if mimetype file exists
if [ ! -f "$WORKSPACE/mimetype" ]; then
    echo -e "${RED}Error: mimetype file not found in $WORKSPACE${NC}"
    echo "The EPUB structure appears to be corrupted"
    exit 1
fi

echo -e "${BLUE}📦 EPUB Rebuilder${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Output: $OUTPUT"
echo "Source: $WORKSPACE"
echo

# Remove existing output file if present
if [ -f "$OUTPUT" ]; then
    echo -e "${YELLOW}⚠${NC}  Output file exists, removing..."
    rm -f "$OUTPUT"
fi

# Change to workspace directory
cd "$WORKSPACE" || exit 1

# Step 1: Add mimetype (MUST be first, MUST be uncompressed)
echo -e "${GREEN}→${NC} Adding mimetype (uncompressed)..."
zip -0 -X "../../$OUTPUT" mimetype

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to add mimetype${NC}"
    cd ../..
    exit 1
fi

# Step 2: Add META-INF directory
if [ -d "META-INF" ]; then
    echo -e "${GREEN}→${NC} Adding META-INF/..."
    zip -r "../../$OUTPUT" META-INF/
else
    echo -e "${YELLOW}⚠${NC}  Warning: META-INF directory not found"
fi

# Step 3: Add OEBPS (or whatever the content folder is called)
# Find the content folder (could be OEBPS, EPUB, OPS, content, etc.)
CONTENT_DIR=""
for dir in OEBPS EPUB OPS content Content; do
    if [ -d "$dir" ]; then
        CONTENT_DIR="$dir"
        break
    fi
done

if [ -n "$CONTENT_DIR" ]; then
    echo -e "${GREEN}→${NC} Adding $CONTENT_DIR/..."
    zip -r "../../$OUTPUT" "$CONTENT_DIR/"
else
    echo -e "${RED}Error: Content directory not found${NC}"
    echo "Expected one of: OEBPS, EPUB, OPS, content"
    cd ../..
    exit 1
fi

# Return to original directory
cd ../..

echo
echo -e "${GREEN}✓ EPUB created successfully!${NC}"
echo
echo "File: $OUTPUT"
echo "Size: $(du -h "$OUTPUT" | cut -f1)"
echo

# Quick validation
echo -e "${GREEN}→${NC} Running quick validation..."
if unzip -t "$OUTPUT" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} ZIP integrity check: PASSED"
else
    echo -e "${RED}✗${NC} ZIP integrity check: FAILED"
    echo "The EPUB may be corrupted"
    exit 1
fi

# Count files
FILE_COUNT=$(unzip -l "$OUTPUT" | tail -1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Files in archive: $FILE_COUNT"

echo
echo "Next steps:"
echo "  1. Test the EPUB in a reader:"
echo "     open $OUTPUT"
echo
echo "  2. Or validate with EPUBCheck:"
echo "     java -jar epubcheck.jar $OUTPUT"
echo
echo "  3. If there are issues, run:"
echo "     ./validate.sh $OUTPUT"
echo
