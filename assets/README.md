# Visual Assets for EPUB Translator

This folder contains screenshots, GIFs, and videos demonstrating the EPUB Translator in action.

## Directory Structure

```
assets/
├── screenshots/          # Static images (PNG, JPG)
│   ├── 01-original-epub.png
│   ├── 02-translation-progress.png
│   ├── 03-translated-in-reader.png
│   ├── 04-side-by-side.png
│   └── 05-glossary-example.png
├── gifs/                # Animated demonstrations
│   ├── quick-demo.gif
│   └── glossary-usage.gif
└── video/               # Links to video tutorials
    └── tutorial-link.md
```

## Screenshots to Create

### 1. Original EPUB File (`01-original-epub.png`)

**What to show:**
- Original EPUB file in Finder/File Explorer
- File size, icon, name visible
- Optionally: File opened in Apple Books/Calibre showing English text

**Recommended specs:**
- Resolution: 1920x1080 or higher
- Format: PNG
- Tool: macOS Screenshot (Cmd+Shift+4) or Windows Snipping Tool

### 2. Translation in Progress (`02-translation-progress.png`)

**What to show:**
- Terminal window with Claude Code running
- Output showing:
  - EPUB extracted message
  - Progress indicators (chapters translated)
  - Subagent activity if visible
  - Time elapsed/estimated

**Example text to capture:**
```
EPUB Translator: Starting translation...

✓ Extracted EPUB to epub_workspace/
✓ Found 31 chapters
✓ Using glossary: warhammer40k-en-cs.json

Translating chapters in parallel:
  Chapter 1  ████████████████████ 100% Complete
  Chapter 2  ████████████████████ 100% Complete
  ...
```

### 3. Translated Book in Reader (`03-translated-in-reader.png`)

**What to show:**
- Translated EPUB opened in Apple Books, Calibre, or other reader
- Czech text (or target language) visible
- Table of contents showing translated chapter names
- Reader interface showing language detected as Czech

**Key elements:**
- Book cover
- TOC with "Kapitola 1", "Kapitola 2" etc.
- Sample page with Czech text
- Formatting preserved (bold, italics, paragraphs)

### 4. Side-by-Side Comparison (`04-side-by-side.png`)

**What to show:**
- Two windows open side by side:
  - Left: Original EPUB (English)
  - Right: Translated EPUB (Czech)
- Same chapter/page visible in both
- Highlighting: proper names preserved, text translated

**Example to show:**
```
Original (English):        Translated (Czech):
Cortein gripped the        Cortein sevřel
controls of the Mars       ovládací prvky Mars
Triumphant.                Triumphant.
```

### 5. Glossary Example (`05-glossary-example.png`)

**What to show:**
- Glossary file open (warhammer40k-en-cs.json)
- Highlighting entries:
  - PRESERVE: "Cortein"
  - TRANSLATE: "Chapter" → "Kapitola"
  - PRESERVE_WITH_GRAMMAR: "bolter" with declension
- Show how these appear in translated text

## GIFs to Create

### Quick Demo (`quick-demo.gif`)

**Duration:** 30 seconds
**Shows:**
1. Starting Claude Code (3 sec)
2. Typing command: `claude "translate book.epub from English to Czech"` (5 sec)
3. Progress bars moving (15 sec, sped up)
4. Output file appearing (2 sec)
5. Opening in reader (5 sec)

