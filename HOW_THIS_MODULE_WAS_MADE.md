# How This Module Was Made

**Migration from scenarios/blog_writer to reusable Amplifier module**

---

## The Problem

The blog_writer had sophisticated style extraction that analyzed writing samples to capture an author's unique voice. This was valuable for ANY content generation needing personalization, but was locked inside a single-purpose tool.

Other apps (email generators, social media tools, documentation writers) all need style matching but had to build it from scratch.

---

## The Solution: Extract as Reusable Module

**What We Extracted** (~200 LOC from blog_writer/style_extractor/):
- LLM-powered style analysis
- Pydantic StyleProfile model
- Defensive JSON parsing with retry
- Default profile fallbacks

**What We Left Behind**:
- Blog-specific review logic (source_reviewer, style_reviewer)
- User feedback integration
- Draft iteration workflow

---

## Migration Decisions

### Decision 1: Keep Pydantic Model
**Chose**: StyleProfile as Pydantic BaseModel
**Why**: Type safety, validation, easy serialization
**Alternative**: Plain dict would be simpler but loses type checking

### Decision 2: Async Interface
**Chose**: Async for LLM calls
**Why**: All style extraction involves network I/O
**Alternative**: Sync would be simpler but blocks

### Decision 3: to_prompt_text() Helper
**Chose**: Add convenience method for LLM integration
**Why**: Common need to convert profile to prompt guidance
**Alternative**: Leave formatting to consumers

---

## Key Learnings

### From Original Implementation
1. **Sample limits prevent context overflow** - 5 files × 3K chars works well
2. **Defensive parsing is essential** - LLMs don't always return clean JSON
3. **Default profiles enable graceful degradation** - Better than failing
4. **Array responses happen** - LLM sometimes returns `[{...}]` instead of `{...}`

### From Migration
1. **Git sources are mandatory** - Path dependencies break standalone
2. **Capability registry enables sharing** - Multiple modules use same profile
3. **Path expansion critical** - Always `.expanduser()` for config paths

---

## Reusability

Use cases for this module:
- Blog post generation
- Email response writers
- Social media content creators
- Code comment generators
- Any personalized content generation

---

**Created**: 2025-10-22
**Migration From**: scenarios/blog_writer (production-tested)
**Status**: Active development
