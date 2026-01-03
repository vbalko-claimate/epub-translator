# Context Management for EPUB Translation

**Critical guide for handling large books without running out of memory**

---

## The Problem

EPUB books are **massive** in terms of AI context:

**Typical 300-page novel:**
- 31 chapters
- ~3,000 words per chapter
- ~4,000-8,000 tokens per chapter (including HTML markup)
- **Total: 124,000-248,000 tokens**

**AI context limits:**
| AI Assistant | Context Window | Can Handle |
|--------------|---------------|------------|
| Claude Sonnet 4.5 | 200K tokens | ~25-50 chapters (with skill) |
| Claude Opus 4 | 200K tokens | ~25-50 chapters |
| ChatGPT-4 Turbo | 128K tokens | ~15-30 chapters |
| Gemini 1.5 Pro | 1M tokens | Entire book! |
| Gemini Pro (old) | 32K tokens | ~4-8 chapters only |

**The risk:** Try to translate all 31 chapters in one conversation → Run out of context around chapter 15 → Lose all progress!

---

## Solution 1: Subagents (Claude Code Only)

**Best approach for Claude Code users:** The skill AUTOMATICALLY handles context management using Task subagents.

### How It Works

```bash
# You run this simple command:
claude "translate book.epub from English to Czech"

# Behind the scenes, the skill:
1. Extracts EPUB
2. Identifies 31 chapters
3. Launches 5-10 Task subagents IN PARALLEL:
   - Subagent 1: Chapters 1-2 (fresh context)
   - Subagent 2: Chapters 3-4 (fresh context)
   - Subagent 3: Chapters 5-6 (fresh context)
   - Subagent 4: Chapters 7-8 (fresh context)
   - Subagent 5: Chapters 9-10 (fresh context)
4. Waits for completion
5. Launches next wave of 5 subagents for chapters 11-20
6. Continues until all 31 chapters done
7. Updates metadata
8. Rebuilds EPUB
```

### Why Subagents Solve Context Issues

**Each subagent:**
- Has its own FRESH 200K context window
- Translates only 1-2 chapters (uses ~10K-20K tokens)
- Never exceeds limits
- Runs independently (if one fails, others continue)

**Main conversation:**
- Only coordinates (minimal context usage)
- Tracks progress with TodoWrite
- Never reads full chapter content

**Result:** Can translate books of ANY size!

### Subagent Strategy for Different Book Sizes

**Small book (10-15 chapters):**
```
Wave 1: Chapters 1-10 (5 subagents × 2 chapters)
Wave 2: Chapters 11-15 (3 subagents × 1-2 chapters)
Total time: ~20-30 minutes
```

**Medium book (20-30 chapters):**
```
Wave 1: Chapters 1-10 (5 subagents × 2 chapters)
Wave 2: Chapters 11-20 (5 subagents × 2 chapters)
Wave 3: Chapters 21-30 (5 subagents × 2 chapters)
Total time: ~40-60 minutes
```

**Large book (40-50 chapters):**
```
Wave 1: Chapters 1-10
Wave 2: Chapters 11-20
Wave 3: Chapters 21-30
Wave 4: Chapters 31-40
Wave 5: Chapters 41-50
Total time: ~60-90 minutes
```

**Epic book (100+ chapters):**
```
Process in 10-chapter waves
Run 10 waves total
Total time: ~2-3 hours
```

---

## Solution 2: Manual Session Management (All AI Assistants)

**For users of Claude.ai (web), ChatGPT, Gemini, Cursor, etc.**

### The Workflow

**DON'T:**
```
❌ Paste all 31 chapter prompts into one conversation
❌ Try to translate entire book in single session
❌ Keep asking "now do chapter 16, now chapter 17..."
```

**DO:**
```
✓ Create separate chat sessions for batches
✓ Start fresh conversation every 5-10 chapters
✓ Use parallel browser tabs for speed
```

### Batch Translation Strategy

**Step 1: Plan Your Batches**

For 31-chapter book:
```
Session 1: Chapters 1-5
Session 2: Chapters 6-10
Session 3: Chapters 11-15
Session 4: Chapters 16-20
Session 5: Chapters 21-25
Session 6: Chapters 26-31
```

**Step 2: Open Multiple Browser Tabs**

```
Browser Tab 1: New Claude.ai chat → Chapters 1-5
Browser Tab 2: New Claude.ai chat → Chapters 6-10
Browser Tab 3: New Claude.ai chat → Chapters 11-15
Browser Tab 4: New Claude.ai chat → Chapters 16-20
Browser Tab 5: New Claude.ai chat → Chapters 21-25
```

All run simultaneously! **Parallel processing without CLI tools.**

**Step 3: Use Same Prompt Template**

In each tab, paste the same prompt structure:

