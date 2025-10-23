"""Basic usage examples for amplifier-module-style-extraction."""

import asyncio
from pathlib import Path

from amplifier_module_style_extraction import StyleExtractor
from amplifier_module_style_extraction import StyleProfile


async def example_basic_extraction():
    """Extract style from writing samples."""
    extractor = StyleExtractor()

    profile = await extractor.extract_style(Path("~/my_blog_posts"))

    print(f"Tone: {profile.tone}")
    print(f"Voice: {profile.voice}")
    print(f"Vocabulary: {profile.vocabulary_level}")
    print(f"Common phrases: {', '.join(profile.common_phrases[:5])}")


async def example_serialize_profile():
    """Save and reuse extracted profiles."""
    extractor = StyleExtractor()

    # Extract once
    profile = await extractor.extract_style(Path("~/writings"))

    # Save to file
    with open("author_style.json", "w") as f:
        f.write(profile.model_dump_json(indent=2))

    # Load later
    with open("author_style.json") as f:
        loaded = StyleProfile.model_validate_json(f.read())

    print(f"Loaded profile: {loaded.tone}")


async def example_use_in_prompts():
    """Use extracted style to guide LLM content generation."""
    extractor = StyleExtractor()

    profile = await extractor.extract_style(Path("~/writings"))

    # Convert to prompt guidance
    style_text = profile.to_prompt_text()

    # Use in content generation
    prompt = f"""
Write a blog post about distributed systems.

Match this writing style:
{style_text}

Topic: The benefits of event-driven architecture
"""

    print("Prompt with style guidance:")
    print(prompt)


async def example_error_handling():
    """Handle extraction failures gracefully."""
    from amplifier_module_style_extraction import StyleExtractionError

    extractor = StyleExtractor()

    try:
        profile = await extractor.extract_style(Path("~/nonexistent"))
    except StyleExtractionError as e:
        print(f"Extraction failed: {e}")
        # Fallback: use default or prompt user
        profile = StyleProfile(
            tone="conversational",
            vocabulary_level="moderate",
            sentence_structure="varied",
            paragraph_length="medium",
            voice="active",
            common_phrases=[],
            writing_patterns=[],
            examples=[],
        )

    print(f"Using profile with tone: {profile.tone}")


if __name__ == "__main__":
    print("=== Basic Extraction ===")
    asyncio.run(example_basic_extraction())

    print("\n=== Serialize Profile ===")
    asyncio.run(example_serialize_profile())

    print("\n=== Use in Prompts ===")
    asyncio.run(example_use_in_prompts())

    print("\n=== Error Handling ===")
    asyncio.run(example_error_handling())
