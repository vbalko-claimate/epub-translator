# EPUB Format Reference

Complete technical reference for EPUB structure and translation workflow.

## EPUB Basics

**EPUB (Electronic Publication)** is an open standard format for eBooks. Technically, it's a ZIP archive containing:
- XHTML content files
- CSS stylesheets
- Images and media
- Metadata files

## File Structure

```
book.epub (ZIP archive)
├── mimetype                    # MUST be first, uncompressed
├── META-INF/
│   ├── container.xml          # Points to content.opf
│   └── com.apple.ibooks.display-options.xml (optional)
└── OEBPS/                     # Content folder (name varies)
    ├── content.opf            # Package document (metadata)
    ├── toc.ncx                # Navigation Control for XML
    ├── *.xhtml                # Chapter files
    ├── css/                   # Stylesheets
    │   └── *.css
    └── image/                 # Media files
        └── *.jpg, *.png
```

## Critical Files

### 1. mimetype

**Location:** Root of ZIP
**Content:** Single line, no newline
**Purpose:** Identifies file as EPUB

```
application/epub+zip
```

**CRITICAL:** Must be:
- First file in ZIP archive
- Stored uncompressed (ZIP compression level 0)
- No trailing newline

### 2. META-INF/container.xml

**Purpose:** Points to the main OPF file

```xml
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf"
                  media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>
```

**Translation:** Don't modify this file

### 3. content.opf (Package Document)

**Purpose:** Metadata, manifest, spine (reading order)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf">
    <metadata>
        <dc:title>Book Title</dc:title>
        <dc:creator>Author Name</dc:creator>
        <dc:language>en-GB</dc:language>  <!-- ⚠️ CHANGE THIS -->
        <dc:identifier>ISBN-13</dc:identifier>
        <dc:date>2024-01-01</dc:date>
    </metadata>

    <manifest>
        <!-- List of all files in EPUB -->
        <item id="chapter1" href="chapter-1.xhtml" media-type="application/xhtml+xml"/>
        <item id="css1" href="css/style.css" media-type="text/css"/>
    </manifest>

    <spine toc="ncx">
        <!-- Reading order -->
        <itemref idref="chapter1"/>
        <itemref idref="chapter2"/>
    </spine>
</package>
```

**Translation tasks:**
- Change `<dc:language>` to target language code (e.g., `cs-CZ`, `de-DE`, `fr-FR`)
- Optionally update `<dc:title>` if translating title
- Keep all other metadata unchanged

### 4. toc.ncx (Navigation)

**Purpose:** Table of contents for eReader navigation

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="unique-id"/>
    </head>

    <docTitle>
        <text>Book Title</text>
    </docTitle>

    <navMap>
        <navPoint id="navpoint1" playOrder="1">
            <navLabel>
                <text>Prologue</text>  <!-- ⚠️ TRANSLATE THIS -->
            </navLabel>
            <content src="prologue.xhtml"/>
        </navPoint>

        <navPoint id="navpoint2" playOrder="2">
            <navLabel>
                <text>Chapter 1</text>  <!-- ⚠️ TRANSLATE THIS -->
            </navLabel>
            <content src="chapter-1.xhtml"/>
        </navPoint>
    </navMap>
</ncx>
```

**Translation tasks:**
- Translate all `<text>` elements inside `<navLabel>`
- Keep all other attributes and structure unchanged

### 5. Chapter XHTML Files

**Purpose:** Actual book content

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Chapter 1</title>
        <link href="css/style.css" rel="stylesheet" type="text/css"/>
    </head>
    <body xml:lang="en-GB">  <!-- ⚠️ CHANGE THIS -->
        <div class="chapter">
            <h1 id="chapter1">Chapter 1</h1>  <!-- ⚠️ TRANSLATE -->

            <p class="first-para">
                The sun rose over the distant hills...  <!-- ⚠️ TRANSLATE -->
            </p>

            <p class="body-text">
                <span class="character-name">John</span> walked through  <!-- ⚠️ PRESERVE NAMES -->
                the streets of <span class="place">London</span>.
            </p>

            <p class="body-text">
                <img src="image/map.jpg" alt="Map"/>  <!-- ⚠️ DON'T CHANGE -->
            </p>
        </div>
    </body>
