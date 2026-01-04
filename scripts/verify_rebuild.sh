#!/bin/bash
# EPUB Rebuild Verification - Ensure rebuilt EPUB contains translated content
# Usage: ./verify_rebuild.sh <epub_file>

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

EPUB_FILE="$1"
WORKSPACE="epub_workspace/translated"

if [ -z "$EPUB_FILE" ]; then
    echo "Usage: $0 <rebuilt.epub>"
    echo
    echo "This verifies that the rebuilt EPUB contains"
    echo "the translated files from the workspace."
    exit 1
fi

if [ ! -f "$EPUB_FILE" ]; then
    echo -e "${RED}Error: EPUB file not found: $EPUB_FILE${NC}"
    exit 1
fi

if [ ! -d "$WORKSPACE" ]; then
    echo -e "${RED}Error: Workspace not found: $WORKSPACE${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 EPUB Rebuild Verification${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "EPUB: $EPUB_FILE"
echo "Workspace: $WORKSPACE"
echo

# Create temp directory for extraction
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Extract EPUB to temp
echo -e "${GREEN}→${NC} Extracting EPUB to temporary location..."
unzip -q "$EPUB_FILE" -d "$TEMP_DIR"

# Find content directory in both workspace and EPUB
WORKSPACE_CONTENT=""
for dir in OEBPS EPUB OPS content Content; do
    if [ -d "$WORKSPACE/$dir" ]; then
        WORKSPACE_CONTENT="$WORKSPACE/$dir"
        break
    fi
done

EPUB_CONTENT=""
for dir in OEBPS EPUB OPS content Content; do
    if [ -d "$TEMP_DIR/$dir" ]; then
        EPUB_CONTENT="$TEMP_DIR/$dir"
        break
    fi
done

if [ -z "$WORKSPACE_CONTENT" ]; then
    echo -e "${RED}✗ Could not find content directory in workspace${NC}"
    exit 1
fi

if [ -z "$EPUB_CONTENT" ]; then
    echo -e "${RED}✗ Could not find content directory in EPUB${NC}"
    exit 1
fi

echo -e "${GREEN}→${NC} Found content directories:"
echo "  Workspace: $WORKSPACE_CONTENT"
echo "  EPUB: $EPUB_CONTENT"
echo

# Check 1: File count comparison
WORKSPACE_FILES=$(find "$WORKSPACE_CONTENT" -type f -name "*.xhtml" | wc -l | tr -d ' ')
EPUB_FILES=$(find "$EPUB_CONTENT" -type f -name "*.xhtml" | wc -l | tr -d ' ')

echo -e "${GREEN}→${NC} Checking file counts..."
echo "  Workspace XHTML files: $WORKSPACE_FILES"
echo "  EPUB XHTML files: $EPUB_FILES"

if [ "$WORKSPACE_FILES" -ne "$EPUB_FILES" ]; then
    echo -e "${RED}✗ File count mismatch!${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} File counts match"
echo

# Check 2: File size comparison
echo -e "${GREEN}→${NC} Checking file sizes..."
MISMATCH=0

for workspace_file in "$WORKSPACE_CONTENT"/*.xhtml; do
    if [ -f "$workspace_file" ]; then
        filename=$(basename "$workspace_file")
        epub_file="$EPUB_CONTENT/$filename"

        if [ ! -f "$epub_file" ]; then
            echo -e "${RED}✗${NC} Missing in EPUB: $filename"
            MISMATCH=1
            continue
        fi

        workspace_size=$(stat -f%z "$workspace_file" 2>/dev/null || stat -c%s "$workspace_file" 2>/dev/null)
        epub_size=$(stat -f%z "$epub_file" 2>/dev/null || stat -c%s "$epub_file" 2>/dev/null)

        if [ "$workspace_size" -ne "$epub_size" ]; then
            echo -e "${YELLOW}⚠${NC}  Size mismatch: $filename"
            echo "    Workspace: $workspace_size bytes"
            echo "    EPUB: $epub_size bytes"
            MISMATCH=1
        fi
    fi
done

if [ $MISMATCH -eq 1 ]; then
    echo -e "${RED}✗ File size mismatches detected!${NC}"
    echo
    echo "This means the rebuilt EPUB contains DIFFERENT files"
    echo "than what's in the workspace. The rebuild may have"
    echo "used the wrong source directory."
    exit 1
fi

echo -e "${GREEN}✓${NC} All file sizes match"
echo

# Check 3: Content sampling (check if files are actually translated)
echo -e "${GREEN}→${NC} Content sampling (checking for translation)..."

# Sample 3 random files
SAMPLE_FILES=$(find "$WORKSPACE_CONTENT" -type f -name "*.xhtml" | head -3)
UNTRANSLATED=0

for workspace_file in $SAMPLE_FILES; do
    filename=$(basename "$workspace_file")
    epub_file="$EPUB_CONTENT/$filename"

    if [ -f "$epub_file" ]; then
        # Compare MD5 checksums
        workspace_md5=$(md5 -q "$workspace_file" 2>/dev/null || md5sum "$workspace_file" | cut -d' ' -f1)
        epub_md5=$(md5 -q "$epub_file" 2>/dev/null || md5sum "$epub_file" | cut -d' ' -f1)

        if [ "$workspace_md5" = "$epub_md5" ]; then
            echo -e "${GREEN}✓${NC} $filename - checksums match"
        else
            echo -e "${RED}✗${NC} $filename - checksums DO NOT match"
            UNTRANSLATED=1
        fi
    fi
done

if [ $UNTRANSLATED -eq 1 ]; then
    echo
    echo -e "${RED}✗ Content mismatch detected!${NC}"
    echo
    echo "The EPUB files differ from workspace files."
    echo "This suggests the rebuild used the wrong source."
    exit 1
fi

echo

# Final verdict
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ VERIFICATION PASSED${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo "The rebuilt EPUB contains the translated files"
echo "from the workspace. Translation successful!"
echo
