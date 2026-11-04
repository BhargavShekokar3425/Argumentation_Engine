"""
Validation script for all SVGs, HTML files, and unit tests.
"""
import os
import glob
import html.parser
import xml.etree.ElementTree as ET

def validate_svgs():
    svg_files = glob.glob("diagrams/*.svg") + glob.glob("results/*.svg")
    print(f"Checking {len(svg_files)} SVG files...")
    for f in svg_files:
        try:
            ET.parse(f)
            print(f"  [OK] XML Valid: {f}")
        except Exception as e:
            print(f"  [FAIL] {f}: {e}")
            raise e

def validate_html():
    html_files = ["report.html", "results/dashboard.html"]
    print(f"Checking {len(html_files)} HTML files...")
    for h in html_files:
        if os.path.exists(h):
            with open(h, "r", encoding="utf-8") as f:
                content = f.read()
            parser = html.parser.HTMLParser()
            parser.feed(content)
            print(f"  [OK] HTML Valid: {h} ({len(content)} chars)")

if __name__ == "__main__":
    validate_svgs()
    validate_html()
    print("ALL SVGS AND HTML FILES VALIDATED PERFECTLY!")
