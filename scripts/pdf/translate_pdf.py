#!/usr/bin/env python3
"""
PDF Page Translation Helper

This script helps prepare JSON files for translation via Claude Code Task subagents.
It does NOT use Claude API - instead it's designed to work with Claude Code subscription.

The actual translation happens through:
1. Claude Code main conversation creates Task subagents
2. Each subagent reads JSON files, translates text, writes back
3. Glossary rules passed in subagent prompt (same as EPUB workflow)

This script is optional - mainly for validation and preprocessing.

Usage:
    # Validate extracted pages are ready for translation
    python translate_pdf.py --validate pdf_workspace/extracted/

    # Generate subagent prompt template
    python translate_pdf.py --generate-prompt --pages 1-5 --glossary warhammer40k-en-cs.json
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional


def load_glossary(glossary_path: Optional[str]) -> Dict:
    """
    Load glossary file (JSON, TXT, or CSV format).

    Reuses the glossary system from epub-translator with 4 modes:
    - PRESERVE: Never translate
    - TRANSLATE: Use specific translation
    - PRESERVE_WITH_GRAMMAR: Keep word, apply target grammar
    - CONTEXT: Decide based on usage

    Args:
        glossary_path: Path to glossary file (None to skip)

    Returns:
        Dictionary with glossary rules
    """
    if not glossary_path:
        return {"preserve": [], "translate": {}, "preserve_with_grammar": [], "context": {}}

    glossary_file = Path(glossary_path)

    if not glossary_file.exists():
        # Try looking in glossaries/ directory
        alt_path = Path("glossaries") / glossary_file.name
        if alt_path.exists():
            glossary_file = alt_path
        else:
            alt_path2 = Path("../../glossaries/community") / glossary_file.name
            if alt_path2.exists():
                glossary_file = alt_path2
            else:
                print(f"Warning: Glossary not found: {glossary_path}", file=sys.stderr)
                return {"preserve": [], "translate": {}, "preserve_with_grammar": [], "context": {}}

    # Parse based on file extension
    if glossary_file.suffix == ".json":
        with open(glossary_file, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Extract terms from nested structure
            glossary = {
                "preserve": [],
                "translate": {},
                "preserve_with_grammar": [],
                "context": {}
            }

            # Flatten nested categories (characters, factions, weapons, etc.)
            for category, terms in data.items():
                if category == "metadata":
                    continue

                for term, info in terms.items():
                    mode = info.get("mode", "preserve")

                    if mode == "preserve":
                        glossary["preserve"].append(term)
                    elif mode == "translate":
                        glossary["translate"][term] = info.get("translation", term)
                    elif mode == "preserve_with_grammar":
                        glossary["preserve_with_grammar"].append(term)
                    elif mode == "context":
                        glossary["context"][term] = info.get("note", "")

            return glossary

    elif glossary_file.suffix == ".txt":
        # Simple TXT format parsing
        glossary = {"preserve": [], "translate": {}, "preserve_with_grammar": [], "context": {}}

        with open(glossary_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("PRESERVE:"):
                    term = line.split(":", 1)[1].strip()
                    glossary["preserve"].append(term)
                elif line.startswith("TRANSLATE:"):
                    parts = line.split(":", 1)[1].strip().split("→")
                    if len(parts) == 2:
                        glossary["translate"][parts[0].strip()] = parts[1].strip()
                elif line.startswith("PRESERVE_WITH_GRAMMAR:"):
                    term = line.split(":", 1)[1].strip()
                    glossary["preserve_with_grammar"].append(term)

        return glossary

    else:
        print(f"Warning: Unsupported glossary format: {glossary_file.suffix}", file=sys.stderr)
        return {"preserve": [], "translate": {}, "preserve_with_grammar": [], "context": {}}


def format_glossary_for_prompt(glossary: Dict) -> str:
    """
    Format glossary rules for Claude subagent prompt.

    Args:
        glossary: Glossary dictionary

    Returns:
        Formatted string for prompt
    """
    lines = []

    if glossary["preserve"]:
        lines.append("PRESERVE (never translate):")
        for term in glossary["preserve"][:30]:  # Show more terms
            lines.append(f"  - {term}")
        if len(glossary["preserve"]) > 30:
            lines.append(f"  ... and {len(glossary['preserve']) - 30} more")

    if glossary["translate"]:
        lines.append("\nTRANSLATE (use these exact translations):")
        for source, target in list(glossary["translate"].items())[:30]:
            lines.append(f"  - {source} → {target}")
        if len(glossary["translate"]) > 30:
            lines.append(f"  ... and {len(glossary['translate']) - 30} more")

    if glossary["preserve_with_grammar"]:
        lines.append("\nPRESERVE_WITH_GRAMMAR (keep word, apply target language grammar):")
        for term in glossary["preserve_with_grammar"][:20]:
            lines.append(f"  - {term}")

    return "\n".join(lines) if lines else "No glossary rules"


def generate_subagent_prompt(
    page_range: str,
    extracted_dir: str,
    output_dir: str,
    source_lang: str,
    target_lang: str,
    glossary_path: Optional[str] = None
) -> str:
    """
    Generate prompt for Claude Code Task subagent.

    This is what you'll use in Claude Code main conversation:
    Use Task tool with subagent_type="general-purpose" and this prompt.

    Args:
        page_range: Page range (e.g., "1-5")
        extracted_dir: Directory with extracted JSON
        output_dir: Output directory for translated JSON
        source_lang: Source language
        target_lang: Target language
        glossary_path: Path to glossary file (optional)

    Returns:
        Formatted prompt for Task subagent
    """
    # Load glossary if provided
    glossary = load_glossary(glossary_path)
    glossary_section = format_glossary_for_prompt(glossary)

    # Parse page range
    if "-" in page_range:
        start, end = map(int, page_range.split("-"))
        page_files = [f"page_{i:03d}.json" for i in range(start, end + 1)]
    else:
        page_num = int(page_range)
        page_files = [f"page_{page_num:03d}.json"]

    prompt = f"""Translate PDF pages {page_range} from {source_lang} to {target_lang}.

