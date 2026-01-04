# EPUB Translator - Universal AI-Powered Book Translation

> Translate EPUB books between languages using AI code assistants while preserving formatting, structure, and metadata.

**Works with:** Claude Code, Gemini CLI, Cursor, Codex, GitHub Copilot, and any AI assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/vbalko-claimate/epub-translator?style=social)](https://github.com/vbalko-claimate/epub-translator/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/vbalko-claimate/epub-translator?style=social)](https://github.com/vbalko-claimate/epub-translator/network/members)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub Issues](https://img.shields.io/github/issues/vbalko-claimate/epub-translator)](https://github.com/vbalko-claimate/epub-translator/issues)
[![Documentation](https://img.shields.io/badge/docs-complete-blue)](docs/)
[![Glossaries](https://img.shields.io/badge/glossaries-community-purple)](glossaries/community/)

## See It In Action

**📺 [Live Demo & Screenshots](DEMO.md)** - See what the translation process looks like

**🎬 [Video Tutorial](assets/video/tutorial-link.md)** - 3-minute walkthrough (coming soon)

Want to see real examples? Check out the [Baneblade case study](examples/baneblade-case-study.md) showing a complete 300-page book translation.

## Features

- ✅ **Preserves Structure** - HTML/XML tags, CSS styling, and formatting stay intact
- ✅ **Maintains Navigation** - Chapter structure, TOC, and metadata preserved
- ✅ **Smart Translation** - Protects proper names and technical terms
- ✅ **Glossary Support** - Use translation dictionaries for consistency (i18n-style)
- ✅ **Community Glossaries** - Pre-made dictionaries for popular universes (Warhammer 40k, Harry Potter)
- ✅ **Batch Processing** - Translate multiple chapters/pages in parallel
- ✅ **Universal Compatibility** - Works with ANY AI assistant
- ✅ **Native Claude Skill** - Fully automated for Claude Code users

## Quick Start

### Option 1: For Claude Code Users (Fully Automated)

1. **Clone this repository:**
   ```bash
   cd ~/.claude/skills/
   git clone https://github.com/vbalko-claimate/epub-translator.git
   ```

2. **Translate a book:**
   ```bash
   claude "translate this EPUB book from English to Czech: book.epub"
   ```

That's it! Claude will automatically extract, translate, and rebuild your EPUB.

**📖 [Detailed Installation Guide →](INSTALLATION.md)**

### Option 2: For All Other AI Assistants (Manual Workflow)

**For EPUB:**
1. **Extract the EPUB:**
   ```bash
   mkdir epub_workspace
   unzip book.epub -d epub_workspace/
   ```

2. **Use prompt templates** from [`prompts/`](prompts/) directory:
   - Copy each prompt in sequence
   - Paste into your AI assistant (Claude web, Gemini, Cursor, etc.)
   - Follow the step-by-step instructions

3. **Rebuild the EPUB:**
   ```bash
   cd epub_workspace
   zip -0 -X ../translated.epub mimetype
   zip -r ../translated.epub META-INF OEBPS
   ```

### PDF Translation (Optional)

If you have a PDF book, you can convert it to EPUB and then translate it:

**Prerequisites:**
- None! Pure Python (auto-installs ALL dependencies on first run)

**Workflow:**
```bash
# 1. Convert PDF to EPUB
python scripts/convert_pdf_to_epub.py mybook.pdf

# 2. Translate the EPUB (existing workflow)
claude "translate mybook.epub from English to Czech"
```

**Quality expectations:**
- **Good for:** Novels, simple text books, standard layouts
- **Acceptable for:** Technical books with some tables/diagrams
- **Not suitable for:** Multi-column papers, scanned PDFs, layout-critical documents

**Image handling:**
- ✅ Extracts embedded images from PDF
- ✅ Preserves JPEG, PNG, GIF, TIFF formats
- ✅ Automatically embeds images in EPUB
- ⚠️ Images placed at end of each chapter
- ⚠️ Small decorative images (<100x100px) filtered out

**Important:** PDF→EPUB conversion is lossy (layout changes from fixed to reflowable). If you need to preserve exact PDF formatting, use a dedicated PDF editor instead.

## Real-World Example

**Book:** Baneblade by Guy Haley (Warhammer 40k)
**Pages:** 300+
**Chapters:** 31 (Prologue, Chapters 1-29, Epilogue)
**Time:** ~2 hours
**Quality:** All proper names preserved, formatting intact, valid EPUB

[See full case study →](examples/baneblade-case-study.md)

## How It Works

### EPUB Translation

EPUB files are ZIP archives containing XHTML files for each chapter. This workflow:

1. **Extracts** the EPUB to access individual chapter files
2. **Translates** each chapter while preserving HTML structure
3. **Updates** metadata (language codes, TOC labels)
4. **Rebuilds** everything into a valid EPUB

```
book.epub (ZIP)
├── mimetype
├── META-INF/container.xml
└── OEBPS/
    ├── content.opf (metadata - update language)
    ├── toc.ncx (navigation - translate labels)
    ├── chapter-1.xhtml (translate content)
    ├── chapter-2.xhtml (translate content)
    ├── css/ (preserve untouched)
    └── images/ (preserve untouched)
```

**[Learn more about EPUB structure →](docs/how-it-works.md)**

## Supported Languages

Any language pair! Examples:
- 🇬🇧 English → 🇨🇿 Czech
- 🇫🇷 French → 🇬🇧 English
- 🇪🇸 Spanish → 🇩🇪 German
- 🇯🇵 Japanese → 🇬🇧 English
- And any other combination!

## Documentation

- **[How It Works](docs/how-it-works.md)** - Understanding EPUB structure
- **[Glossary System](docs/glossary-system.md)** - 📚 Control translations with dictionaries
- **[Context Management](docs/context-management.md)** - ⚠️ Critical: Avoid running out of memory
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[Examples](docs/examples.md)** - Step-by-step walkthrough sessions

## Translation Glossaries

**Use pre-made dictionaries for consistent translations:**

- 📖 **Warhammer 40,000** ([en→cs](glossaries/community/warhammer40k-en-cs.json)) - Official + community terms
- 📖 **Template** ([template.txt](glossaries/template.txt)) - Create your own glossary

**How glossaries work:**
```
PRESERVE: Cortein           ← Never translate (character name)
TRANSLATE: Mars → Mars      ← Use specific translation
PRESERVE_WITH_GRAMMAR: bolter  ← Keep word, apply Czech cases (bolteru, bolterem)
CONTEXT: Chapter → depends  ← "Kapitola" in headings, "Řád" for military units
```

**Usage:**
```bash
# Claude Code
claude "translate book.epub using glossary warhammer40k-en-cs.json"

# Manual (any AI)
# Include glossary terms in your translation prompts
```

[Learn more about glossaries →](docs/glossary-system.md)

## Tool Comparison

| Feature | Claude Skill | Universal Prompts |
|---------|-------------|-------------------|
| **Automation** | Fully automated | Semi-manual |
| **AI Compatibility** | Claude Code only | Any AI assistant |
| **Setup Complexity** | Install once | Copy-paste prompts |
| **Speed** | Fastest (~2 hrs) | Slower (~3-4 hrs) |
| **Best For** | Repeat translations | One-time use |

## Requirements

**All users need:**
- ZIP/UNZIP utilities (built-in on Mac/Linux, install on Windows)
- An EPUB file to translate
- Access to an AI code assistant

**Claude Code users additionally need:**
- [Claude Code CLI](https://github.com/anthropics/claude-code) installed
- Skill installed in `~/.claude/skills/epub-translator`

## Translation Quality Tips

### What Gets Preserved ✅

- **Proper names**: Characters, places, organizations (e.g., "Mars Triumphant" stays as-is)
- **Technical terms**: Genre-specific terminology (e.g., "Baneblade", "lascannon")
- **HTML structure**: All tags, CSS classes, image references
- **Formatting**: Bold, italics, paragraph styles

### What Gets Translated 📝

- **Narrative text**: Dialogue, descriptions, narration
- **Chapter titles**: "Chapter 1" → "Kapitola 1" (or your target language)
- **Metadata**: Table of Contents, About the Author sections
- **Navigation labels**: Prologue → Prolog, Epilogue → Epilog

[See translation best practices →](claude-skill/TRANSLATION_GUIDE.md)

## Contributing

Contributions are welcome! Whether it's:
- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🌍 Prompt templates for new AI assistants

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

- [ ] Support for more ebook formats (MOBI, AZW3)
- [ ] GUI application for non-technical users
- [ ] Enhanced translation memory/glossary support
- [ ] Batch translation of multiple books

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Created by [Vladimir Balko](https://github.com/vladimirbalko)

Inspired by translating "Baneblade" by Guy Haley (Warhammer 40k novel) from English to Czech.

## Links

- **📝 Blog Post:** [How I Translated a 300-Page Book in 2 Hours](medium-link)
- **🐛 Issues:** [GitHub Issues](https://github.com/vladimirbalko/epub-translator/issues)
- **💬 Discussions:** [GitHub Discussions](https://github.com/vladimirbalko/epub-translator/discussions)
- **⭐ Star this repo** if you find it useful!

---

**Made with ❤️ for book lovers who can't wait for official translations**
