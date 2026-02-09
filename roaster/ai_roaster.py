"""AI-powered brutal roast generator using OpenAI and Groq APIs."""

import os
from typing import Optional

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

try:
    import openai

    _HAS_OPENAI = True
except ImportError:
    _HAS_OPENAI = False

try:
    from groq import Groq

    _HAS_GROQ = True
except ImportError:
    _HAS_GROQ = False


def generate_ai_roasts(profile_text: str, num_roasts: int = 3) -> list[str]:
    """Generate brutal, custom AI roasts based on profile text.

    Args:
        profile_text: The profile/resume text to roast
        num_roasts: Number of roasts to generate (default 3)

    Returns:
        List of roast strings. Empty list if API is unavailable or on error.
    """
    # Try Groq first (free tier)
    if _HAS_GROQ:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key and groq_api_key != "your_groq_api_key_here":
            print(f"[AI Roaster] Using Groq API...")
            try:
                client = Groq(api_key=groq_api_key)

                prompt = f"""You are a BRUTAL, SAVAGE career roaster. Your job is to SHRED this profile with harsh, cutting roasts.
Do NOT hold back. Point out clichés, weak writing, generic buzzwords, lazy descriptions, and everything wrong with it.
Be ruthless, funny, and devastating. Each roast should be 1-2 sentences of pure savage truth.

Profile text:
---
{profile_text}
---

Generate exactly {num_roasts} roasts, one per line. JUST the roasts, no intro. Be BRUTAL."""

                print(f"[AI Roaster] Calling Groq API for {num_roasts} roasts...")
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.9,
                    max_tokens=300,
                )

                roasts_text = response.choices[0].message.content.strip()
                roasts = [r.strip() for r in roasts_text.split("\n") if r.strip()]

                print(f"[AI Roaster] ✓ Generated {len(roasts)} brutal roasts with Groq")
                return roasts[:num_roasts]

            except Exception as e:
                print(f"[AI Roaster] Groq failed: {type(e).__name__}: {e}")

    # Fallback to OpenAI
    if not _HAS_OPENAI:
        print("[AI Roaster] ERROR: Neither Groq nor OpenAI modules available")
        return []

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[AI Roaster] ERROR: OPENAI_API_KEY not found in environment")
        return []

    if not api_key.startswith("sk-"):
        print(
            f"[AI Roaster] ERROR: OPENAI_API_KEY appears invalid (got {api_key[:20]}...)"
        )
        return []

    print(f"[AI Roaster] Using OpenAI API...")
    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""You are a BRUTAL, SAVAGE career roaster. Your job is to SHRED this profile with harsh, cutting roasts.
Do NOT hold back. Point out clichés, weak writing, generic buzzwords, lazy descriptions, and everything wrong with it.
Be ruthless, funny, and devastating. Each roast should be 1-2 sentences of pure savage truth.

Profile text:
---
{profile_text}
---

Generate exactly {num_roasts} roasts, one per line. JUST the roasts, no intro. Be BRUTAL."""

        print(f"[AI Roaster] Calling OpenAI API for {num_roasts} roasts...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=150,  # Even smaller to save quota
        )

        roasts_text = response.choices[0].message.content.strip()
        roasts = [r.strip() for r in roasts_text.split("\n") if r.strip()]

        print(f"[AI Roaster] ✓ Generated {len(roasts)} brutal roasts with OpenAI")
        return roasts[:num_roasts]

    except Exception as e:
        print(f"[AI Roaster] ✗ FAILED: {type(e).__name__}: {e}")
        return []


def generate_ai_suggestions(profile_text: str) -> list[str]:
    """Generate AI-powered improvement suggestions.

    Args:
        profile_text: The profile/resume text to analyze

    Returns:
        List of suggestion strings. Empty list if API is unavailable.
    """
    # Try Groq first (free tier)
    if _HAS_GROQ:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key and groq_api_key != "your_groq_api_key_here":
            print(f"[AI Suggestions] Using Groq API...")
            try:
                client = Groq(api_key=groq_api_key)

                prompt = f"""You are a brutally honest career fixer. Read this WEAK profile and tell them exactly what needs to change to make it actually competitive.
Be savage about the problems. Don't sugarcoat anything. Give harsh, specific, actionable fixes.

Profile text:
---
{profile_text}
---

Generate 3-4 harsh improvement directives, one per line. JUST the fixes, no intro. Be BRUTAL and specific."""

                print("[AI Suggestions] Calling Groq API for suggestions...")
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=300,
                )

                suggestions_text = response.choices[0].message.content.strip()
                suggestions = [
                    s.strip() for s in suggestions_text.split("\n") if s.strip()
                ]

                print(
                    f"[AI Suggestions] ✓ Generated {len(suggestions)} suggestions with Groq"
                )
                return suggestions

            except Exception as e:
                print(f"[AI Suggestions] Groq failed: {type(e).__name__}: {e}")

    # Fallback to OpenAI
    if not _HAS_OPENAI:
        print("[AI Suggestions] ERROR: Neither Groq nor OpenAI modules available")
        return []

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[AI Suggestions] ERROR: OPENAI_API_KEY not found in environment")
        return []

    if not api_key.startswith("sk-"):
        print(
            f"[AI Suggestions] ERROR: OPENAI_API_KEY appears invalid (got {api_key[:20]}...)"
        )
        return []

    print(f"[AI Suggestions] Using OpenAI API...")
    try:
        client = openai.OpenAI(api_key=api_key)

        prompt = f"""You are a brutally honest career fixer. Read this WEAK profile and tell them exactly what needs to change to make it actually competitive.
Be savage about the problems. Don't sugarcoat anything. Give harsh, specific, actionable fixes.

Profile text:
---
{profile_text}
---

Generate 3-4 harsh improvement directives, one per line. JUST the fixes, no intro. Be BRUTAL and specific."""

        print("[AI Suggestions] Calling OpenAI API for suggestions...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,  # Even smaller to save quota
        )

        suggestions_text = response.choices[0].message.content.strip()
        suggestions = [s.strip() for s in suggestions_text.split("\n") if s.strip()]

        print(
            f"[AI Suggestions] ✓ Generated {len(suggestions)} suggestions with OpenAI"
        )
        return suggestions

    except Exception as e:
        print(f"[AI Suggestions] ✗ FAILED: {type(e).__name__}: {e}")
        return []
