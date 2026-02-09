def roast_profile(analysis: dict) -> list[str]:
    """Create savage, brutal roasts based on analysis.

    NO MERCY. Go hard or go home.
    """
    roasts: list[str] = []

    wc = analysis.get("word_count", 0)
    cliches = analysis.get("cliches", [])
    sentences = analysis.get("sentences", 0)

    # Length based
    if wc == 0:
        roasts.append("Your profile is blank. Literally nothing. Are you a ghost?")
    elif wc < 40:
        roasts.append(
            "Your profile is shorter than a tweet. Did you run out of ideas or was that intentional?"
        )
    elif wc < 120:
        roasts.append(
            "This is barely a profile. You spent more time thinking about how lazy you could be than writing it."
        )
    elif wc > 350:
        roasts.append(
            "Your profile is so long, recruiters will close the tab before reaching paragraph 2. Nobody cares about your entire life story."
        )

    # Clichés - HARSH
    if cliches:
        joined = ", ".join(cliches)
        roasts.append(
            f"Using '{joined}' is so cringe. Every mediocre candidate copies this garbage. You're not special."
        )

    # Sentence structure - BRUTAL
    if sentences and sentences < 3:
        roasts.append(
            "Three sentences and you think you have a profile? That's not a summary, that's a cry for help."
        )

    # If nothing else, be savage
    if not roasts:
        roasts.append(
            "Your profile is forgettable. Recruiters will skim it, forget you existed, and move on. Is that what you want?"
        )
        roasts.append(
            "You didn't stand out. You blended in with everyone else. Why should anyone choose you over the next guy?"
        )
        roasts.append(
            "This reads like you gave up halfway through. Show some ambition or find a new career."
        )

    return roasts
