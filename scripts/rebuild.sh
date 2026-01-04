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

    # Defensive check: Warn if we're about to add a lot of files
    FILE_COUNT=$(find "$CONTENT_DIR" -type f | wc -l | tr -d ' ')
    XHTML_COUNT=$(find "$CONTENT_DIR" -type f -name "*.xhtml" | wc -l | tr -d ' ')

    echo "  Files to add: $FILE_COUNT (including $XHTML_COUNT XHTML files)"

    # Verify we're using the translated workspace, not original
    if [ -d "../original/$CONTENT_DIR" ]; then
        # Compare file sizes to detect if we're using original vs translated
        SAMPLE_FILE=$(find "$CONTENT_DIR" -type f -name "*.xhtml" | head -1)
        if [ -n "$SAMPLE_FILE" ]; then
            ORIG_SAMPLE="../original/$SAMPLE_FILE"
            if [ -f "$ORIG_SAMPLE" ]; then
                TRANS_SIZE=$(stat -f%z "$SAMPLE_FILE" 2>/dev/null || stat -c%s "$SAMPLE_FILE" 2>/dev/null)
                ORIG_SIZE=$(stat -f%z "$ORIG_SAMPLE" 2>/dev/null || stat -c%s "$ORIG_SAMPLE" 2>/dev/null)

                if [ "$TRANS_SIZE" -eq "$ORIG_SIZE" ]; then
                    echo -e "${YELLOW}⚠${NC}  WARNING: Files appear unchanged from original!"
                    echo "  This may mean translation didn't happen."
                    echo "  Sample: $(basename "$SAMPLE_FILE") is $TRANS_SIZE bytes (same as original)"
                    echo
                    read -p "Continue anyway? (y/N): " -n 1 -r
                    echo
                    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                        echo "Rebuild cancelled."
                        cd ../..
                        exit 1
                    fi
                fi
            fi
        fi
    fi

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
echo -e "${BLUE}→${NC} Running rebuild verification..."
echo

# Run verification script if available
if [ -f "scripts/verify_rebuild.sh" ]; then
    if ./scripts/verify_rebuild.sh "$OUTPUT"; then
        echo -e "${GREEN}✓${NC} Rebuild verification PASSED"
    else
        echo -e "${RED}✗${NC} Rebuild verification FAILED"
        echo
        echo "The rebuilt EPUB does NOT match the workspace!"
        echo "This means the translation may not have been applied."
        echo
        echo "Possible causes:"
        echo "  1. Translation agents didn't save files properly"
        echo "  2. Wrong workspace directory used"
        echo "  3. Files were reverted after translation"
        echo
        exit 1
    fi
else
    echo -e "${YELLOW}⚠${NC}  Verification script not found, skipping..."
fi

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
