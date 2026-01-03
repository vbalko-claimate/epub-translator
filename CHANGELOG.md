# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### To Do
- Add video tutorial
- Create visual assets (screenshots, GIFs)
- Publish Medium blog post
- Add more community glossaries (Harry Potter, Star Wars, etc.)

## [1.0.0] - 2025-01-03

### Added

#### Core Functionality
- **Claude Code Skill** for fully automated translation
  - SKILL.md with YAML frontmatter
  - REFERENCE.md with EPUB technical specifications
  - TRANSLATION_GUIDE.md with best practices
  - Bash scripts: extract.sh, rebuild.sh, validate.sh
  - Automatic subagent usage for context management

- **Universal Prompt Templates** for all AI assistants
  - 6 sequential prompts for manual workflow
  - Compatible with Claude.ai, Gemini CLI, Cursor, etc.
  - Step-by-step instructions in each prompt

#### Documentation
- **README.md** - Main documentation with features, quick start, examples
- **INSTALLATION.md** - Complete installation guide for both skill and manual workflow
- **DEMO.md** - Live demo structure with sample outputs and recording instructions
- **CONTRIBUTING.md** - Guidelines for community contributors
- **LICENSE** - MIT License

#### Advanced Documentation
- **docs/how-it-works.md** - EPUB format explanation
- **docs/context-management.md** - Critical guide for handling large books
- **docs/glossary-system.md** - Comprehensive glossary documentation
- **docs/troubleshooting.md** - Common issues and solutions
- **docs/examples.md** - Step-by-step walkthrough sessions

#### Examples
- **examples/baneblade-case-study.md** - Real-world 300-page translation
- **examples/session-transcript.md** - Complete walkthrough of "The Little Prince"

#### Glossary System
- **glossaries/README.md** - Glossary system overview
- **glossaries/template.txt** - Template for creating custom glossaries
- **glossaries/community/warhammer40k-en-cs.json** - Warhammer 40,000 glossary (100+ terms)
- Support for 4 translation modes:
  - PRESERVE: Never translate
  - TRANSLATE: Always use specific translation
  - PRESERVE_WITH_GRAMMAR: Keep word, apply target language grammar
  - CONTEXT: Different translations based on usage

#### Assets Structure
- **assets/README.md** - Instructions for creating visual assets
- **assets/screenshots/** - Directory for screenshots
- **assets/gifs/** - Directory for animated demos
- **assets/video/** - Directory for video tutorials
- **assets/video/tutorial-link.md** - Video recording guide

#### GitHub Setup
- **CHANGELOG.md** - This file
- **.gitignore** - Excludes workspace files, temporary files, user glossaries
- GitHub badges for stars, forks, issues, documentation, glossaries

### Features

#### Translation Features
- Preserves HTML/XML structure and CSS styling
- Maintains chapter navigation and metadata
- Protects proper names and technical terms
- Batch processing with parallel translation
- Glossary support for consistent terminology
- Language code updates (e.g., en-GB → cs-CZ)

#### Context Management
- **Critical:** Automatic subagent usage for large books
- Prevents context overflow (books can be 100K-250K tokens)
- Parallel chapter translation
- Manual session batching for non-Claude Code users

#### Quality Features
- EPUB validation scripts
- ZIP integrity checking
- XML validation
- EPUBCheck integration
- Reader compatibility verification

### Target Audience
- AI code assistant users (Claude Code, Gemini CLI, Cursor, Codex, etc.)
- Intermediate technical level (not beginners, not hardcore developers)
- Book lovers who can't wait for official translations

### Supported Languages
- Any language pair
- Examples: English ↔ Czech, French ↔ English, Spanish ↔ German, Japanese ↔ English

### Real-World Testing
- Successfully translated "Baneblade" by Guy Haley
- 300 pages, 31 chapters
- English → Czech
- ~2 hours translation time
- ~$6 API cost
- All proper names preserved, formatting intact

### Requirements
- ZIP/UNZIP utilities (built-in on Mac/Linux)
- EPUB file to translate
- Access to AI code assistant
- For Claude Code users: Claude Code CLI installed

### Platform Support
- **macOS:** Fully supported, works out of the box
- **Linux:** Fully supported, requires zip/unzip installation
- **Windows:** Supported via WSL (recommended) or Git Bash

## Initial Release Notes

This is the first public release of EPUB Translator. The project was born from the need to translate "Baneblade" (Warhammer 40k novel) from English to Czech when no official translation was available.

The tool has been designed with two audiences in mind:
1. **Claude Code users** - Get fully automated translation with one command
2. **Everyone else** - Use universal prompts with any AI assistant

Key innovation: **Context management** through mandatory subagent usage ensures even 300+ page books can be translated without running out of memory.

The **glossary system** allows users to control exactly what gets translated and what stays preserved, with support for community-contributed glossaries for popular book series.

### Known Limitations
- Visual assets (screenshots, GIFs, video) not yet created
- Medium blog post not yet published
- Only one community glossary available (Warhammer 40k)
- MOBI and AZW3 formats not yet supported

### Next Steps
1. Create visual assets and demos
2. Publish Medium blog post
3. Gather community feedback
4. Add more community glossaries
5. Consider GUI application for non-technical users

---

## Version History

- **v1.0.0** (2025-01-03) - Initial public release

---

**For the full version history, see:** https://github.com/vbalko-claimate/epub-translator/releases
