# Contributing to EPUB Translator

Thank you for considering contributing to EPUB Translator! 🎉

## Ways to Contribute

### 1. 📖 Share Translation Glossaries

Have you created a glossary for a popular book series?

**What we need:**
- Glossaries for popular universes (Star Wars, Game of Thrones, etc.)
- Based on official translations where available
- At least 50 terms

**How to contribute:**
1. Create glossary file in `glossaries/community/[universe]-[source]-[target].[format]`
2. Include metadata (sources, version, author)
3. Test with actual book translation
4. Submit pull request

**Example:**
```json
{
  "metadata": {
    "universe": "Star Wars",
    "source_language": "en",
    "target_language": "de",
    "version": "1.0",
    "author": "YourName",
    "sources": ["Official German translations", "Wookieepedia DE"]
  },
  "characters": {
    "Luke Skywalker": {
      "translation": "Luke Skywalker",
      "mode": "preserve"
    }
  }
}
```

### 2. 🐛 Report Bugs

Found an issue? Open a GitHub Issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, AI assistant used)
- EPUB file details (if relevant)

### 3. ✨ Suggest Features

Have an idea? Open a GitHub Discussion with:
- What problem it solves
- How it would work
- Example use case

### 4. 📝 Improve Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify confusing sections
- Add examples
- Translate documentation to other languages

### 5. 🔧 Code Contributions

**Areas we need help:**
- Testing with different AI assistants (Gemini, Cursor, etc.)
- Platform-specific improvements (Windows, Linux)
- Validation scripts
- Error handling

## Development Process

### Before Starting

1. **Check existing issues** - Someone might already be working on it
2. **Open a discussion** - For larger changes, discuss first
3. **Fork the repository** - Work in your own copy

### Making Changes

1. **Create a branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test thoroughly:**
   - Test with a real EPUB file
   - Try different scenarios
   - Check on your platform

4. **Commit with clear messages:**
   ```bash
   git commit -m "Add French glossary for Harry Potter series"
   ```

### Submitting Pull Request

1. **Update your fork:**
   ```bash
   git pull origin main
   ```

2. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Open Pull Request** with:
   - Clear title
   - Description of changes
   - Why this change is needed
   - How you tested it

## Code Style

### Markdown Files

- Use ATX-style headers (`# Header`)
- Code blocks with language specified: ` ```bash `
- Lists with consistent indentation
- Line length ~80-100 chars (not strict)

### Bash Scripts

- Use `#!/bin/bash` shebang
- Include comments for non-obvious code
- Use `set -e` to exit on errors
- Quote variables: `"$VARIABLE"`

### Glossary Files

**JSON:**
- Indent with 2 spaces
- Include metadata section
- Alphabetize when possible

**TXT:**
- Group by category (characters, places, etc.)
- Include comments explaining decisions
- Use consistent formatting

**CSV:**
- Include headers: `term,translation,mode,notes`
- UTF-8 encoding

## Testing Guidelines

### For Glossaries

- [ ] Test with at least one full chapter
- [ ] Verify terms are applied correctly
- [ ] Check PRESERVE vs TRANSLATE work as expected
- [ ] Ensure no accidental translations

### For Scripts

- [ ] Run on macOS and Linux (if possible)
- [ ] Test with various EPUB structures
- [ ] Handle edge cases (missing files, etc.)
- [ ] Check exit codes and error messages

### For Documentation

- [ ] Verify all links work
- [ ] Check code examples are correct
- [ ] Ensure instructions are clear
- [ ] Test commands actually work

## Community Guidelines

### Be Respectful

- Welcome newcomers
- Assume good intentions
- Provide constructive feedback
- Help others learn

### Copyright & Licensing

- Only contribute content you have rights to
- Glossaries based on official translations: cite sources
- All contributions licensed under MIT (project license)
- Don't include copyrighted book content

### Translation Ethics

- Respect copyright laws
- Glossaries are tools, not encouragement for piracy
- Note if glossary is for public domain books
- Cite official translation sources when used

## Questions?

- **General questions:** Open a GitHub Discussion
- **Bug reports:** Open a GitHub Issue
- **Quick questions:** Add comment to existing issue/PR

## Recognition

Contributors are recognized in:
- README.md (major contributions)
- Glossary metadata files (glossary authors)
- Release notes

## First-Time Contributors

New to open source? Welcome! 🎉

Good first issues:
- Add glossary for popular book series
- Fix typos in documentation
- Test on different platforms
- Improve examples

We're here to help - don't hesitate to ask questions!

---

Thank you for contributing! 📚✨
