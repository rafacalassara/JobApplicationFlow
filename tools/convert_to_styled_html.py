#!/usr/bin/env python3
import os
import re
import subprocess
from pathlib import Path
import markdown
from bs4 import BeautifulSoup


def markdown_to_html(markdown_file, html_file, css_file):
    """Convert markdown to HTML with styling."""
    print(f"Converting {markdown_file} to styled HTML...")

    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Pre-process markdown content to handle bold text and links
    # Replace markdown bold with HTML strong tags
    md_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', md_content)

    # Replace markdown links with HTML anchor tags
    md_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                        r'<a href="\2">\1</a>', md_content)

    # Convert to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'nl2br', 'sane_lists']
    )

    # Use BeautifulSoup to parse and clean up HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Read CSS content
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()

    # Create full HTML document with CSS
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Rafael Calassara - Resume</title>
    <style>
{css_content}
    </style>
</head>
<body>
{soup.prettify()}
</body>
</html>
"""

    # Write to HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"HTML created successfully: {html_file}")
    return html_file


def html_to_pdf(html_file, pdf_file):
    """Convert HTML to PDF using WeasyPrint."""
    print(f"Converting HTML to PDF...")

    try:
        import weasyprint
        weasyprint.HTML(filename=str(html_file)).write_pdf(pdf_file)
        print(f"PDF created successfully: {pdf_file}")
    except Exception as e:
        print(f"Error converting to PDF: {e}")
        print("Trying alternative method...")
        try:
            # Try using wkhtmltopdf if available
            subprocess.run(['wkhtmltopdf', html_file, pdf_file], check=True)
            print(f"PDF created successfully using wkhtmltopdf: {pdf_file}")
        except:
            print("Failed to convert to PDF. Please try viewing the HTML file directly.")


if __name__ == "__main__":
    # Get paths
    script_dir = Path(__file__).parent.parent
    markdown_file = script_dir / "outputs" / "crew_generated_resume.md"
    html_file = script_dir / "outputs" / "rafael_calassara_resume.html"
    css_file = script_dir / "md-to-pdf.css"
    pdf_file = script_dir / "outputs" / "rafael_calassara_resume.pdf"

    # Convert markdown to HTML
    html_file = markdown_to_html(markdown_file, html_file, css_file)

    # Convert HTML to PDF
    html_to_pdf(html_file, pdf_file)
