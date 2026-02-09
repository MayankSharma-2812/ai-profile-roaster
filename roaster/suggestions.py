def generate_suggestions(analysis: dict) -> list[str]:
    """Produce concise, actionable suggestions based on analysis."""
    tips: list[str] = []

    wc = analysis.get("word_count", 0)
    cliches = analysis.get("cliches", [])
    skills = analysis.get("skills", [])
    numbers = analysis.get("numbers_found", [])

    # Word count advice
    if wc == 0:
        tips.append("Add a short summary describing your role and goals.")
    elif wc < 80:
        tips.append("Expand your profile with 2–3 specific achievements.")
    elif wc > 300:
        tips.append("Trim less-relevant details; focus on impact and outcomes.")

    # Quantify
    if not numbers:
        tips.append(
            "Include measurable outcomes (percent improvements, time saved, revenue, etc.)."
        )

    # Cliches
    if cliches:
        tips.append(
            f"Replace overused phrases ({', '.join(cliches)}) with concrete examples."
        )

    # Skills
    if skills:
        tips.append(f"Show how you used {', '.join(skills)} in projects with results.")
    else:
        tips.append("List technical skills and the context where you applied them.")

    # General best-practices
    tips.append("Lead with impact — start bullets with action verbs and results.")
    tips.append("Use consistent tense and clean formatting (bullets, short sentences).")

    return tips
