# Video Tutorial

## Full 3-Minute Tutorial

**Status:** Coming soon

**Planned content:**
- Installation (30 seconds)
- Translation demo (2 minutes)
- Verification (30 seconds)

**Platform:** YouTube

**Link:** [To be added after recording]

---

## Recording Checklist

- [ ] Record installation sequence
- [ ] Record translation of sample book
- [ ] Record verification in reader
- [ ] Edit video (add captions, speed up slow parts)
- [ ] Upload to YouTube
- [ ] Add link here
- [ ] Embed in README.md
- [ ] Share on social media

---

## Alternative: Screen Recording Instructions

If you want to record your own demo:

### Script (3 minutes)

**00:00-00:30** - Introduction
```
"Hi, I'll show you how to translate an EPUB book using AI code assistants.
This is 'Baneblade', a 300-page Warhammer 40k novel in English."
[Show file on desktop]
```

**00:30-01:00** - Installation
```bash
cd ~/.claude/skills/
git clone https://github.com/vbalko-claimate/epub-translator.git
```
```
"That's it for installation!"
```

**01:00-02:00** - Translation
```bash
claude "translate baneblade.epub from English to Czech"
```
[Show terminal output - can speed up if needed]
- Highlight: extraction, parallel translation, rebuild
- Show: "31 chapters translated in ~2 hours"

**02:00-02:30** - Verification
- Open translated EPUB in Apple Books
- Show table of contents (Kapitola 1, Kapitola 2...)
- Read a sample paragraph in Czech
- "Perfect! Formatting preserved, proper names intact"

**02:30-03:00** - Conclusion
```
"Translated 300 pages in 2 hours for about $6.
Visit github.com/vbalko-claimate/epub-translator for more info."
```
[Show GitHub URL on screen]

### Recording Tools

**Recommended:**
- **macOS:** QuickTime Player (File → New Screen Recording)
- **Windows:** Xbox Game Bar (Win+G)
- **Linux:** SimpleScreenRecorder
- **Cross-platform:** [OBS Studio](https://obsproject.com/) (free, professional)

**Settings:**
- Resolution: 1920x1080
- Frame rate: 30 fps
- Audio: Include microphone narration
- Format: MP4

### Editing (Optional)

**Tools:**
- **Simple:** iMovie (macOS), Movie Maker (Windows)
- **Advanced:** DaVinci Resolve (free, cross-platform)

**Edits to make:**
- Speed up slow parts (waiting for translation)
- Add text overlays for key points
- Add captions for accessibility
- Trim mistakes/pauses

### Upload to YouTube

1. Create YouTube account (if needed)
2. Upload → Select file
3. **Title:** "EPUB Translator - Translate Books with AI in 2 Hours"
4. **Description:**
```
Demonstration of the EPUB Translator tool using AI code assistants.

Translate EPUB books between languages while preserving formatting, structure, and metadata.

GitHub: https://github.com/vbalko-claimate/epub-translator
Blog: [Medium link]

Timestamps:
00:00 - Introduction
00:30 - Installation
01:00 - Translation
02:00 - Verification
02:30 - Conclusion
```
5. **Tags:** EPUB, translation, AI, Claude Code, book translation, ebook, automation
6. **Thumbnail:** Screenshot of translation in progress

### After Upload

1. Get YouTube URL (e.g., `https://www.youtube.com/watch?v=...`)
2. Add to this file
3. Update README.md with embedded video
4. Share on social media

---

**When ready, replace this placeholder with actual video link.**