FILES TO TRANSLATE:
{chr(10).join([f"  - {extracted_dir}/{f}" for f in page_files])}

WORKFLOW:

1. For each page JSON file:
   a) Use Read tool to load: {extracted_dir}/page_XXX.json
   b) For each block in the JSON:
      - Read the "text" field
      - Translate it from {source_lang} to {target_lang}
      - Apply glossary rules (see below)
      - Check if translated text is longer than original
      - If overflow >10%, add "overflow_warning": true and "suggested_size"
      - Store as "original_text" and "translated_text" in the block
   c) Use Write tool to save: {output_dir}/page_XXX.json

2. Skip translation for blocks where type is "header" or "footer"

3. Preserve ALL metadata: bbox, font, size, flags, color, type

GLOSSARY RULES:
{glossary_section}

OVERFLOW DETECTION:
```python
# Estimate width: rough approximation
original_width = bbox[2] - bbox[0]
original_estimated = len(original_text) * font_size * 0.5
translated_estimated = len(translated_text) * font_size * 0.5

if translated_estimated > original_width * 1.1:  # 10% overflow
    block["overflow_warning"] = true
    # Suggest reduced font size
    block["suggested_size"] = font_size * (original_width / translated_estimated) * 0.95
```

JSON OUTPUT FORMAT:
```json
{{
  "page_num": 1,
  "width": 595.32,
  "height": 841.92,
  "blocks": [
    {{
      "text": "...",  // Keep original for reference
      "original_text": "Chapter 1",
      "translated_text": "Kapitola 1",
      "bbox": [72.0, 100.0, 200.0, 120.0],
      "font": "Times-Bold",
      "size": 18.0,
      "flags": 16,
      "color": 0,
      "type": "heading",
      "overflow_warning": false
    }}
  ]
}}
```

CRITICAL:
- Use Read tool (not Bash cat)
- Use Write tool (not Bash echo)
- Preserve exact JSON structure
- Apply glossary rules strictly
- Report progress: "✓ Page X: Y blocks translated"
"""

    return prompt


def validate_extracted_pages(extracted_dir: str) -> bool:
    """
    Validate that extracted JSON files are ready for translation.

    Args:
        extracted_dir: Directory with extracted JSON files

    Returns:
        True if valid, False otherwise
    """
    extracted_path = Path(extracted_dir)

    if not extracted_path.exists():
        print(f"Error: Directory not found: {extracted_dir}", file=sys.stderr)
        return False

    json_files = sorted(extracted_path.glob("page_*.json"))

    if not json_files:
        print(f"Error: No page_*.json files found in {extracted_dir}", file=sys.stderr)
        return False

    print(f"✓ Found {len(json_files)} page files")

    # Validate first file structure
    with open(json_files[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    required_keys = ["page_num", "width", "height", "blocks"]
    for key in required_keys:
        if key not in data:
            print(f"Error: Missing key '{key}' in JSON", file=sys.stderr)
            return False

    if data["blocks"]:
        block = data["blocks"][0]
        block_keys = ["text", "bbox", "font", "size", "type"]
        for key in block_keys:
            if key not in block:
                print(f"Warning: Block missing key '{key}'", file=sys.stderr)

    print(f"✓ JSON structure valid")
    print(f"  Sample: Page {data['page_num']}, {len(data['blocks'])} blocks")

    return True


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="PDF translation helper for Claude Code workflow",
        epilog="Example: python translate_pdf.py --generate-prompt --pages 1-5"
    )

    parser.add_argument(
        "--validate",
        metavar="DIR",
        help="Validate extracted JSON files are ready for translation"
    )

    parser.add_argument(
        "--generate-prompt",
        action="store_true",
        help="Generate Task subagent prompt for Claude Code"
    )

    parser.add_argument(
        "--pages",
        help="Page range (e.g., '1-5', '3')"
    )

    parser.add_argument(
        "--source",
        default="en",
        help="Source language code (default: en)"
    )

    parser.add_argument(
        "--target",
        default="cs",
        help="Target language code (default: cs)"
    )

    parser.add_argument(
        "--glossary",
        help="Path to glossary file (JSON or TXT)"
    )

    parser.add_argument(
        "--extracted-dir",
        default="pdf_workspace/extracted",
        help="Directory with extracted JSON (default: pdf_workspace/extracted)"
    )

    parser.add_argument(
        "--output-dir",
        default="pdf_workspace/translated",
        help="Output directory for translated JSON (default: pdf_workspace/translated)"
    )

    args = parser.parse_args()

    # Validate mode
    if args.validate:
        is_valid = validate_extracted_pages(args.validate)
        return 0 if is_valid else 1

    # Generate prompt mode
    if args.generate_prompt:
        if not args.pages:
            print("Error: --pages required for --generate-prompt", file=sys.stderr)
            return 1

        prompt = generate_subagent_prompt(
            page_range=args.pages,
            extracted_dir=args.extracted_dir,
            output_dir=args.output_dir,
            source_lang=args.source,
            target_lang=args.target,
            glossary_path=args.glossary
        )

        print("\n" + "="*80)
        print("TASK SUBAGENT PROMPT")
        print("="*80)
        print("\nCopy this prompt and use it with:")
        print(f"  Task tool, subagent_type='general-purpose'\n")
        print("="*80 + "\n")
        print(prompt)
        print("\n" + "="*80)

        return 0

    # No mode specified
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
