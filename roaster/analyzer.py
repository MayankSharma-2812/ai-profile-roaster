"""Profile analysis utilities.

This module attempts to use spaCy if available, but falls back to
lightweight heuristics so the package works even without models.
"""

from typing import Optional
import re

try:
    import spacy

    _HAS_SPACY = True
except Exception:
    spacy = None
    _HAS_SPACY = False

# Common clichés / overused phrases to flag (lowercase)
CLICHES = [
    "hardworking",
    "hard working",
    "team player",
    "passionate",
    "self motivated",
    "self-motivated",
    "fast learner",
    "results driven",
    "detail oriented",
]

SKILLS_LOOKUP = [
    "python",
    "java",
    "sql",
    "aws",
    "docker",
    "kubernetes",
    "javascript",
    "react",
    "node",
    "c++",
    "c#",
]


def _load_spacy_model() -> Optional[object]:
    """Load spaCy model if available, otherwise return None."""
    if not _HAS_SPACY:
        return None
    try:
        return spacy.load("en_core_web_sm")
    except Exception:
        return None


def _simple_tokenize(text: str):
    words = re.findall(r"[A-Za-z0-9+#]+", text)
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return words, [s for s in sentences if s]


def analyze_profile(text: str) -> dict:
    """Analyze profile text and return a dictionary of findings.

    Returns keys: word_count, cliches, sentences, skills, numbers_found
    """
    text = (text or "").strip()

    nlp = _load_spacy_model()

    if nlp is not None:
        doc = nlp(text)
        words = [t.text for t in doc if t.is_alpha or t.like_num]
        sentences = list(doc.sents)
    else:
        words, sentences = _simple_tokenize(text)

    word_count = len(words)

    lower = text.lower()
    found_cliches = []
    for c in CLICHES:
        # simple whole-word check
        if re.search(r"\b" + re.escape(c) + r"\b", lower):
            found_cliches.append(c)

    # detect simple skills
    found_skills = [
        s for s in SKILLS_LOOKUP if re.search(r"\b" + re.escape(s) + r"\b", lower)
    ]

    # find numeric achievements like '50%', '30x', or '5 years'
    numbers = re.findall(r"\b\d{1,3}%|\b\d+\s?(?:years?|yrs?)|\b\d+x\b|\b\d+\b", text)

    return {
        "word_count": word_count,
        "cliches": found_cliches,
        "sentences": len(sentences),
        "skills": found_skills,
        "numbers_found": numbers,
    }
