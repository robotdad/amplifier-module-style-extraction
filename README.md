# amplifier-module-style-extraction

> **⚠️ DEPRECATED:** This standalone module is deprecated in favor of the integrated version in [amplifier-bundle-blog-creator](https://github.com/robotdad/amplifier-bundle-blog-creator).
>
> **New location:** The tool module version with Amplifier protocol support is available in the bundle at `modules/tool-style-extraction/`
>
> **For new projects:** Use the bundle instead - it includes this functionality as a proper Amplifier tool module with improved integration.
>
> This repository remains for reference and backward compatibility only.

---

**Extract and apply writing style from text samples for Amplifier applications**

Analyze writing samples to extract tone, voice, vocabulary patterns, and structural preferences, then use those profiles to guide content generation.

---

## Installation

```bash
pip install git+https://github.com/robotdad/amplifier-dev#subdirectory=amplifier-module-style-extraction
```

Or add to your `pyproject.toml`:

```toml
[tool.uv.sources.amplifier-module-style-extraction]
git = "https://github.com/robotdad/amplifier-dev"
subdirectory = "amplifier-module-style-extraction"
branch = "main"
```

---

## Quick Start

```python
from pathlib import Path
from amplifier_module_style_extraction import StyleExtractor

# Initialize extractor
extractor = StyleExtractor()

# Extract style from writing samples
profile = await extractor.extract_style(Path("~/my_writings"))

# Use the profile
print(f"Writing tone: {profile.tone}")
print(f"Voice preference: {profile.voice}")
print(f"Common phrases: {', '.join(profile.common_phrases[:3])}")

# Convert to prompt text for LLM guidance
style_guidance = profile.to_prompt_text()
```

---

## Features

- **Comprehensive Style Analysis**: Extracts tone, vocabulary, sentence structure, voice, patterns
- **LLM-Powered Extraction**: Uses Claude to analyze writing samples intelligently
- **Pydantic Models**: Type-safe profiles with validation
- **Defensive Parsing**: Handles LLM response variations gracefully
- **Capability Integration**: Works with Amplifier coordinator for shared profiles
- **Standalone Mode**: Works independently without Amplifier

---

## API Reference

### StyleExtractor

Primary interface for style extraction.

```python
class StyleExtractor:
    async def extract_style(self, samples_dir: Path) -> StyleProfile:
        """Extract style profile from writing samples.

        Args:
            samples_dir: Directory containing author's writing samples (*.md)

        Returns:
            StyleProfile containing extracted style characteristics

        Raises:
            StyleExtractionError: When extraction fails or no samples found
        """
```

### StyleProfile

Extracted writing style profile (Pydantic model).

```python
class StyleProfile(BaseModel):
    tone: str                      # Overall tone (formal, conversational, technical)
    vocabulary_level: str          # Vocabulary complexity (simple, moderate, advanced)
    sentence_structure: str        # Typical sentence patterns
    paragraph_length: str          # Paragraph length preference
    voice: str                     # Active/passive voice preference
    common_phrases: list[str]      # Frequently used phrases
    writing_patterns: list[str]    # Common structural patterns
    examples: list[str]            # Example sentences capturing style

    def to_prompt_text(self) -> str:
        """Convert to natural language for LLM prompts."""
```

---

## Usage Examples

### Basic Extraction

```python
from pathlib import Path
from amplifier_module_style_extraction import StyleExtractor

extractor = StyleExtractor()

# Extract from your writing samples
profile = await extractor.extract_style(Path("~/blog_posts"))

# Examine the profile
print(f"Tone: {profile.tone}")
print(f"Vocabulary: {profile.vocabulary_level}")
print(f"Voice: {profile.voice}")
```

### Use in Content Generation

```python
# Extract author's style
profile = await extractor.extract_style(Path("~/writings"))

# Use in LLM prompt
prompt = f"""
Write a blog post about AI in software development.

Follow this writing style:
{profile.to_prompt_text()}
"""

# Generate content matching the style
result = await llm.complete(prompt)
```

### Serialize and Reuse

```python
# Extract once
profile = await extractor.extract_style(Path("~/writings"))

# Save for later use
with open("my_style.json", "w") as f:
    f.write(profile.model_dump_json(indent=2))

# Load and reuse
with open("my_style.json") as f:
    profile = StyleProfile.model_validate_json(f.read())
```

### Handle Extraction Failures

```python
from amplifier_module_style_extraction import StyleExtractionError

try:
    profile = await extractor.extract_style(Path("~/empty_dir"))
except StyleExtractionError as e:
    print(f"Extraction failed: {e}")
    # Use default profile or prompt user for samples
```

---

## Configuration

### Writing Samples

The extractor works best with:
- **3-5 representative documents** (more is fine, but diminishing returns)
- **Markdown format** (*.md files)
- **Similar genre** (all blog posts, all technical writing, etc.)
- **Recent work** (reflects current style better than old writing)

### Sample Processing

- Processes up to 5 files (configurable)
- Limits to 3,000 characters per file (prevents context overflow)
- Combines samples for holistic analysis
- Uses Claude Haiku for cost efficiency

---

## Integration with Amplifier

### Capability Registry Pattern

When used in Amplifier apps, register with coordinator:

```python
# In your module initialization
coordinator.register_capability("style_extraction.analyzer", extractor)
coordinator.register_capability("style_extraction.current_profile", profile)

# In consuming code - use capability first
extractor = coordinator.get_capability("style_extraction.analyzer")
if not extractor:
    from amplifier_module_style_extraction import StyleExtractor
    extractor = StyleExtractor()  # Standalone fallback
```

This allows multiple modules to share the same style profile without re-extraction.

---

## Error Handling

The module handles failures gracefully:

- **No samples found**: Returns default profile with warning
- **LLM extraction fails**: Retries with feedback, falls back to default
- **Invalid JSON responses**: Uses defensive parsing, retries if needed
- **Partial extraction**: Returns profile with available fields, defaults for missing

```python
# Example: Graceful degradation
profile = await extractor.extract_style(Path("~/writings"))

# Even if extraction partially fails, you get a usable profile
# Check which fields have meaningful values
if profile.common_phrases:
    print(f"Found {len(profile.common_phrases)} common phrases")
else:
    print("Using default profile - no samples processed")
```

---

## Development

### Setup

```bash
cd amplifier-module-style-extraction
uv sync --dev
```

### Run Tests

```bash
uv run pytest
```

### Type Checking

```bash
uv run pyright
```

---

## Contributing

See the main [Amplifier contributing guide](https://github.com/microsoft/amplifier-dev/blob/main/CONTRIBUTING.md).

This module follows the [Amplifier module development patterns](https://github.com/microsoft/amplifier-dev/blob/main/docs/MODULE_DEVELOPMENT.md).

---

## License

MIT License - See [LICENSE](https://github.com/robotdad/amplifier-dev/blob/main/LICENSE) file.

---

## Learn More

- [HOW_THIS_MODULE_WAS_MADE.md](./HOW_THIS_MODULE_WAS_MADE.md) - Creation story and patterns
- [examples/](./examples/) - Additional usage examples
- [Amplifier Documentation](https://github.com/microsoft/amplifier-dev/blob/main/docs/)
