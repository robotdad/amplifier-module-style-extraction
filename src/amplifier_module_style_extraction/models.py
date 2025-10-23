"""Data models for style extraction operations."""

from pydantic import BaseModel
from pydantic import Field


class StyleExtractionError(Exception):
    """Raised when style extraction fails."""


class StyleProfile(BaseModel):
    """Author style profile extracted from writing samples.

    This model captures the essential characteristics of an author's writing
    style for use in guiding content generation to match that style.

    All fields are required to ensure complete style representation.

    Attributes:
        tone: Overall tone (e.g., "formal", "conversational", "technical")
        vocabulary_level: Vocabulary complexity (e.g., "simple", "moderate", "advanced")
        sentence_structure: Typical sentence patterns (e.g., "short and direct", "complex and flowing")
        paragraph_length: Paragraph length preference (e.g., "short", "medium", "long")
        voice: Active vs passive voice preference (e.g., "active", "passive", "mixed")
        common_phrases: List of frequently used phrases or expressions
        writing_patterns: List of common structural patterns (e.g., "problem-solution", "storytelling")
        examples: Example sentences that capture the style

    Example:
        >>> profile = StyleProfile(
        ...     tone="conversational",
        ...     vocabulary_level="moderate",
        ...     sentence_structure="short and direct",
        ...     paragraph_length="medium",
        ...     voice="active",
        ...     common_phrases=["in other words", "as it turns out"],
        ...     writing_patterns=["problem-solution", "example-driven"],
        ...     examples=["Clear communication matters.", "Let's dive in."]
        ... )
        >>> assert profile.tone == "conversational"
        >>> assert len(profile.common_phrases) == 2
    """

    tone: str = Field(description="Overall tone (formal, conversational, technical, etc.)")
    vocabulary_level: str = Field(description="Vocabulary complexity (simple, moderate, advanced)")
    sentence_structure: str = Field(description="Typical sentence patterns")
    paragraph_length: str = Field(description="Typical paragraph length preference")
    voice: str = Field(description="Active vs passive voice preference")
    common_phrases: list[str] = Field(default_factory=list, description="Frequently used phrases or expressions")
    writing_patterns: list[str] = Field(default_factory=list, description="Common structural patterns")
    examples: list[str] = Field(default_factory=list, description="Example sentences capturing style")

    def to_prompt_text(self) -> str:
        """Convert style profile to natural language for LLM prompts.

        Transforms the structured style profile into prose guidance that can be
        included in LLM prompts to guide content generation toward this style.

        Returns:
            Natural language description of the style suitable for prompt inclusion

        Example:
            >>> profile = StyleProfile(
            ...     tone="conversational",
            ...     vocabulary_level="moderate",
            ...     sentence_structure="short and direct",
            ...     paragraph_length="medium",
            ...     voice="active",
            ...     common_phrases=["in practice", "for example"],
            ...     writing_patterns=["problem-solution"],
            ...     examples=["Clear communication matters."]
            ... )
            >>> prompt_text = profile.to_prompt_text()
            >>> assert "conversational tone" in prompt_text
            >>> assert "moderate vocabulary" in prompt_text
            >>> assert "short and direct" in prompt_text
        """
        parts = [
            f"Write with a {self.tone} tone.",
            f"Use {self.vocabulary_level} vocabulary level.",
            f"Structure sentences: {self.sentence_structure}.",
            f"Prefer {self.paragraph_length} paragraphs.",
            f"Use {self.voice} voice.",
        ]

        if self.common_phrases:
            phrases = ", ".join(f'"{p}"' for p in self.common_phrases[:5])
            parts.append(f"Common phrases include: {phrases}.")

        if self.writing_patterns:
            patterns = ", ".join(self.writing_patterns)
            parts.append(f"Follow these patterns: {patterns}.")

        if self.examples:
            parts.append("Example style:")
            for example in self.examples[:3]:
                parts.append(f'  - "{example}"')

        return "\n".join(parts)
