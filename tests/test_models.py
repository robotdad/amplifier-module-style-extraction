"""Tests for style extraction models."""

import pytest
from amplifier_module_style_extraction.models import StyleProfile
from pydantic import ValidationError


def test_style_profile_creation():
    """Test creating a StyleProfile with all fields."""
    profile = StyleProfile(
        tone="conversational",
        vocabulary_level="moderate",
        sentence_structure="short and direct",
        paragraph_length="medium",
        voice="active",
        common_phrases=["in practice", "for example"],
        writing_patterns=["problem-solution", "example-driven"],
        examples=["Clear communication matters.", "Let's dive in."],
    )

    assert profile.tone == "conversational"
    assert profile.vocabulary_level == "moderate"
    assert profile.sentence_structure == "short and direct"
    assert profile.paragraph_length == "medium"
    assert profile.voice == "active"
    assert len(profile.common_phrases) == 2
    assert len(profile.writing_patterns) == 2
    assert len(profile.examples) == 2


def test_style_profile_minimal():
    """Test creating a StyleProfile with minimal fields."""
    profile = StyleProfile(
        tone="formal",
        vocabulary_level="advanced",
        sentence_structure="complex",
        paragraph_length="long",
        voice="passive",
    )

    assert profile.tone == "formal"
    assert profile.vocabulary_level == "advanced"
    assert profile.common_phrases == []
    assert profile.writing_patterns == []
    assert profile.examples == []


def test_style_profile_validation_required_fields():
    """Test that required fields are enforced."""
    with pytest.raises(ValidationError):
        StyleProfile()  # type: ignore[call-arg]

    with pytest.raises(ValidationError):
        StyleProfile(tone="conversational")  # type: ignore[call-arg]


def test_style_profile_to_prompt_text_basic():
    """Test converting profile to prompt text."""
    profile = StyleProfile(
        tone="conversational",
        vocabulary_level="moderate",
        sentence_structure="short and direct",
        paragraph_length="medium",
        voice="active",
    )

    prompt_text = profile.to_prompt_text()

    assert "conversational tone" in prompt_text
    assert "moderate vocabulary" in prompt_text
    assert "short and direct" in prompt_text
    assert "medium paragraphs" in prompt_text
    assert "active voice" in prompt_text


def test_style_profile_to_prompt_text_with_phrases():
    """Test prompt text includes common phrases."""
    profile = StyleProfile(
        tone="conversational",
        vocabulary_level="moderate",
        sentence_structure="varied",
        paragraph_length="medium",
        voice="active",
        common_phrases=["in practice", "for example", "as it turns out"],
    )

    prompt_text = profile.to_prompt_text()

    assert "in practice" in prompt_text
    assert "for example" in prompt_text
    assert "as it turns out" in prompt_text


def test_style_profile_to_prompt_text_with_patterns():
    """Test prompt text includes writing patterns."""
    profile = StyleProfile(
        tone="technical",
        vocabulary_level="advanced",
        sentence_structure="complex",
        paragraph_length="long",
        voice="active",
        writing_patterns=["problem-solution", "thesis-evidence-conclusion"],
    )

    prompt_text = profile.to_prompt_text()

    assert "problem-solution" in prompt_text
    assert "thesis-evidence-conclusion" in prompt_text


def test_style_profile_to_prompt_text_with_examples():
    """Test prompt text includes example sentences."""
    profile = StyleProfile(
        tone="conversational",
        vocabulary_level="moderate",
        sentence_structure="short and direct",
        paragraph_length="medium",
        voice="active",
        examples=["Clear communication matters.", "Let's get started.", "Here's what works."],
    )

    prompt_text = profile.to_prompt_text()

    assert "Clear communication matters." in prompt_text
    assert "Let's get started." in prompt_text
    assert "Here's what works." in prompt_text


def test_style_profile_to_prompt_text_limits_examples():
    """Test that to_prompt_text limits examples to first 3."""
    many_examples = [f"Example {i}." for i in range(10)]

    profile = StyleProfile(
        tone="conversational",
        vocabulary_level="moderate",
        sentence_structure="varied",
        paragraph_length="medium",
        voice="active",
        examples=many_examples,
    )

    prompt_text = profile.to_prompt_text()

    assert "Example 0." in prompt_text
    assert "Example 1." in prompt_text
    assert "Example 2." in prompt_text
    assert "Example 9." not in prompt_text


def test_style_profile_to_prompt_text_limits_phrases():
    """Test that to_prompt_text limits phrases to first 5."""
    many_phrases = [f"phrase{i}" for i in range(10)]

    profile = StyleProfile(
        tone="conversational",
        vocabulary_level="moderate",
        sentence_structure="varied",
        paragraph_length="medium",
        voice="active",
        common_phrases=many_phrases,
    )

    prompt_text = profile.to_prompt_text()

    assert "phrase0" in prompt_text
    assert "phrase4" in prompt_text
    assert "phrase9" not in prompt_text


def test_style_profile_serialization():
    """Test that StyleProfile can be serialized and deserialized."""
    profile = StyleProfile(
        tone="conversational",
        vocabulary_level="moderate",
        sentence_structure="short and direct",
        paragraph_length="medium",
        voice="active",
        common_phrases=["test phrase"],
        writing_patterns=["test pattern"],
        examples=["Test example."],
    )

    json_str = profile.model_dump_json()
    loaded = StyleProfile.model_validate_json(json_str)

    assert loaded.tone == profile.tone
    assert loaded.vocabulary_level == profile.vocabulary_level
    assert loaded.common_phrases == profile.common_phrases
    assert loaded.writing_patterns == profile.writing_patterns
    assert loaded.examples == profile.examples


def test_style_profile_dict_serialization():
    """Test that StyleProfile can be converted to/from dict."""
    profile = StyleProfile(
        tone="formal",
        vocabulary_level="advanced",
        sentence_structure="complex",
        paragraph_length="long",
        voice="passive",
    )

    profile_dict = profile.model_dump()
    loaded = StyleProfile.model_validate(profile_dict)

    assert loaded.tone == profile.tone
    assert loaded.vocabulary_level == profile.vocabulary_level