```
Translate these EPUB chapters from English to Czech.

Files:
- epub_workspace/translated/OEBPS/chapter-1.xhtml
- epub_workspace/translated/OEBPS/chapter-2.xhtml
- epub_workspace/translated/OEBPS/chapter-3.xhtml
- epub_workspace/translated/OEBPS/chapter-4.xhtml
- epub_workspace/translated/OEBPS/chapter-5.xhtml

[... rest of prompt from 03-translate-chapter.md ...]
```

Just change the chapter numbers for each tab!

**Step 4: Track Progress**

Keep a text file or notepad:

```
Translation Progress: My Book

✓ Chapters 1-5 (Tab 1) - DONE
✓ Chapters 6-10 (Tab 2) - DONE
⏳ Chapters 11-15 (Tab 3) - IN PROGRESS
⏳ Chapters 16-20 (Tab 4) - IN PROGRESS
⏳ Chapters 21-25 (Tab 5) - IN PROGRESS
[ ] Chapters 26-31 (Tab 6) - TODO

Metadata:
[ ] Table of Contents
[ ] About the Author
[ ] Language codes (content.opf, toc.ncx)

Final:
[ ] Rebuild EPUB
[ ] Validate
```

### Context Budget Per Session

**Safe limits per conversation:**

| AI | Context Limit | Safe Chapter Count |
|----|---------------|-------------------|
| Claude Sonnet | 200K | 5-10 chapters |
| ChatGPT-4 | 128K | 3-5 chapters |
| Gemini Pro (old) | 32K | 1-2 chapters |
| Gemini 1.5 Pro | 1M | All chapters! |

**Rule of thumb:** If AI says "I need to summarize our conversation", you're too close to limit. Start new session!

---

## Solution 3: Chapter Splitting (Large Chapters)

**Problem:** Some chapters are HUGE (fantasy epics, technical books)

Example:
- Chapter 1: 15,000 words
- That's ~20,000 tokens just for ONE chapter!

### How to Split

**Step 1: Identify the midpoint**

```bash
# Count paragraphs in chapter
grep -c '<p' epub_workspace/translated/OEBPS/chapter-1.xhtml
# Output: 450 paragraphs

# Midpoint: paragraph ~225
```

**Step 2: Find a paragraph ID near midpoint**

```bash
# Look for paragraph IDs around line 225
sed -n '220,230p' epub_workspace/translated/OEBPS/chapter-1.xhtml | grep '<p'

# Output:
# <p id="para-223" class="Body-Text">Some text here...</p>
# <p id="para-224" class="Body-Text">More text...</p>
# <p id="para-225" class="Body-Text">This is the midpoint!</p>
```

**Step 3: Translate in two passes**

**Pass 1 (First Half):**
```
Translate the FIRST HALF of chapter-1.xhtml from English to Czech.

File: epub_workspace/translated/OEBPS/chapter-1.xhtml

ONLY translate from:
- Beginning of file
- UP TO (but not including): <p id="para-225">

DO NOT translate paragraphs after para-225 yet!

[... rest of translation rules ...]
```

**Pass 2 (Second Half):**
```
Translate the SECOND HALF of chapter-1.xhtml from English to Czech.

File: epub_workspace/translated/OEBPS/chapter-1.xhtml

ONLY translate from:
- <p id="para-225"> (continue from previous translation)
- TO: End of file

The first half was already translated, just do this second part.

[... rest of translation rules ...]
```

**Step 4: Verify**

```bash
# Check that xml:lang was changed throughout
grep 'xml:lang="cs-CZ"' epub_workspace/translated/OEBPS/chapter-1.xhtml
# Should appear at top of file

# Check both halves translated
head -100 chapter-1.xhtml | grep -i "Czech text pattern"
tail -100 chapter-1.xhtml | grep -i "Czech text pattern"
```

---

## Solution 4: Use Larger Context Models

**Gemini 1.5 Pro: 1 Million Token Context**

This model can theoretically handle an ENTIRE BOOK in one conversation!

**Test it:**
```
Gemini 1.5 Pro session:

Translate this entire EPUB book from English to Spanish.

I'll provide chapter files one by one. After all chapters are done,
I'll ask you to update metadata and help rebuild.

Chapter 1: [paste chapter-1.xhtml content]
Chapter 2: [paste chapter-2.xhtml content]
...
Chapter 31: [paste chapter-31.xhtml content]

[All chapters fit in 1M context!]
```

**Caveats:**
- Might be slower (processing 1M tokens takes time)
- More expensive ($$ per request)
- Still better to batch for quality control

---

## Solution 5: Translation Memory (Advanced)

**For book series or consistent terminology:**

Create a "translation memory" file:

**File: `translation-memory.txt`**
```
Source: spaceship
Target: kosmická loď

Source: laser cannon
Target: laserové dělo

Source: command deck
Target: velitelský můstek

[... 100+ entries ...]
```

**Use in prompts:**
```
Use this translation memory for consistency:

spaceship → kosmická loď
laser cannon → laserové dělo
command deck → velitelský můstek

Translate chapter-5.xhtml using EXACTLY these translations.
```

**Benefits:**
- Consistency across all chapters
- Faster translation (AI reuses memory)
- Less context needed (pre-decided terminology)

