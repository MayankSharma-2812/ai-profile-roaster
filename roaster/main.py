import argparse
from rich import print

from roaster.parser import extract_text
from roaster.analyzer import analyze_profile
from roaster.roast_engine import roast_profile
from roaster.suggestions import generate_suggestions


def main():
    parser = argparse.ArgumentParser(description="🔥 AI Profile Roaster")
    parser.add_argument("file", help="Profile / resume text file")
    args = parser.parse_args()

    text = extract_text(args.file)
    analysis = analyze_profile(text)

    roasts = roast_profile(analysis)
    tips = generate_suggestions(analysis)

    print("\n[bold red]🔥 ROAST[/bold red]")
    for r in roasts:
        print(f"- {r}")

    print("\n[bold green]✅ HOW TO FIX IT[/bold green]")
    for t in tips:
        print(f"- {t}")


if __name__ == "__main__":
    main()
