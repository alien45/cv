import markdown
from weasyprint import HTML
import re
from datetime import datetime, timezone

# Load external header and footer
with open("pdf_header.md", "r", encoding="utf-8") as f:
    pdf_header = f.read().strip()

with open("pdf_footer.md", "r", encoding="utf-8") as f:
    pdf_footer = f.read().strip()

# Replace {{DATE}} placeholder with current UTC date
pdf_footer = pdf_footer.replace("{{DATE}}", datetime.now(timezone.utc).strftime("%Y-%m-%d"))

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
    margin: 10mm 10mm;
  }
  body {
    font-family: Arial, sans-serif;
    padding: 0;
    margin: 0;
  }
  h1, h2, h3 {
    color: #2c3e50;
    margin: 0.25em 0 0;
    font-weight: normal;
  }
  h1 {
    margin-bottom: 0.25em;
    margin-top: -0.5em;
  }
  h2 {
    font-weight: 900;
    margin: .25em 0 0.1em;
  }
  h3 {
    font-weight: 600;
    margin-top: 0.5em;
    margin-botton: 0.25em
  }
  /* Remove bottom spacing from experience date range */
  h3 + p {
    margin: 0.14em 0;
  }
  p {
    margin: 0.25em 0;
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
    overflow-x: auto;
    padding: 10px;
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
    padding-left: 1.2em;
    margin-left: 0;
    margin-bottom: 0.25em;
    margin-top: 0;
    margin-bottom: 0;
  }
  ul ul {
    list-style-type: disc;
    padding-left: 1.2em;
  }
  ul ul ul {
    list-style-type: disc;
    padding-left: 1.2em;
  }
  li {
    margin-bottom: 0.2em;
  }
  #footer-references {
    font-size: 110%;
    font-weight: 600;
    margin-top: 1em;
    text-align: center;
  }
</style>
"""

# Metadata title block
meta = """
<title>Toufiqur R. Chowdhury – Full Stack Developer Resume</title>
<meta name="author" content="Toufiqur R. Chowdhury">
<meta name="subject" content="Full Stack Developer Resume">
<meta name="keywords" content="Toufiq, Toufiqur Chowdhury, Toufiqur R. Chowdhury, Full Stack Developer, Frontend Developer, Resume, JavaScript, TypeScript, React, Node.js, Blockchain, Polkadot, Python, Golang, Go, Remote Developer">
"""

# Export to PDF
html_page = f"<!DOCTYPE html><html><head>{meta}{style}</head><body>{html_content}</body></html>"
HTML(string=html_page).write_pdf("Toufiqur_Chowdhury_CV.pdf")
