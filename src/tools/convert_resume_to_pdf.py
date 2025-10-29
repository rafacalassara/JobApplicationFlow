#!/usr/bin/env python3
import os
import markdown2
import weasyprint
from pathlib import Path
from paths import from_root


def convert_md_to_pdf(markdown_file: Path, output_pdf: Path, css_file: Path) -> bool:
    """Convert markdown file to PDF with CSS styling using markdown2.
    
    Args:
        markdown_file (Path): Path to the markdown file to convert.
        output_pdf (Path): Path to the output PDF file.
        css_file (Path): Path to the CSS file containing styles.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    print(f"Converting {markdown_file} to PDF with styling from {css_file}...")

    # Read markdown content
    with open(markdown_file.as_posix(), 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert to HTML using markdown2 which handles HTML in markdown better
    html_content = markdown2.markdown(
        md_content,
        extras=[
            'fenced-code-blocks',
            'tables',
            'header-ids',
            'break-on-newline',
            'cuddled-lists',
            'smarty-pants',
            'html-classes'
        ]
    )

    # Create full HTML document with CSS
    with open(css_file.as_posix(), 'r', encoding='utf-8') as f:
        css_content = f.read()

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Resume</title>
    <style>
        {css_content}
        
        /* Additional styles to ensure proper rendering */
        strong {{
            font-weight: bold;
            display: inline;
        }}
        
        a {{
            color: #1A5276;
            text-decoration: none;
        }}
        
        .job-title {{
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

    # Create temporary HTML file
    temp_html = Path(markdown_file).with_suffix('.temp.html')
    with open(temp_html.as_posix(), 'w', encoding='utf-8') as f:
        f.write(full_html)

    # Convert to PDF using WeasyPrint
    weasyprint.HTML(filename=temp_html.as_posix()).write_pdf(output_pdf.as_posix())

    # Remove temporary HTML file
    os.remove(temp_html.as_posix())

    print(f"PDF created successfully: {output_pdf}")

    return True


if __name__ == "__main__":
    # Get paths anchored at project root
    markdown_file = from_root("outputs", "crew_generated_resume.md")
    css_file = from_root("src", "md-to-pdf.css")
    output_pdf = from_root("outputs", "crew_generated_resume.pdf")

    # Convert markdown to PDF
    convert_md_to_pdf(markdown_file, output_pdf, css_file)
