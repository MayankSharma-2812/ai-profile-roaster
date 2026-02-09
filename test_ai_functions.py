#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from roaster.ai_roaster import generate_ai_roasts, generate_ai_suggestions

# Test with a simple profile
test_profile = """
John Doe
Software Engineer with 5 years of experience in Python and JavaScript. 
Passionate about learning new technologies and working in team environments.
"""

print("Testing AI roasts with new API key...")
roasts = generate_ai_roasts(test_profile, num_roasts=3)
print(f"✅ Generated {len(roasts)} roasts:")
for i, roast in enumerate(roasts, 1):
    print(f"{i}. {roast}")

print(f"\nTesting AI suggestions with new API key...")
suggestions = generate_ai_suggestions(test_profile)
print(f"✅ Generated {len(suggestions)} suggestions:")
for i, suggestion in enumerate(suggestions, 1):
    print(f"{i}. {suggestion}")
