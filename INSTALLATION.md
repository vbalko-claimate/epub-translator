# Installation Guide

Complete step-by-step installation instructions for EPUB Translator.

---

## Choose Your Path

**Path 1:** [Claude Code Skill](#claude-code-skill-fully-automated) (Recommended for Claude Code users)
- ✅ Fully automated translation
- ✅ One command to translate entire book
- ✅ No manual steps needed

**Path 2:** [Universal Prompts](#universal-prompts-manual-workflow) (For all other AI assistants)
- ✅ Works with Claude.ai web, Cursor, Gemini CLI, etc.
- ✅ No installation needed
- ✅ Copy-paste prompts

---

## Claude Code Skill (Fully Automated)

### Prerequisites

**1. Install Claude Code CLI**

If you don't have Claude Code yet:

```bash
# macOS/Linux
brew install claude

# Or download from:
# https://claude.ai/download
```

**2. Verify installation:**

```bash
claude --version
# Should show: claude version x.x.x
```

**3. Authenticate:**

```bash
claude auth login
# Follow the prompts to authenticate with your Anthropic account
```

### Install the Skill

**Option A: Clone from GitHub (Recommended)**

```bash
# 1. Navigate to Claude skills directory
cd ~/.claude/skills/

# 2. Clone the repository
git clone https://github.com/vbalko-claimate/epub-translator.git

# 3. The skill is now installed!
# Verify:
ls ~/.claude/skills/epub-translator/claude-skill/
# Should show: SKILL.md, REFERENCE.md, TRANSLATION_GUIDE.md, scripts/
```

**Option B: Download ZIP**

```bash
# 1. Download ZIP from GitHub
# Go to: https://github.com/vbalko-claimate/epub-translator
# Click: Code → Download ZIP

# 2. Extract the ZIP file

# 3. Copy to Claude skills directory
cp -r ~/Downloads/epub-translator-main ~/.claude/skills/epub-translator

# 4. Verify installation
ls ~/.claude/skills/epub-translator/claude-skill/
```

**Option C: Manual copy (if you already downloaded)**

```bash
# If you have the repository locally
cp -r /path/to/epub-translator ~/.claude/skills/

# Example:
cp -r ~/Documents/epub-translator ~/.claude/skills/
```

### Verify Installation

```bash
# Check that skill files exist
ls -la ~/.claude/skills/epub-translator/claude-skill/

# Should show:
# SKILL.md
# REFERENCE.md
# TRANSLATION_GUIDE.md
# scripts/extract.sh
# scripts/rebuild.sh
# scripts/validate.sh
```

### Test the Skill

**Simple test:**

```bash
# Create a test request
claude "do you have the epub-translator skill installed?"

# Claude should respond acknowledging the skill
```

**Full test (with a small EPUB):**

```bash
# Get a small test EPUB (public domain book)
curl -o test-book.epub "https://www.gutenberg.org/ebooks/1342.epub.noimages"

# Translate it
claude "translate test-book.epub from English to Spanish"

# Claude will:
# 1. Extract the EPUB
# 2. Identify chapters
# 3. Translate using subagents
# 4. Rebuild EPUB
# 5. Output: test-book-translated.epub
```

### Troubleshooting Installation

**Issue:** "Skill not found"

**Fix:**
```bash
# Check skill location
ls ~/.claude/skills/

# Should show "epub-translator" folder
# If not, reinstall:
cd ~/.claude/skills/
git clone https://github.com/vbalko-claimate/epub-translator.git
```

**Issue:** "Permission denied" on scripts

**Fix:**
```bash
# Make scripts executable
chmod +x ~/.claude/skills/epub-translator/scripts/*.sh
```

**Issue:** Claude doesn't recognize the skill

**Fix:**
```bash
# Ensure SKILL.md exists and has correct YAML frontmatter
cat ~/.claude/skills/epub-translator/claude-skill/SKILL.md | head -10

# Should start with:
# ---
# name: epub-translator
# description: ...
# ---
```

### Update the Skill

```bash
# Navigate to skill directory
cd ~/.claude/skills/epub-translator

# Pull latest changes
git pull origin main

# Or download latest release from GitHub
```

---

## Universal Prompts (Manual Workflow)

### Prerequisites

**Required:**
- ✅ Any AI code assistant (Claude.ai web, Cursor, Gemini CLI, etc.)
- ✅ ZIP/UNZIP utilities (pre-installed on Mac/Linux)
- ✅ Terminal access

**Optional:**
- EPUBCheck for validation (advanced users)

### Installation

**No installation needed!** Just clone/download the repository:

**Option 1: Git clone**

```bash
git clone https://github.com/vbalko-claimate/epub-translator.git
cd epub-translator
```

**Option 2: Download ZIP**

1. Go to: https://github.com/vbalko-claimate/epub-translator
2. Click: Code → Download ZIP
3. Extract to your desired location

### How to Use

**Step 1: Navigate to prompts folder**

```bash
cd epub-translator/prompts/
ls
# Shows:
# 01-setup-workspace.md
# 02-identify-chapters.md
# 03-translate-chapter.md
# 04-translate-metadata.md
# 05-update-config.md
# 06-rebuild-epub.md
```

**Step 2: Open prompts in order**

Open each `.md` file in a text editor and follow instructions:

```bash
# macOS
open 01-setup-workspace.md

# Linux
xdg-open 01-setup-workspace.md

# Windows
notepad 01-setup-workspace.md
```

**Step 3: Copy-paste to your AI assistant**

Each prompt file has a section:
```
## Prompt Text (Copy from here)
```

Copy everything after that header and paste into:
- Claude.ai web chat
- Cursor IDE
- Gemini chat
- Any AI assistant

**Step 4: Follow each step sequentially**

Work through all 6 prompts in order:
1. Setup workspace (extract EPUB)
2. Identify chapters
3. Translate chapters (use multiple sessions!)
4. Translate metadata
5. Update config files
6. Rebuild EPUB

---

## Additional Tools Installation

### EPUBCheck (Optional Validation)

**macOS:**
```bash
brew install epubcheck

# Usage:
epubcheck translated-book.epub
```

**Linux:**
```bash
# Download from GitHub
wget https://github.com/w3c/epubcheck/releases/download/v5.1.0/epubcheck-5.1.0.zip
unzip epubcheck-5.1.0.zip
cd epubcheck-5.1.0

# Usage:
java -jar epubcheck.jar /path/to/book.epub
```

**Windows:**
1. Download from: https://github.com/w3c/epubcheck/releases
2. Extract ZIP
3. Run: `java -jar epubcheck.jar book.epub`

### Calibre (Optional EPUB Reader/Editor)

**All platforms:**

Download from: https://calibre-ebook.com/download

**Usage:**
- Open and test translated EPUBs
- Edit metadata
- Convert formats

---

## Glossaries Installation

### Using Community Glossaries

**Already included in the repository!**

Location: `glossaries/community/`

**Available:**
- `warhammer40k-en-cs.json` - Warhammer 40,000 (English → Czech)
- More coming soon!

**Usage:**

**With Claude Code Skill:**
```bash
claude "translate book.epub from English to Czech using glossary glossaries/community/warhammer40k-en-cs.json"
```

**With manual prompts:**
1. Open glossary file
2. Copy terms into your translation prompt
3. Apply consistently across all chapters

### Creating Your Own Glossary

```bash
# Copy template
cp glossaries/template.txt glossaries/my-book-en-es.txt

# Edit with your terms
nano glossaries/my-book-en-es.txt
# or
code glossaries/my-book-en-es.txt

# Use in translation
claude "translate my-book.epub using glossary glossaries/my-book-en-es.txt"
```

---

## Platform-Specific Notes

### macOS

**Everything should work out of the box!**

- ZIP/UNZIP: ✅ Pre-installed
- Bash scripts: ✅ Compatible
- File paths: ✅ No issues

**Optional tools:**
```bash
# Install Homebrew (if not already)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install helpful tools
brew install epubcheck
brew install calibre
```

### Linux

**ZIP utilities:**

```bash
# Debian/Ubuntu
sudo apt-get install zip unzip

# RedHat/CentOS
sudo yum install zip unzip

# Arch
sudo pacman -S zip unzip
```

**Bash scripts:**
✅ Fully compatible

**File paths:**
✅ No issues

### Windows

**Recommended: Use WSL (Windows Subsystem for Linux)**

```powershell
# Install WSL
wsl --install

# Restart computer
# Then install Ubuntu from Microsoft Store

# Inside WSL:
sudo apt-get update
sudo apt-get install zip unzip git

# Clone repository inside WSL
cd ~
git clone https://github.com/vbalko-claimate/epub-translator.git
```

**Alternative: Git Bash**

1. Install Git for Windows: https://git-scm.com/download/win
2. Use Git Bash terminal
3. Scripts should work

**Alternative: PowerShell**

Scripts need adaptation. See `docs/troubleshooting.md` for Windows-specific commands.

---

## Verify Everything Works

### Quick Test Checklist

**For Claude Code Skill:**

```bash
# 1. Verify skill installed
ls ~/.claude/skills/epub-translator/claude-skill/SKILL.md

# 2. Verify scripts are executable
ls -la ~/.claude/skills/epub-translator/scripts/
# Should show: -rwxr-xr-x (executable)

# 3. Test with Claude
claude "do you have the epub-translator skill?"
# Should respond affirmatively

# 4. Download test EPUB
curl -o pride-prejudice.epub "https://www.gutenberg.org/ebooks/1342.epub.noimages"

# 5. Translate a small section (test)
claude "analyze the structure of pride-prejudice.epub and tell me how many chapters it has"
# Should extract and analyze successfully
```

**For Universal Prompts:**

```bash
# 1. Verify files downloaded
ls epub-translator/prompts/
# Should show all 6 .md files

# 2. Verify bash scripts work
cd epub-translator/scripts/
./extract.sh
# Should show usage instructions

# 3. Test extraction manually
mkdir test-workspace
unzip pride-prejudice.epub -d test-workspace/
ls test-workspace/
# Should show extracted files
```

---

## Getting Help

**Installation issues:**

1. Check [Troubleshooting Guide](docs/troubleshooting.md)
2. Open GitHub Issue: https://github.com/vbalko-claimate/epub-translator/issues
3. Tag with `installation` label

**Common issues:**

- **"Command not found: claude"** → Claude Code CLI not installed
- **"Permission denied"** → Scripts not executable (run `chmod +x`)
- **"Skill not found"** → Wrong installation path
- **"ZIP not found"** → Install zip utilities

**Community support:**

- GitHub Discussions: https://github.com/vbalko-claimate/epub-translator/discussions
- Issues: https://github.com/vbalko-claimate/epub-translator/issues

---

## Next Steps

After successful installation:

1. **Read Quick Start:** [README.md](README.md#quick-start)
2. **Try a small book first:** Start with ~10 chapters
3. **Learn about glossaries:** [Glossary System](docs/glossary-system.md)
4. **Understand context management:** [Context Management](docs/context-management.md)
5. **See real example:** [Baneblade Case Study](examples/baneblade-case-study.md)

---

## Uninstallation

**Remove Claude Code Skill:**

```bash
rm -rf ~/.claude/skills/epub-translator
```

**Remove downloaded repository:**

```bash
rm -rf /path/to/epub-translator
```

**Clean up workspace files:**

```bash
# Remove any epub_workspace folders created during translation
rm -rf epub_workspace
```

---

**Installation complete!** 🎉 Ready to translate books!
