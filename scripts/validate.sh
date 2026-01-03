#!/bin/bash
# EPUB Validator - Check EPUB structure and integrity
# Usage: ./validate.sh <book.epub>

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
EPUB_FILE="$1"

# Show usage if no file provided
if [ -z "$EPUB_FILE" ]; then
    echo "Usage: $0 <file.epub>"
    echo
    echo "Example:"
    echo "  $0 translated_book.epub"
    echo
    echo "This will check:"
    echo "  - ZIP integrity"
    echo "  - EPUB structure"
    echo "  - Required files presence"
    echo "  - XML validity (basic)"
    exit 1
fi

# Check if file exists
if [ ! -f "$EPUB_FILE" ]; then
    echo -e "${RED}Error: File '$EPUB_FILE' not found${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 EPUB Validator${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "File: $EPUB_FILE"
echo "Size: $(du -h "$EPUB_FILE" | cut -f1)"
echo

ERRORS=0
WARNINGS=0

# Test 1: ZIP Integrity
echo -e "${BLUE}Test 1: ZIP Integrity${NC}"
if unzip -t "$EPUB_FILE" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} ZIP archive is valid"
else
    echo -e "${RED}✗${NC} ZIP archive is corrupted"
    ((ERRORS++))
fi

# Test 2: Check mimetype
echo
echo -e "${BLUE}Test 2: Mimetype${NC}"
MIMETYPE=$(unzip -p "$EPUB_FILE" mimetype 2>/dev/null || echo "")
if [ "$MIMETYPE" = "application/epub+zip" ]; then
    echo -e "${GREEN}✓${NC} Mimetype is correct"
else
    echo -e "${RED}✗${NC} Mimetype is incorrect or missing"
    echo "  Expected: application/epub+zip"
    echo "  Found: $MIMETYPE"
    ((ERRORS++))
fi

# Test 3: Required files
echo
echo -e "${BLUE}Test 3: Required Files${NC}"

# Check META-INF/container.xml
if unzip -l "$EPUB_FILE" | grep -q "META-INF/container.xml"; then
    echo -e "${GREEN}✓${NC} META-INF/container.xml found"
else
    echo -e "${RED}✗${NC} META-INF/container.xml missing"
    ((ERRORS++))
fi

# Check content.opf (should be present)
if unzip -l "$EPUB_FILE" | grep -q "content.opf"; then
    echo -e "${GREEN}✓${NC} content.opf found"
else
    echo -e "${YELLOW}⚠${NC}  content.opf not found (might have different name)"
    ((WARNINGS++))
fi

# Check toc.ncx
if unzip -l "$EPUB_FILE" | grep -q "toc.ncx"; then
    echo -e "${GREEN}✓${NC} toc.ncx found"
else
    echo -e "${YELLOW}⚠${NC}  toc.ncx not found (might be EPUB 3)"
    ((WARNINGS++))
fi

# Test 4: File count
echo
echo -e "${BLUE}Test 4: Structure${NC}"
FILE_COUNT=$(unzip -l "$EPUB_FILE" | grep -c "^-" || echo "0")
echo "  Total files: $FILE_COUNT"

XHTML_COUNT=$(unzip -l "$EPUB_FILE" | grep -c "\.xhtml$" || echo "0")
echo "  XHTML files: $XHTML_COUNT"

HTML_COUNT=$(unzip -l "$EPUB_FILE" | grep -c "\.html$" || echo "0")
echo "  HTML files: $HTML_COUNT"

CSS_COUNT=$(unzip -l "$EPUB_FILE" | grep -c "\.css$" || echo "0")
echo "  CSS files: $CSS_COUNT"

IMAGE_COUNT=$(unzip -l "$EPUB_FILE" | grep -cE "\.(jpg|jpeg|png|gif|svg)$" || echo "0")
echo "  Images: $IMAGE_COUNT"

if [ "$XHTML_COUNT" -eq 0 ] && [ "$HTML_COUNT" -eq 0 ]; then
    echo -e "${RED}✗${NC} No content files found"
    ((ERRORS++))
else
    echo -e "${GREEN}✓${NC} Content files present"
fi

# Test 5: XML Validation (basic)
echo
echo -e "${BLUE}Test 5: XML Validation (Basic)${NC}"
TEMP_DIR=$(mktemp -d)
unzip -q "$EPUB_FILE" -d "$TEMP_DIR"

# Check container.xml
if command -v xmllint &> /dev/null; then
    if [ -f "$TEMP_DIR/META-INF/container.xml" ]; then
        if xmllint --noout "$TEMP_DIR/META-INF/container.xml" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} container.xml is valid XML"
        else
            echo -e "${RED}✗${NC} container.xml has XML errors"
            ((ERRORS++))
        fi
    fi

    # Check first XHTML file
    FIRST_XHTML=$(find "$TEMP_DIR" -name "*.xhtml" | head -1)
    if [ -n "$FIRST_XHTML" ]; then
        if xmllint --noout "$FIRST_XHTML" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} Sample XHTML file is valid XML"
        else
            echo -e "${RED}✗${NC} Sample XHTML file has XML errors"
            echo "  File: $(basename "$FIRST_XHTML")"
            ((ERRORS++))
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC}  xmllint not installed, skipping XML validation"
    echo "  Install with: brew install libxml2 (macOS) or apt-get install libxml2-utils (Linux)"
    ((WARNINGS++))
fi

# Cleanup
rm -rf "$TEMP_DIR"

# Test 6: Recommended checks
echo
echo -e "${BLUE}Test 6: Recommended (EPUBCheck)${NC}"
if command -v java &> /dev/null; then
    if [ -f "epubcheck.jar" ]; then
        echo "Running EPUBCheck..."
        java -jar epubcheck.jar "$EPUB_FILE"
    else
        echo -e "${YELLOW}⚠${NC}  EPUBCheck not found in current directory"
        echo "  Download from: https://github.com/w3c/epubcheck/releases"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC}  Java not installed, cannot run EPUBCheck"
    echo "  Install Java to use official EPUB validator"
    ((WARNINGS++))
fi

# Summary
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo
    echo "Your EPUB is valid and ready to use."
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ ${WARNINGS} warning(s)${NC}"
    echo
    echo "EPUB is valid but has some minor issues."
    echo "It should work in most readers."
    exit 0
else
    echo -e "${RED}✗ ${ERRORS} error(s), ${WARNINGS} warning(s)${NC}"
    echo
    echo "EPUB has structural problems that should be fixed."
    echo "It may not work properly in all readers."
    exit 1
fi