---

## Recommended Workflow by Tool

### Claude Code (CLI)

```bash
# Just run this - skill handles everything automatically!
claude "translate book.epub from English to Czech"

# Skill will:
# 1. Use subagents (no context issues)
# 2. Process in parallel (fast)
# 3. Track progress (TodoWrite)
# 4. Validate output

# You: Make coffee, come back in 30-60 minutes ☕
```

**Complexity:** ⭐ (easiest)

---

### Claude.ai / ChatGPT (Web)

```
Plan:
[ ] Extract EPUB manually (unzip)
[ ] Open 5 browser tabs
[ ] Tab 1: Chapters 1-5
[ ] Tab 2: Chapters 6-10
[ ] Tab 3: Chapters 11-15
[ ] Tab 4: Chapters 16-20
[ ] Tab 5: Chapters 21-31
[ ] New tab: Update metadata
[ ] Rebuild EPUB (bash commands in terminal)
[ ] Validate

Time: ~2-3 hours (with parallel tabs)
```

**Complexity:** ⭐⭐⭐ (moderate, manual coordination)

---

### Cursor / VS Code AI

```
Use Cursor's chat feature:

Session 1 (Composer):
- Translate chapters 1-5
- When done, close composer

Session 2 (New Composer):
- Translate chapters 6-10
- Fresh context each time

Continue until done.

Time: ~3-4 hours (sequential)
```

**Complexity:** ⭐⭐⭐ (moderate, sequential)

---

### Gemini 1.5 Pro (1M Context)

```
Single session:
- Paste all 31 chapters one by one
- Translate in order
- Update metadata
- Get rebuild commands

Time: ~4-6 hours (single session, but slower processing)
```

**Complexity:** ⭐⭐ (simple, but slow)

---

## Emergency: Context Overflow Recovery

**Symptom:** AI says "I've reached my context limit" halfway through translation

**Recovery steps:**

1. **Save progress:**
   ```bash
   # Check which chapters are done
   grep -l 'xml:lang="cs-CZ"' epub_workspace/translated/OEBPS/*.xhtml > done.txt

   # List remaining
   grep -L 'xml:lang="cs-CZ"' epub_workspace/translated/OEBPS/*.xhtml > todo.txt
   ```

2. **Start fresh session:**
   - Open new chat/tab
   - Paste prompts for remaining chapters only
   - Continue from where you left off

3. **Use checklist to track:**
   ```
   ✓ Chapter 1 - DONE
   ✓ Chapter 2 - DONE
   ...
   ✓ Chapter 14 - DONE
   ✗ Chapter 15 - CONTEXT LIMIT HIT
   [ ] Chapter 16 - TODO
   [ ] Chapter 17 - TODO
   ...
   ```

4. **Resume translation:**
   New session starting at Chapter 15

**You don't lose work!** Translated chapters are already saved to files.

---

## Best Practices Summary

**DO:**
✓ Use subagents if available (Claude Code skill)
✓ Batch chapters into groups of 5-10
✓ Start new sessions frequently
✓ Use parallel tabs/windows for speed
✓ Track progress with checklist
✓ Validate after each batch

**DON'T:**
✗ Try to translate all chapters in one session
✗ Ignore context warnings from AI
✗ Assume "I have 200K context, I'll be fine"
✗ Read entire chapters into main conversation
✗ Summarize previous translations (wastes context)

---

## Context Usage Calculator

**Estimate your context needs:**

```python
# Python calculator
chapters = 31
words_per_chapter = 3000
html_markup_multiplier = 1.3  # XHTML adds ~30% tokens
tokens_per_word = 1.3  # Average for English

total_tokens = chapters * words_per_chapter * html_markup_multiplier * tokens_per_word

print(f"Total context needed: {int(total_tokens):,} tokens")

# Output: Total context needed: 157,170 tokens
# Claude Sonnet 200K: ✓ Can fit (with room for prompts)
# ChatGPT-4 128K: ✗ Won't fit! Need batching.
```

**Rule:** If total > 80% of context limit, BATCH IT!

---

## Future: Streaming Translation

**Experimental approach:**

Instead of loading entire chapter → translating → writing:

```
1. Read chapter line by line (streaming)
2. Translate each paragraph immediately
3. Write translated paragraph to output
4. Move to next paragraph
5. Never hold full chapter in memory
```

This could theoretically allow UNLIMITED book size!

**Implementation:** Not yet available in standard AI assistants, but possible with custom agents.

---

## Conclusion

Context management is **critical** for EPUB translation success.

**Easiest:** Use Claude Code skill (automatic subagents)
**Manual:** Batch chapters into 5-10 chapter groups
**Advanced:** Use Gemini 1.5 Pro for large context
**Recovery:** Track progress, resume from failures

With proper context management, you can translate **any size book** without hitting limits.

---

**Next:** [Troubleshooting](troubleshooting.md#context-limit-reached--out-of-memory) for specific error messages
