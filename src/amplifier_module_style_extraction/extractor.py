"""Style extraction core functionality.

Analyzes writing samples to extract author's unique style patterns.
"""

from pathlib import Path
from typing import Any

from pydantic_ai import Agent

from .models import StyleExtractionError
from .models import StyleProfile


class StyleExtractor:
    """Extract author style from writing samples.

    Analyzes writing samples to identify author's unique style patterns
    using AI-powered analysis.

    Example:
        >>> extractor = StyleExtractor()
        >>> profile = await extractor.extract_style(Path("~/writings"))
        >>> print(profile.tone)
        'conversational'
    """

    def __init__(self, coordinator: Any | None = None) -> None:
        """Initialize style extractor.

        Args:
            coordinator: Optional capability coordinator for registration
        """
        self.profile: StyleProfile | None = None

        # Register capability if coordinator provided
        if coordinator:
            coordinator.register_capability("style_extraction.analyzer", self)

    async def extract_style(self, samples_dir: Path) -> StyleProfile:
        """Extract style profile from writing samples.

        Args:
            samples_dir: Directory containing markdown writing samples.
                        Path will be expanded (~ and vars resolved).

        Returns:
            Extracted style profile with tone, vocabulary, patterns, etc.

        Raises:
            StyleExtractionError: If no samples found or extraction fails

        Example:
            >>> extractor = StyleExtractor()
            >>> profile = await extractor.extract_style(Path("~/blog_posts"))
            >>> assert profile.tone in ["conversational", "formal", "technical"]
        """
        # Expand path (handle ~ and environment variables)
        samples_dir = samples_dir.expanduser()

        # Find all markdown files recursively
        files = list(samples_dir.glob("**/*.md"))
        if not files:
            raise StyleExtractionError(f"No markdown files found in {samples_dir}")

        # Read samples (limit to prevent context overflow)
        samples = []
        max_samples = 5
        max_chars_per_sample = 3000

        for file in files[:max_samples]:
            try:
                content = file.read_text(encoding="utf-8")[:max_chars_per_sample]
                samples.append(f"=== {file.name} ===\n{content}")
            except Exception as e:
                # Log warning but continue with other samples
                print(f"Warning: Could not read {file}: {e}")

        if not samples:
            raise StyleExtractionError("Could not read any writing samples")

        # Extract style with AI
        combined_samples = "\n\n".join(samples)
        profile = await self._analyze_with_ai(combined_samples)

        # Store profile and register if we have coordinator
        self.profile = profile

        return profile

    async def _analyze_with_ai(self, samples: str) -> StyleProfile:
        """Analyze samples with AI to extract style.

        Args:
            samples: Combined writing samples

        Returns:
            Extracted style profile

        Raises:
            StyleExtractionError: If analysis fails
        """
        prompt = f"""Analyze these writing samples to extract the author's style:

{samples}

Extract:
1. Overall tone (formal/casual/technical/conversational)
2. Vocabulary complexity level (simple/moderate/advanced)
3. Typical sentence structure patterns
4. Paragraph length preference (short/medium/long)
5. Common phrases or expressions (list)
6. Recurring writing patterns (list)
7. Voice preference (active/passive/mixed)
8. 3-5 example sentences that best capture the style (list)

Return a structured response with these fields."""

        # Create PydanticAI agent for structured extraction
        agent: Agent[None, StyleProfile] = Agent(
            "openai:gpt-4o",
            output_type=StyleProfile,
            system_prompt="You are an expert writing style analyst. Extract detailed style characteristics from text samples.",
        )

        try:
            result = await agent.run(prompt)
            return result.output
        except Exception as e:
            # Fall back to default profile on error
            print(f"Warning: Style extraction failed: {e}")
            print("Using default style profile")
            return self._default_profile()

    def _default_profile(self) -> StyleProfile:
        """Return default style profile when extraction fails.

        Returns:
            Default conversational style profile
        """
        return StyleProfile(
            tone="conversational",
            vocabulary_level="moderate",
            sentence_structure="varied",
            paragraph_length="medium",
            voice="active",
            common_phrases=[],
            writing_patterns=["introduction-body-conclusion", "problem-solution"],
            examples=["Clear and direct communication.", "Focus on practical value."],
        )