**Tool:** [LICEcap](https://www.cockos.com/licecap/) (free, Mac/Windows)
**Specs:**
- Resolution: 1280x720
- Frame rate: 10-15 fps
- File size: Keep under 5 MB

### Glossary Usage Demo (`glossary-usage.gif`)

**Duration:** 20 seconds
**Shows:**
1. Opening glossary file (3 sec)
2. Highlighting PRESERVE/TRANSLATE terms (5 sec)
3. Running translation command (2 sec)
4. Opening output, highlighting same terms preserved (10 sec)

## Video Tutorial

### Full Tutorial (`tutorial-link.md`)

**Platform:** YouTube
**Duration:** 3 minutes
**Script:**

**00:00-00:30** - Introduction
- "Hi, I'll show you how to translate EPUB books using AI"
- Show book file on desktop

**00:30-01:00** - Installation
```bash
cd ~/.claude/skills/
git clone https://github.com/vbalko-claimate/epub-translator.git
```

**01:00-02:00** - Translation
- Run command
- Show progress (speed up if needed)
- Explain subagents working in parallel

**02:00-02:30** - Verification
- Open in Apple Books
- Show TOC
- Read sample paragraph

**02:30-03:00** - Conclusion
- "300 pages in 2 hours for $6"
- "Visit GitHub for more info"
- Show URL: https://github.com/vbalko-claimate/epub-translator

**Tool:** OBS Studio (free) or QuickTime (macOS)
**Upload to:** YouTube, embed link in README

## Recording Tools

### Screenshots
- **macOS:** Cmd+Shift+4 (built-in)
- **Windows:** Snipping Tool or Snip & Sketch
- **Linux:** Flameshot, GNOME Screenshot

### GIFs
- **macOS/Windows:** [LICEcap](https://www.cockos.com/licecap/) (free)
- **macOS:** Kap (modern alternative)
- **Linux:** Peek

### Video
- **Cross-platform:** [OBS Studio](https://obsproject.com/) (free, professional)
- **macOS:** QuickTime Player (built-in)
- **Windows:** Xbox Game Bar (Win+G)
- **Linux:** SimpleScreenRecorder

## File Naming Convention

Use descriptive, numbered names:
- `01-original-epub.png` - Original file
- `02-translation-progress.png` - Terminal output
- `03-translated-in-reader.png` - Result in reader
- `04-side-by-side.png` - Comparison
- `05-glossary-example.png` - Glossary usage

For variations:
- `02a-translation-progress-claude.png` - Claude Code
- `02b-translation-progress-cursor.png` - Cursor IDE

## Image Specifications

### Screenshots
- **Format:** PNG (lossless)
- **Resolution:** Minimum 1280x720, recommended 1920x1080
- **Size:** Keep under 2 MB each (compress if needed)
- **DPI:** 72 DPI (web standard)

### GIFs
- **Format:** GIF
- **Resolution:** 1280x720 or 1024x768
- **Frame rate:** 10-15 fps (balance between smoothness and file size)
- **Size:** Keep under 5 MB (compress with [ezgif.com](https://ezgif.com/optimize))
- **Duration:** 15-30 seconds max

### Videos
- **Format:** MP4 (H.264)
- **Resolution:** 1920x1080
- **Upload to:** YouTube (embed in README)
- **Duration:** 2-5 minutes

## Using Assets in Documentation

### In README.md

```markdown
## See It In Action

![Translation in Progress](assets/screenshots/02-translation-progress.png)

![Quick Demo](assets/gifs/quick-demo.gif)

[Watch 3-minute tutorial →](assets/video/tutorial-link.md)
```

### In DEMO.md

Reference screenshots:
```markdown
### Before Translation

![Original EPUB](../assets/screenshots/01-original-epub.png)
```

### In Blog Post

Upload images to Medium directly, but keep originals here for:
- GitHub README
- Future blog posts
- Documentation updates

## Placeholder Images

Until real screenshots are available, we have:
- Text descriptions in DEMO.md
- Code blocks showing expected output
- Placeholder comments in README

## Contributing Assets

If you've translated a book and want to share your screenshots:

1. Follow naming convention above
2. Ensure no copyrighted content visible (book text snippets are OK for demo purposes)
3. Compress images appropriately
4. Submit PR with assets in this folder
5. Update DEMO.md to reference your images

## Copyright Notice

Screenshots and demos are for educational/documentation purposes only. Do not include:
- Full pages of copyrighted books
- Identifiable personal information
- API keys or credentials

Keep samples to short excerpts (1-2 paragraphs) for demonstration purposes under fair use.

---

**Status:** Placeholder structure created. Actual assets to be added.

**See:** [DEMO.md](../DEMO.md) for expected content and examples.
