import markdown
from weasyprint import HTML
import re
from datetime import datetime

# Load external header and footer
with open("pdf_header.md", "r", encoding="utf-8") as f:
    pdf_header = f.read().strip()

with open("pdf_footer.md", "r", encoding="utf-8") as f:
    pdf_footer = f.read().strip()

# Replace {{DATE}} placeholder with current UTC date
pdf_footer = pdf_footer.replace("{{DATE}}", datetime.utcnow().strftime("%Y-%m-%d"))

# Load README content
with open("README.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Remove blocks marked for exclusion
md_content = re.sub(
    r'<!-- PDF-IGNORE-START -->.*?<!-- PDF-IGNORE-END -->',
    '',
    md_content,
    flags=re.DOTALL
)

# Remove single-line ignores
md_content = "\n".join(
    line for line in md_content.splitlines()
    if "<!-- PDF-IGNORE -->" not in line
)

# Combine everything
full_markdown = "\n\n".join([
    pdf_header,
    md_content.strip(),
    pdf_footer
])

# Convert to HTML
html_content = markdown.markdown(full_markdown, extensions=["fenced_code", "tables"])
# html_content = markdown.markdown(
#     full_markdown,
#     extensions=["fenced_code", "tables", "sane_lists"]
# )

# Styling
style = """
<style>
  @page {
    margin: 20mm 15mm;
  }
  body {
    font-family: sans-serif;
    padding: 0;
    max-width: 850px;
    margin: 0 auto;
  }
  h1, h2, h3 {
    color: #2c3e50;
    margin: 1em 0 0.5em 0;
    font-weight: normal;
  }
  h1 {
    margin-top: -1em;
  }
  h2 {
    margin: 0.5em 0 0.25em;
  }
  h3 {
    margin: 0.25em 0 0.125em;
  }
  a {
    color: #0366d6;
    text-decoration: none;
  }
  code {
    background: #f6f8fa;
    padding: 2px 4px;
    font-size: 90%;
  }
  pre {
    background: #f0f0f0;
    padding: 10px;
    overflow-x: auto;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1em;
  }
  th, td {
    border: 1px solid #ccc;
    padding: 6px 10px;
    text-align: left;
  }
  ul {
    list-style-type: disc;
    margin-left: 0.5em;
    margin-bottom: 0.5em;
  }
  ul ul {
    list-style-type: disc;
    margin-left: 1em;
  }
  ul ul ul {
    list-style-type: disc;
    margin-left: 1.5em;
  }
  li {
    margin-bottom: 0.2em;
  }
</style>
"""

# Export to PDF
html_page = f"<!DOCTYPE html><html><head>{style}</head><body>{html_content}</body></html>"
HTML(string=html_page).write_pdf("Toufiqur_Chowdhury_CV.pdf")