</html>
```

**Translation tasks:**
- Change `xml:lang` attribute in `<body>` tag
- Translate text content inside `<p>`, `<h1>`, `<h2>`, etc.
- **Preserve:**
  - All HTML tags and attributes
  - CSS class names
  - Image references
  - Anchor IDs
  - Proper names (when appropriate)

## Language Codes

Common language codes for `<dc:language>` and `xml:lang`:

| Language | Code |
|----------|------|
| English (UK) | `en-GB` |
| English (US) | `en-US` |
| Czech | `cs-CZ` |
| German | `de-DE` |
| French | `fr-FR` |
| Spanish (Spain) | `es-ES` |
| Italian | `it-IT` |
| Polish | `pl-PL` |
| Russian | `ru-RU` |
| Japanese | `ja-JP` |
| Chinese (Simplified) | `zh-CN` |
| Chinese (Traditional) | `zh-TW` |

## Common EPUB Variations

### Naming Conventions

Chapter files might be named:
- `chapter-1.xhtml`, `chapter-2.xhtml`
- `content-1.xhtml`, `content-2.xhtml`
- `6-40k-Content.xhtml`, `6-40k-Content-2.xhtml` (InDesign export)
- `text/chapter001.xhtml`

### Content Folder Names

Instead of `OEBPS/`, you might see:
- `EPUB/`
- `OPS/`
- `content/`

The actual name is defined in `META-INF/container.xml`

### Optional Files

Some EPUBs include:
- `cover.xhtml` - Cover page
- `toc.xhtml` - HTML table of contents (in addition to NCX)
- `nav.xhtml` - EPUB 3 navigation document
- Fonts folder with custom fonts
- Audio/video files

## EPUB Versions

**EPUB 2.0.1** (most common)
- Uses `toc.ncx` for navigation
- DTD: XHTML 1.1
- Older but widely supported

**EPUB 3.x** (modern)
- Uses `nav.xhtml` (HTML5) for navigation
- Better multimedia support
- Can still include NCX for backwards compatibility

## Translation Checklist

When translating an EPUB:

- [ ] **Metadata** (content.opf)
  - [ ] Change `<dc:language>` code

- [ ] **Navigation** (toc.ncx)
  - [ ] Translate all `<navLabel><text>` entries

- [ ] **Chapter files** (*.xhtml)
  - [ ] Change `xml:lang` attribute
  - [ ] Translate text content
  - [ ] Preserve HTML structure
  - [ ] Keep proper names

- [ ] **Table of Contents** (if separate XHTML file)
  - [ ] Translate TOC entries

- [ ] **About/Metadata pages**
  - [ ] Translate "About the Author"
  - [ ] Translate book descriptions

- [ ] **Don't touch**
  - [ ] CSS files
  - [ ] Images
  - [ ] Fonts
  - [ ] META-INF/container.xml
  - [ ] mimetype

## Validation

After translation, validate:

1. **ZIP integrity:**
   ```bash
   unzip -t translated.epub
   ```

2. **EPUB structure:**
   - Use [EPUBCheck](https://github.com/w3c/epubcheck)
   - Or online validators

3. **Test in readers:**
   - Apple Books
   - Calibre
   - Adobe Digital Editions

## Rebuilding EPUB

Correct order is critical:

```bash
cd translated_content/

# Step 1: Add mimetype FIRST, uncompressed
zip -0 -X ../book.epub mimetype

# Step 2: Add everything else, compressed
zip -r ../book.epub META-INF OEBPS

# Verify
unzip -t ../book.epub
```

**Wrong order will break the EPUB!**

## Common Issues

### Issue: EPUB won't open
**Likely cause:** Incorrect ZIP structure
**Fix:** Ensure mimetype is first and uncompressed

### Issue: Navigation doesn't work
**Likely cause:** Didn't translate toc.ncx
**Fix:** Update all `<navLabel><text>` elements

### Issue: Broken formatting
**Likely cause:** Changed HTML tags or CSS classes
**Fix:** Only translate text content, preserve tags exactly

### Issue: Special characters broken
**Likely cause:** Wrong encoding
**Fix:** Ensure UTF-8 encoding throughout

## Further Reading

- [EPUB Specification](http://idpf.org/epub/30)
- [EPUB 2.0.1 Spec](http://idpf.org/epub/201)
- [EPUB Structural Semantics](http://idpf.org/epub/vocab/structure/)
