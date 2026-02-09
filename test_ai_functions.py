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

print("Testing AI roasts...")
roasts = generate_ai_roasts(test_profile, num_roasts=2)
print(f"Roasts: {roasts}")

print("\nTesting AI suggestions...")
suggestions = generate_ai_suggestions(test_profile)
print(f"Suggestions: {suggestions}")
